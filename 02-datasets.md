---
layout: page
title: Datasets
permalink: /datasets/
files:
  - path: /datasets/mg_agencesboa_v1.zip
    title: BOA offices in Madagascar
    description: A list of all BOA offices in Madagascar.
  - path: /datasets/mg_lyceespublics_v1.zip
    title: Public high schools in Madagascar
    description: Details of public high schools (lycées) across Madagascar.
  - path: /datasets/mg_populationfokontany_v1.zip
    title: 2009 Population by fokontany in Madagascar
    description: Population data by fokontany from the year 2009, in a zipped shapefile.
  - path: /datasets/mg_profilsrnmajeures_v1.zip
    title: Slope along major roads in Madagascar
    description: Slope data along major roads in Madagascar.
---

## Available Datasets

Explore my collection of free datasets below. Click the download button to access the files.

<table>
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
        <strong>Format:</strong> {{ file.format }}<br/>
        <strong>Size:</strong> {{ file.size }} {{ file.size_unit }}
      </td>
      <td width="10em">
        <a href="{{ file.path }}" class="pageButton" aria-label="Download {{ file.title }}">
          <span class="buttonText">Download</span>
        </a>
      </td>
    </tr>
    {%- endfor -%}
  </tbody>
</table>
