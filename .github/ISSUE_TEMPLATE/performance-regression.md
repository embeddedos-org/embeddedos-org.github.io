---
name: Performance Regression
about: Automated report from CI/CD when performance degrades
title: "[CI] Performance regression — {{ date | date('YYYY-MM-DD') }}"
labels: ["bug", "ci-automated", "performance"]
assignees: []
---

## Performance Regression Detected

The nightly CI/CD audit found performance issues on the website.

### Details

**Workflow Run:** [View on GitHub]({{ env.RUN_URL }})
**Date:** {{ date | date('YYYY-MM-DD HH:mm') }} UTC

### Issues Found

```
{{ env.PERF_ISSUES }}
```

### Performance Budgets

| Metric | Budget |
|--------|--------|
| Page load | < 5s |
| FCP | < 3s |
| Single resource | < 1MB |
| No JS console errors | 0 |
