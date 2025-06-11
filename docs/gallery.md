---
layout: null
title: Галерея
---

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ page.title }}</title>
  <!-- lightGallery v1 -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lightgallery@1.10.0/dist/css/lightgallery.min.css">
  <style>
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
    {% assign images = site.static_files | where_exp:"file","file.path contains '/plot/'" and (file.extname == '.jpg' or file.extname == '.jpeg' or file.extname == '.png' or file.extname == '.gif')" %}
    {% for img in images %}
      <a href="{{ img.path }}">
        <img src="{{ img.path }}" alt="image">
      </a>
    {% endfor %}
  </div>
  <!-- lightGallery v1 -->
  <script src="https://cdn.jsdelivr.net/npm/lightgallery@1.10.0/dist/js/lightgallery.min.js"></script>
  <script>
    lightGallery(document.getElementById('lightgallery'), {
      selector: 'a'
    });
  </script>
</body>
</html>
