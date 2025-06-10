---
layout: null
title: Галерея
---

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ page.title }}</title>
  <!-- lightGallery CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lightgallery@2.7.2/css/lightgallery-bundle.min.css">
  <style>
    /* Простейшее оформление */
    .gallery {
      display: flex; flex-wrap: wrap; gap: 10px;
      margin: 20px 0;
    }
    .gallery a img {
      width: 160px;
      height: auto;
      border: 1px solid #ccc;
      background: #fafafa;
      display: block;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <h1>{{ page.title }}</h1>

  <div id="lightgallery" class="gallery">
    {% assign images = site.static_files | where_exp:"file","file.path contains '/plot/'" %}
    {% for img in images %}
      <a href="{{ img.path }}">
        <img src="{{ img.path }}" alt="image">
      </a>
    {% endfor %}
  </div>

  <!-- lightGallery JS -->
  <script src="https://cdn.jsdelivr.net/npm/lightgallery@2.7.2/lightgallery.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lightgallery@2.7.2/plugins/thumbnail/lg-thumbnail.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lightgallery@2.7.2/plugins/zoom/lg-zoom.min.js"></script>
  <script>
    lightGallery(document.getElementById('lightgallery'), {
      selector: 'a',
      plugins: [lgThumbnail, lgZoom],
      thumbnail: true
    });
  </script>
</body>
</html>