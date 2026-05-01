---
name: Broken Link Report
about: Automated report from CI/CD when broken links are detected
title: "[CI] Broken links detected — {{ date | date('YYYY-MM-DD') }}"
labels: ["bug", "ci-automated", "links"]
assignees: []
---

## Broken Links Detected

The nightly CI/CD audit found broken links on the website.

### Details

**Workflow Run:** [View on GitHub]({{ env.RUN_URL }})
**Date:** {{ date | date('YYYY-MM-DD HH:mm') }} UTC

### Broken Links

```
{{ env.BROKEN_LINKS }}
```

### How to Fix

1. Check if the target page/URL still exists
2. Update or remove the broken link in the source HTML file
3. Push the fix — the deploy workflow will re-test automatically

### Source Files to Check

- `index.html`
- `getting-started.html`
- `docs/*.html`
- `books.html`
- `flow.html`
- `hardware-lab.html`
- `kids.html`
- `404.html`
