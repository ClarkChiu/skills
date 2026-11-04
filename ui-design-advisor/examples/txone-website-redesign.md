# Design Brief — TXOne Networks website redesign

> Worked example of the `ui-design-advisor` workflow. The request was: "If you
> were to redesign the TXOne Networks website, how would you do it?" Every choice
> below is routed from `data/` (the file + row each decision came from is cited),
> then reasoned over — not invented. After this brief, implementation hands off to
> the built-in `frontend-design` skill.

## 1. Product & screen

Marketing/corporate website for **TXOne Networks** — OT / ICS / cyber-physical
systems cybersecurity. Four product lines under one platform: **Edge** (network
defense), **Stellar** (endpoint), **Element** (security inspection), **Sennin**
(enterprise orchestration). Core promise: **"zero operational disruption."**

**Audience:** CISOs and security directors, OT/plant engineers, and facility
managers in critical infrastructure (manufacturing, energy, semiconductors,
healthcare). Two reading levels at once — security buyers and operations buyers.

**Current-site weaknesses to fix** (from review): repeated messaging blocks, weak
visual differentiation between the four product lines, and dense technical specs
that overwhelm non-technical stakeholders.

## 2. Direction (one coherent language, not a menu)

Routed primarily from `ui-reasoning.csv` row 5 **B2B Service** → *Trust & Authority
+ Minimalism, Professional blue + Neutral grey, must-have: case-studies +
ROI-messaging; avoid playful design, hidden credentials, AI purple/pink gradients.*

### Style — `styles.csv`
- **Base: Minimalism & Swiss Style** (row 1) — enterprise/dashboard/SaaS, grid-based,
  WCAG AAA, fast. This is the trust-and-clarity backbone and directly counters the
  "dense, overwhelming" weakness.
- **Accent treatment: restrained Dark Mode (OLED)** (row 7) — used only for the
  "security operations" band and the closing CTA, giving the industrial/SOC feel TXOne
  already leans on, without making the whole marketing site dark (see anti-patterns).
- **Light mode is primary; dark is sectional.** (Marketing site — see anti-pattern
  on dark-by-default below.)

### Palette — `colors.csv` row 5 (B2B Service) + insurance-row "protected green"
| Role | Hex | Note |
|---|---|---|
| Primary (authority) | `#0F172A` navy | from B2B Service row |
| Secondary / surface | `#334155` slate | |
| CTA / action accent | `#0369A1` security blue | WCAG-checked accent |
| CTA on dark bands | `#38BDF8` | navy text on it is 8.33:1 |
| Trust / status ("protected", zero-disruption) | `#16A34A` green | from Insurance Platform row (security-blue + protected-green); use for marks, and for text on navy (5.42:1). As small text on white it's only 3.3:1 |
| Trust text on light surfaces | `#166534` | 7.13:1 on white, 6.35:1 on the highlighted table column |
| Threat / alert | `#DC2626` red | destructive, used sparingly |
| Background (light) | `#F8FAFC` | |
| Text foreground | `#020617` | |
| Border | `#E2E8F0` | |

Rationale: navy = authority/trust; security blue drives action; a dedicated
**status green** visually encodes the "zero operational disruption" promise wherever
uptime/coverage is shown; red is reserved for the threat narrative only.

### Typography — `typography.csv` rows 4 + 10
- **Headings: Space Grotesk** (row 4 "Tech Startup") — distinctive, technical-modern,
  credible without looking like a generic corporate template. The built page swaps
  this for Chakra Petch; the comment at the top of the page says why.
- **Body: IBM Plex Sans** (row 10 "Developer Mono") — high readability with
  engineering credibility.
