# 批評清單：zh-TW → EN

精翻第三步用。逐段對照原文檢查初稿，只列問題不改寫。

> **邊界**：本清單抓「中文結構殘留在英文裡」的中式英文。AI 生成腔（filler、宣傳腔、AI 詞彙）歸 `humanizer` 的英文側，MUST NOT 在此收錄該類規則。

## 1. 準確性

- 事實、數字、日期、專有名詞逐段與原文對照。
- 漏譯、增譯、改義。
- 術語是否全篇同一譯法、是否符合 `01-analysis.md` 術語表（`terms-en-zhtw.md` 反查）。

## 2. 中式英文（每條附壞例 → 改法）

- **冠詞缺漏**：Open browser and check config → Open the browser and check the config。中文沒有冠詞，逐句補查 a／an／the。
- **時態單一**：Yesterday we deploy the new version → Yesterday we deployed the new version。中文動詞不變形，檢查全篇時態是否照時間線走。
- **主詞懸空（懸垂修飾）**：After restarting the router, the packets were captured → After restarting the router, we captured the packets。
- **直譯搭配錯誤**：open the light → turn on the light；learn knowledge → gain/acquire knowledge；big rain → heavy rain。搭配詞（collocation）逐一存疑。
- **簡單句串接**：全篇都是短句逗號串 → 用從屬子句、分詞結構合併，變化句型。
- **中文語序殘留**：We very much value this → We highly value this；副詞位置照英文慣例。
- **單複數**：中文名詞無複數形，逐句補查可數名詞。

## 3. 語域（技術寫作慣例）

- 主動語態優先；動詞優先於名詞化（make a decision → decide、perform an analysis → analyze）。
- 砍冗詞：in order to → to、due to the fact that → because。
- 標題大小寫全篇一致（sentence case 或 title case 擇一）。
- 語氣直接：技術文件不繞彎，該是指令就用祈使句。
