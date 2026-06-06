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
| 2026-06-02 | product-spec-builder | cozyengine `.agent/skills` 4-skill 同源包（清單真源）；另有更強別套 github.com/deanpeters/Product-Manager-Skills | zinohome（別套：deanpeters） | 部分（官方 PM plugin 已含 spec 生成） | 🟦 參考自製（薄 persona；spec 生成用官方 PM plugin，毒蛇挑洞 persona 自寫；deanpeters 別套授權 CC BY-NC-SA 不宜收錄） |
| 2026-06-02 | dev-builder | github.com/zinohome/cozyengine（.agent/skills 4-skill 同源包） | zinohome | 是（原生 scaffold＋design-gate＋frontend-design 已涵蓋） | 🟥 跳過（通用前端 web persona；源 0★單人、無授權、SKILL.md 無 frontmatter、教 agent 自動裝包；對使用者深水區無缺口） |
| 2026-06-02 | ui-ux-pro-max | github.com/nextlevelbuilder/ui-ux-pro-max-skill（cozyengine 抄一份） | nextlevelbuilder | 部分（frontend-design，但屬上游設計決策層） | 🟨 **已收錄為自建 `ui-design-advisor`**（收資料層 CSV：84 風格／160 色盤／161 推理規則…；逐檔審全 repo PASS、收錄目標🟢LOW；丟 uipro-cli／腳本；⚠️87.6k★/134commit 星數疑慮。另併入 3 個 MIT 資料源見本機日誌） |
| 2026-06-02 | ui-prompt-generator | cozyengine `.agent/skills`（luodashiv5 亦抄） | zinohome | 否 | 🟥 跳過（薄 persona，服務圖生 mockup 小眾流，非使用者需求；設計決策 ui-ux-pro-max 更richer） |
| 2026-06-02 | deep-research | github.com/199-biotechnologies/claude-deep-research-skill | 199-biotechnologies | 是（內建 deep-research） | 🟥 跳過（用內建。功能：多來源網路研究，搜→讀→綜合→附引用） |
| 2026-06-02 | minimax-docx / -pdf / -xlsx | github.com/MiniMax-AI/skills | MiniMax-AI | 是（內建 docx/pdf/xlsx） | 🟥 跳過（用內建。功能：以 python-docx／reportlab／openpyxl 生 Word／PDF／Excel） |
| 2026-06-02 | pptx-generator | github.com/MiniMax-AI/skills | MiniMax-AI | 是（內建 pptx） | 🟥 跳過（用內建 ppt-master。功能：以 python-pptx 生 PowerPoint） |
| 2026-06-05 | book-to-skill | github.com/virgiliojr94/book-to-skill | virgiliojr94 | 否 | 🟥 跳過（一次性 generator，用時再拉） |
| 2026-06-06 | LRC（Loong Recall） | github.com/zhibaiYingChuan/LRC | zhibaiYingChuan | 是（內建記憶＋Grep/Agent 找碼） | 🟥 跳過（MCP server 非 skill；重複內建記憶＋搜尋；授權 NOASSERTION／自訂研究授權；1 週單人未驗；語意核心 GraphCodeBERT 對本使用者邊際） |
| 2026-06-06 | AiToEarn | github.com/yikart/AiToEarn | yikart | 否（內容變現平台，非技能） | 🟥 跳過（創作者內容變現平台，不在使用者守備範圍；需第三方帳號＋社群授權＋機器人式自動互動，封號／信任風險；MIT、18.2k★，但再紅不等於適合） |

_由 `skill-curator` 維護。新評估在當日本機工作日誌完成後，把中性一列同步到這裡。_
