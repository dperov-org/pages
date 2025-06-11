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
    {% assign images = site.static_files 
        | where_exp:"file","file.path contains '/plot/' and file.path matches '\\.(jpg|jpeg|png|gif)$'" %}
    {% for img in images %}
      <div class="gallery-item">
        <a href="{{ site.baseurl }}{{ img.path | remove_first: '/' }}">
          <img
            src="{{ site.baseurl }}{{ img.path | remove_first: '/' }}"
            alt="{{ img.name }}"
            data-pswp-src="{{ site.baseurl }}{{ img.path | remove_first: '/' }}"
            data-pswp-filename="{{ img.name }}"
          >
        </a>
        <div class="file-name">{{ img.name }}</div>
      </div>
    {% endfor %}
  </div>

  <!-- PhotoSwipe core -->
  <script src="https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe-lightbox.esm.min.js" type="module"></script>
  <script type="module">
    function loadImgSize(src) {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve({w: img.naturalWidth, h: img.naturalHeight});
        img.onerror = reject;
        img.src = src;
      });
    }

    async function enhanceGallery() {
      const thumbs = document.querySelectorAll('#gallery a img');
      for (const img of thumbs) {
        if (!img.dataset.pswpWidth || !img.dataset.pswpHeight) {
          const {w, h} = await loadImgSize(img.src);
          img.dataset.pswpWidth = w;
          img.dataset.pswpHeight = h;
        }
      }

      // А теперь формируем PhotoSwipe-объекты
      const items = Array.from(thumbs).map(img => ({
        src: img.dataset.pswpSrc,
        msrc: img.src,
        width: Number(img.dataset.pswpWidth),
        height: Number(img.dataset.pswpHeight),
        alt: img.alt,
        filename: img.dataset.pswpFilename
      }));

      // Инициализация PhotoSwipe с миниатюрами (thumbnails)
      const lightbox = new PhotoSwipeLightbox({
        gallery: '#gallery',
        children: 'a',
        pswpModule: () => import('https://cdn.jsdelivr.net/npm/photoswipe@5/dist/photoswipe.esm.min.js'),
        showHideAnimationType: 'fade'
      });

      lightbox.on('openingAnimationEnd', () => {
        // Рендерим панель миниатюр под увеличенным изображением
        const pswp = lightbox.pswp;
        let thumbsBar = pswp.element.querySelector('.pswp-thumbs-bar');
        if (thumbsBar) return;

        thumbsBar = document.createElement('div');
        thumbsBar.className = 'pswp-thumbs-bar';
        thumbsBar.style.cssText = 'display:flex;gap:6px;overflow-x:auto;padding:8px 0;justify-content:center; background:rgba(255,255,255,0.97); position:absolute; bottom:0; left: 0; right:0; z-index: 1400;';

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

          pswp.on('change', () => {
            // Подсвечивать активный thumbnail
            thumbsBar.childNodes.forEach((el, i) => el.style.borderColor = i===pswp.currIndex ? '#33f' : '#ccc');
          });
          thumbsBar.appendChild(thumbImg);
        });
        pswp.element.appendChild(thumbsBar);
      });

      lightbox.init();
    }

    enhanceGallery();
  </script>
</body>
</html>