---
layout: page
title: Projects
permalink: /projects/
kicker: Web applications
summary: "Small tools built around a single geographic question: how far, how steep, how reachable."
description: "Interactive web applications built with Python and open geospatial tools, including terrain-aware walking routes in rural Madagascar."
---

<div class="project-grid">
  {%- assign projects = site.projects | sort: "order" -%}
  {%- for project in projects -%}
    {% include project-card.html project=project level=2 %}
  {%- endfor -%}
</div>

<p class="collection-foot">
  <a class="link-arrow" href="https://apps.privatemajory.top/" target="_blank" rel="noopener">
    All apps at apps.privatemajory.top
    {% include icon.html name="arrow-up-right" class="icon" %}
  </a>
</p>
