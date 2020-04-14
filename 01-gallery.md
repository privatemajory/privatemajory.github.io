---
layout: page
title: Gallery
permalink: /gallery/
images:
  - image: 2019-05-21_b3d_andavamamba.png
    caption: Andavamamba
  - image: 2019-05-21_b3d_galapagos.png
    caption: Galapagos
  - image: 2019-05-21_b3d_gorges_tsiribihina.png
    caption: Gorges du Tsiribihina
  - image: 2019-05-21_b3d_tsiroanomandidy_part.png
    caption: Tsiroanomandidy
  - image: 2019-05-21_inkscape_ihorombe_relief_map.png
    caption: Ihorombe
  - image: 2019-05-21_inkscape_mdg_relief_map.png
    caption: Madagascar relief map
  - image: 2019-05-21_qgis_cape_verde.png
    caption: Cape Verde
  - image: 2019-05-21_qgis_galapagos_tanaka.png
    caption: Galapagos Tanaka contours
  - image: 2019-05-21_qgis_mdg_urban_road_slope.png
    caption: Madagascar urban road rlope
  - image: 2019-05-21_qgis_nosy-be.png
    caption: Nosy Be
  - image: 2019-06-29_b3d_nyc.png
    caption: Financial District of Manhattan 3D
  - image: 2019-07-05_qgis_united_kingdoms_of_madagascar.png
    caption: United Kingdoms of Madagascar
  - image: 2019-07-13_b3d_manhattan.png
    caption: Financial District of Manhattan
  - image: 2019-08-07_qgis_tampere.png
    caption: Downtown Tampere
  - image: 2019-08-08_b3d_tampere_landscape.png
    caption: Downtown Tampere, landscape view
  - image: 2019-10-01_mdg_river_basins.png
    caption: Madagascar river basins
  - image: 2019-10-01_qgis_mdg_hrsl.png
    caption: Madagascar settlement map
  - image: 2019-10-08_qgis_antananarivo_shortest_route_1.png
    caption: Shortest route to Mahamasina
  - image: 2019-10-26_b3d_fianarantsoa_part_1.png
    caption: 3D map of Fianarantsoa
    
---

<div id="imggallery" class="justified-gallery">
{%- for entry in page.images -%}
  <a href="/gallery_content/{{ entry.image }}">
    <img alt="{{ entry.caption }}" src="/gallery_content/thumb/{{ entry.image }}">
  </a>
{%- endfor -%}
</div>
