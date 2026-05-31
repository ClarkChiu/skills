# 台灣繁體中文排版規則 (full reference)

The reasoning behind every transform in `scripts/normalize.py`, plus edge cases
the script intentionally leaves to human judgment. Read this when a result is
questioned or you face a case the script doesn't cover.

## Table of contents
1. 盤古之白 — CJK ↔ Latin/digit spacing
2. 全形 / 半形 punctuation
3. 引號 — quotation marks
4. 簡轉繁 + 台灣用語 (OpenCC)
5. 異體字 / 台↔臺
6. Protected spans
7. Taiwan vs mainland China — quick contrast
8. Cases the script does NOT handle

---

## 1. 盤古之白 — CJK ↔ Latin/digit spacing

**Rule:** insert one half-width space between a Han character and an adjacent
Latin letter or digit. `使用Python3寫程式` → `使用 Python3 寫程式`.

**Why:** Han glyphs are full-width and visually dense; Latin glyphs are
proportional and narrow. Without a gap the two scripts collide and reading slows.
The name 盤古之白 ("Pangu's whitespace") jokes that the space separates Chinese
and Western like Pangu separated heaven and earth.

**Boundaries that get a space:** Han↔letter, Han↔digit, and a handful of symbols
(`@ & = $ % ^ * - + /`). **No space** is added around full-width punctuation —
it already carries its own visual padding — or between two Han characters, or
inside a Latin word.

**Edge cases (human judgment):**
- Brand/product names that embed digits: `Web3`, `iPhone 15`, `4K`, `K8s`, `C#`.
  The boundary space (`看 iPhone`) is correct; a space *inside* the name is not.
  The script spaces only at the CJK boundary, so it rarely breaks these — but
  scan for it.
- Units: `5GB`, `3.5公斤`. `5GB` → `5GB` stays (digit-letter, no CJK boundary);
  `3.5公斤` → `3.5 公斤` (digit↔Han). Both are acceptable Taiwan style; some
  style guides also write `5 GB`. The script does not force a space *inside*
  number-unit pairs.

---

## 2. 全形 / 半形 punctuation

**Rule:** punctuation in Chinese context uses full-width (全形) forms; English
context keeps half-width (半形).

| 半形 | 全形 | When |
|------|------|------|
| `,` | `，` | between/after Han |
| `.` | `。` | after Han, end of sentence (NOT decimals) |
| `;` | `；` | Chinese context |
| `:` | `：` | Chinese context |
| `?` | `？` | after Han |
| `!` | `！` | after Han |
| `()` | `（）` | when contents/surroundings are Chinese |

**Why:** full-width marks are designed on the same em grid as Han characters, so
they align vertically and sit correctly in the character flow. A half-width
comma after a Han character leaves an awkward gap and breaks the rhythm.

**The script is context-aware:** it only converts a mark adjacent to CJK. So
`中文,英文` → `中文，英文` but `func(a, b)` and `2, 3, 5` stay half-width. The
period is special-cased: `中文.` → `中文。` but `8.2.10` and `v3.14` are
protected as version/decimal spans and never touched.

**Taiwan note on 。** Taiwan/Hong Kong traditionally center the 句號 (`。`) and
逗號 in vertical text; in horizontal digital text the standard U+3002 `。` /
U+FF0C `，` are correct, which is what the script emits.

---

## 3. 引號 — quotation marks

**Rule:** Taiwan uses corner brackets — primary 「」, nested 『』. Convert
straight `"` / curly `" "` to 「」 and `'` / `' '` to 『』.

```
他說"你好"     → 他說「你好」
他說"我說『嗨』" → 他說「我說『嗨』」
```

**Why:** this is the clearest single marker of Taiwan vs mainland convention.
Mainland Simplified uses `""` and `''` (curved); Taiwan/HK Traditional uses the
corner brackets 「」『』. Using `""` in a 繁體 document reads as mainland or
careless.

**The script** maps curly quotes directly and pairs straight quotes greedily
*within a single line*. An unpaired straight quote (apostrophe, inch mark) is
left alone. Quotes inside protected code spans are never converted —
`` `git commit -m "x"` `` keeps its ASCII quotes.

---

## 4. 簡轉繁 + 台灣用語 (OpenCC s2twp)

**Rule:** convert Simplified Chinese to Traditional using the **Taiwan** standard
*with phrase conversion* — config `s2twp`.

The `p` matters: plain `s2t` only swaps characters (软→軟). `s2twp` also
localizes **vocabulary**:

| 簡體/大陸 | 台灣 |
|-----------|------|
| 软件 | 軟體 |
| 鼠标 | 滑鼠 |
| 视频 | 影片 |
| 内存 | 記憶體 |
| 程序 | 程式 |
| 网络 | 網路 |
| 点击 | 點選 |
| 设置 | 設定 |

**Why:** character-only conversion produces "Traditional-looking Simplified" —
技術文章 full of 軟件/鼠標/視頻 that no Taiwanese writer would use. Vocabulary
localization is what makes the output actually read as Taiwan Chinese.

**Dependency:** OpenCC is an optional Python package. If absent, the script
prints a loud warning to stderr and exits with code 2, and this step is skipped.
Install with `pip install opencc-python-reimplemented`. Never silently pass
simplified text through as if converted.

---

## 5. 異體字 / 台↔臺

**異體字** are variant glyphs for the same character. Taiwan has standard
(正體) preferences. The script applies a small, conservative map (e.g. 裏→裡)
— OpenCC already handles most variants, so this is only for residue.

**台 vs 臺:** the official government form is 臺 (臺灣, 臺北), but 台 is
overwhelmingly common and fully accepted. Forcing 台→臺 surprises most users, so
it is **OFF by default**. Pass `--formal-tai` when the user explicitly wants the
official form (government documents, formal publishing).

---

## 6. Protected spans (never modified)

To avoid corrupting technical content, these are pulled out before any transform
and restored verbatim afterward:

- Fenced code blocks ` ``` … ``` ` and inline code `` `…` ``
- URLs `https://…`
- Emails
- Version numbers / decimal chains: `8.2.10`, `3.14`
- File paths: `src/main.py`, `app/db/util.py`

Spacing (盤古之白) IS applied around these after restoration — `版本3.14` →
`版本 3.14`, `在src/x.py` → `在 src/x.py` — because the boundary space is
correct; only their internal content is protected.

---

## 7. Taiwan vs mainland China — quick contrast

| Feature | 台灣 繁體 (this skill) | 大陸 簡體 |
|---------|------------------------|-----------|
| Quotation marks | 「」『』 | "" '' |
| Characters | Traditional 正體 | Simplified |
| Vocabulary | 軟體/影片/程式/記憶體 | 软件/视频/程序/内存 |
| Book titles | 《》（same） | 《》 |
| 全形 punctuation | yes | yes |

The skill's job is the left column. If a user wants the right column, this is the
wrong skill.

## 8. Cases the script does NOT handle (by design)

- **着重号 (emphasis dots)** and **专名号 (proper-noun underline)** — these are
  presentation marks (CSS/markup), not plain-text transforms. typo.css renders
  them via styling; out of scope for text normalization.
- **标点挤压 / hanging punctuation / kerning** — visual layout, belongs to the
  rendering layer (CSS `text-spacing`, fonts), not the text.
- **Line-breaking / 避頭尾 rules** — layout-engine concern.
- **Semantic rewrites** — the skill never changes wording or meaning, only
  typography and character normalization.
