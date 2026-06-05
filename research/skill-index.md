# 外部 Skill 評估索引 (public)

> 本表是「**對本專案使用者的適配決定**」記錄，**不是對各 skill 品質或作者的評斷**。
> 同一個 skill 對別人可能很適合。**裝前一律自行跑 `skill-auditor`** 重新評估。
> 完整稽核報告與詳細理由保留在本機、未版控（`research/audits/`、當日工作日誌）。
>
> 裁決：🟩 直接裝 ｜ 🟦 參考自製（自寫貼合本專案的版本）｜ 🟨 收錄＋客製（把上游原檔複製進儲存庫，再照需求改）｜ 🟥 跳過（不適配本專案，多為已被內建涵蓋）

| 日期 | Skill | 來源 | 作者 | 重複內建? | 裁決 |
|---|---|---|---|---|---|
| 2026-06-02 | humanizer (EN) | github.com/blader/humanizer | blader | 否 | 🟨 收錄 |
| 2026-06-02 | humanizer-zh-TW | github.com/kevintsai1202/Humanizer-zh-TW | kevintsai1202 | 否 | 🟨 收錄 |
| 2026-06-02 | brainstorming | github.com/obra/superpowers | obra | 部分（doc-coauthoring） | 🟦 參考自製 |
| 2026-06-02 | product-spec-builder | github.com/luodashiv5/please_answer_this_era_5.0 | luodashiv5 | 部分 | 🟦 參考自製 |
| 2026-06-02 | dev-builder | github.com/zinohome/cozyengine | zinohome | 局部（後端 scaffolding 空白） | 🟦 參考自製 |
| 2026-06-02 | ui-ux-pro-max | github.com/nextlevelbuilder/ui-ux-pro-max-skill | nextlevelbuilder | 部分（frontend-design） | 🟨 收錄 |
| 2026-06-02 | ui-prompt-generator | github.com/luodashiv5/please_answer_this_era_5.0 | luodashiv5 | 否 | 🟥 跳過 |
| 2026-06-02 | deep-research | github.com/199-biotechnologies/claude-deep-research-skill | 199-biotechnologies | 是（內建 deep-research） | 🟥 跳過（用內建。功能：多來源網路研究，搜→讀→綜合→附引用） |
| 2026-06-02 | minimax-docx / -pdf / -xlsx | github.com/MiniMax-AI/skills | MiniMax-AI | 是（內建 docx/pdf/xlsx） | 🟥 跳過（用內建。功能：以 python-docx／reportlab／openpyxl 生 Word／PDF／Excel） |
| 2026-06-02 | pptx-generator | github.com/MiniMax-AI/skills | MiniMax-AI | 是（內建 pptx） | 🟥 跳過（用內建 ppt-master。功能：以 python-pptx 生 PowerPoint） |
| 2026-06-05 | book-to-skill | github.com/virgiliojr94/book-to-skill | virgiliojr94 | 否 | 🟥 跳過（一次性 generator，用時再拉） |

_由 `skill-curator` 維護。新評估在當日本機工作日誌完成後，把中性一列同步到這裡。_
