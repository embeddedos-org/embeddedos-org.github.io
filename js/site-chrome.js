/* EmbeddedOS Site Chrome — single source of truth for navbar + footer.
   Replaces any existing .navbar / .footer on DOMContentLoaded. The baked-in
   HTML on each page is kept as a graceful fallback when JS is disabled or
   this script fails to load. CSS class names are intentionally identical to
   the legacy markup so the existing stylesheet and Playwright tests keep
   working without modification. */
(function () {
  'use strict';

  var SITE_VERSION = 'v0.1.0';

  var NAV_LINKS = [
    { href: '/index.html',                              label: 'Home',            key: 'home' },
    { href: '/getting-started.html',                    label: 'Get Started',     key: 'getting-started' },
    { href: '/docs/index.html',                         label: 'Docs',            key: 'docs' },
    { href: 'https://embeddedos-org.github.io/eApps/',  label: '\u{1F3EA} App Store', key: 'eapps',         cls: 'nav-github' },
    { href: '/kids.html',                               label: 'Kids \u{1F3AE}',  key: 'kids' },
    { href: '/hardware-lab.html',                       label: 'Hardware Lab \u{1F50C}', key: 'hardware-lab' },
    { href: '/flow.html',                               label: 'Flow',            key: 'flow' },
    { href: '/books.html',                              label: '\u{1F4DA} Books', key: 'books' },
    { href: '/get-involved.html',                       label: '\u{1F91D} Get Involved', key: 'get-involved' },
    { href: 'https://github.com/embeddedos-org',        label: '\u2605 GitHub',   key: 'github',          cls: 'nav-github' }
  ];

  function escAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  }

  function buildNavInner(activeKey) {
    var linksHtml = NAV_LINKS.map(function (l) {
      var cls = l.cls || '';
      if (l.key === activeKey) cls = (cls + ' active').trim();
      var clsAttr = cls ? ' class="' + escAttr(cls) + '"' : '';
      return '<a href="' + escAttr(l.href) + '"' + clsAttr + '>' + l.label + '</a>';
    }).join('');

    return [
      '<div class="nav-inner">',
        '<a href="/index.html" class="logo"><span class="logo-icon">EoS</span> EmbeddedOS <span class="nav-version">', SITE_VERSION, '</span></a>',
        '<button class="nav-toggle" type="button" aria-label="Menu">&#9776;</button>',
        '<div class="nav-links">', linksHtml,
          '<button class="nav-search-btn" type="button" aria-label="Search" title="Search (/)">&#128269;</button>',
        '</div>',
      '</div>'
    ].join('');
  }

  var FOOTER_INNER_HTML = [
    '<div class="footer-inner">',
      '<div class="footer-brand">',
        '<h3 style="margin-bottom:0.5rem">EmbeddedOS</h3>',
        '<p>An open-source embedded operating system for the next generation of intelligent devices.</p>',
        '<div style="display:flex;gap:0.5rem;flex-wrap:wrap">',
          '<span class="badge badge-blue">MIT</span>',
          '<span class="badge badge-green">Open Source</span>',
          '<span class="badge badge-purple">Community</span>',
        '</div>',
      '</div>',
      '<div>',
        '<h4>Documentation</h4>',
        '<ul>',
          '<li><a href="/getting-started.html">Getting Started</a></li>',
          '<li><a href="/docs/eos.html">EoS Kernel</a></li>',
          '<li><a href="/docs/eboot.html">eBoot</a></li>',
          '<li><a href="/docs/ebuild.html">ebuild</a></li>',
        '</ul>',
      '</div>',
      '<div>',
        '<h4>Components</h4>',
        '<ul>',
          '<li><a href="/docs/eipc.html">EIPC</a></li>',
          '<li><a href="/docs/eai.html">EAI</a></li>',
          '<li><a href="/docs/eni.html">ENI</a></li>',
          '<li><a href="/docs/eosuite.html">eApps</a></li>',
          '<li><a href="/docs/eosim.html">EoSim</a></li>',
          '<li><a href="/docs/eostudio.html">EoStudio</a></li>',
          '<li><a href="/docs/edb.html">eDB</a></li>',
          '<li><a href="/docs/ebrowser.html">eBrowser</a></li>',
          '<li><a href="/docs/eoffice.html">eOffice</a></li>',
        '</ul>',
      '</div>',
      '<div>',
        '<h4>Community</h4>',
        '<ul>',
          '<li><a href="https://github.com/embeddedos-org">GitHub Organization</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/issues">Report Issues</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/discussions">Discussions</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/blob/main/CONTRIBUTING.md">Contributing</a></li>',
        '</ul>',
      '</div>',
      '<div>',
        '<h4>Connect</h4>',
        '<ul class="social-list">',
          '<li><a class="social-link social-youtube" href="https://www.youtube.com/@EmbeddedOS_ORG" target="_blank" rel="noopener" aria-label="YouTube"><span class="social-icon">\u25B6</span> YouTube</a></li>',
          '<li><a class="social-link social-linkedin" href="https://www.linkedin.com/company/embedded-operating-systems-research-foundation" target="_blank" rel="noopener" aria-label="LinkedIn"><span class="social-icon">in</span> LinkedIn</a></li>',
          '<li><a class="social-link social-x" href="https://x.com/EmbeddedOS_ORG" target="_blank" rel="noopener" aria-label="X (Twitter)"><span class="social-icon">\u{1D54F}</span> X (Twitter)</a></li>',
          '<li><a class="social-link social-facebook" href="https://www.facebook.com/people/Embedded-Operating-Systems-Research-Foundation/61588978691494/" target="_blank" rel="noopener" aria-label="Facebook"><span class="social-icon">f</span> Facebook</a></li>',
        '</ul>',
      '</div>',
    '</div>',
    '<div class="footer-bottom">',
      '&copy; 2025\u20132026 EmbeddedOS Project &bull; Licensed under MIT &bull; Built with care for embedded developers',
    '</div>'
  ].join('');

  function detectActive() {
    var path = (window.location.pathname || '').replace(/\/+$/, '');
    if (path === '' || /\/index\.html$/.test(path) && !/\/(docs|eApps|downloads)\//.test(path)) {
      if (path === '' || path === '/index.html') return 'home';
    }
    if (/getting-started\.html$/.test(path)) return 'getting-started';
    if (/\/docs(\/index\.html)?$/.test(path)) return 'docs';
    if (/\/docs\//.test(path)) return 'docs';
    if (/\/eApps(\/index\.html)?$/.test(path)) return 'eapps';
    if (/kids\.html$/.test(path)) return 'kids';
    if (/hardware-lab\.html$/.test(path)) return 'hardware-lab';
    if (/flow\.html$/.test(path)) return 'flow';
    if (/books\.html$/.test(path)) return 'books';
    if (/get-involved\.html$/.test(path)) return 'get-involved';
    return null;
  }

  function inject() {
    try {
      var nav = document.querySelector('nav.navbar');
      if (nav) {
        nav.setAttribute('role', 'navigation');
        nav.setAttribute('aria-label', 'Main navigation');
        nav.innerHTML = buildNavInner(detectActive());
      }
      var footer = document.querySelector('footer.footer');
      if (footer) {
        footer.setAttribute('role', 'contentinfo');
        footer.innerHTML = FOOTER_INNER_HTML;
      }

      // Wire hamburger toggle (matches legacy inline-onclick behaviour:
      // toggling .open on the sibling .nav-links container).
      var toggle = document.querySelector('.nav-toggle');
      if (toggle) {
        toggle.addEventListener('click', function () {
          var links = document.querySelector('.nav-links');
          if (links) links.classList.toggle('open');
        });
      }

      // Wire search button (legacy used inline onclick="EosSearch.open()").
      var searchBtn = document.querySelector('.nav-search-btn');
      if (searchBtn) {
        searchBtn.addEventListener('click', function () {
          if (typeof EosSearch !== 'undefined' && typeof EosSearch.open === 'function') {
            EosSearch.open();
          }
        });
      }
    } catch (e) {
      /* fall back silently to baked-in HTML */
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else {
    inject();
  }
})();
