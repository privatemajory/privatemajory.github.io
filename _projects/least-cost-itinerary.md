---
title: Least cost itinerary
summary: A web app that estimates walking routes in rural Madagascar using elevation and surface roughness.
status: Web application
year: "2024"
image_slug: lcpath
image_alt: Map interface of the point-to-point walking route app
app_url: https://apps.privatemajory.top/lcpath
stack:
  - Flask
  - Leaflet.js
  - Chart.js
order: 1
permalink: /projects/walk-between-two-points/
---

The app estimates a walking route between two points in rural Madagascar, taking the terrain into account.

Rather than treating every kilometre as the same, it uses elevation and ground roughness to estimate a least-cost route. The map shows the route, and a profile chart shows its distance and elevation.

## What it does

- Pick a start and end point directly on the map.
- Estimate the fastest walking route across the terrain.
- Read the distance and elevation profile for the chosen path.
- Compare how the route changes when the endpoints move.

## How it works

The route is calculated over a terrain model that accounts for slope and ground roughness. Leaflet displays the map, a Flask app calculates the route, and Chart.js draws the profile.

The app is intended for rural Madagascar, where steep slopes and uneven ground affect travel time.

## Try it

Try the app at [apps.privatemajory.top/lcpath](https://apps.privatemajory.top/lcpath).
