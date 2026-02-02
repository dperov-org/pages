---
layout: null
title: Галерея Plot
---

<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{{ page.title }}</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe.css">
  <style>
    body { font-family: Arial, sans-serif; }
    .gallery {
      display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;
    }
    .gallery-item {
      display: flex; flex-direction: column; align-items: center; width: 160px;
      word-break: break-all;
    }
    .gallery-item img {
      width: 160px; height: auto;
      border: 1px solid #ccc; border-radius: 4px; background: #fafafa;
      margin-bottom: 6px;
      cursor: pointer;
    }
    .file-name {
      font-size: 13px;
      word-break: break-all;
      text-align: center;
      color: #555;
    }
  </style>
</head>
<body>
  <h1>{{ page.title }}</h1>
  <div class="gallery" id="gallery">
    {% assign images = site.static_files | where_exp:"file","file.path contains '/plot/'" and 
      (file.extname == '.jpg' or file.extname == '.jpeg' or file.extname == '.png' or file.extname == '.gif')" %}
    {% for img in images %}
      <div class="gallery-item">
        <a href="{{ site.baseurl }}{{ img.path }}">
          <img
            src="{{ site.baseurl }}{{ img.path }}"
            alt="{{ img.name }}"
            data-pswp-src="{{ site.baseurl }}{{ img.path }}"
            data-pswp-filename="{{ img.name }}"
          >
        </a>
        <div class="file-name">{{ img.name }}</div>
      </div>
    {% endfor %}
  </div>

  <script type="module">
    import PhotoSwipeLightbox from 'https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe-lightbox.esm.min.js';

    function loadImgSize(src) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve({w: img.naturalWidth, h: img.naturalHeight});
        img.onerror = reject;
        img.src = src;
      });
    }

    async function enhanceGallery() {
      const anchors = document.querySelectorAll('#gallery a');
      // Получаем размеры
      for (const a of anchors) {
        const img = a.querySelector('img');
        if (img && (!img.dataset.pswpWidth || !img.dataset.pswpHeight)) {
          const {w, h} = await loadImgSize(img.src);
          img.dataset.pswpWidth = w;
          img.dataset.pswpHeight = h;
          a.dataset.pswpWidth = w;
          a.dataset.pswpHeight = h;
        }
      }
      // PhotoSwipeLightbox автоиспользует data-pswp-width/height

      const lightbox = new PhotoSwipeLightbox({
        gallery: '#gallery',
        children: 'a',
        pswpModule: () => import('https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe.esm.min.js'),
        showHideAnimationType: 'fade'
      });

      let thumbsBar = null;
      lightbox.on('afterInit', () => {
        const pswp = lightbox.pswp;
        if (thumbsBar) thumbsBar.remove();
        thumbsBar = document.createElement('div');
        thumbsBar.className = 'pswp-thumbs-bar';
        thumbsBar.style.cssText = 'display:flex;gap:6px;overflow-x:auto;padding:8px 0;justify-content:center;background:rgba(255,255,255,0.97);position:absolute;bottom:0;left:0;right:0;z-index:1400;';

        const items = [];
        document.querySelectorAll('#gallery a img').forEach((imgEl) => {
          items.push({
            msrc: imgEl.src,
            filename: imgEl.alt
          });
        });

        items.forEach((item, idx) => {
          const thumbImg = document.createElement('img');
          thumbImg.src = item.msrc;
          thumbImg.alt = item.filename;
          thumbImg.style.width = '60px';
          thumbImg.style.height = 'auto';
          thumbImg.style.cursor = 'pointer';
          thumbImg.style.border = '2px solid #ccc';
          thumbImg.style.borderRadius = '3px';
          thumbImg.style.background = '#eee';
          thumbImg.style.marginRight = '3px';
          if (pswp.currIndex === idx)
            thumbImg.style.borderColor = '#33f';

          thumbImg.onclick = () => pswp.goTo(idx);

          thumbsBar.appendChild(thumbImg);
        });

        pswp.element.appendChild(thumbsBar);

        pswp.on('change', () => {
          thumbsBar.childNodes.forEach((el, i) => el.style.borderColor = i===pswp.currIndex ? '#33f' : '#ccc');
        });

        // Удаляем панели миниатюр при закрытии
        pswp.on('close', () => {
          if (thumbsBar) { thumbsBar.remove(); thumbsBar = null; }
        });
      });

      lightbox.init();
    }

    enhanceGallery();
  </script>
</body>
</html>