---
title: Least cost itinerary
summary: An interactive app that estimates the fastest walking route between two points in rural Madagascar, using elevation and surface roughness instead of straight-line distance.
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

The app answers a simple question with a terrain-aware answer: what is the fastest way to travel across rural Madagascar?

Instead of drawing a straight line, it combines elevation and surface-roughness data to estimate a least-cost route. The result is a path that follows the terrain and a profile chart that shows where the walking gets steep.

## What it does

- Pick a start and end point directly on the map.
- Estimate the fastest walking route across the terrain.
- Read the distance and elevation profile for the chosen path.
- Compare how the route changes when the endpoints move.

## How it works

The route is calculated over a terrain model that accounts for both slope and ground roughness. The map is rendered with Leaflet, the calculation runs in a small Flask application, and Chart.js draws the route profile.

The application is built for rural Madagascar, where steep terrain and uneven ground make distance alone a poor guide to travel time.

## Try it

The app is live at [apps.privatemajory.top/lcpath](https://apps.privatemajory.top/lcpath). It is part of a small collection of geospatial web applications hosted at [apps.privatemajory.top](https://apps.privatemajory.top/).
