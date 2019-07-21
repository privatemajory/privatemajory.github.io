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
  # - image: 2019-05-21_inkscape_mdg_relief_map.png
  #   caption: Madagascar Relief Map
  - image: 2019-05-21_qgis_cape_verde.png
    caption: Cape Verde
  - image: 2019-05-21_qgis_galapagos_tanaka.png
    caption: Galapagos Tanaka Contours
  - image: 2019-05-21_qgis_mdg_urban_road_slope.png
    caption: Madagascar Urban Road Slope
  - image: 2019-05-21_qgis_nosy-be.png
    caption: Nosy Be
  # - image: 2019-06-29_b3d_nyc.png
  #   caption: New York City
  - image: 2019-07-05_qgis_united_kingdoms_of_madagascar.png
    caption: United Kingdoms of Madagascar
  - image: 2019-07-13_b3d_manhattan.png
    caption: Financial District of Manhattan
---
<div id="imggallery" class="justified-gallery">
{%- for entry in page.images -%}
  <a href="/Images/{{ entry.image }}">
    <img alt="{{ entry.caption }}" src="/Images/thumb/{{ entry.image }}">
  </a>
{%- endfor -%}
</div>