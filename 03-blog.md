---
layout: page
title: Posts
permalink: /blog/
kicker: Blog
summary: "Notes on GIS workflows, OpenStreetMap practice and the small decisions behind a map."
description: "Notes on GIS workflows, OpenStreetMap mapping and terrain analysis, mostly from working with data in Madagascar."
---

<div class="blog">
  {%- if site.posts.size > 0 -%}
    {%- assign latest = site.posts.first -%}
    {%- assign latest_words = latest.content | strip_html | number_of_words -%}
    {%- assign latest_reading = latest_words | divided_by: 200 | at_least: 1 -%}
    <a class="post-feature" href="{{ latest.url | relative_url }}">
      {%- assign latest_thumb = latest.thumb | default: latest.image -%}
      {%- if latest_thumb -%}
        <span class="post-feature__thumb">
          <img src="{{ latest_thumb | relative_url }}"
               srcset="{{ latest_thumb | replace: '-320.webp', '-160.webp' | relative_url }} 160w, {{ latest_thumb | relative_url }} 320w"
               sizes="(min-width: 900px) 7.5rem, 12vw"
               alt=""
               width="320"
               height="320"
               loading="eager"
               decoding="async">
        </span>
      {%- endif -%}
      <div class="post-feature__body">
        <span class="post-meta">
          <span class="chip chip--accent">Latest</span>
          <time datetime="{{ latest.date | date_to_xmlschema }}">{{ latest.date | date: "%b %-d, %Y" }}</time>
          <span class="sep"></span>
          <span>{{ latest_reading }} min read</span>
        </span>
        <h2 class="post-feature__title">{{ latest.title | escape }}</h2>
        {%- if latest.description -%}
          <span class="post-feature__excerpt">{{ latest.description }}</span>
        {%- endif -%}
        <span class="link-arrow">
          Read the post
          {% include icon.html name="arrow-right" class="icon" %}
        </span>
      </div>
    </a>

    <ul class="post-list">
      {%- for post in site.posts offset: 1 -%}
        {%- assign words = post.content | strip_html | number_of_words -%}
        {%- assign reading = words | divided_by: 200 | at_least: 1 -%}
        {%- assign thumb = post.thumb | default: post.image -%}
        <li>
          <a class="post-item" href="{{ post.url | relative_url }}">
            {%- if thumb -%}
              <span class="post-item__thumb">
                <img src="{{ thumb | relative_url }}"
                     srcset="{{ thumb | replace: '-320.webp', '-160.webp' | relative_url }} 160w, {{ thumb | relative_url }} 320w"
                     sizes="4rem"
                     alt=""
                     width="320"
                     height="320"
                     loading="lazy"
                     decoding="async">
              </span>
            {%- endif -%}
            <div class="post-item__body">
              <span class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%b %-d, %Y" }}</time>
                <span class="sep"></span>
                <span>{{ reading }} min read</span>
              </span>
              <h2 class="post-item__title">{{ post.title | escape }}</h2>
              {%- if post.description -%}
                <span class="post-item__excerpt">{{ post.description }}</span>
              {%- endif -%}
            </div>
            {% include icon.html name="arrow-up-right" class="icon" %}
          </a>
        </li>
      {%- endfor -%}
    </ul>

    <p class="collection-foot">
      <a class="link-arrow" href="{{ '/feed.xml' | relative_url }}">
        {% include icon.html name="rss" class="icon" %}
        Subscribe via RSS
      </a>
    </p>
  {%- else -%}
    <p class="lede">No posts yet.</p>
  {%- endif -%}
</div>
