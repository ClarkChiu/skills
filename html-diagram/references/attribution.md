# Attribution

## What this skill is

`html-diagram` is a **vendor & customize** skill: the SKILL.md (workflow,
hard requirements, boundaries) is written from scratch for this project, scoped
narrowly to **self-contained HTML/SVG diagrams** (architecture / stack /
sequence / flowchart). The bundled reference HTML files are vendored upstream
content, not original.

## Vendored reference files

`references/architecture-example.html` and everything under
`references/html-effectiveness/` are copied **verbatim** from upstream.

- **Immediate source:** `plannotator/effective-html`
  (https://github.com/plannotator/effective-html), MIT-licensed bundle. The
  `architecture-example.html` finished example originates here (skills/html-diagram).
- **Original gallery:** the `html-effectiveness/*.html` examples are from
  **ThariqS/html-effectiveness** (https://github.com/ThariqS/html-effectiveness,
  also at https://thariqs.github.io/html-effectiveness/), **Apache License 2.0**
  — author Thariq Shihipar. The Apache-2.0 `LICENSE` file is vendored alongside
  them; keep it there.

### Curation (not the full gallery)

Only the diagram-relevant subset of the 20-file gallery is vendored, to keep the
skill narrow:

- `05-design-system.html`, `07-prototype-animation.html`,
  `08-prototype-interaction.html`, `10-svg-illustrations.html`,
  `13-flowchart-diagram.html` (+ `LICENSE`, `README.md`).

The omitted files (code review, slide deck, status/incident report, PR write-up,
editor UIs, explainers, etc.) duplicate the built-in `web-artifacts-builder` /
`slide-deck` territory and are intentionally left out. If the scope ever widens
to general technical HTML deliverables, pull the rest from the same commit.

## Security note

All vendored HTML is self-contained: verified (2026-06-14) to have **no external
`<script src>`, no CDN, no fetch/XHR/WebSocket/beacon execution, no network
calls** — the only `http(s)` reference is a plain link to the upstream project
homepage. Inline scripts are dark-mode toggles and diagram interactivity only.
Re-scan after any upstream re-sync.

## Licenses

- Vendored gallery: **Apache-2.0** (ThariqS/html-effectiveness). LICENSE bundled.
- Bundle path: **MIT** (plannotator/effective-html).
- This skill's own SKILL.md / evals: MIT (project default).

Both upstream licenses are permissive and allow this redistribution with
attribution; this file is that attribution.

`sources.lock` pins both upstreams; `skill-evolve` uses it to detect upstream
changes worth re-syncing.
