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
| 2026-06-06 | Opportunity-Mining-Agent | github.com/whitesungun876/Opportunity-Mining-Agent | whitesungun876 | 否（自架研究應用程式，非技能） | 🟥 跳過，歸用時再拉（從 GitHub 議題挖新創機會的自架全端程式；偏創業窄用途、非當前需求；11★單人未驗；方法可取。Apache-2.0、有模擬模式） |
| 2026-06-06 | Readme.skill (readme-skill) | github.com/study8677/Readme.skill | study8677 | 否 | 🟥 跳過，歸用時再拉（把本機 AI CLI 歷史產成去識別化開發者檔案＋可分享 SVG 海報；虛榮型一次性產生器、非守備範圍；讀全機最敏感 AI 歷史、海報要外流且脫敏屬自我宣告。MIT、132★、v2.5.1 活躍。完整逐檔稽核未做＝裁決跳過） |
| 2026-06-06 | Heartbeat-Like-A-Man | github.com/loryoncloud/Heartbeat-Like-A-Man | loryoncloud | 否 | 🟦 參考自製 → 已建 `solo-think`（OpenClaw 心跳 cron 包：離線時 agent「沒事找事」。對外那半=自主探索/社群巡邏=無監督對外貼文，高形象風險；對內那半=做夢思考/思考佇列/寫 memory，有用。取對內、砍全部對外、OpenClaw→Hermes、簡→臺灣繁體；純頻率＋時段控制、兩層只對內強制（toolsets file＋allowed-tools）。MIT、75★。未在 Hermes 實測） |
| 2026-06-07 | 「20 個 Claude 提示詞」文章 | blocktempo.com/20-claude-prompts-productivity（譯自 @AnatoliKopadze X 討論串） | AnatoliKopadze | 部分（多條被模型原生能力、CLAUDE.md 反對協議、humanizer 涵蓋） | 🟦 參考自製 → 已建 `tutor`（取 #18 費曼＋#20 蘇格拉底：價值在硬規則協定，不釘住模型必破功回開講）與 `roleplay-coach`（取 #9 談判＋#10 面試＋#12 困難對話：真實抵抗＋一回合一句＋開演前誠實閘門＋必做覆盤）。其餘 15 條 🟥 跳過（模型原生能力或低頻一次性，用時臨場下指令）。純文字無程式碼、零資安面；來源無授權聲明（NOASSERTION），未逐字收錄，技能為原創重述掛 MIT。逐條裁定見當日本機日誌 |
| 2026-06-08 | guizang-social-card-skill | github.com/op7418/guizang-social-card-skill | op7418（歸藏） | 與 slide-deck 相鄰不重複（簡報 PDF vs 社群卡 PNG） | 🟦 參考自製（社群卡片圖生成器，HTML→PNG，28 版式/10 主題；原鎖小紅書 3:4＋公眾號 21:9、不發文不管理＝與使用者「管理 IG/FB」雙重落差。資安 SAFE；授權不一致 AGPL/ISC＝不宜 vendor；3077★ 但建立 12 天。取設計系統原則自製：改鎖 IG 4:5 輪播＋LinkedIn、render 改用 agent-browser 取代 playwright。待 design-gate 設計） |
| 2026-06-08 | taste-skill | github.com/Leonxlnx/taste-skill | Leonxlnx | 是（重複 ui-design-advisor → frontend-design 管線） | 🟦 參考自製（純前端登陸頁／作品集的有品味產生器，帶三段刻度〔變化／動態／密度〕；純前端網頁偏離使用者守備、又與既有介面管線同生態位。資安無虞（已查主技能＋skill.sh＝純提示／純查表；12 個變體未逐一開，裁決非安裝故不必）。MIT、37.2k★ 但 4 個月病毒級熱度、單人。整包不裝不收錄；可選擇性把「情境判讀宣告／反預設清單／三段刻度」挑進 ui-design-advisor，低優先） |
| 2026-06-08 | yao-open-skills（整包合集） | github.com/yaojingang/yao-open-skills | yaojingang（姚金剛） | 部分 | 🟥 整包不可裝（內含作者自宣告的故意提示注入樣本＋自肥版權戳記；MIT、3 個月帳號衝 1097★。個別技能裁決見下列。完整稽核見當日本機紀錄） |
| 2026-06-08 | yao-bayesian-skill | github.com/yaojingang/yao-open-skills | yaojingang | 否 | 🟦 參考自製（紮實：1160 行真做 prior odds × 概似比更新＋Beta-Binomial 共軛；本地計算無網路。決策簇首選素材） |
| 2026-06-08 | yao-crux-skill | github.com/yaojingang/yao-open-skills | yaojingang | 否 | 🟦 參考自製（紮實方法：《矛盾論》主／次矛盾診斷＋程式化清晰度評分；本地、無網路） |
| 2026-06-08 | yao-kelly-skill | github.com/yaojingang/yao-open-skills | yaojingang | 否 | 🟦 參考自製（低優先；真 Kelly 公式＋對數成長極大化，需資本配置場景才用） |
| 2026-06-08 | yao-websecurity-skill | github.com/yaojingang/yao-open-skills | yaojingang | 部分（內建資安審查） | 🟦 參考自製（挖 V001–V275 弱點本體 CSV；非主動掃描＝人工逐條＋報告引擎，腳本謹慎） |
| 2026-06-08 | security-test-hskills（codereview／knowledge／techselect 三個） | github.com/yaojingang/yao-open-skills | yaojingang | — | 🟥 不可當技能裝（作者自宣告的故意注入樣本）／🟨 收作 skill-auditor 紅隊測試集（已知答案、標好注入行號，最高價值再利用） |
| 2026-06-08 | yao-gametheory／business／expert／learning-builder／tutorial-skill | github.com/yaojingang/yao-open-skills | yaojingang | 是（重疊 tutor／doc-coauthoring／slide-deck） | 🟥 跳過（gametheory 不解 Nash 均衡；其餘深度多在提示、與既有教學／文件技能重疊） |
| 2026-06-08 | yao-weread／copyright／open-skills-sync | github.com/yaojingang/yao-open-skills | yaojingang | — | 🟥 跳過（weread＝微信讀書付費閘道＋金鑰、CN 平台低相關；copyright＝戳作者版權自肥；sync＝他們 repo 自綁治理工具） |
| 2026-06-08 | mattpocock/skills（整包合集） | github.com/mattpocock/skills | mattpocock（Matt Pocock） | 部分（engineering 簇重疊既有） | 🟥 整包不裝＋逐項挖（120k★、MIT、可信作者、資安 SAFE；走 skills.sh 非 APM。engineering 規劃/除錯簇多重疊 design-gate／systematic-debugging／內建 skill-creator。個別裁決見下列。完整稽核見當日本機紀錄） |
| 2026-06-08 | tdd（mattpocock） | github.com/mattpocock/skills | mattpocock | 否（verify-before-done 只是完成閘門非建構迴圈） | 🟦 參考自製 → **已建 `tdd`**（正向 red-green-refactor 建構法、貼 pytest／協定真 socket；接進 design-gate→tdd→verify 管線） |
| 2026-06-08 | git-guardrails-claude-code（mattpocock） | github.com/mattpocock/skills | mattpocock | 否（無內建對應） | 🟨 收錄＋客製 → **已建 `git-guardrails`**（PreToolUse hook 擋危險 git；錨定強化、放行 --force-with-lease、不擋 master、合併不覆蓋 RTK；17 案測試） |
| 2026-06-08 | caveman（mattpocock） | github.com/mattpocock/skills | mattpocock | 否 | 🟦 參考自製 → **已建 `terse`**（砍內容不砍文法、語言感知，修正 caveman 中文怪腔怪調） |
| 2026-06-08 | to-prd／to-issues／triage（mattpocock） | github.com/mattpocock/skills | mattpocock | 否 | 🟦 參考自製 → **已建 `to-issues`**（計畫→垂直切片 GitHub issue、發布前確認、design-gate 下游；to-prd/triage 暫緩）。grill-with-docs 的 ADR/統一語彙已併進 `design-gate` |
| 2026-06-08 | diagnose／grill-me／write-a-skill 等重疊與 stack 專屬技能（mattpocock） | github.com/mattpocock/skills | mattpocock | 是 | 🟥 跳過（diagnose≈systematic-debugging、grill-me≈design-gate、write-a-skill≈內建 skill-creator；shoehorn/Husky/scaffold＝TS/JS 專屬；zoom-out 瑣碎、安裝器、deprecated／in-progress／personal） |

_由 `skill-curator` 維護。新評估在當日本機工作日誌完成後，把中性一列同步到這裡。_
