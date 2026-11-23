---
layout: page
title: Projects
permalink: /projects/
kicker: Tools
summary: "Small GIS tools, including an app for estimating walking routes in rural Madagascar."
description: "Web mapping tools by Dolly Andriatsiferana, including an app for estimating walking routes in rural Madagascar."
---

<div class="project-grid">
  {%- assign projects = site.projects | sort: "order" -%}
  {%- for project in projects -%}
    {% include project-card.html project=project level=2 %}
  {%- endfor -%}
</div>

<p class="collection-foot">
  <a class="link-arrow" href="https://apps.privatemajory.top/" target="_blank" rel="noopener">
    Browse all apps
    {% include icon.html name="arrow-up-right" class="icon" %}
  </a>
</p>
