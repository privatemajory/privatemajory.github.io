# Adding a dataset

The archive in `datasets/` is the **source of truth**. Each one ships its own
`metadata.txt`, and `scripts/build_datasets.py` reads the facts out of it:
title, author, date, CRS, language, source and the field schema. You never type
those into a template.

The only hand-written part is the English-facing copy, the theme and the
licence, in `_data/dataset_meta.yml`.

---

## Quick start

1. Build a ZIP containing your data file(s) **and** a `metadata.txt`.
2. Drop the ZIP in `datasets/`.
3. Add an entry to `_data/dataset_meta.yml`.
4. If the theme is new, add it to `_data/dataset_themes.yml`.
5. Run the builder, then Jekyll:

   ```sh
   python scripts/build_datasets.py
   bundle exec jekyll build
   ```

6. Commit the ZIP, the generated files, and your `dataset_meta.yml` entry.

---

## `metadata.txt`

Plain `key: value` lines, followed by a field list. French or English keys are
both accepted; matching is case-insensitive and by **substring**, and the first
match wins.

| Key (any of) | Becomes | Used for |
| --- | --- | --- |
| `Titre`, `Title` | `original_title` | Shown as provenance under "Original description" |
| `Auteur`, `Author` | `author` | The citation block and the CC BY-SA attribution |
| anything containing `Date` | `date` | "First published" |
| `Description` | `original_description` | Quoted on the dataset page |
| `Langue`, `Language` | `language` | `FR` → French, `EN` → English, `MG` → Malagasy |
| `Format` | `format` | Shown as the dataset's format, e.g. `CSV`, `Shapefile` |
| `Système de coordonnées`, `Coordinate system` | `crs` | An `EPSG:xxxx` code is extracted if present |
| `Nom du fichier`, `Files` | `declared_files` | Informational only |

Then a line that is exactly `Champs:`, `Fields:` or `Colonnes:` switches to field
mode. Every line after it must look like `- field_name: description`:

```
Nom du fichier:               mg_sante_v1.csv
Format:                       CSV
Système de coordonnées:       WGS 84 Latitude Longitude (EPSG 4326)
Langue:                       FR (Français)
Titre:                        Centres de santé à Madagascar
Auteur:                       Manda Andriatsiferana
Date de la première version:  2026-01-15
Description:                  Une liste des centres de santé de base à Madagascar.

Champs:
  - nom:       Nom du centre
  - region:    Région
  - longitude: Longitude (degré décimal)
  - latitude:  Latitude (degré décimal)
```

> **The field list must come last.** Once `Champs:` is seen, every remaining
> line is parsed as a field, so nothing can follow it.

### Field names must match your columns

Descriptions are matched to actual columns in this order:

1. exact name,
2. underscores stripped and lowercased,
3. **prefix match**: `Densite_pa` picks up the description for `Densite_par_ha`.

Step 3 exists because **shapefiles truncate field names to 10 characters** in
the DBF. If a description is missing on the dataset page, the name in
`metadata.txt` doesn't line up with the real column.

---

## `_data/dataset_meta.yml`

One entry per archive. All paths relative to the repository root.

| Field | Required | Purpose |
| --- | --- | --- |
| `file` | yes | The ZIP filename. **This is the join key.** It must match exactly. |
| `slug` | yes | URL: `/datasets/<slug>/`. Also the JSON filename. |
| `title` | yes | English title shown on the site |
| `summary` | yes | One-line English summary |
| `theme` | yes | Must exist in `_data/dataset_themes.yml` |
| `license` | yes | Must exist in `_data/licenses.yml` |
| `geometry` | yes | `point`, `polygon` or `none` |
| `source` | no | Provenance line, e.g. `INSTAT, 2009` |
| `tags` | no | Extra search keywords |

```yaml
- file: mg_sante_v1.zip
  slug: health-facilities
  title: Health facilities in Madagascar
  summary: Basic health centres with their region and coordinates.
  theme: health
  license: CC-BY-SA-4.0
  geometry: point
  source: Ministère de la Santé
  tags:
    - health
    - services
```

A `file` with no matching entry is **skipped** with
`skip <name>.zip: no entry in _data/dataset_meta.yml`.

