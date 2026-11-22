#!/usr/bin/env python3
"""Generate the responsive image set used by the site.

Source originals stay out of the published build (see `exclude` in
_config.yml); this script writes WebP/JPEG derivatives into assets/images.
Run from the repository root:

    python scripts/build_images.py
"""

from __future__ import annotations

import io
import json
import urllib.request
from pathlib import Path

import yaml
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "gallery_content"
OUT = ROOT / "assets" / "images"
MAP_WIDTHS = (640, 1200, 1920)
HERO_WIDTHS = (1280, 1920, 2560)
WEBP_QUALITY = 80
JPEG_QUALITY = 82


def load_rgb(path: Path) -> Image.Image:
    image = Image.open(path)
    image = ImageOps.exif_transpose(image)
    if image.mode in ("RGBA", "LA", "P"):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, (247, 243, 234))
        background.paste(image, mask=image.getchannel("A"))
        return background
    return image.convert("RGB")


def resize(image: Image.Image, width: int) -> Image.Image:
    height = max(1, round(image.height * width / image.width))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_webp(image: Image.Image, base: Path, width: int) -> None:
    resized = resize(image, width)
    resized.save(
        base.with_name(f"{base.name}-{width}.webp"),
        "WEBP",
        quality=WEBP_QUALITY,
        method=6,
    )


def save_jpg(image: Image.Image, base: Path, width: int) -> None:
    resized = resize(image, width)
    resized.save(
        base.with_name(f"{base.name}-{width}.jpg"),
        "JPEG",
        quality=JPEG_QUALITY,
        optimize=True,
        progressive=True,
    )


def widths_for(original_width: int, candidates: tuple[int, ...]) -> list[int]:
    widths = [width for width in candidates if width < original_width - 40]
    widths.append(min(original_width, candidates[-1]))
    return sorted(set(widths))


def build_map_images() -> dict:
    maps = yaml.safe_load((ROOT / "_data" / "maps.yml").read_text(encoding="utf-8"))
    sizes: dict[str, dict] = {}
    out_dir = OUT / "maps"
    out_dir.mkdir(parents=True, exist_ok=True)

    for entry in maps:
        source = SOURCE / entry["image"]
        if not source.exists():
            print(f"missing source: {source}")
            continue
        image = load_rgb(source)
        widths = widths_for(image.width, MAP_WIDTHS)
        base = out_dir / entry["slug"]
        for width in widths:
            save_webp(image, base, width)
        # One modest JPEG fallback for browsers without WebP support.
        save_jpg(image, base, min(widths[0], 800))
        largest = widths[-1]
        sizes[entry["slug"]] = {
            "width": largest,
            "height": max(1, round(image.height * largest / image.width)),
            "widths": widths,
        }
        print(f"map {entry['slug']:<20} {image.width}x{image.height} -> {widths}")

    (ROOT / "_data" / "map_sizes.yml").write_text(
        yaml.safe_dump(sizes, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return sizes


def build_hero() -> None:
    source = SOURCE / "2023-07-12_b3d_itasy_hexagons.jpg"
    image = load_rgb(source)
    out_dir = OUT / "hero"
    out_dir.mkdir(parents=True, exist_ok=True)
    for width in widths_for(image.width, HERO_WIDTHS):
        save_webp(image, out_dir / "itasy", width)
        print(f"hero {width}")
    save_jpg(image, out_dir / "itasy", 1280)


def build_project_cards() -> None:
    jobs = [
        ("lcpath", ROOT / "img" / "lcpath.jpg"),
    ]
    for slug, source in jobs:
        if not source.exists():
            print(f"missing card source: {source}")
            continue
        image = load_rgb(source)
        out_dir = OUT / "projects"
        out_dir.mkdir(parents=True, exist_ok=True)
        widths = widths_for(image.width, (800, 1200, 1600))
        for width in widths:
            save_webp(image, out_dir / slug, width)
        save_jpg(image, out_dir / slug, widths[0])
        print(f"card projects/{slug:<12} {image.width}x{image.height} -> {widths}")


def build_blog_assets() -> None:
    """Small square thumbnails for the index plus a 1200x630 social image.

    Blog posts do not have a representative wide image, so the index uses a
    square crop and the social card uses a separate, deliberately chosen
    source rather than the full-width graph in the article body.
    """
    jobs = [
        ("road-networks", ROOT / "img" / "road-network-comps.png", (0.5, 0.5)),
        ("osm-mapping", ROOT / "img" / "village_mapping.png", (0.5, 0.5)),
        ("road-steepness", ROOT / "img" / "mdg_urban_road_slope_2.png", (0.5, 0.35)),
    ]
    out_dir = OUT / "blog"
    out_dir.mkdir(parents=True, exist_ok=True)

    for slug, source, centering in jobs:
        if not source.exists():
            print(f"missing blog source: {source}")
            continue
        image = load_rgb(source)

        side = min(image.width, image.height)
        square = ImageOps.fit(image, (side, side), method=Image.Resampling.LANCZOS, centering=centering)
        for size in (160, 320):
            square.resize((size, size), Image.Resampling.LANCZOS).save(
                out_dir / f"{slug}-square-{size}.webp", "WEBP", quality=84, method=6
            )

        social = ImageOps.fit(image, (1200, 630), method=Image.Resampling.LANCZOS, centering=centering)
        social.save(out_dir / f"{slug}-og.jpg", "JPEG", quality=84, optimize=True, progressive=True)

        print(f"blog {slug:<16} {image.width}x{image.height} -> square 160/320 + og 1200x630")


def build_profile() -> None:
    url = "https://raw.githubusercontent.com/privatemajory/signature/master/img/profile.png"
    out_dir = OUT / "profile"
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = response.read()
    except Exception as error:  # noqa: BLE001 - report and keep going
        print(f"profile download failed: {error}")
        return
    image = Image.open(io.BytesIO(data))
    image = ImageOps.exif_transpose(image).convert("RGB")
    side = min(image.width, image.height)
    image = ImageOps.fit(image, (side, side), method=Image.Resampling.LANCZOS, centering=(0.5, 0.35))
    for width in (480, 900):
        resized = image.resize((width, width), Image.Resampling.LANCZOS)
        resized.save(out_dir / f"portrait-{width}.webp", "WEBP", quality=84, method=6)
        resized.save(out_dir / f"portrait-{width}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    print("profile portrait 480/900")


def build_og_image() -> None:
    source = SOURCE / "2023-07-12_b3d_itasy_hexagons.jpg"
    image = load_rgb(source)
    image = ImageOps.fit(image, (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    image = ImageEnhance.Brightness(image).enhance(0.72)
    image = ImageEnhance.Contrast(image).enhance(1.05)
    (OUT / "og-default.jpg").parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT / "og-default.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    print("og-default.jpg 1200x630")


def main() -> None:
    for folder in ("maps", "hero", "projects", "blog", "profile"):
        (OUT / folder).mkdir(parents=True, exist_ok=True)
    build_map_images()
    build_hero()
    build_project_cards()
    build_blog_assets()
    build_profile()
    build_og_image()

    total = sum(path.stat().st_size for path in OUT.rglob("*") if path.is_file())
    print(f"total generated: {total / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    main()
