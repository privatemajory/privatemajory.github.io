---
layout: page
title: About
permalink: /about/
kicker: About
summary: "Geographer and geomatics specialist, currently a field GIS specialist at Médecins Sans Frontières in Madagascar."
description: "About Dolly Andriatsiferana, a geographer and geomatics specialist working across the geospatial chain of collection, analysis and delivery for NGOs and institutions in Madagascar."
---

<section class="about-intro">
  <figure class="about-portrait">
    <picture>
      <source type="image/webp"
              srcset="{{ '/assets/images/profile/portrait-480.webp' | relative_url }} 480w, {{ '/assets/images/profile/portrait-900.webp' | relative_url }} 900w"
              sizes="(min-width: 860px) 34vw, 90vw">
      <img src="{{ '/assets/images/profile/portrait-480.jpg' | relative_url }}"
           alt="Portrait of Dolly Andriatsiferana"
           width="480"
           height="480"
           loading="eager"
           decoding="async">
    </picture>
  </figure>

  <div class="about-intro__text">
    <p>I am a geographer and geomatics specialist, currently a field GIS specialist at Médecins Sans Frontières in Madagascar. For eight years I have worked across the whole geospatial chain, collecting, analysing and delivering data for NGOs and institutions including MSF, Operation Fistula and GRET, mostly in community health, humanitarian response and development.</p>
    <p>Most of my work is about Madagascar: its relief, its cities, the way people move across both. I care about maps that explain something rather than decorate it, which usually means starting from the data, whether a digital elevation model, a road network or a census table, and working out what question it can actually answer before opening a design tool.</p>
    <p>I build GIS solutions rather than one-off maps: spatial databases held to OpenStreetMap standards, automation in FME and Python, dashboards and small web applications. I have contributed to OpenStreetMap since 2015, and I share the results here: the maps, the datasets and the notes on how they were made.</p>
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
