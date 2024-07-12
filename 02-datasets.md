---
layout: page
title: Datasets
permalink: /datasets/
files:
  - path: /datasets/mg_agencesboa_v1.zip
    title: BOA offices in Madagascar
    description: A list of all BOA (Bank of Africa) offices in Madagascar.
    size: 5
    size_unit: KB
    format: CSV
  - path: /datasets/mg_lyceespublics_v1.zip
    title: Public high schools in Madagascar
    description: Details of public high schools (lycées) across Madagascar.
    size: 5
    size_unit: KB
    format: CSV
  - path: /datasets/mg_populationfokontany_v1.zip
    title: 2009 Population by fokontany in Madagascar
    description: Population data by fokontany from the year 2009, in a zipped shapefile.
    size: 20
    size_unit: MB
    format: SHP
  - path: /datasets/mg_profilsrnmajeures_v1.zip
    title: Slope along major roads in Madagascar
    description: Slope data along major roads in Madagascar.
    size: 688
    size_unit: KB
    format: CSV
  - path: /datasets/mg_centrales_electriques_v1.zip
    title: Power plants in Madagascar
    description: Power plants in Madagascar, with details such as geographic location, operator and power.
    size: 6
    size_unit: KB
    format: CSV
  - path: /datasets/mg_lacs_v1.zip
    title: Lakes in Madagascar
    description: Lakes in Madagascar, with details such as geographic location, geographic shape and area.
    size: 124
    size_unit: KB
    format: CSV
---

Explore my collection of free datasets below. Click the download button to access the files.

<table class="datasetsTable">
  <thead>
    <tr>
      <th>Title</th>
      <th>Details</th>
      <th>Download</th>
    </tr>
  </thead>
  <tbody>
    {%- for file in page.files -%}
    <tr class="flink">
      <td>
        <strong>{{ file.title }}</strong><br/>
        <small>{{ file.description }}</small>
      </td>
      <td>
        <small>
          <strong>Format:</strong> {{ file.format }}<br/>
          <strong>Size:</strong> {{ file.size }} {{ file.size_unit }}
        </small>
      </td>
      <td width="10em">
        <a href="{{ file.path }}" class="pageButton" aria-label="Download {{ file.title }}">
          <i class="fas fa-download white-icon"></i>
          <span class="buttonText">Download</span>
        </a>
      </td>
    </tr>
    {%- endfor -%}
  </tbody>
</table>
