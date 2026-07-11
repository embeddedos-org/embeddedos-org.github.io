/* EmbeddedOS Site Chrome — single source of truth for navbar + footer.
   v1.1.0 — nav links wrapped in <li> for proper CSS nth-child alignment,
   improved hamburger with aria-expanded, mobile menu auto-close on link click. */
(function () {
  'use strict';

  var SITE_VERSION = 'v1.0.0';

  var NAV_LINKS = [
    { href: '/index.html',                              label: 'Home',                   key: 'home' },
    { href: '/getting-started.html',                    label: 'Get Started',            key: 'getting-started' },
    { href: '/docs/index.html',                         label: 'Docs',                   key: 'docs' },
    { href: 'https://embeddedos-org.github.io/eApps/', label: '\u{1F3EA} App Store',    key: 'eapps',        cls: 'nav-github' },
    { href: '/kids.html',                               label: 'Kids \u{1F3AE}',         key: 'kids' },
    { href: '/hardware-lab.html',                       label: 'Hardware Lab \u{1F50C}', key: 'hardware-lab' },
    { href: '/flow.html',                               label: 'Flow',                   key: 'flow' },
    { href: '/books.html',                              label: '\u{1F4DA} Books',         key: 'books' },
    { href: '/stacks/index.html',                       label: '\u{1F3ED} Stacks',       key: 'stacks' },
    { href: '/get-involved.html',                       label: '\u{1F91D} Get Involved', key: 'get-involved' },
    { href: '/index.html#health-devices',               label: '\u2764\uFE0F Health',    key: 'health' },
    { href: 'https://github.com/embeddedos-org',        label: '\u2605 GitHub',          key: 'github',       cls: 'nav-github' }
  ];

  function escAttr(s) {
    return String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  }

  function buildNavInner(activeKey) {
    var linksHtml = NAV_LINKS.map(function (l) {
      var cls = l.cls || '';
      if (l.key === activeKey) cls = (cls + ' active').trim();
      var clsAttr = cls ? ' class="' + escAttr(cls) + '"' : '';
      var extAttr = l.href.startsWith('http') ? ' target="_blank" rel="noopener"' : '';
      return '<li><a href="' + escAttr(l.href) + '"' + clsAttr + extAttr + '>' + l.label + '</a></li>';
    }).join('');

    return [
      '<div class="nav-inner">',
        '<a href="/index.html" class="logo">',
          '<span class="logo-icon">EoS</span>',
          ' EmbeddedOS ',
          '<span class="nav-version">', SITE_VERSION, '</span>',
        '</a>',
        '<button class="nav-toggle" type="button" aria-label="Toggle navigation menu" aria-expanded="false">',
          '<span class="hamburger-bar"></span>',
          '<span class="hamburger-bar"></span>',
          '<span class="hamburger-bar"></span>',
        '</button>',
        '<ul class="nav-links" role="list">', linksHtml,
          '<li class="nav-search-item"><button class="nav-search-btn" type="button" aria-label="Search (press /)" title="Search (/)">&#128269;</button></li>',
        '</ul>',
      '</div>'
    ].join('');
  }

  var FOOTER_INNER_HTML = [
    '<div class="footer-inner">',
      '<div class="footer-brand">',
        '<div class="footer-logo">',
          '<span class="logo-icon">EoS</span>',
          '<span class="footer-logo-text">EmbeddedOS</span>',
        '</div>',
        '<p>An open-source embedded operating system for the next generation of intelligent devices.</p>',
        '<div class="footer-badges">',
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
          '<li><a href="/docs/index.html">All Docs</a></li>',
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
          '<li><a href="/stacks/index.html">\u{1F3ED} Stacks</a></li>',
        '</ul>',
      '</div>',
      '<div>',
        '<h4>Health Devices</h4>',
        '<ul>',
          '<li><a href="/index.html#health-devices">\u2764\uFE0F Overview</a></li>',
          '<li><a href="https://github.com/embeddedos-org/HealthKey-Ulta" target="_blank" rel="noopener">HEALTH-KEY ULTRA</a></li>',
          '<li><a href="https://github.com/embeddedos-org/HEALTH-BAND-Neuro" target="_blank" rel="noopener">HEALTH-BAND Neuro</a></li>',
          '<li><a href="https://github.com/embeddedos-org/HealthKey-Ulta/tree/main/companion-app" target="_blank" rel="noopener">EoS Health App</a></li>',
          '<li><a href="https://github.com/embeddedos-org/HealthKey-Ulta/tree/main/patent" target="_blank" rel="noopener">Patent Docs</a></li>',
        '</ul>',
      '</div>',
      '<div>',
        '<h4>Community</h4>',
        '<ul>',
          '<li><a href="https://github.com/embeddedos-org" target="_blank" rel="noopener">GitHub Organization</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/issues" target="_blank" rel="noopener">Report Issues</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/discussions" target="_blank" rel="noopener">Discussions</a></li>',
          '<li><a href="https://github.com/embeddedos-org/eos/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Contributing</a></li>',
          '<li><a href="/get-involved.html">\u{1F91D} Get Involved</a></li>',
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
    if (/\/stacks(\/(index\.html|eai-edge\.html))?$/.test(path)) return 'stacks';
    if (/\/stacks\//.test(path)) return 'stacks';
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
      // Wire hamburger toggle with aria-expanded
      var toggle = document.querySelector('.nav-toggle');
      if (toggle) {
        toggle.addEventListener('click', function () {
          var links = document.querySelector('.nav-links');
          var expanded = toggle.getAttribute('aria-expanded') === 'true';
          if (links) links.classList.toggle('open');
          toggle.setAttribute('aria-expanded', String(!expanded));
        });
      }
      // Close mobile menu when a nav link is clicked
      document.querySelectorAll('.nav-links a').forEach(function (a) {
        a.addEventListener('click', function () {
          var links = document.querySelector('.nav-links');
          var t = document.querySelector('.nav-toggle');
          if (links) links.classList.remove('open');
          if (t) t.setAttribute('aria-expanded', 'false');
        });
      });
      // Wire search button
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
