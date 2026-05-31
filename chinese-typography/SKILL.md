---
name: chinese-typography
description: >-
  台灣繁體中文排版與正規化 (Taiwan Traditional Chinese typography & normalization).
  Cleans up Chinese text to Taiwan publishing convention: inserts 盤古之白 (a space
  between Han characters and Latin letters / numbers), converts half-width ASCII
  punctuation to full-width 全形 (，。；：？！（）), fixes quotation marks to corner
  brackets 「」『』, converts Simplified→Traditional with Taiwan vocabulary
  (软件→軟體, 鼠标→滑鼠, 视频→影片 via OpenCC s2twp), and corrects common 異體字.
  USE THIS SKILL whenever the user wants to format, clean up, normalize, tidy,
  proofread, or fix the typography/punctuation of Traditional Chinese (繁體中文 /
  台灣中文) text — whether they paste the text directly or point at a .md/.txt
  file. Trigger on phrases like 「排版」「正規化」「中文格式」「全形半形」「盤古之白」
  「簡轉繁」「台灣用語」「中英文加空格」「標點符號修正」, or any request to make
  mixed Chinese-English text read correctly. Also use when reviewing a Markdown
  doc, README, or article written in Traditional Chinese for typographic polish.
  Do NOT use for Simplified-Chinese-only output targeting mainland China, or for
  translation between languages.
---

# 台灣繁體中文排版正規化

Mixed Chinese-English text is full of small typographic errors that are tedious
to fix by hand and easy to do inconsistently: missing spaces between 中文 and
English, half-width commas where 全形 belongs, straight `"` quotes instead of
「」, simplified characters and mainland vocabulary leaking in. These rules are
**deterministic** — there is one right answer per case — so a script does the
work far more reliably than fixing them by eye, and you stay consistent across a
whole document.

The skill bundles that script. Your job is to **run it, read the diff, and apply
judgment only on the genuinely ambiguous cases** the script flags — not to
re-implement spacing rules in your head.

## The one command you need

```bash
python3 <skill>/scripts/normalize.py [INPUT] [FLAGS]
```

`<skill>` is this skill's directory. The script reads from stdin, a file
argument, or `--text`, and writes normalized text to stdout. It never edits a
file unless you pass `--in-place`.

| Goal | Command |
|------|---------|
| Normalize pasted text | `echo "文字…" \| python3 …/normalize.py` |
| Preview a file as a diff | `python3 …/normalize.py doc.md --diff` |
| Normalize a file, rewrite it | `python3 …/normalize.py doc.md --in-place` |
| Normalize a file → stdout (keep original) | `python3 …/normalize.py doc.md` |
| One-off string | `python3 …/normalize.py --text "使用Python3"` |

## Workflow

1. **Run it.** Pipe the pasted text, or pass the file. For a file the user
   cares about, default to `--diff` first so you (and they) can see exactly what
   changed before touching the original.
2. **Check the OpenCC warning.** If stderr prints `WARNING: OpenCC not installed`
   (exit code 2), the Simplified→Traditional + Taiwan-vocabulary step was
   **skipped** — the text may still contain simplified characters. Don't claim
   the text was fully normalized. Either install it
   (`pip install opencc-python-reimplemented`) and rerun, or tell the user this
   step was skipped. Failing loud here matters: silently shipping 简体 in a
   繁體 document is exactly the bug this skill exists to prevent.
3. **Show the result.** Present the normalized text (or the diff). If anything in
   the diff looks wrong, say so — see *When to override the script* below.
4. **Apply** with `--in-place` once the user is happy, or just hand back the
   normalized text for a pasted snippet.

## What the script fixes (and why)

Each rule reflects Taiwan publishing convention. Full detail and the rationale
live in `references/typography-rules.md` — read it when a result surprises you
or the user questions a specific change.

- **盤古之白** — one half-width space between Han and Latin/digits: `Python3` in
  `使用Python3` → `使用 Python3`. Improves legibility; it is the single most
  common omission in Chinese tech writing.
- **全形標點** — ASCII punctuation *in Chinese context* becomes full-width:
  `中文,` → `中文，`, `對吧?` → `對吧？`. The script only converts marks adjacent
  to CJK, so English sentences and code stay half-width.
- **引號 → 「」『』** — straight/curly quotes become corner brackets, the Taiwan
  standard (mainland uses `""`). Nested quotes use `『』`.
- **簡轉繁 + 台灣用語** — OpenCC `s2twp`: not just character conversion but
  vocabulary localization — 软件→軟體, 鼠标→滑鼠, 视频→影片, 内存→記憶體.
