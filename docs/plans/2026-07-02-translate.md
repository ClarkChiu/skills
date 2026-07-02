# translate 技能實作計畫

> 依已批准的設計 `docs/specs/2026-07-02-translate-design.md` 拆任務。
> 取捨（沿用 social-card 計畫前例）：程式類任務給完整可跑碼；文字 reference 給**內容規格＋驗收標準**，執行時依規格撰寫。
> 全域約束：純文字技能、零腳本；SKILL.md 與中文向 references 用臺灣繁體；非目標清單（設計 §1）是硬邊界，執行中不得「順手加回」上游功能。

## 任務 1：技能骨架＋SKILL.md

- 建 `translate/SKILL.md`，frontmatter：`name: translate`；`description` 含觸發語（翻譯／快翻／精翻／中翻英／英翻中／translate to Chinese/English／refined translation，並寫明 EN↔zh-TW 雙向、兩模式、Do NOT 用於其他語言對）；`allowed-tools: Read, Write, Edit, Grep, Glob`。
- 正文段落（對應設計 §2–§6 摘要層，細節指向 references）：
  1. 模式表（快翻／精翻）＋觸發規則（預設快翻；整份檔案或約 800 字以上提示建議精翻）＋「繼續精翻」升級（沿用快翻結果當初稿、不重翻）。
  2. 翻譯原則六條（設計 §3，MUST 級：事實一致、程式碼區塊不翻、術語首現附原文）。
  3. 詞彙表權威順序四層（設計 §4）——**只指路**到 `chinese-typography/user-dictionary.json`、`glossary.md` 與本技能 `references/terms-en-zhtw.md`，不複製內容。
  4. 精翻流程一覽＋輸出目錄規則（檔案來源→旁邊 `<basename>-<方向>/`；對話貼文→中間檔進系統暫存區、譯文貼回對話），細節指 `references/refined-workflow.md`。
  5. 長文策略（先全篇分析建術語表→分節翻→批評步兜底）＋天花板註記（幾萬字級再評估 Python 分塊）。
  6. 完成時下游建議（zh-TW→建議 chinese-typography 正規化；發表→humanizer）＋邊界宣告（翻譯腔歸本技能、AI 腔歸 humanizer）。
- **驗收**：frontmatter 三欄齊；MUST NOT（批評步不動筆）字樣出現；無 EXTEND.md／分塊腳本／子代理字樣。
- 驗證：`head -20 translate/SKILL.md`（frontmatter）；`grep -c "MUST" translate/SKILL.md` ≥ 2；`grep -iL "EXTEND" translate/SKILL.md` 回傳檔名（表示不含）。

## 任務 2：`references/refined-workflow.md`（精翻四步詳則）

- 每步的輸入／動作／輸出檔格式模板：
  - `01-analysis.md`：內容摘要／術語表（全文抽詞＋詞彙層合併結果）／語氣評估／翻譯難點（比喻、雙關、長句，各附建議策略）。
  - `02-draft.md`：初稿；套翻譯原則＋術語表；分節翻譯時逐節標記來源段落錨點。
  - `03-critique.md`：**只診斷**——格式為「問題類別／位置／描述／建議修法」清單＋結尾統計（嚴重 X 項、改善 Y 項）；明文 MUST NOT 內含改寫後全文。批評依方向載入對應清單檔。
  - `04-final.md`：逐項回應批評的最終稿；收尾整篇通讀檢查（敘事一致、節間銜接、術語一致、格式保留）。
- 快翻升級路徑：把既有快翻產出存為 `02-draft.md`（補做 `01-analysis.md` 的術語表段）再進批評步。
- **驗收**：四個檔各有明確模板；「只診斷」約束在 03 段落用 MUST NOT 陳述。
- 驗證：`grep -n "MUST NOT" translate/references/refined-workflow.md` 至少 1 筆落在 critique 段。

## 任務 3：`references/critique-en2zhtw.md`（EN→zh-TW 批評清單）

- 四區塊（設計 §6）：準確性（事實／數字／專有名詞逐段對照、漏譯增譯改義）；翻譯腔（歐化「進行了…」與「…性」名詞化、被動濫用被／由／受到、連接詞堆疊因此／然而／此外、代名詞冗餘、長定語）——每條附一組「壞例→改法」；臺灣用語（對照詞彙層、抓軟件／視頻／信息類混入）；排版預檢（只抓大的，正式修正歸 chinese-typography）。
- 檔頭聲明邊界：本清單抓「源語言結構殘留」；AI 生成腔（灌水、三段式、AI 詞彙）歸 humanizer，此處 MUST NOT 收錄該類規則。
- **驗收**：每個翻譯腔條目都有例句；不含任何 humanizer 的 AI 詞彙規則。
- 驗證：`grep -c "→" translate/references/critique-en2zhtw.md` ≥ 5（壞例→改法對）。

## 任務 4：`references/critique-zhtw2en.md`（zh-TW→EN 批評清單）

- 三區塊：準確性（同上）；中式英文（冠詞缺漏、時態單一、主詞懸空、直譯搭配錯誤如 open the light、簡單句串接）——每條附「壞例→改法」；語域（技術寫作慣例：主動語態、動詞優先、砍冗詞、標題大小寫一致）。
- 同樣的檔頭邊界聲明。
- 驗證：`grep -c "→" translate/references/critique-zhtw2en.md` ≥ 5。