- **Data / specs: JetBrains Mono** (row 10) — for the proof figures only ("1,500+
  OT-native threat signatures"). Monospaced numbers read as precise and verifiable;
  on labels or table words it's the "technical" costume from `anti-default.md` §2.
- Google Fonts: `Space Grotesk` + `IBM Plex Sans` + `JetBrains Mono` (import strings
  in `typography.csv`).

### Charts / data viz — `charts.csv`
Marketing site stays light on charts. Where efficacy is shown, use **plain figures**
(coverage %, signatures), not a dashboard. (A real SOC/product dashboard would instead
route to the *Financial Dashboard* / *Analytics Dashboard* rows — out of scope for the
public site.)

### Effects & motion
Swiss restraint: subtle hover (200–250ms), section transitions, feature reveals.
No parallax-heavy or glitch effects (wrong register for security/enterprise).

## 3. Page structure — `landing.csv` (fixes the current weaknesses)

1. **Hero** (`Minimal Single Column`, row 4) — one headline on "zero operational
   disruption", one primary CTA (*Book an OT assessment*), sticky-nav CTA. No stat
   strip: the figures sit in Outcomes, so the hero doesn't repeat them.
2. **The problem** — why OT security ≠ IT security, followed by a dark "operations"
   band for the production lifecycle.
3. **One platform, four roles** — Edge / Stellar / Element / Sennin as a single
   labelled framework, each with a one-line job. **Directly fixes the weak
   product-line differentiation.**
4. **Proof** (`Hero + Testimonials + CTA`, row 2) — critical-infrastructure case
   studies + customer logos (manufacturing, energy, semiconductors). B2B Service
   *must-have: case-studies.*
5. **Outcomes / ROI** — signature/coverage figures in JetBrains Mono, as plain rows
   rather than cards. B2B Service *must-have: ROI-messaging.*
6. **OT-native vs generic IT security** (`Comparison Table + CTA`, row 7) —
   highlights TXOne's unique value and reinforces differentiation.
7. **CTA** — book assessment / demo, contrasting accent: navy on `#38BDF8`, 8.33:1.

## 4. Accessibility — `accessibility/wcag-checklist.md`
Target **WCAG 2.2 AA** (not optional — critical-infrastructure and government buyers
make it a procurement requirement). P0: 4.5:1 text contrast (computed in section 6;
the palette's accents don't all pass as small text), visible keyboard focus, full
keyboard nav, non-color-only status (pair the green/red with icons + labels).

## 5. Anti-patterns to avoid (from the rows used)
- AI purple/pink gradients, playful styling, "hidden credentials" (B2B Service
  anti-patterns) — wrong trust signal for security buyers.
- **Dark mode by default** on the marketing site (SaaS row anti-pattern) — keep dark
  for the operations band and the closing CTA.
- Repeated messaging blocks and dense spec dumps (the current site's two weaknesses)
  — one idea per band, specs behind progressive disclosure.

These look like the defaults in `anti-default.md` §2, and are kept on purpose:

- **One eyebrow, on the hero only** — it names the category for a reader arriving
  cold. No other section has one.
- **Stage numbers in the lifecycle band** — the four stages really do run in order.
- **Four equal product cards** — four real products of equal standing, and the fix
  for the weak product-line differentiation.

## 6. Checks (measured on the built page, 2026-11-04)
- **State coverage:** buttons and nav links define hover and `:focus-visible`,
  checked by hovering and tabbing through them. The ring is `#0369A1` on light
  (5.67:1) and `#38BDF8` in the dark CTA band (8.33:1). Cards aren't links, so they
  have no hover. There's no disabled control and no theme switch on this page.
- **Computed contrast:** all text elements pass at 1440 px wide (98 of them) and 390 px
  wide (94, because the nav links are hidden there). The lowest is 4.55:1: `#64748B` on
  the page background, for captions, the table's generic-IT column and the footer. The
  ghost button's border uses the same color; it's the only button without a fill.
- **Type floor:** the smallest text is 12 px. Headings are 1.26× or more of the body
  text they sit with. The longest paragraph runs 48ch: these are short blurbs, not
  running text, so the 65–75ch measure doesn't come into play.

## 7. Handoff
Implement with the **`frontend-design`** skill. Stack: **Next.js** (marketing site,
SEO, static-first) — pass `data/ui-ux-pro-max/stacks/nextjs.csv` rules alongside
this brief. Build light-mode-first with the navy/security-blue/status-green system
above; treat the two dark bands as themed sections, not a global mode.

---
*Sources used: `ui-reasoning.csv` (r5, r1), `styles.csv` (r1, r7), `colors.csv`
(r5 B2B Service, r41 Insurance), `typography.csv` (r4, r10), `landing.csv` (r1, r2,
r4, r7), `charts.csv`, `accessibility/wcag-checklist.md`. Data provenance: see
`../references/attribution.md`.*
