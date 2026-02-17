---
layout: default
---

<div class="hero-section">
  <div class="hero-slider" id="hero-slider">
    {% for file in site.static_files %}
      {% if file.path contains 'slider_content' and file.extname == '.jpg' or file.extname == '.jpeg' %}
        <img src="{{ file.path }}" alt="Map Gallery Background">
      {% endif %}
    {% endfor %}
  </div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-inner">
      <img src="https://raw.githubusercontent.com/privatemajory/signature/master/img/profile.png" alt="Profile" class="profile-image">
      <div class="hero-text">
        <h1>Dolly Andriatsiferana</h1>
        <p>Geographer specializing in GIS, web mapping, and data visualization with open-source geospatial technologies.</p>
      </div>
      <div class="button-container">
        <a href="/gallery/" class="pageButton">
          <i class="fas fa-images"></i>
          <span class="buttonText">Maps</span>
        </a>
        <a href="/projects/" class="pageButton">
          <i class="fas fa-code"></i>
          <span class="buttonText">Projects</span>
        </a>
        <a href="/blog/" class="pageButton">
          <i class="fas fa-blog"></i>
          <span class="buttonText">Blog</span>
        </a>
      </div>
    </div>
  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    var slider = new IdealImageSlider.Slider({
      selector: '#hero-slider',
      height: 'auto',
      interval: 5000,
      transitionDuration: 2500,
      effect: 'fade',
      overflow: 'hidden'
    });

    slider.start();
  });
</script>