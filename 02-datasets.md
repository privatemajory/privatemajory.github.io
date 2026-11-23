---
layout: page
title: Datasets
permalink: /datasets/
kicker: Open data
summary: "Free geospatial datasets for Madagascar, packaged for reuse."
description: "Free datasets about Madagascar: population, schools, power plants, lakes, roads and Bank of Africa offices. CSV and shapefile, with field schemas and previews."
---

{%- assign datasets = site.data.datasets -%}
{%- assign formats = datasets | map: "primary_format" | uniq -%}

<p class="lede">Download the datasets and check their fields, coordinate systems, sources and licences before using them.</p>

<div class="catalog" data-catalog>

  <div class="catalog__controls">
    <div class="catalog__search">
      <label class="visually-hidden" for="dataset-search">Search datasets</label>
      {% include icon.html name="compass" class="icon catalog__search-icon" %}
      <input type="search"
             id="dataset-search"
             placeholder="Search by name, field or tag…"
             autocomplete="off"
             data-dataset-search>
    </div>

    <div class="catalog__filters">
      <div class="filter-group" role="group" aria-label="Filter by theme">
        <button class="filter" type="button" data-dataset-theme="all" aria-pressed="true">
          All<span>{{ datasets.size }}</span>
        </button>
        {%- for theme in site.data.dataset_themes -%}
          {%- assign count = datasets | where: "theme", theme.slug | size -%}
          {%- if count > 0 -%}
            <button class="filter" type="button" data-dataset-theme="{{ theme.slug }}" aria-pressed="false">
              {{ theme.label }}<span>{{ count }}</span>
            </button>
          {%- endif -%}
        {%- endfor -%}
      </div>

      <div class="filter-group" role="group" aria-label="Filter by format">
        <button class="filter" type="button" data-dataset-format="all" aria-pressed="true">Any format</button>
        {%- for format in formats -%}
          {%- assign count = datasets | where: "primary_format", format | size -%}
          <button class="filter" type="button" data-dataset-format="{{ format }}" aria-pressed="false">
            {{ format }}<span>{{ count }}</span>
          </button>
        {%- endfor -%}
      </div>
    </div>

    <div class="catalog__sort">
      <label for="dataset-sort">Sort</label>
      <select id="dataset-sort" data-dataset-sort>
        <option value="theme">Theme</option>
        <option value="title">Title</option>
        <option value="records">Records</option>
        <option value="newest">Newest</option>
      </select>
    </div>
  </div>

  <p class="catalog__count" role="status" data-dataset-count></p>

  <div class="dataset-grid" data-dataset-grid>
    {%- for dataset in datasets -%}
      {% include dataset-card.html dataset=dataset level=2 %}
    {%- endfor -%}
  </div>

  <p class="catalog__empty" data-dataset-empty hidden>
    No datasets match these filters.
    <button class="link-arrow" type="button" data-dataset-reset>Reset filters</button>
  </p>
</div>

<section class="catalog-links">
  <h2>Download the catalog</h2>
  <p>Download the full catalog as JSON or CSV, or get the JSON for a single dataset.</p>
  <ul>
    <li><a href="{{ '/datasets/catalog.json' | relative_url }}"><code>catalog.json</code></a>: every dataset with its fields, licence and file list</li>
    <li><a href="{{ '/datasets/catalog.csv' | relative_url }}"><code>catalog.csv</code></a>: one row per dataset</li>
    <li><code>/datasets/&lt;slug&gt;.json</code>: a single dataset, for example <a href="{{ '/datasets/lakes.json' | relative_url }}"><code>lakes.json</code></a></li>
  </ul>
  <p class="muted">Every file is UTF-8 and comma-delimited. Archives keep their original filenames, so existing download links continue to work.</p>
</section>
