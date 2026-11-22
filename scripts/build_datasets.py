#!/usr/bin/env python3
"""Build the dataset catalog from the archives themselves.

The ZIPs in ``datasets/`` are the source of truth: each one ships a
``metadata.txt`` describing its title, author, date, CRS, language, source and
full field schema. This script reads that, normalises the archives, and emits:

  _data/datasets.yml              catalog consumed by every page
  _datasets/<slug>.md             one stub page per dataset
  datasets/<file>.csv             raw CSV alongside each ZIP
  datasets/catalog.json           machine-readable catalog
  datasets/catalog.csv            flat catalog
  datasets/<slug>.json            per-dataset record

Normalisation (the "hygiene" pass) rewrites each archive in place, keeping
filenames identical so every existing download URL keeps working:

  * text decoded from cp1252/latin-1 and re-encoded as UTF-8
  * delimiters unified to the RFC 4180 comma
  * nested folders flattened

Uses only the Python standard library plus PyYAML, which the image pipeline
already depends on. No GIS libraries are required at build time.
"""

from __future__ import annotations

import csv
import io
import json
import re
import struct
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "datasets"
DATA = ROOT / "_data"
COLLECTION = ROOT / "_datasets"

OUTLINE = DATA / "madagascar_outline.yml"
VIEWBOX = (535.0, 1000.0)
LAKES_SIMPLIFY_TOL = 0.02
# Lakes below this area are sub-pixel at preview size, so they are drawn as a
# small circle instead of a polygon. 0.0008 deg2 is roughly 9 km2.
POLYGON_MIN_DEGREES = 0.0008

DBF_TYPES = {
    "C": "Text",
    "N": "Number",
    "F": "Decimal",
    "D": "Date",
    "L": "Boolean",
    "M": "Memo",
}

DELIMITERS = (",", ";", "\t", "|", ":")


# --------------------------------------------------------------------------
# decoding and parsing helpers
# --------------------------------------------------------------------------


def decode_text(raw: bytes) -> str:
    """Decode a text file that may predate UTF-8."""
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", "replace")


def sniff_delimiter(text: str) -> str:
    """Pick the delimiter that yields the most, most-consistent columns."""
    lines = [line for line in text.splitlines() if line.strip()][:8]
    if not lines:
        return ","
    best, best_score = ",", 0
    for candidate in DELIMITERS:
        counts = [len(next(csv.reader([line], delimiter=candidate))) for line in lines]
        score = min(counts) if min(counts) > 1 else 0
        if score > best_score:
            best, best_score = candidate, score
    return best


