---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: page
---
<style>  
  .no-border-table, .no-border-table td, .no-border-table tr {
    border: none;
  }
</style>

<div class="overlay-content">
  <table class="no-border-table">
    <tr>
      <td style="width: 120px;">
        <img src="https://raw.githubusercontent.com/privatemajory/signature/master/img/profile.png" alt="Photo" style="width: 120px; height: 120px;">
      </td>
      <td>
        <p>
          I'm Dolly Andriatsiferana, a geographer from Madagascar with a deep love for maps. This page is a showcase of my cartographic creations and insights into the world of mapping. Enjoy your visit!
        </p>
          <div id="buttons_1" style="margin: auto; width: auto; text-align: left; display: block; margin-bottom: 10px">
            <a href="/gallery" class="pageButton"><span class="buttonText">Explore Maps</span></a>
            <a href="/blog" class="pageButton"><span class="buttonText">Mapping Insights</span></a>
          </div>
      </td>
    </tr>
  </table>
</div>

<div id="slider" style="margin: auto; margin-bottom: 20px">
  {% for file in site.static_files %}
    {% if file.path contains 'slider_content' and file.extname == '.jpg' or file.extname == '.jpeg' %}
      <img src="{{ file.path }}" alt="Slider Image">
    {% endif %}
  {% endfor %}
</div>
