---
name: SEO Issue Report
about: Automated report from CI/CD when SEO problems are detected
title: "[CI] SEO issues detected — {{ date | date('YYYY-MM-DD') }}"
labels: ["enhancement", "ci-automated", "seo"]
assignees: []
---

## SEO Issues Detected

The nightly CI/CD audit found SEO problems on the website.

### Details

**Workflow Run:** [View on GitHub]({{ env.RUN_URL }})
**Date:** {{ date | date('YYYY-MM-DD HH:mm') }} UTC

### Issues Found

```
{{ env.SEO_ISSUES }}
```

### SEO Checklist

- [ ] Every page has `<title>` containing "EmbeddedOS"
- [ ] Every page has `<meta name="description">` (50-160 chars)
- [ ] Every page has `<link rel="canonical">`
- [ ] Every page has OG tags (og:title, og:description, og:image)
- [ ] Every page has exactly one `<h1>`
- [ ] JSON-LD structured data is valid
- [ ] `robots.txt` and `sitemap.xml` are accessible
