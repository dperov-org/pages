---
layout: null
title: Галерея на PhotoSwipe v5
---

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ page.title }}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe.css">
  <style>
    .gallery {
      display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;
    }
    .gallery a img {
      width: 160px; height: auto;
      border: 1px solid #ccc; border-radius: 4px; background: #fafafa;
    }
  </style>
</head>
<body>
  <h1>{{ page.title }}</h1>

  <div class="gallery" id="gallery">
    {% assign images = site.static_files | where_exp:"file","file.path contains '/plot/'" and (file.extname == '.jpg' or file.extname == '.jpeg' or file.extname == '.png' or file.extname == '.gif')" %}
    {% for img in images %}
      <a href="{{ site.baseurl }}{{ img.path }}">
        <img src="{{ site.baseurl }}{{ img.path }}" alt="image">
      </a>    
    {% endfor %}
  </div>

  <!-- PhotoSwipe Core -->
  <script src="https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe-lightbox.esm.min.js" type="module"></script>
  <script type="module">
    // Получение размеров изображений на лету для корректной работы PhotoSwipe
    function loadImgSize(src) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve({w: img.naturalWidth, h: img.naturalHeight});
        img.onerror = reject;
        img.src = src;
      });
    }

    async function enhanceGallery() {
      const links = document.querySelectorAll('#gallery a');
      for (const a of links) {
        // Если data-pswp-width не установлен, детектим размер
        if (!a.dataset.pswpWidth || !a.dataset.pswpHeight) {
          const size = await loadImgSize(a.href);
          a.dataset.pswpWidth = size.w;
          a.dataset.pswpHeight = size.h;
        }
      }

      // Теперь инициализируем PhotoSwipe
      const lightbox = new PhotoSwipeLightbox({
        gallery: '#gallery',
        children: 'a',
        pswpModule: () => import('https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe.esm.min.js')
      });
      lightbox.init();
    }

    enhanceGallery();
  </script>
</body>
</html>