# Merge proposal: embeddedos-org.github.io → www.embeddedos.org

**Status:** PROPOSAL — awaiting Aswin's approval. No archive, delete, or
redirect action has been taken. Refs #158.

## Inventory (26 HTML pages, 2026-10-01)

| Old-site page | www.embeddedos.org coverage | Verdict |
|---|---|---|
| `index.html` | `/` (homepage) | Covered — redirect |
| `404.html` | 404 route | Covered — redirect |
| `getting-started.html` | `/getting-started` (srpatcha's #62 accuracy work) | Covered — redirect |
| `get-involved.html` | `/get-involved`, `/community` | Covered — redirect |
| `downloads/index.html` | `/downloads` | Covered — redirect |
| `eApps/index.html` | `/eapps` (EApps.tsx) | Covered — redirect |
| `docs/index.html` | `/docs` | Covered — redirect |
| `docs/eos.html` … `docs/eserviceapps.html` (13 product docs) | `/eboot`, `/ebuild`, `/eai`, `/edb`, `/eipc`, `/eni`, `/eoffice`, `/eosim`, `/eostudio`, `/ebrowser`, `/docs` | Covered — redirect each |
| `books.html` (727 lines, Press book library) | `/books` (Books.tsx) | Covered — verify 1:1, then redirect |
| `stacks/eai-edge.html` | `/eai-edge` (EAIEdge) | Covered — redirect |
| `stacks/index.html` (253 lines, stack catalog) | No `/stacks` route found | **Unique — port content** |
| `kids.html` (119 lines, Kids Guide) | No kids route found | **Unique — port content** |
| `hardware-lab.html` (323 lines, Hardware Lab Guide) | No hardware-lab route found | **Unique — port content** |
| `flow.html` (331 lines, Platform Flow) | `/architecture` partially; flow diagram unique | **Unique — port diagram/content** |
| `docs/embeddedos-ecosystem-guide.md` | `/docs` ecosystem section | Verify, then redirect |

## What moves (on approval)

1. **Port 4 unique content sets** to www.embeddedos.org as new routes:
   - `/stacks` (from `stacks/index.html`)
   - `/kids` (from `kids.html`)
   - `/hardware-lab` (from `hardware-lab.html`)
   - `/platform-flow` (from `flow.html`; merge with `/architecture` if overlap)
2. **Verify** `books.html` → `/books` and `docs/embeddedos-ecosystem-guide.md`
   → `/docs` are 1:1 (no dropped sections).
3. **Archive** this repo (GitHub archive, read-only) — do NOT delete.
4. **Redirect**: GitHub Pages → www.embeddedos.org via `<meta refresh>` on
   `index.html` + repo-level redirect notice, or DNS-level if available.

## Undo path

- Archiving is reversible (unarchive in repo settings).
- This repo's git history is the full backup; the port commits on
  www.embeddedos.org are revertable independently.
- No content is deleted at any step — archive, not delete.

## Do NOT

- Do not archive before the 4 unique content sets are live on www.embeddedos.org.
- Do not touch srpatcha's PR #159 (salvage work) — coordinate, don't duplicate.
- Do not break existing inbound links: keep the redirect page live for 6 months.
