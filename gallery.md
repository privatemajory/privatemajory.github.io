---
layout: page
title: Gallery
permalink: /gallery/
images:
  - image: 2019-05-21_b3d_andavamamba.png
  - image: 2019-05-21_b3d_galapagos.png
  - image: 2019-05-21_b3d_gorges_tsiribihina.png
  - image: 2019-05-21_b3d_tsiroanomandidy_part.png
  - image: 2019-05-21_handdrawn_bishes.png
  - image: 2019-05-21_handdrawn_xenobyle.png
  - image: 2019-05-21_inkscape_ihorombe_relief_map.png
  - image: 2019-05-21_inkscape_mdg_relief_map.png
  - image: 2019-05-21_qgis_cape_verde.png
  - image: 2019-05-21_qgis_galapagos_tanaka.png
  - image: 2019-05-21_qgis_madagascar_urban_population.png
  - image: 2019-05-21_qgis_mdg_urban_road_slope.png
  - image: 2019-05-21_qgis_nosy-be.png
---
<div id="imggallery" >
{%- for entry in page.images -%}
  <a href="/Images/{{ entry.image }}">
    <img src="/Images/thumb/{{ entry.image }}">
  </a>   
{%- endfor -%}
</div>