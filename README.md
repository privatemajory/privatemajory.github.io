# privatemajory.github.io

Source for [privatemajory.github.io](https://privatemajory.github.io/), the
portfolio and map archive of Dolly Andriatsiferana.

Built with Jekyll 4 and a small amount of vanilla JavaScript. No CSS framework,
no jQuery, no runtime dependencies.

## Requirements

- Ruby 3.2+ with Bundler
- Python 3.10+ with Pillow and PyYAML (only to regenerate images)

## Local development

```sh
bundle install
bundle exec jekyll serve
```

The site is served at <http://127.0.0.1:4000/>.

## Regenerating images

The responsive image set in `assets/images/` is generated from the originals in
`gallery_content/`. Run this after adding or changing a map:

```sh
pip install Pillow PyYAML
python scripts/build_images.py
```

The script writes WebP derivatives at 640/1200/1920px (plus a JPEG fallback),
project and post cards, the portrait, and the social preview image, then records
the intrinsic dimensions in `_data/map_sizes.yml`.

Adding a map means: drop the original in `gallery_content/`, add an entry to
`_data/maps.yml`, then regenerate.

## Datasets

`datasets/*.zip` are the source of truth. Each archive ships a `metadata.txt`
recording its title, author, date, CRS, language, source and field schema, and
that is what the site publishes. Nothing about a dataset is typed into a
template by hand.

```sh
python scripts/build_datasets.py
```

The script uses only the standard library plus PyYAML (already required by the
image pipeline). No GIS libraries are needed at build time. It parses each
`metadata.txt`, normalises the archives in place (UTF-8, comma delimiters, flat
folders, with filenames unchanged so download URLs keep working), writes the raw
CSVs alongside, renders dependency-free SVG mini-maps, and emits
`_data/datasets.yml`, `_datasets/<slug>.md`, `datasets/catalog.json`,
`datasets/catalog.csv` and `datasets/<slug>.json`.

**To add a dataset, follow [`docs/datasets.md`](docs/datasets.md)**, which
covers the `metadata.txt` format, the `dataset_meta.yml` fields, themes,
licences, mini-map rules and the common failure modes.

### Licences

Datasets are CC BY-SA 4.0, except `lakes`, which is ODbL 1.0 because its
geometry is derived from OpenStreetMap.

### The country outline

`_data/madagascar_outline.yml` is a simplified national outline, generated once
from the fokontany polygons by dissolving and simplifying at 0.05°, then
pre-projected into the mini-map viewBox. It is a static asset: regenerating it
would need a GIS stack, but nothing at build time does.

## Content

| Path | Purpose |
| --- | --- |
| `_data/maps.yml` | The map archive (title, slug, category, featured) |
| `_data/dataset_meta.yml` | Curated dataset copy, theme and licence (hand-written) |
| `_data/datasets.yml` | Generated dataset catalog; do not edit by hand |
| `_data/navigation.yml` | Header and footer navigation |
| `_data/social.yml` | Footer and About links |
| `_data/map_categories.yml` | Gallery filter categories |
| `_data/dataset_themes.yml` | Dataset facet labels |
| `_data/licenses.yml` | Licence names, URLs and summaries |
| `_projects/` | Project case studies |
| `_datasets/` | Generated dataset stubs, one per dataset |
| `_posts/` | Blog posts |

## Architecture

```
_layouts/        default, home, page, post, project, gallery, dataset
_includes/       head, header, footer, nav-dialog, icon, map-card, project-card, dataset-card, lightbox
_sass/           _fonts, _tokens, _base, _layout, _components, _pages
assets/css/      main.scss (entry point)
assets/js/       main.js (nav, theme, reveal, TOC), gallery.js (filters, lightbox), datasets.js (catalog)
scripts/         build_images.py, build_datasets.py, check_links.py
docs/            datasets.md (how to add a dataset)
```

Design tokens live in `_sass/_tokens.scss` as CSS custom properties, including a
dark theme under `[data-theme="dark"]`. Fonts are self-hosted:
Satoshi (Fontshare) for UI and body, Fraunces (SIL OFL) for display.

## Deployment

`.github/workflows/pages.yml` builds and deploys to GitHub Pages. Set the Pages
source to **GitHub Actions** in the repository settings. The workflow generates
images, builds the dataset catalog, builds with Jekyll, and uploads the
artifact.

## Checks

```sh
python scripts/check_links.py   # verifies every internal link resolves in _site
```

Every page scores 100 for accessibility, best practices and SEO in Lighthouse.
