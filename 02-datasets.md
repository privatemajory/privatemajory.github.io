---
layout: page
title: Datasets
permalink: /datasets/
files:
  - path: /downloads/datasets/mg_agencesboa_v1.zip
    title: BOA Offices in Madagascar
    format: CSV
    size: 4
  - path: /downloads/datasets/mg_lyceespublics_v1.zip
    title: Public Lycées in Madagascar
    format: CSV
    size: 5
  - path: /downloads/datasets/mg_populationfokontany_v1.zip
    title: 2009 Population by Fokontany in Madagascar
    format: Shapefile
    size: 20264
---
<table>
{%- for file in page.files -%}
  <tr class="flink"><td>{{ file.title }}</td><td><u>Format</u>: {{file.format}}<br/><u>Size</u>: {{file.size}} kb</td><td width="10em"><a href="{{ file.path }}" class="pageButton" alt="{{ file.path }}"><span class="buttonText">Download</span></a></td></tr>
{%- endfor -%}
</table>