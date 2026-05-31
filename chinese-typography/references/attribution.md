# 參考來源 (sources & attribution)

The rules in this skill are derived from established Chinese-typography
conventions and the following projects. None of their code is copied; the skill
re-implements the rules natively (盤古之白 spacing) or calls an independent
library (OpenCC).

## Primary sources

- **pangu.js** — Vinta Chien. <https://github.com/vinta/pangu.js> (MIT).
  The 盤古之白 (CJK ↔ Latin/digit spacing) rule set. `scripts/normalize.py`
  re-implements the core spacing regex natively to avoid a runtime dependency;
  the boundary definitions follow pangu.js.

- **OpenCC** — Open Chinese Convert. <https://github.com/BYVoid/OpenCC> (Apache-2.0).
  Used directly (optional dependency, `opencc-python-reimplemented`) for
  Simplified→Traditional conversion with Taiwan vocabulary via the `s2twp`
  config.

- **typo.css** — Sofish Lin. <https://github.com/sofish/typo.css> (MIT).
  Reviewed for Chinese web-typography conventions. It is a CSS reset, so its
  display-layer rules (着重号 emphasis dots, 专名号 proper-noun underline, line
  rhythm) are intentionally **out of scope** for this text-normalization skill —
  documented in `typography-rules.md §8`. Credited for confirming the
  Taiwan/mainland punctuation conventions.

- **fudesign2008/open-skills `chinese-format`** — FuDesign2008.
  <https://github.com/FuDesign2008/open-skills> (MIT).
  Prior-art agent skill for Chinese punctuation formatting. This skill follows
  its punctuation-conversion approach and deliberately extends beyond it: it adds
  Taiwan 「」『』 quotation marks, enforces (not optional) 盤古之白 spacing,
  performs Simplified→Traditional + Taiwan-vocabulary conversion, and ships a
  deterministic script rather than relying on the model. The fudesign skill is
  Simplified-Chinese / mainland-oriented; this one is Taiwan Traditional.

## Prior art surveyed (comparable projects)

Reviewed to benchmark coverage and decide which rules to adopt. The skill stays
intentionally narrower than these full linters (see `typography-rules.md §8` for
what is deliberately out of scope), but several rules were adopted or validated
against them.

- **AutoCorrect** — huacnlee. <https://github.com/huacnlee/autocorrect>
  (Apache-2.0, ~1.6k★; used by MDN Web Docs, Apache APISIX). Rust CJK linter
  doing 盤古之白 + bidirectional width normalization via Tree-sitter per-language
  AST. Does **no** Simplified→Traditional (this skill's OpenCC step is a clear
  edge over it). Informed: backtick/`$`/dash spacing as distinct rules, and the
  idea of a brand-name casing dictionary.

- **zhlint** — jinjiang / zhlint-project.
  <https://github.com/zhlint-project/zhlint> · <https://zhlint.jinjiang.dev/>
  (MIT). Markdown-AST-aware Chinese text linter. Source of several adopted
  rules: ellipsis/dash normalization, duplicate-/mixed-punctuation handling,
  no-space-inside/outside full-width quotes & brackets, abbreviation guard
  (`skipAbbrs`), pure-English-run skip (`skipPureWestern`). Its `skipZhUnits`
  (no space between a number and a Chinese date/time unit) was **intentionally
  NOT adopted** — this skill's user prefers the space (`5 月`, `12 時 30 分`).

- **中文文案排版指北 (chinese-copywriting-guidelines)** — sparanoid.
  <https://github.com/sparanoid/chinese-copywriting-guidelines> (Taiwan-authored,
  Traditional). The canonical community ruleset; validated the 「」 quote choice,
  full-width punctuation, and proper-noun casing rule (`GitHub`, `iOS`,
  `JavaScript`).

- **StarCC** — StarCC0. <https://github.com/StarCC0/starcc-py>. Newer
  segmentation-aware simp↔trad framework. Evaluated as an OpenCC alternative and
  **declined**: its dictionaries are downstream of OpenCC's, so it is no more
  authoritative for Taiwan vocabulary, and it does not solve the 臺/台 question.
  Noted as a possible future enhancement for rare longest-match disambiguation
  only.

## Reference standards

- **教育部《重訂標點符號手冊》修訂版** (2008 公布) — the binding Taiwan
  punctuation spec.
  <https://language.moe.gov.tw/001/upload/files/site_content/m0001/hau/haushou.htm>
  Mandates 「」/『』 quotes, each mark occupying one 全形 cell, 頓號 、 for lists,
  and the …… / —— forms. Direct basis for the punctuation rules.

- **教育部《異體字字典》** (正式七版, 2024) — the binding orthography spec.
  <https://dict.variants.moe.edu.tw/> — defines 正字 vs 異體字. Per this
  dictionary **臺 is the 正字 and 台 its 異體字**; the skill's default 臺→台 is a
  deliberate *common-usage-over-orthodoxy* choice (the user rarely uses 臺),
  reversible with `--formal-tai`. See `typography-rules.md §5`.

- **W3C 中文排版需求 (clreq)** — *Requirements for Chinese Text Layout*.
  <https://www.w3.org/International/clreq/> — authoritative reference for
  全形/半形 punctuation and CJK layout conventions.

- **OpenCC config semantics** — config list and the `s2twp` chain
  (`STPhrases → STCharacters → TWPhrases → TWVariantsPhrases → TWVariants`):
  <https://github.com/BYVoid/OpenCC/blob/master/data/config/s2twp.json>.
  Issue [#1001](https://github.com/BYVoid/OpenCC/issues/1001) documents why bare
  `s2t` is not a user-facing default. Confirms `s2twp` (vocab-localizing) is the
  correct conversion authority, and that OpenCC does **not** touch
  punctuation/spacing — so typography stays in this skill's hand-rules, running
  strictly *after* OpenCC.

## Note on a removed source

The user originally supplied an iThome article URL
(`ithelp.ithome.com.tw/articles/10369821`). On review that article is a
prompt-optimizer install tutorial with **no** typography content — the word
正規化 there refers to *prompt* normalization, not text normalization. It was
not used. If a different iThome typography article was intended, swap it in here.
