# Output format — HTML (this skill) vs native .pptx

This skill renders to **one self-contained HTML file**. That is the right default for
*viewing and sharing* — a link anyone can open, infinite design freedom, zero
dependencies, trivially hosted. But HTML cannot be opened or hand-edited in PowerPoint,
and some contexts genuinely require an editable `.pptx`. Know which you need before you
start.

## How to choose

| You need… | Use |
|-----------|-----|
| A link to share (chat, web, mobile), or a projected/standalone deck | **HTML — this skill** |
| Design freedom, animation, QR, an offline self-contained file to forward | **HTML — this skill** |
| A file a colleague will hand-edit in PowerPoint / Keynote / Google Slides | **native .pptx** |
| To drop into a corporate PowerPoint template, or print/archive as Office | **native .pptx** |
| Speaker notes voiced as audio narration | **native .pptx** (see below) |

The two are **complementary, not competing**. The *design principles* in
`principles.md` (one idea per slide, the type scale, deck rhythm, shadow discipline) are
**output-agnostic** — they apply equally to HTML and to .pptx. Only the final renderer
differs. So pick the renderer by deliverable need; the craft transfers either way.

## For editable .pptx: ppt-master

We do **not** build a .pptx exporter here — faithfully converting HTML→pptx is a losing
battle, and a mature MIT tool already does the hard part. For native, editable PowerPoint
use **ppt-master** by Hugo He (https://github.com/hugohe3/ppt-master, MIT): it
hand-authors SVG per slide and converts to real DrawingML shapes/text, so the output
opens and edits in PowerPoint. We already borrowed several of its *principles* (deck
rhythm, shadow discipline, key-info emphasis — see `attribution.md`); for the .pptx
*output* itself, use the tool directly rather than reimplementing it.

**Before adopting it, audit it (`skill-auditor`).** It is a high-capability skill by
design: it runs shell tooling (SVG→pptx conversion, LibreOffice rendering) and, if you
enable its optional AI image-generation / audio-narration features, it sends your prompts
and your API keys to whichever third-party provider you configure (OpenAI, Stability,
Replicate, MiniMax, Alibaba DashScope, Zhipu, etc. — many CN and international endpoints).
None of that is covert — it is what the features do — but it means: review which
providers you enable, keep your `.env` keys scoped, and don't feed it sensitive source
documents you wouldn't want leaving your machine. Run a first generation in a sandbox.
