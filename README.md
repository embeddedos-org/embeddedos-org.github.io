# EmbeddedOS Website (GitHub Pages)

[![CI](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/ci.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/ci.yml)
[![CodeQL](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/codeql.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/codeql.yml)
[![Scorecard](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/scorecard.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/scorecard.yml)
[![Deploy](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/embeddedos-org/embeddedos-org.github.io/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

The **EmbeddedOS developer portal** — a static site served via GitHub Pages.
This is the public entry point to the EmbeddedOS (EoS) ecosystem: static HTML,
CSS, and vanilla JavaScript, no build step required. Package name:
`embeddedos-website`.

## Pages

| File | Page |
|---|---|
| `index.html` | Home / landing |
| `getting-started.html` | Getting started guide |
| `get-involved.html` | Contributing / community |
| `hardware-lab.html` | Hardware lab |
| `books.html` | Books / long-form docs index |
| `flow.html` | Ecosystem flow / overview |
| `kids.html` | Kids / education |
| `404.html` | Not-found page |

Supporting content:

```
js/          animations.js, ebot-chat.js, search.js, site-chrome.js
stacks/      Technology stack pages (eai-edge.html, index.html)
eApps/       eApps index + icons
downloads/   Downloads index
docs/        Component docs (ebrowser, ebuild, eai, eos, ...) + book/
style.css    Global styles
sitemap.xml, robots.txt, _headers, favicon.svg, og-image.png
```

## Develop

Serve the site locally (static file server on port 8080):

```bash
npm run serve      # npx http-server . -p 8080 -s
```

Then open http://localhost:8080.

## Test

Tests use [Playwright](https://playwright.dev). The config
(`playwright.config.js`) runs specs from `tests/` across chromium, firefox,
webkit, and a mobile-chrome viewport against `http://localhost:8080` (override
with `BASE_URL`). Start the server (`npm run serve`) in another terminal first.

```bash
npm test               # all Playwright specs
npm run test:chromium  # chromium only
npm run test:links     # link checks
npm run test:seo       # SEO checks
npm run test:perf      # performance checks
npm run test:a11y      # accessibility checks
npm run test:responsive

npm run check:links    # linkinator crawl of the running site
npm run lint:html      # html-validate
npm run lighthouse     # Lighthouse CI collect
npm run audit          # test + check:links
```

## Deploy

The site is deployed to GitHub Pages via the `deploy.yml` workflow. Content is
served as-is from the repository root.

## License

MIT — see [LICENSE](LICENSE).
