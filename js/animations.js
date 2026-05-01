/* EmbeddedOS — Scroll Reveal & UI Enhancements */
(function () {
  'use strict';

  /* ── Scroll Reveal (IntersectionObserver) ── */
  function initScrollReveal() {
    var els = document.querySelectorAll(
      '.product-card, .hw-item, .arch-diagram, ' +
      '[class*="section"] > h2, [class*="section"] > p.section-subtitle, ' +
      '.hero-stats .stat, .quick-link'
    );
    if (!els.length || !('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('eos-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    els.forEach(function (el) {
      el.classList.add('eos-reveal');
      observer.observe(el);
    });
  }

  /* ── Scroll-to-Top Button ── */
  function initScrollTop() {
    var existing = document.querySelector('.scroll-top-btn');
    var btn;
    if (existing) {
      btn = existing;
    } else {
      btn = document.createElement('button');
      btn.className = 'scroll-top-btn';
      btn.setAttribute('aria-label', 'Scroll to top');
      btn.innerHTML = '&#8593;';
      btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      document.body.appendChild(btn);
    }
    window.addEventListener('scroll', function () {
      btn.style.display = window.scrollY > 400 ? 'flex' : 'none';
    }, { passive: true });
  }

  /* ── Active Nav Highlight ── */
  function initActiveNav() {
    var path = window.location.pathname.replace(/\/$/, '/index.html');
    var links = document.querySelectorAll('.nav-links a[href]');
    links.forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || href.startsWith('http') || href.startsWith('#')) return;
      if (path.endsWith(href) || path.endsWith('/' + href)) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
      }
    });
  }

  /* ── Stagger animation delays for grid items ── */
  function initStagger() {
    document.querySelectorAll('.product-grid, .hw-grid').forEach(function (grid) {
      var items = grid.children;
      for (var i = 0; i < items.length; i++) {
        items[i].style.transitionDelay = (i * 0.05) + 's';
      }
    });
  }

  /* ── Initialize everything on DOM ready ── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    initScrollReveal();
    initScrollTop();
    initActiveNav();
    initStagger();
  }
})();
