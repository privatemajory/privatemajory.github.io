---
layout: page
title: Portfolio
permalink: /gallery/
images:
  - image: 2023-07-12_b3d_itasy_hexagons.jpg
    caption: Lake Itasy
  - image: 2023-07-12_b3d_mayotte.jpg
    caption: Mayotte
  - image: 2023-07-12_b3d_st_louis.jpg
    caption: Saint-Louis Island (Senegal)
  - image: 2023-07-12_drainage_divide_map.jpg
    caption: Madagascar west/east drainage divide
  - image: 2023-07-12_qgis_5_largest_lakes.jpg
    caption: Madagascar's 5 largest lakes
  - image: 2023-07-12_qgis_buildings_in_antananarivo.jpg
    caption: Antananarivo buildings coloured by terrain slope
  - image: 2023-07-12_qgis_toamasina_land_cover.jpg
    caption: Land cover of Toamasina  
  - image: 2019-08-08_b3d_tampere_landscape.jpg
    caption: Downtown Tampere, landscape view
  - image: 2019-05-21_b3d_galapagos.jpg
    caption: Galapagos
  - image: 2019-10-01_mdg_river_basins.jpg
    caption: Madagascar river basins
  # - image: 2019-05-21_b3d_gorges_tsiribihina.jpg
  #   caption: Gorges du Tsiribihina
  # - image: 2019-05-21_b3d_tsiroanomandidy_part.jpg
  #   caption: Tsiroanomandidy
  - image: 2019-05-21_qgis_cape_verde.jpg
    caption: Cape Verde
  # - image: 2019-10-08_qgis_antananarivo_shortest_route_1.jpg
  #   caption: Shortest route to Mahamasina
  - image: 2023-07-18_qgis_antananarivo_shortest_route_2.jpg
    caption: Shortest route to Mahamasina (remake)
  - image: 2019-10-26_b3d_fianarantsoa_part_1.jpg
    caption: 3D map of Fianarantsoa
  - image: 2020-04-14_b3d_lalangina_relief.jpg
    caption: Map of Lalangina
  - image: 2022-07-18_qgis_mdg_nobody_lives_here.jpg
    caption: Madagascar nobody lives here
  # - image: 2019-05-21_qgis_galapagos_tanaka.jpg
  #   caption: Galapagos Tanaka contours
  - image: 2019-05-21_qgis_mdg_urban_road_slope.jpg
    caption: Madagascar urban road rlope
  - image: 2019-05-21_qgis_nosy-be.jpg
    caption: Nosy Be
  - image: 2019-06-29_b3d_nyc.jpg
    caption: Financial District of Manhattan 3D
  - image: 2019-07-05_qgis_united_kingdoms_of_madagascar.jpg
    caption: United Kingdoms of Madagascar
  - image: 2019-07-13_b3d_manhattan.jpg
    caption: Financial District of Manhattan
  - image: 2019-10-01_qgis_mdg_hrsl.jpg
    caption: Madagascar settlement map
  - image: 2019-05-21_inkscape_ihorombe_relief_map.jpg
    caption: Ihorombe
  - image: 2019-08-07_qgis_tampere.jpg
    caption: Downtown Tampere
---

<div id="imggallery" class="justified-gallery">
{%- for entry in page.images -%}
  <a href="/gallery_content/{{ entry.image }}">
    <img alt="{{ entry.caption }}" src="/gallery_content/thumb/{{ entry.image }}">
  </a>
{%- endfor -%}
</div>