## 任務 5：`references/terms-en-zhtw.md`（術語對照表，雙向共用）

- 起始 25–40 條，聚焦使用者領域：網路／協定（signaling→信令、NAT traversal→NAT 穿越、latency→延遲、throughput→吞吐量、packet→封包、router→路由器、switch→交換器、firmware→韌體、bandwidth→頻寬…）、測試自動化（test fixture、flaky test、regression…）、雲端／DevOps（container→容器、deployment→部署、IaC、CI/CD 維持縮寫…）。表格式：`| EN | zh-TW | 備註（但書／不譯場合） |`。
- 檔頭寫維護規則：新詞先查 `user-dictionary.json` 與 `glossary.md`（它們凌駕本表）；兩處都沒有才加這裡。
- **驗收**：≥25 條；含 signaling→信令；權威順序聲明在檔頭。
- 驗證：`grep -c "^|" translate/references/terms-en-zhtw.md` ≥ 27（表頭 2＋條目 25）。

## 任務 6：`references/attribution.md`＋`translate/sources.lock`（成對）

- attribution 照 `tdd/references/attribution.md` 結構：上游 `JimLiu/baoyu-skills` → `skills/baoyu-translate`（MIT）、**方法改寫零檔案收錄**、評估指向 `research/audits/2026-07-02-baoyu-skills.md`（🟦）。「改了什麼」：三模式砍成兩模式（普通模式併入升級路徑）；EXTEND.md／bun 分塊腳本／子代理平行／圖片語言檢查全部不帶；目標語 zh-CN→zh-TW＋雙向；批評清單方向化並與 humanizer 畫界；詞彙表接進 chinese-typography 用詞層。Re-sync 指引：skill-evolve 時挖上游批評維度與流程改進，保留本地的兩模式與詞彙接線。
- sources.lock（技能根目錄，照 design-gate 的格式）：`checked_at: 2026-07-02`；source `JimLiu/baoyu-skills`：`ref: main`、`commit: a4e78af8136f`、`date: 2026-07-02`、`license: MIT`、`skills: ["baoyu-translate"]`、note 說明方法改寫非收錄。
- 驗證：兩檔並存（`ls translate/sources.lock translate/references/attribution.md`）；lock 內 commit 與稽核紀錄一致。
- **提交**：`git add translate/ && git commit -m "✨ feat(translate): 自建 EN↔zh-TW 三段式翻譯技能（參考自製自 baoyu-translate）"`

## 任務 7：`evals/evals.json`（六案，對應設計 §8 驗收準則）

照 `terse/evals/evals.json` 格式（`skill_name`／`_note`／`evals[]`，每案 `id`、`name`、`lang`、`prompt`、`expected_output`、`assertions[]`）：

1. `terminology-signaling`：快翻含 signaling 的英文段→「信令」＋首現附原文括號。
2. `refined-produces-four-files`：精翻檔案→01–04 四檔存在，`03-critique.md` 只含問題清單（assertion：不含改寫後全文）。
3. `critique-catches-passive`：被動密集英文精翻→批評點名被動濫用、final 對應句改自然句式。
4. `direction-specific-checklist`：zh-TW→EN 精翻→批評查冠詞／時態（不出現中譯方向的翻譯腔條目）。
5. `upgrade-no-retranslate`：快翻後說「繼續精翻」→不重翻初稿、直接批評（assertion：沿用原稿詞句可辨識）。
6. `code-block-unchanged`：含程式碼區塊的原文→區塊逐位元不變（`deterministic: true`）。

- 驗證：`python3 -c "import json;d=json.load(open('translate/evals/evals.json'));print(len(d['evals']))"` → `6`。
- **提交**：`📝 test(translate): 六案 evals 對應設計驗收準則`

## 任務 8：登錄四件套

1. `apm.yml`：dependencies.apm 的 `- ./daily-brief/` 之後加 `- ./translate/`。
2. `README.md` 自建技能表末尾加一列：名稱連結＋說明（兩模式、批評只診斷、雙向清單、詞彙層接線、與 humanizer 邊界、改寫自 JimLiu/baoyu-skills 方法非檔 MIT）。
3. `skill-curator/references/skill-map.md`：B 簇改為三段管線 `translate (譯) → humanizer (voice) → chinese-typography (typography)`＋新技能條目（含與 humanizer 邊界）；「Boundaries vs built-in」表加一列。
4. symlink：`ln -s /mnt/d/project/skills/translate /root/.claude/skills/translate`。
- 驗證：`grep -n "translate" apm.yml README.md skill-curator/references/skill-map.md | head`；`ls -la /root/.claude/skills/translate`。
- **提交**：`📝 docs(skills): 登錄 translate——apm.yml／README 表／skill-map＋全域 symlink`

## 任務 9：設計與計畫文件入版控

- `git add docs/specs/2026-07-02-translate-design.md docs/plans/2026-07-02-translate.md research/skill-index.md chinese-typography/references/glossary.md`
- **提交**：`📝 docs: translate 設計＋計畫；skill-index 補 2026-07-02 六筆評估；glossary 釘「文字」`

## 完成定義

- [ ] 9 個檔案存在且過各自驗證指令
- [ ] 三處登錄＋symlink 可解析
- [ ] evals 6 案、JSON 可解析
- [ ] attribution＋sources.lock 成對、commit 釘 `a4e78af8136f`
- [ ] 三個提交訊息合 gitmoji＋Conventional、無 Co-Authored-By