def parse_csv(text: str) -> tuple[list[str], list[list[str]]]:
    delimiter = sniff_delimiter(text)
    rows = [row for row in csv.reader(io.StringIO(text), delimiter=delimiter) if any(cell.strip() for cell in row)]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def render_csv(header: list[str], rows: list[list[str]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buffer.getvalue()


KEY_MATCHERS = (
    ("coordonn", "crs"),
    ("coordinate system", "crs"),
    ("titre", "original_title"),
    ("title", "original_title"),
    ("auteur", "author"),
    ("author", "author"),
    ("date", "date"),
    ("description", "original_description"),
    ("langue", "language"),
    ("language", "language"),
    ("format", "format"),
    ("fichier", "declared_files"),
    ("file", "declared_files"),
)

FIELD_RE = re.compile(r"^\s*-\s*(.+?)\s*:\s*(.*)$")


def parse_metadata(text: str) -> dict:
    """Parse the French/English key:value metadata.txt into a normalised dict."""
    meta: dict = {"fields": []}
    in_fields = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.rstrip(":").lower() in ("champs", "fields", "colonnes"):
            in_fields = True
            continue

        if in_fields:
            match = FIELD_RE.match(line)
            if match:
                meta["fields"].append({"name": match.group(1).strip(), "description": match.group(2).strip()})
            continue

        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key_lower = key.strip().lower()
        value = value.strip()
        for needle, target in KEY_MATCHERS:
            if needle in key_lower:
                meta.setdefault(target, value)
                break

    return meta


def dbf_schema(raw: bytes) -> dict:
    """Read field names, types and the record count from a DBF header."""
    record_count = struct.unpack("<I", raw[4:8])[0]
    fields = []
    position = 32
    while position < len(raw) and raw[position] != 0x0D:
        name = raw[position : position + 11].split(b"\x00")[0].decode("latin-1").strip()
        type_code = chr(raw[position + 11])
        length = raw[position + 16]
        decimals = raw[position + 17]
        fields.append(
            {
                "name": name,
                "type": DBF_TYPES.get(type_code, type_code),
                "length": length,
                "decimals": decimals,
            }
        )
        position += 32
    return {"records": record_count, "fields": fields}


def shp_bounds(raw: bytes) -> list[float]:
    """The .shp header stores the bounding box as four doubles at offset 36."""
    xmin, ymin, xmax, ymax = struct.unpack("<dddd", raw[36:68])
    return [round(xmin, 4), round(ymin, 4), round(xmax, 4), round(ymax, 4)]


# --------------------------------------------------------------------------
# geometry helpers for the mini-maps
# --------------------------------------------------------------------------


def douglas_peucker(points: list[tuple[float, float]], tolerance: float) -> list[tuple[float, float]]:
    """Simplify a ring. Pure stdlib so the build needs no GIS stack."""
    if len(points) < 3:
        return points

    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]

    while stack:
        start, end = stack.pop()
        if end <= start + 1:
            continue
        ax, ay = points[start]
        bx, by = points[end]
        dx, dy = bx - ax, by - ay
        norm = (dx * dx + dy * dy) ** 0.5
        farthest, distance = -1, -1.0
        for index in range(start + 1, end):
            px, py = points[index]
            if norm == 0:
                d = ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
            else:
                d = abs(dy * px - dx * py + bx * ay - by * ax) / norm
            if d > distance:
                farthest, distance = index, d
        if distance > tolerance:
            keep[farthest] = True
            stack.append((start, farthest))
            stack.append((farthest, end))

    return [point for point, kept in zip(points, keep) if kept]


RING_RE = re.compile(r"\(([-0-9eE.,\s]+)\)")
PAIR_RE = re.compile(r"(-?\d+(?:\.\d+)?)[ ,]+(-?\d+(?:\.\d+)?)")


def wkt_rings(value: str) -> list[list[tuple[float, float]]]:
    rings = []
    for group in RING_RE.findall(value or ""):
        points = [(float(x), float(y)) for x, y in PAIR_RE.findall(group)]
        if len(points) >= 4:
            rings.append(points)
    return rings


def ring_area(points: list[tuple[float, float]]) -> float:
    area = 0.0
    for index in range(len(points) - 1):
        x1, y1 = points[index]
        x2, y2 = points[index + 1]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2


class Projector:
    def __init__(self, bounds: list[float]):
        self.lon_min, self.lat_min, self.lon_max, self.lat_max = bounds

    def __call__(self, lon: float, lat: float) -> tuple[float, float]:
        x = (lon - self.lon_min) / (self.lon_max - self.lon_min) * VIEWBOX[0]
        y = (self.lat_max - lat) / (self.lat_max - self.lat_min) * VIEWBOX[1]
        return round(x, 1), round(y, 1)


def path_from_rings(rings: list[list[tuple[float, float]]], project: Projector, tolerance: float) -> str:
    parts = []
    for ring in rings:
        simplified = douglas_peucker(ring, tolerance)
        if len(simplified) < 3:
            continue
        commands = []
        for index, (lon, lat) in enumerate(simplified):
            x, y = project(lon, lat)
            commands.append(("M" if index == 0 else "L") + f"{x} {y}")
        parts.append("".join(commands) + "Z")
    return "".join(parts)


def build_map_svg(slug: str, label: str, features: str, kind: str) -> str:
    outline = yaml.safe_load(OUTLINE.read_text(encoding="utf-8"))
    return (
        f'<svg class="dataset-map" viewBox="{outline["viewbox"]}" role="img" '
        f'aria-label="{label}" preserveAspectRatio="xMidYMid meet">'
        f'<path class="dataset-map__land" d="{outline["path"].strip()}"/>'
        f'<g class="dataset-map__features" data-kind="{kind}">{features}</g>'
        f"</svg>"
    )


# --------------------------------------------------------------------------
# archive handling
# --------------------------------------------------------------------------


def normalise_archive(entries: dict[str, bytes]) -> tuple[dict[str, bytes], dict]:
    """Flatten, transcode and re-delimit one archive."""
    normalised: dict[str, bytes] = {}
    notes = {"encoding_fixed": [], "delimiter_fixed": [], "flattened": []}

    for name, raw in entries.items():
        if name.endswith("/"):
            continue
        flat = name.split("/")[-1]
        if flat != name:
            notes["flattened"].append(f"{name} -> {flat}")

        lower = flat.lower()
        if lower.endswith("metadata.txt"):
            text = decode_text(raw)
            if text.encode("utf-8") != raw:
                notes["encoding_fixed"].append(flat)
            normalised[flat] = text.encode("utf-8")
        elif lower.endswith(".csv"):
            text = decode_text(raw)
            delimiter = sniff_delimiter(text)
            header, rows = parse_csv(text)
            body = render_csv(header, rows)
            if delimiter != ",":
                notes["delimiter_fixed"].append(f"{flat} ({delimiter!r} -> ',')")
            if body.encode("utf-8") != raw:
                notes.setdefault("encoding_fixed", [])
                if flat not in notes["encoding_fixed"]:
                    notes["encoding_fixed"].append(flat)
            normalised[flat] = body.encode("utf-8")
        else:
            normalised[flat] = raw

    return normalised, notes


def format_bytes(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / 1024 / 1024:.1f} MB"
    if size >= 1024:
        return f"{round(size / 1024)} KB"
    return f"{size} B"


def humanise_language(value: str) -> str:
    match = re.match(r"([A-Za-z]{2})", value or "")
    names = {"FR": "French", "EN": "English", "MG": "Malagasy"}
    return names.get(match.group(1).upper(), value) if match else (value or "Not specified")


def epsg_from_crs(value: str):
    match = re.search(r"EPSG[:\s]*(\d+)", value or "")
    return int(match.group(1)) if match else None


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def build_description_index(meta_fields: list[dict]) -> dict[str, str]:
    """Index documented field descriptions by exact and normalised name."""
    index: dict[str, str] = {}
    for field in meta_fields:
        name = field.get("name", "")
        description = field.get("description", "")
        if not name:
            continue
        index.setdefault(name, description)
        index.setdefault(name.replace("_", "").lower(), description)
    return index


def describe_field(column: str, index: dict[str, str]) -> str:
    """Look up a column's description, tolerating the DBF 10-character limit.

    Shapefiles store field names truncated to 10 characters, so a documented
    ``Densite_par_ha`` arrives as ``Densite_pa``. Fall back to a prefix match in
    that direction only, to avoid ambiguous hits.
    """
    if column in index:
        return index[column]
    normalised = column.replace("_", "").lower()
    if normalised in index:
        return index[normalised]
    for name, description in index.items():
        if name.startswith(normalised):
            return description
    return ""


def public_record(dataset: dict) -> dict:
    """The dataset without build-time presentation payloads."""
    return {key: value for key, value in dataset.items() if key != "map_svg"}


def main() -> None:
    curated = {entry["file"]: entry for entry in yaml.safe_load((DATA / "dataset_meta.yml").read_text(encoding="utf-8"))}
    themes = {item["slug"]: item["label"] for item in yaml.safe_load((DATA / "dataset_themes.yml").read_text(encoding="utf-8"))}
    licenses = yaml.safe_load((DATA / "licenses.yml").read_text(encoding="utf-8"))
    site = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    site_url = (site.get("url") or "").rstrip("/")

    catalog = []
    COLLECTION.mkdir(exist_ok=True)

    for zip_path in sorted(DATASETS.glob("*.zip")):
        entry = curated.get(zip_path.name)
        if not entry:
            print(f"skip {zip_path.name}: no entry in _data/dataset_meta.yml")
            continue

        with zipfile.ZipFile(zip_path) as archive:
            original = {info.filename: archive.read(info) for info in archive.infolist()}

        normalised, notes = normalise_archive(original)

        meta_name = next((n for n in normalised if n.lower().endswith("metadata.txt")), None)
        meta = parse_metadata(decode_text(normalised[meta_name])) if meta_name else {}

        # Rewrite the archive in place with the same filename. A fixed
        # timestamp keeps the bytes identical across runs, so a rebuild does
        # not churn the repository.
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as out:
            for name in sorted(normalised):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                out.writestr(info, normalised[name])
        zip_path.write_bytes(buffer.getvalue())
        zip_bytes = zip_path.stat().st_size

        # Raw CSVs, so nobody has to unzip a 5 KB file.
        files = []
        csv_files = [n for n in sorted(normalised) if n.lower().endswith(".csv")]
        for name in csv_files:
            target = DATASETS / name
            target.write_bytes(normalised[name])
            header, rows = parse_csv(decode_text(normalised[name]))
            files.append(
                {
                    "name": name,
                    "path": f"/datasets/{name}",
                    "url": f"{site_url}/datasets/{name}" if site_url else f"/datasets/{name}",
                    "format": "CSV",
                    "bytes": target.stat().st_size,
                    "size": format_bytes(target.stat().st_size),
                    "records": len(rows),
                    "delimiter": "comma",
                }
            )

        declared_format = meta.get("format", "") or "ZIP"

        records = None
        fields = []
        bounds = None
        dbf_fields = None

        if csv_files:
            header, rows = parse_csv(decode_text(normalised[csv_files[0]]))
            records = sum(f["records"] for f in files)
            documented = build_description_index(meta.get("fields", []))
            fields = [
                {"name": column, "type": "", "description": describe_field(column, documented)}
                for column in header
            ]
            preview_rows = rows[:8]
            preview = {"columns": header, "rows": preview_rows}
        else:
            dbf_name = next((n for n in normalised if n.lower().endswith(".dbf")), None)
            shp_name = next((n for n in normalised if n.lower().endswith(".shp")), None)
            if dbf_name:
                dbf_fields = dbf_schema(normalised[dbf_name])
                records = dbf_fields["records"]
            if shp_name:
                bounds = shp_bounds(normalised[shp_name])
            documented = build_description_index(meta.get("fields", []))
            source_fields = dbf_fields["fields"] if dbf_fields else []
            for field in source_fields:
                fields.append(
                    {
                        "name": field["name"],
                        "type": field["type"],
                        "description": describe_field(field["name"], documented),
                    }
                )
            preview = None
            if not fields:
                fields = [{"name": f["name"], "type": "", "description": f["description"]} for f in meta.get("fields", [])]

        if not files:
            # Shapefiles are useless split across four files, so the archive
            # stays the single download and is presented as one entry. Built
            # here, after the record count is known.
            files.append(
                {
                    "name": zip_path.name,
                    "path": f"/datasets/{zip_path.name}",
                    "url": f"{site_url}/datasets/{zip_path.name}" if site_url else f"/datasets/{zip_path.name}",
                    "format": declared_format,
                    "bytes": zip_bytes,
                    "size": format_bytes(zip_bytes),
                    "records": records,
                    "delimiter": None,
                }
            )

        licence = licenses.get(entry["license"], {})
        author = meta.get("author", "")
        if entry["license"] == "ODbL-1.0":
            attribution = "© OpenStreetMap contributors"
        else:
            attribution = f"© {author}" if author else ""

        # Mini-maps, only where the coordinates are actually usable.
        map_svg = None
        projector = Projector(bounds or [43.177, -25.606, 50.485, -11.951])
        if entry["geometry"] == "point" and csv_files:
            header, rows = parse_csv(decode_text(normalised[csv_files[0]]))
            try:
                lon_i = header.index("Longitude")
                lat_i = header.index("Latitude")
            except ValueError:
                lon_i = lat_i = None
            if lon_i is not None:
                dots = []
                for row in rows:
                    try:
                        x, y = projector(float(row[lon_i]), float(row[lat_i]))
                    except (ValueError, IndexError):
                        continue
                    dots.append(f'<circle cx="{x}" cy="{y}" r="6"/>')
                if dots:
                    map_svg = build_map_svg(
                        entry["slug"],
                        f"Locations of the {len(dots)} records in {entry['title']}",
                        "".join(dots),
                        "point",
                    )
        elif entry["geometry"] == "polygon" and csv_files:
            header, rows = parse_csv(decode_text(normalised[csv_files[0]]))
            if "poly_wkt" in header:
                wkt_i = header.index("poly_wkt")
                polygons: list[list[tuple[float, float]]] = []
                bubbles: list[tuple[float, float]] = []
                for row in rows:
                    rings = wkt_rings(row[wkt_i] if wkt_i < len(row) else "")
                    if not rings:
                        continue
                    ring = max(rings, key=ring_area)
                    if ring_area(ring) >= POLYGON_MIN_DEGREES:
                        polygons.append(ring)
                    else:
                        xs = [point[0] for point in ring]
                        ys = [point[1] for point in ring]
                        bubbles.append((sum(xs) / len(xs), sum(ys) / len(ys)))

                parts = []
                if polygons:
                    parts.append(f'<path d="{path_from_rings(polygons, projector, LAKES_SIMPLIFY_TOL)}"/>')
                for lon, lat in bubbles:
                    x, y = projector(lon, lat)
                    parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2"/>')

                if parts:
                    total = len(polygons) + len(bubbles)
                    map_svg = build_map_svg(
                        entry["slug"],
                        f"Distribution of {total} features in {entry['title']}",
                        "".join(parts),
                        "polygon",
                    )

        dataset = {
            "slug": entry["slug"],
            "title": entry["title"],
            "summary": entry["summary"],
            "theme": entry["theme"],
            "theme_label": themes.get(entry["theme"], entry["theme"].title()),
            "geometry": entry["geometry"],
            "geometry_label": {"point": "Points", "polygon": "Polygons", "none": "No geometry"}.get(entry["geometry"], entry["geometry"]),
            "tags": entry.get("tags", []),
            "license": entry["license"],
            "license_short": licence.get("short", entry["license"]),
            "license_name": licence.get("name", entry["license"]),
            "license_url": licence.get("url", ""),
            "license_summary": licence.get("summary", ""),
            "attribution": attribution,
            "source": entry.get("source", ""),
            "format": declared_format,
            "crs": meta.get("crs", ""),
            "crs_epsg": epsg_from_crs(meta.get("crs", "")),
            "language": meta.get("language", ""),
            "language_label": humanise_language(meta.get("language", "")),
            "author": author,
            "date": meta.get("date", ""),
            "original_title": meta.get("original_title", ""),
            "original_description": meta.get("original_description", ""),
            "records": records,
            "bounds": bounds,
            "zip_path": f"/datasets/{zip_path.name}",
            "zip_url": f"{site_url}/datasets/{zip_path.name}" if site_url else f"/datasets/{zip_path.name}",
            "zip_bytes": zip_bytes,
            "zip_size": format_bytes(zip_bytes),
            "files": files,
            "primary_path": files[0]["path"],
            "primary_format": declared_format,
            "fields": fields,
            "preview": preview,
            "map_svg": map_svg,
        }
        catalog.append(dataset)

        (COLLECTION / f"{entry['slug']}.md").write_text(
            f"---\nslug: {entry['slug']}\n---\n", encoding="utf-8"
        )
        (DATASETS / f"{entry['slug']}.json").write_text(
            json.dumps(public_record(dataset), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        fixed = len(notes["encoding_fixed"]) + len(notes["delimiter_fixed"])
        print(
            f"{entry['slug']:<20} {records if records is not None else '-':>6} records  "
            f"{format_bytes(zip_bytes):>8} zip  {len(fields):>2} fields  "
            f"{'map' if map_svg else '   '}  {fixed} fixed"
        )

    (DATA / "datasets.yml").write_text(
        yaml.safe_dump(catalog, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8"
    )

    # Machine-readable catalog.
    (DATASETS / "catalog.json").write_text(
        json.dumps(
            {
                "title": "Open data by Dolly Andriatsiferana",
                "homepage": site_url or "/",
                "count": len(catalog),
                "datasets": [public_record(item) for item in catalog],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    with (DATASETS / "catalog.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["slug", "title", "theme", "format", "geometry", "records", "crs", "language", "author", "date", "license", "download", "zip"])
        for item in catalog:
            writer.writerow(
                [
                    item["slug"],
                    item["title"],
                    item["theme_label"],
                    item["primary_format"],
                    item["geometry_label"],
                    item["records"] if item["records"] is not None else "",
                    item["crs"],
                    item["language_label"],
                    item["author"],
                    item["date"],
                    item["license_short"],
                    item["primary_path"],
                    item["zip_path"],
                ]
            )

    print(f"\n{len(catalog)} datasets -> _data/datasets.yml, datasets/catalog.json, datasets/catalog.csv")


if __name__ == "__main__":
    main()
