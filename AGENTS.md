# Repository Agent Guide

## Scope

This repository is the source for the EmbeddedOS GitHub Pages site at
<https://embeddedos-org.github.io/>. It is a static site built from HTML, CSS,
and vanilla JavaScript; there is no application build step.

## Structure

- Root `*.html` files are the primary public pages.
- `docs/`, `stacks/`, `eApps/`, and `downloads/` contain additional site pages.
- `docs/wiki/` mirrors the six published repository Wiki pages in source control.
- `style.css` contains global styles.
- `js/site-chrome.js` is the shared source of truth for navigation and footer
  markup. Update it when changing site-wide community links.
- `tests/` contains Playwright and Python test suites.
- `.github/workflows/` contains CI and deployment automation.

## Working Safely

- Start changes from the protected `master` branch and work on a feature branch.
- Keep edits focused. Do not modify generated artifacts or unrelated content.
- Preserve the static-site structure and existing accessibility attributes.
- Do not add secrets, credentials, internal hostnames, or production data.
- Treat the checked-in files as authoritative. The GitHub Wiki is a published
  navigation layer, not the source of truth for code or policy.
- Pull requests must use a closing keyword for an issue in this repository,
  such as `Fixes #123`.

## Validation

Install dependencies with `npm install` when needed, then serve the repository
root with `npm run serve`. Run checks appropriate to the change:

```bash
npm run test:chromium
npm run test:links
npm run lint:html
```

For documentation and workflow changes, also validate YAML syntax, Markdown
links, and relative file targets. Review `git diff --check` before committing.
Document every command run and any check that could not be completed in the
pull request.

## Contributions

Follow [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the
pull request template. Report suspected vulnerabilities through the private
channel described in `SECURITY.md`, never through a public issue.
