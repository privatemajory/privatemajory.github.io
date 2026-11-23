---
layout: page
title: About
permalink: /about/
kicker: About
summary: "Geographer and GIS specialist based in Madagascar."
description: "Dolly Andriatsiferana is a geographer and GIS specialist working in Madagascar."
experience_start_date: "2018-04-01"
---

{%- assign experience_start_year = page.experience_start_date | date: "%Y" | plus: 0 -%}
{%- assign experience_years = site.time | date: "%Y" | plus: 0 | minus: experience_start_year -%}
{%- assign experience_start_month_day = page.experience_start_date | date: "%m%d" | plus: 0 -%}
{%- assign current_month_day = site.time | date: "%m%d" | plus: 0 -%}
{%- if current_month_day < experience_start_month_day -%}
  {%- assign experience_years = experience_years | minus: 1 -%}
{%- endif -%}

<section class="about-intro">
  <figure class="about-portrait">
    <picture>
      <source type="image/webp"
              srcset="{{ '/assets/images/profile/portrait-480.webp' | relative_url }} 480w, {{ '/assets/images/profile/portrait-900.webp' | relative_url }} 900w"
              sizes="(min-width: 860px) 34vw, 90vw">
      <img src="{{ '/assets/images/profile/portrait-480.jpg' | relative_url }}"
           alt="Portrait of Dolly Andriatsiferana"
           loading="eager"
           decoding="async">
    </picture>
  </figure>

  <div class="about-intro__text">
    <p>I am a geographer, GIS and open data specialist. I have spent {{ experience_years }} {% if experience_years == 1 %}year{% else %}years{% endif %} collecting, analysing and preparing geospatial data for organisations working in community health, humanitarian response and local development.</p>
    <p>Most of my work is about Madagascar: its physical environment, its human settlements, and how both interact. I care about maps that explain something out of the data, working out what question it can actually answer.</p>
  </div>
</section>

<div class="about-sections">
  <section class="about-block">
    <h2>What I do</h2>
    <ul>
      <li>Cartography and data visualization</li>
      <li>Data processing and spatial analysis</li>
      <li>Web mapping</li>
      <li>Open data</li>
    </ul>
  </section>

  <section class="about-block">
    <h2>Tools</h2>
    <ul>
      <li>QGIS · GRASS GIS · ArcGIS Pro · Tableau · Dash</li>
      <li>FME · PostGIS · Python</li>
      <li>Leaflet.js · ArcGIS Online · Flask · GeoServer</li>
      <li>OpenStreetMap · Wikidata</li>
    </ul>
  </section>

  <section class="about-block">
    <h2>Elsewhere</h2>
    <ul>
      {%- for link in site.data.social -%}
        <li>
          <a href="{{ link.url }}"{% unless link.url contains 'mailto:' %} target="_blank" rel="me noopener"{% endunless %}>{{ link.title }}</a>
        </li>
      {%- endfor -%}
    </ul>
  </section>
</div>

<section class="about-block about-work">
  <h2>Selected work</h2>
  <div class="about-work__links">
    <a class="link-arrow" href="{{ '/gallery/' | relative_url }}">Maps{% include icon.html name="arrow-right" class="icon" %}</a>
    <a class="link-arrow" href="{{ '/projects/' | relative_url }}">Web applications{% include icon.html name="arrow-right" class="icon" %}</a>
    <a class="link-arrow" href="{{ '/datasets/' | relative_url }}">Open datasets{% include icon.html name="arrow-right" class="icon" %}</a>
  </div>
</section>