- **異體字** — Taiwan-preferred glyphs (裏→裡). Conservative by default. Place
  names 台→臺 are OFF by default (both are accepted; 台 is far more common — this
  user rarely writes 臺); enable with `--formal-tai` only when the official 臺 is
  wanted. OpenCC's `s2twp` forces 臺, so the default reverts it back to 台.
- **省略號／破折號** — Taiwan MOE forms: `...` → `……` (six-dot), `--`/`—` → `——`
  between Han. Runs before the period rule so `...` is never mangled into `。.。`.
- **全形英數 → 半形** — stray full-width letters/digits from pasted text get
  normalized: `ＡＢＣ１２３` → `ABC123` (full-width punctuation is left alone —
  that's wanted). Disable with `--no-width`.
- **專有名詞大小寫** — canonical casing for common tech names: `github` → `GitHub`,
  `ios` → `iOS`, `javascript` → `JavaScript`, `nodejs` → `Node.js`. Word-boundary
  matched so it won't touch English prose. Disable with `--no-casing`.
- **西文縮寫** — `Mr.` `Dr.` `e.g.` `i.e.` `etc.` `Fig.` etc. are protected, so
  their period is never converted to 。.

**Protected, never touched:** fenced/inline code, URLs, emails, file paths,
version numbers and decimals (`8.2.10`, `3.14`), percentages, Western
abbreviations. This is why `src/main.py` and `https://…` survive intact.

**Number + Chinese date/time unit gets a space** (`5月` → `5 月`, `12時30分` →
`12 時 30 分`) by this user's preference — note this diverges from zhlint's
`skipZhUnits` convention, which keeps them tight. It is deliberate.

## Personal dictionary (highest priority)

The script loads `user-dictionary.json` by searching **upward from the script
toward the project root** (the user's skills repo root) — so the file lives at
the repo root, shared across tools and not tied to this skill or to Claude.
Override the path with `--dict`. This is the user's own file and it **outranks
every rule, including OpenCC** — use it to encode their preferences rather than
hard-coding them:

```json
{
  "replacements": {"原文": "目標"},   // verbatim, applied last — wins over everything
  "casing":       {"myapp": "MyApp"}, // extends/overrides the casing table
  "protect":      ["別動我"],          // never altered by any rule
  "formal_tai":   false                // override the 台/臺 default
}
```

When the user states a recurring preference (a term they always write a certain
way, a name to leave alone), prefer adding it here over editing the script.

## Turning rules off

Each stage has a `--no-*` switch (`--no-convert`, `--no-quotes`, `--no-punct`,
`--no-spacing`, `--no-fixes`, `--no-width`, `--no-casing`). Use them when the
user wants only part of the job — e.g. "just add the spaces, don't convert to
traditional" → `--no-convert --no-quotes --no-punct`.

## On conflicts — ask, don't guess

This skill weights mature, comprehensive projects first: **OpenCC `s2twp` is the
authority for simplified→traditional + Taiwan vocabulary**; typography rules
follow established conventions (pangu.js, zhlint, 中文文案排版指北, 教育部標點手冊).
When a mature project's behavior conflicts with the user's stated preference (the
台/臺 case is the canonical example — OpenCC says 臺, the user wants 台), **do not
silently pick one. Surface the conflict and ask the user**, then encode their
answer (in `user-dictionary.json` or a flag). The user has asked to be consulted
on conflicts rather than have them guessed.

## When to override the script

The deterministic rules are right ~99% of the time, but a few cases need your
judgment — the script can't know intent:

- **Proper nouns / brand names** where a space is wrong: `Web3`, `iPhone`,
  `4K`, `K8s`, `C#`. The script spaces around the CJK boundary, not inside
  these, so they are usually fine — but if it spaces inside a name, fix that one
  by hand and mention it.
- **Quotes that aren't quotes**: a straight `"` used as an inch mark or an
  unpaired apostrophe. The script only converts *paired* straight quotes on one
  line, so this is rare, but scan the diff.
- **Deliberate Simplified content** (a quotation, a mainland product name). If
  the user wants part of the text left simplified, run with `--no-convert` and
  convert the rest manually, or restore that span afterward.

When you override, **say what and why** in one line. Don't silently diverge from
the script's output — the user should be able to trust that what the script
touched follows the documented rules.

## Reference

- `references/typography-rules.md` — the full rule set, Taiwan-vs-mainland
  differences, edge cases, and the reasoning behind each rule. Read it when a
  result is questioned or you hit a case the script doesn't cover.
- `references/attribution.md` — sources these rules are derived from.
