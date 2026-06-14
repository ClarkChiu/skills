---
name: html-diagram
description: >-
  Build a single self-contained HTML file whose job is one high-quality SVG
  diagram that makes an architecture, system, or flow click fast — full-screen,
  light on prose, dark-mode-aware, zero dependencies. Covers architecture /
  stack diagrams, sequence & request-flow diagrams, and flowcharts; nodes can be
  clickable and sequences can animate. USE THIS SKILL when the user wants to
  diagram or visualize a system / architecture / data flow / protocol exchange /
  pipeline as a shareable HTML or SVG artifact, or says 「畫架構圖」「系統圖」
  「時序圖」「流程圖」「把這個架構畫出來」「diagram this」「draw the architecture」
  「visualize the stack / the request flow」. Do NOT use for a 16:9 presentation
  deck (that's slide-deck), for fixed-ratio social images (social-card), for a
  general HTML report/explainer/prototype (use the built-in web-artifacts-builder),
  or for building an actual web-app UI (frontend-design).
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# html-diagram — self-contained HTML architecture diagrams

The deliverable is **one `.html` file, no build step, no dependencies**, whose
whole purpose is a single high-quality SVG diagram that makes a system click
fast. Not a report with a picture in it — the diagram *is* the page.

The value of this skill is the bundled reference gallery (real, finished
diagrams to study and match the quality of) plus the discipline below. The
rendering is your own hand-written SVG + CSS.

## When this is the right skill

Use it for **architecture / stack diagrams, sequence & request-flow diagrams,
and flowcharts** delivered as a shareable HTML/SVG file. If the user wants prose
with a diagram inside, that's a general artifact (built-in
`web-artifacts-builder`), not this. See the boundary table at the end.

## Workflow

1. **Understand the system first.** Before drawing, get the boxes and the edges
   straight: what the components are, who calls whom, where the trust / auth
   boundaries sit, what the request path is. A wrong diagram drawn beautifully is
   still wrong. Ask the user if the topology is ambiguous — don't invent edges.
2. **Study the reference gallery.** Read `references/architecture-example.html`
   first — it's a finished, done-well example (full-screen SVG stage, clickable
   nodes, flow chips that light up and animate a request path). Then pull
   technique from `references/html-effectiveness/` as needed:
   - `13-flowchart-diagram.html` — flowchart / decision-flow layout.
   - `10-svg-illustrations.html` — clean hand-authored SVG technique.
   - `05-design-system.html` — the styling bar: tokens, type, spacing, restraint.
   - `07-prototype-animation.html` — animating a sequence of states.
   - `08-prototype-interaction.html` — clickable nodes, hover/focus states.
3. **Draw the SVG by hand, and iterate on it more than anything else.** Spend
   the time here. Lay out nodes on a grid, route edges so they don't cross
   needlessly, label edges with the protocol / call, group by boundary. Prefer
   `<text>`, `<rect>`, `<path>` you control over an auto-layout library.
4. **Make it interactive only when it earns its keep.** Clickable nodes that
   reveal detail, and flow chips that animate a request path through the
   diagram, are worth it for anything non-trivial. Don't animate for decoration.
5. **Self-review against the checklist**, then deliver the single file.

## Hard requirements

- **Self-contained.** One `.html` file. No external `<script src>`, no CDN, no
  web fonts fetched at runtime, no network calls. Everything inline. (The
  reference files honor this — verified zero external resources.)
- **Full-screen, diagram-first.** The SVG is the page. Minimal chrome, minimal
  prose. If you're writing paragraphs, you're in the wrong skill.
- **Dark mode, hand-rolled.** CSS variables on `:root` and `html.dark`; a small
  theme-toggle button; `localStorage` persistence; an apply-before-paint script
  in `<head>` that defaults to `prefers-color-scheme` (so there's no flash).
- **Theme the SVG through CSS classes**, never hard-coded `#hex` inside the SVG —
  fill/stroke come from the CSS variables so the diagram follows the theme.
- **Responsive.** Use a `viewBox` so the diagram scales to any screen; don't pin
  pixel sizes.

## Self-review checklist

- Topology is correct: every edge is a real call/dependency, every boundary real.
- Edges are labeled (protocol / call / what flows), not just lines.
- Toggling dark/light re-themes the SVG with no hard-coded colors left behind.
- No external resource of any kind is fetched; opening the file offline works.
- It reads as a diagram, not a slide and not a report.

## Boundaries (don't reach for the wrong tool)

| Want | Use | Not this because |
|---|---|---|
| A 16:9 presentation that scales on screen → PDF | `slide-deck` | that's a multi-slide deck, not one diagram |
| Fixed-ratio IG/LinkedIn image | `social-card` | that's a raster social card |
| A general HTML report / explainer / prototype (prose + visuals) | built-in `web-artifacts-builder` | this skill is diagram-only by design |
| An actual web-app UI to ship | `frontend-design` | that's product UI, not a diagram artifact |

## References

- `references/architecture-example.html` — the finished worked example.
- `references/html-effectiveness/` — curated subset of the upstream gallery
  (diagram / SVG / design-system / animation / interaction examples).
- `references/attribution.md` — upstream sources & licenses.
