---
layout: default
---

<style>  
  .hero-section {
    position: relative;
    height: 380px;
    overflow: hidden;
    border-radius: 16px;
    margin-bottom: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }

  .hero-slider {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
  }

  .hero-slider img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .hero-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(180deg, 
      rgba(224, 224, 224, 0.85) 0%, 
      rgba(109, 128, 127, 0.75) 50%,
      rgba(24, 68, 61, 0.65) 100%);
    z-index: 2;
  }

  .hero-content {
    position: relative;
    z-index: 3;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    padding: 20px 40px;
  }

  .hero-inner {
    max-width: 800px;
  }

  .profile-image {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s ease;
    margin: 0 auto 10px;
  }

  .profile-image:hover {
    transform: scale(1.05);
  }

  .hero-text h1 {
    font-size: 1.5em;
    margin-bottom: 10px;
    font-weight: 700;
    line-height: 1.2;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .hero-text p {
    font-size: 1em;
    line-height: 1.6;
    margin-bottom: 10px;
    opacity: 0.95;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }

  .button-container {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
  }

  .pageButton {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
  }

  .pageButton:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }

  @media (max-width: 768px) {
    .hero-section {
      height: 400px;
    }
    
    .hero-content {
      padding: 20px;
    }
    
    .hero-text h1 {
      font-size: 1.5em;
    }
    
    .hero-text p {
      font-size: 1em;
    }
    
    .profile-image {
      width: 100px;
      height: 100px;
    }
  }
</style>

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
      <img src="https://raw.githubusercontent.com/privatemajory/signature/master/img/profile.png" 
           alt="Dolly Andriatsiferana" 
           class="profile-image">
      <div class="hero-text">
        <h1>Dolly Andriatsiferana</h1>
        <p>
          Geographer from Madagascar with a deep love for maps. This is my showcase of cartographic creations and insights into the world of mapping. Welcome to my digital atlas!
        </p>
        <div class="button-container">
          <a href="/gallery" class="pageButton">
            <i class="fas fa-map"></i>
            <span class="buttonText">Maps</span>
          </a>
          <a href="/blog" class="pageButton">
            <i class="fas fa-lightbulb"></i>
            <span class="buttonText">Insights</span>
          </a>
          <a href="/datasets" class="pageButton">
            <i class="fas fa-database"></i>
            <span class="buttonText">Datasets</span>
          </a>
          <a href="/media" class="pageButton">
            <i class="fas fa-music"></i>
            <span class="buttonText">Music</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</div>