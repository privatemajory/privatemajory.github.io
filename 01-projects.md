---
layout: page
title: Projects
permalink: /projects/
projects:
  - title: "Optimal walking paths"
    icon: "fas fa-map"
    status: "Web application"
    description: "An interactive web application that uses elevation and roughness data to estimate the fastest path between two points in the Ikongo district. Users can adjust parameters like season, base speed, maximum slope, and uphill/downhill costs to see how different conditions affect the optimal route."
    thumbnail: "lcpath.jpg"
    tech_stack:
      - "Flask"
      - "Leaflet.js"
      - "JavaScript"
      - "GeoJSON"
      - "Rasters"
    demo_url: "https://privatemajory.pythonanywhere.com/"
    details_url: "#"
---

<p>Discover my collection of interactive web applications developed with Python, showcasing data visualization, cartographic solutions, and innovative tools</p>

<div class="project-grid">
  {%- for project in page.projects -%}
    <div class="project-card">
      <div class="project-thumbnail" style="background-image: url('/img/{{ project.thumbnail }}');"></div>
      <div class="project-content">
        <div class="project-header">
          <h3 class="project-title">
            <i class="{{ project.icon }}"></i>{{ project.title }}
          </h3>
          <span class="project-status">{{ project.status }}</span>
        </div>
        <p class="project-description">{{ project.description }}</p>
        <div class="tech-stack">
          {%- for tech in project.tech_stack -%}
            <span class="tech-tag">{{ tech }}</span>
          {%- endfor -%}
        </div>
        <div class="project-links">
          <a href="{{ project.demo_url }}" class="project-link primary" target="_blank">
            <i class="fas fa-rocket"></i> Live demo
          </a>
          <a href="{{ project.details_url }}" class="project-link secondary">
            <i class="fas fa-info-circle"></i> Details
          </a>
        </div>
      </div>
    </div>
  {%- endfor -%}
</div>