---

## Themes and licences

**Themes** live in `_data/dataset_themes.yml`. A dataset whose theme is not
registered still appears in the catalog and in search, but gets **no facet
button**, so it is only reachable via "All".

```yaml
- slug: health
  label: Health
```

**Licences** live in `_data/licenses.yml`, keyed by the id used in
`dataset_meta.yml`, and carry the name, URL and a one-line summary shown on the
dataset page.

> **OpenStreetMap-derived data must be ODbL, not CC BY-SA.** CC BY-SA is not on
> ODbL's compatible-licence list, so publishing OSM-derived geometry under it
> would not satisfy ODbL's share-alike clause. That is why `lakes` uses
> `ODbL-1.0` while everything else uses `CC-BY-SA-4.0`.

---

## What the builder does

`scripts/build_datasets.py` uses only the standard library plus PyYAML, which
the image pipeline already requires. No GIS libraries.

For each archive it:

1. parses `metadata.txt`, and reads CSV headers and row counts;
2. reads the DBF schema and the SHP bounding box with `struct`;
3. **normalises the archive in place**: transcodes cp1252/latin-1 text to
   UTF-8, unifies delimiters to the RFC 4180 comma, and flattens nested folders.
   Filenames are unchanged, so existing download URLs keep working, and a fixed
   ZIP timestamp keeps rebuilds byte-identical;
4. writes the raw CSVs next to the archive, and makes the raw CSV the **primary**
   download for CSV datasets;
5. renders a mini-map where the coordinates allow it;
6. writes `_data/datasets.yml`, `_datasets/<slug>.md`, `datasets/<slug>.json`,
   and refreshes `datasets/catalog.json` and `datasets/catalog.csv`.

Generated files are committed, so a plain `jekyll build` works without Python.

---

## Mini-maps

Rendered as inline SVG, so they follow the light/dark theme automatically.

| Condition | Result |
| --- | --- |
| `geometry: point` + columns named exactly `Longitude` and `Latitude` | A dot per record |
| `geometry: polygon` + a column named exactly `poly_wkt` | Outlines ≥ ~9 km², points for smaller ones |
| `geometry: polygon` + shapefile | A coverage statement from the bbox |
| Anything else | No map |

Column names are matched exactly and are case-sensitive. The projection assumes
**Madagascar**: `_data/madagascar_outline.yml` is the country outline, and a
point dataset without a shapefile falls back to Madagascar's bounding box.

---

## Gotchas

- **The archive must be a `.zip`.** The builder globs `datasets/*.zip`.
- **`file:` must match the ZIP filename exactly**, or the dataset is skipped.
- **Only the first CSV alphabetically** supplies the preview and the schema. Any
  others are still listed and downloadable (see `road-profiles`, which ships four).
- **The `Champs:` block must be last** in `metadata.txt`.
- **A missing `metadata.txt` will not break the build.** You get "Not stated"
  for author and date, and no field descriptions.
- **Licence attribution is derived**: ODbL datasets are attributed to
  "© OpenStreetMap contributors"; everything else to the `Auteur` from
  `metadata.txt`.
- **Renaming a slug changes the URL** and breaks links to the old one. Renaming
  the ZIP is safe as long as you update `file:`.

---

## Verifying

```sh
python scripts/check_links.py     # every internal link resolves in _site
```

Then check that:

- the dataset appears at `/datasets/`,
- its facet button shows the right count,
- searching for a **field name** finds it (the quickest proof that
  `metadata.txt` parsed),
- `/datasets/<slug>/` renders the schema, preview and licence,
- `datasets/<slug>.json` is valid JSON.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| `skip …zip: no entry in _data/dataset_meta.yml` | `file:` doesn't match the ZIP name |
| No facet button for a dataset | Theme missing from `_data/dataset_themes.yml` |
| Author shows "Not stated" | `Auteur:`/`Author:` missing or misspelled in `metadata.txt` |
| Field descriptions blank | Field name doesn't line up with the column (see above) |
| No mini-map | Geometry is `none`, or the coordinate columns aren't named exactly |
| CRS shows "Not specified" | No `Système de coordonnées` line in `metadata.txt` |
