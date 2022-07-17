---
layout: post
title: "Deriving road steepness from a digital elevation model using QGIS"
date: 2019-05-20 10:02:00 +0300
categories: gis
---

Road slopes are an important factor to consider when estimating trip costs and durations. GPS applications sometimes show altitude graphs along itinerary, and consider elevation in trip calculations. Android application [OSMAnd](https://osmand.net/) is one example. In this post I will share one method I have used to fetch road slope data from a digital elevation model (DEM). From the data I could make a slope-along-road graph such as on OSMAnd.

What is needed:
- [QGIS](https://qgis.org/en/site/) software with **qProf** plugin enabled
- some road data in a vector format
- a DEM covering the road data

In this article, I will use as an example the Madagascan Route Nationale 2 (RN 2) from Antananarivo to Toamasina.

<br />
<p class="centeredcontent"><img src="/img/rn2_profile.png" alt="Elevation and slope along the RN 2" /><br /><br />
Elevation and slope along the RN 2. A graph created with the wonderful <a href="https://d3js.org">D3.js</a>.</p>
<br />


## Preparing the data

My elevation data is a Shuttle Radar Topographic Mission (SRTM) DEM with 30 metres spatial resolution. Multiple tiles have been merged to cover the whole RN 2.

My road data has been retrieved from OpenStreetMap. All parts of the RN 2 have been downloaded using [this Overpass query](https://overpass-turbo.eu/?q=LyoKVGhpcyBoYcSGYmVlbiBnxI1lcmF0ZWQgYnkgdGhlIG92xJJwxIlzLXR1cmJvIHdpemFyZC7EgsSdxJ9yaWdpbmFsIHNlxLBjaMSsxIk6CsOiwoDCnHR5cGU6d2HEmmFuxJfEhGdoxZB5PSogxZPEl3JlZj0iTiAyIiDEuiBNYWRhZ8SJY8SwxYjCnQoqLwpbb3V0Ompzb25dW3RpbWXFu8W9MjVdOwovLyBmZXTFgsWdxaBhIMWIwpzFrMWuxbBzxbJyxbTEm8SrxL_FgcWDxLoKe3vEkG9jb2RlQcaYOsadxa_FscSwfX0tPi7GpnLFgsazxYDGjsaQxI_ElMSdciDFoHN1bHRzCigKICDHhXF1xJLEmsSjcnTGkm9yOsaaxYnFlsWYxZHFm8WdxZTHisWhxaPFpcWnxbTHk8WEeVsix6TFmSLGgyLFoGYix6zFpse3KMSwxYDGvsWAx4Box4JhKcaOyInGj8aRcMS3bsedx4vHjcePCsaJxJjGsHnGjj7GjsiWc2tlxL1xdDs&c=Bdgfd8WPKJ).

For things to work, I needed to edit my road data to get **one profile line** at the end, i.e a single feature line from Antananarivo to Toamasina. This means:
- If the line is doubled at some parts (multiple lanes or roundabout), I needed to work it to make it a single line, for example by removing the lane going opposite.
- There should be no gap
- When I was sure there was no more doubled line and all the gaps were filled, I merged all parts to get a single feature line

<br />
<p class="centeredcontent"><img src="/img/doubled_road.gif" alt="Doubled road example" /><br /><br />
Fixing a doubled road section.</p>
<br />


## Resampling

So now I have a line layer with a single feature of the RN 2 from Antananarivo to Toamasina. The next thing to do is choosing a sampling value for the profile. My distance is about 350 km so having a point every 100 m would be too much if I want to visualize it in a 16 cm wide graph (3500 data points!). For the final graph above, I used a sampling of 1 km (about 350 data points) and it looked good enough for a document size graph, without loosing too much detail.

To resample the profile line, I generated points at equal distance of 1 km, then made a new line out of these points. For this, I used the **Points along geometry** processing tool in QGIS, setting the "distance" parameter at 1 km.

To convert the points to a line, I used the **Points to path** processing tool, and used the distance column (created by the previous tool) for the "order field" parameter.

<br />
<p class="centeredcontent"><img src="/img/points_to_path.png" alt="Points to path processing tool" style="width: 90%; max-width: 480px" /><br /><br />
The <em>Points to path</em> processing tool in QGIS.</p>
<br />


## Generating the data

A this point, if it is not the case yet, my profile line (the one I generated from points) and my DEM should be in a projected coordinate system. This is to avoid unit problems in our data. I used the Tananarive (Paris) / Laborde Grid approximation (EPSG 29702), a commonly used projection for Madagascar.

My next step is to generate a profile data from these in qProf, which can be called through the Plugins menu in QGIS's main menu. When the plugin is called, a new qProf panel appears in QGIS's user interface.

Under "Topography" tab, within "DEM input" this is what I did:
- under "Input DEMs" I selected my DEM
- under "Input line" I checked "Line layer" and chose my previously resampled road layer. For the "Line densify distance" I entered my sampling value, 1000 meters.
- I clicked on "Read source data". At this point, qProf warns if the profile exceeds the 10 000 data points limit. This depends on the length of the line and the data points distance. For the sampling value I have chosen, I got 349 data points.

Under "Export" tab and within "Topographic profile data", I exported the data as a CSV text for further editing and visualization in D3.js.

<br />
<p class="centeredcontent"><img src="/img/qprof_interface.png" alt="Generating and exporting the profile data using qProf" style="width: 90%; max-width: 400px" /><br /><br />
Generating and exporting the road profile data using qProf.</p>
<br />

The data I obtained from qProf had these fields:
- ``prof_id``: As I only had one feature in my line layer, it had only one value, 1
- ``rec_id``: Different for each point data, so 1 to 349 in my case
- ``x``: X coordinate
- ``y``: Y coordinate
- ``cds2d``: 2D (horizontal) distance along the profile
- ``z``: Z coordinate (elevation)
- ``cds3d``: 3D (with elevation) distance along the profile
- ``dirslop``: Directional slope along the profile (from Antananarivo to Toamasina) in degrees. Positive values indicate ascents and negative values indicate descents.

The CSV file can be downloaded from [this link](https://raw.githubusercontent.com/privatemajory/rnprof/master/data/profile_n2.csv).

To get the graph at the beginning of this post, I simply plotted the Z coordinate (``z``) and the directional slope (``dirslop``) along the horizontal distance (``cds2d``), to get the elevation and directional slope graphs respectively. I put a live version of the graph with the 4 major roads of Madagascar on [this page](https://privatemajory.github.io/rnprof).

## Going a little further

Using the same base but with a slightly different workflow, I could estimate the average street steepness in the major urban areas of Madagascar:

<br />
<p class="centeredcontent"><img src="/img/mdg_urban_road_slope_2.png" alt="Madagascar average road slope in major urban areas" style="width: 90%; max-width: 480px" /><br /><br />
Average road slope in major urban areas of Madagascar.</p>
<br />
