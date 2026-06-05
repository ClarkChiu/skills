# Skill Evaluation Criteria

> `skill-curator`'s decision brain. Evaluate "should we use it, and how" for an external skill.
> Extracted from the 2026-06-02 11-skill evaluation. Security verdict is delegated to `skill-auditor`;
> discovery to `skill-finder`; this file owns **relevance + decision + record**.

## Start from the user profile

The evaluation is **not** "is this skill good?" but **"is it useful for THIS person's work/life?"**
Read the **"User Profile" section of the repo-root `CLAUDE.md`** (portable source of truth; the `user-profile` memory is only a local cache). Summary: network/systems software engineer (10+ yrs), backbone is **test-automation architecture + DevOps/IaC (Terraform/CI-CD) + cloud (GCP) + Python + protocol/standards research (patents, papers)**, 5+ yrs PM/product, writes **a lot of EN + zh-TW technical docs**. The scope is "skills + LLM to help work and life broadly", not just Chinese processing.
→ Test automation, DevOps/IaC, cloud, networking/protocols, **technical writing**, PM/spec, research, ML are all **highly relevant**, not niche. Depth is in networking/systems/infra/test-automation, so **don't over-weight pure front-end web**.

## Five-step decision pipeline

```
[0] Relevance   → useful for my context (dev/systems/PM/writing/research/life)? No → stop.
[1] Duplication → duplicates a built-in or one of my existing skills? Yes → use the existing one, or "extend mine" rather than install it.
[2] Security    → goes to skill-auditor. Verdict not SAFE → stop (or sandbox only).
[3] Provenance  → author trustworthy? maintained? or a solo 2★ / single fork / two inconsistent copies?
[4] Install or build-your-own → see the table below.
[5] Record      → local detail (gitignored): audits/ + the day's work log; public: one neutral row in research/skill-index.md.
```

## Step 4 core: install vs build-your-own vs skip

Judge **where the skill's value lives**, which decides how to use it:

| Signal | Leans | Why |
|---|---|---|
| Ships **non-trivial code / curated data**, source **trustworthy and maintained** | **install** | reinventing it isn't worth it; installed, it tracks upstream |
| Pure **prose / persona** (value is editable text) | **build-your-own** | copy cost ≈ zero; your own version is customizable and carries no dependency |
| **Weak source** (solo low-star, unmaintained, two inconsistent copies in the repo, no frontmatter) | **build-your-own** | don't tie your production flow to a shaky repo |
| You have a **strong customization need** (zh-TW, your stack, your PM style) | **build-your-own** | your own version gives exactly the variant you want |
| Duplicates a **built-in / existing** capability | **neither** | use the existing one; at most extend yours |
| In between (curated prose, e.g. a translated rule set) | **vendor & customize** | start from the existing file, copy into the repo, add attribution, tune the flavor |
| **Trustworthy source + ships code, but the code is opt-in peripheral and the core value is prose** | **leans build-your-own** | don't be fooled by "has code + good source" into installing — first ask "is that code value for **this user**, or peripheral they won't use?" Peripheral → write the prose yourself; only vendor if you actually need that code |

### Tie-breaker: when "install" and "build-your-own" both apply

A skill can hit **both** "ships code + trustworthy source" (→install) and "value is in prose" (→build-your-own).
Don't average, don't shout install at the sight of code. Deciding question: **"that engineering — is it value this user can't reproduce, or opt-in peripheral they'll never turn on?"**
- Core value and hard to reproduce (e.g. ui-ux-pro-max's 161-palette curation, deep-research's 3200 lines) → **install**.
- Opt-in peripheral this person mostly won't enable (e.g. brainstorming's Visual Companion local server, for a terminal-first full-stack dev) → **build-your-own**: extract the prose, wire it into your own pipeline; only drop to **vendor** if you actually need that peripheral.
(Example: brainstorming has a strong source and ships a node server, but the core value is the "design before code" prose gate → build-your-own, not install.)

### The mantra

> **Engineering you can download, install; text you can write, write your own version of.**
> A prose skill's value is "the text itself" → build-your-own + hang it in your repo (tracked upstream by skill-evolve), steadier than an APM dependency on a thin fork.
> A code/data skill's value is "hard-to-reproduce engineering or curation" → install.

## Risk and install surface (auditor's supplement)

Security "clean" ≠ "zero cost". Even SAFE, look at the **install surface**:

- **Privileged install**: `sudo`, fetch-and-run a remote install script, edits to `~/.bashrc` → high alert (e.g. minimax-docx's setup.sh installing .NET).
- **Unpinned auto-install**: `pip install --break-system-packages`, `npm i -g`, `npx playwright install chromium`, bootstrap-on-import → supply-chain surface.
- **Installer ≠ runtime**: the script itself can be clean while the landmine is in its CLI installer (e.g. ui-ux-pro-max's `extract.ts` shell string interpolation) → **copy the skill dir manually, avoid the CLI**.
- **Auto-installs system deps** (telling the agent to brew/apt things itself) → install them yourself first, don't let it run automatically.
- **Pure prose, no net/shell** = lowest risk tier (e.g. humanizer, product-spec-builder).

## Common traps (from real evaluations)

- **One bullet ≠ one skill**: `minimax-docx、pdf、xlsx` on one line is actually 3. Expand before counting.
- **List sources are low-trust**: a third-party recommendation list mixes authors and quality levels.
- **Same name, different thing**: `dev-builder` collides with `21st-dev-builder-v2`; `ppt-generator` is actually `pptx-generator`. Go to the canonical repo, don't trust the listing.
- **Doubtful star counts**: rendered-page stars without API auth can misread/inflate (superpowers' "215k" is very likely a misread) → mark unverified, not fact.
- **Different skills eat the same file but formats may not be compatible**: product-spec-builder / dev-builder / ui-prompt-generator all consume `Product-Spec.md` but from different authors → confirm the fields before chaining them.
- **process.env isn't necessarily exfil**: `apiKey: process.env.X` straight into an SDK constructor = standard usage; it's exfil only if the key gets woven into a URL/log/third-party request.
- **"document not sent" ≠ safe**: MiniMax doesn't transmit document content, but its install privileges are the real risk.

## Output: recording format

Leave a trail on every evaluation, in **local** and **public** layers (everything under `research/` except `skill-index.md` is gitignored):

- **Local (private)**:
  - `audits/YYYY-MM-DD-<skill>.md`: full SKILL AUDIT REPORT (skill-auditor format).
  - `<YYYY-MM-DD>-skill-research-log.md` (the day's work log): date | name | URL | author | duplicate? | **security highlights | detailed reasoning** — third-party security detail, vulnerabilities, and wording all stay in this layer.
- **Public**: one **neutral** row in `skill-index.md`: date | name | URL | author | duplicates-built-in? | verdict.
  **No** security detail / vulnerability disclosure / commentary on the third party; the verdict is framed as "fit for this project", not a quality judgment.
  Reason: a public repo shouldn't name-and-shame someone else's skill, nor disclose a third party's vulnerability without notice.
  The public index is kept in Chinese (the repo's index language); map the verdicts to its labels: install→直接裝, build-your-own→參考自製, vendor & customize→收錄＋客製, skip→跳過.
- Research ≠ install; before install, v1.0-safe ≠ the version you fetched is safe — re-review the local copy after install.
