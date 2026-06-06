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
  "security operations" bands (threat landscape, live-defense sections), giving the
  industrial/SOC feel TXOne already leans on, without making the whole marketing
  site dark (see anti-patterns).
- Optional subtle **glassmorphism** (row 3) on product cards only, contrast verified
  to 4.5:1.
- **Light mode is primary; dark is sectional.** (Marketing site — see anti-pattern
  on dark-by-default below.)

### Palette — `colors.csv` row 5 (B2B Service) + insurance-row "protected green"
| Role | Hex | Note |
|---|---|---|
| Primary (authority) | `#0F172A` navy | from B2B Service row |
| Secondary / surface | `#334155` slate | |
| CTA / action accent | `#0369A1` security blue | WCAG-checked accent |
| Trust / status ("protected", zero-disruption) | `#16A34A` green | from Insurance Platform row (security-blue + protected-green); use for uptime/coverage signals |
| Threat / alert | `#DC2626` red | destructive, used sparingly |
| Background (light) | `#F8FAFC` | |
| Text foreground | `#020617` | |
| Border | `#E2E8F0` | |

Rationale: navy = authority/trust; security blue drives action; a dedicated
**status green** visually encodes the "zero operational disruption" promise wherever
uptime/coverage is shown; red is reserved for the threat narrative only.

### Typography — `typography.csv` rows 4 + 10
- **Headings: Space Grotesk** (row 4 "Tech Startup") — distinctive, technical-modern,
  credible without looking like a generic corporate template.
- **Body: IBM Plex Sans** (row 10 "Developer Mono") — high readability with
  engineering credibility.
- **Data / specs: JetBrains Mono** (row 10) — for the proof figures TXOne leans on
  ("1,500+ OT-native threat signatures", protocol-level coverage). Monospaced
  numbers read as precise and verifiable.
- Google Fonts: `Space Grotesk` + `IBM Plex Sans` + `JetBrains Mono` (import strings
  in `typography.csv`).

### Charts / data viz — `charts.csv`
Marketing site stays light on charts. Where efficacy is shown, use **single stat
callouts and one simple comparison bar** (coverage %, signatures, MTTR), not a
dashboard. (A real SOC/product dashboard would instead route to the *Financial
Dashboard* / *Analytics Dashboard* rows — out of scope for the public site.)

### Effects & motion
Swiss restraint: subtle hover (200–250ms), section transitions, feature reveals.
No parallax-heavy or glitch effects (wrong register for security/enterprise).

## 3. Page structure — `landing.csv` (fixes the current weaknesses)

1. **Hero** (`Minimal Single Column`, row 4) — one headline on "zero operational
   disruption", one primary CTA (*Book an OT assessment*), sticky-nav CTA.
2. **The problem** — why OT security ≠ IT security (dark "operations" band).
3. **One platform, four roles** — Edge / Stellar / Element / Sennin as a single
   labelled framework, each with a one-line job. **Directly fixes the weak
   product-line differentiation.**
4. **Proof** (`Hero + Testimonials + CTA`, row 2) — critical-infrastructure case
   studies + customer logos (manufacturing, energy, semiconductors). B2B Service
   *must-have: case-studies.*
5. **Outcomes / ROI** — "measurable outcomes", signature/coverage figures in
   JetBrains Mono. B2B Service *must-have: ROI-messaging.*
6. **OT-native vs generic IT security** (`Comparison Table + CTA`, row 7) —
   highlights TXOne's unique value and reinforces differentiation.
7. **CTA** — book assessment / demo, contrasting accent, ≥7:1 contrast.

## 4. Accessibility — `accessibility/wcag-checklist.md`
Target **WCAG 2.2 AA** (not optional — critical-infrastructure and government buyers
make it a procurement requirement). P0: 4.5:1 text contrast (the palette accents are
already WCAG-adjusted in `colors.csv`), visible keyboard focus, full keyboard nav,
non-color-only status (pair the green/red with icons + labels).

## 5. Anti-patterns to avoid (from the rows used)
- AI purple/pink gradients, playful styling, "hidden credentials" (B2B Service
  anti-patterns) — wrong trust signal for security buyers.
- **Dark mode by default** on the marketing site (SaaS row anti-pattern) — keep dark
  for the operations bands only.
- Repeated messaging blocks and dense spec dumps (the current site's two weaknesses)
  — one idea per band, specs behind progressive disclosure.

## 6. Handoff
Implement with the **`frontend-design`** skill. Stack: **Next.js** (marketing site,
SEO, static-first) — pass `data/ui-ux-pro-max/stacks/nextjs.csv` rules alongside
this brief. Build light-mode-first with the navy/security-blue/status-green system
above; treat the dark "operations" bands as a themed section, not a global mode.

---
*Sources used: `ui-reasoning.csv` (r5, r1), `styles.csv` (r1, r7, r3), `colors.csv`
(r5 B2B Service, r41 Insurance), `typography.csv` (r4, r10), `landing.csv` (r1, r2,
r4, r7), `charts.csv`, `accessibility/wcag-checklist.md`. Data provenance: see
`../references/attribution.md`.*
