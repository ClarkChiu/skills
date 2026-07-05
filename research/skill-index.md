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
| 2026-06-02 | dev-builder | github.com/zinohome/cozyengine（.agent/skills 4-skill 同源包） | zinohome | 是（原生 scaffold＋design-gate＋frontend-design 已涵蓋） | 🟥 跳過（通用前端 web persona；源 0★單人、無授權、SKILL.md 無 frontmatter、教 agent 自動裝包；對使用者專長領域無缺口） |
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
| 2026-06-11 | chubbyskills（整包合集，11 技能） | github.com/chubbyguan/chubbyskills | chubbyguan（chubby） | 否（無「媒體→轉錄→知識庫」簇） | 🟥 跳過（媒體轉錄→Obsidian 知識庫工具組；多數綁中國平臺與簡體輸出，與本專案 zh-TW＋Claude 棧對位有限；工程為 yt-dlp＋whisper 薄包裝可自製。日後若建 Muse 入庫技能可參考其管線形狀。完整稽核見當日本機紀錄） |
| 2026-06-11 | SkillSpector（技能安全掃描 CLI，非技能） | github.com/NVIDIA/SkillSpector | NVIDIA | 否（與 `skill-auditor` 互補：它是確定性工具層，auditor 是 LLM 判斷層） | 🟩 直接裝（比照 rtk 前例作外部 CLI 工具：記 README 外部 CLI 說明、不進 apm.yml；釘 commit、uv 隔離安裝。已接進 skill-auditor 當選用靜態前置） |
| 2026-06-12 | UZI-Skill（股票深度分析） | github.com/wbh604/UZI-Skill | wbh604 | 否（無投資分析簇） | 🟦 參考自製（同日重評：使用者補充有被動指數投資並考慮自製台股／美股版。不裝——A股／簡體／主動選股面向不對位；但人格資料化、適配閘門、分布式輸出、按維度抓取的管線是可參考的架構。詳見當日本機日誌） |
| 2026-06-12 | orange-line-illustration（紐約客風插畫） | github.com/orange2ai/orange-line-illustration | orange2ai | 否（slide-deck／social-card 風格家族未含插畫軸） | 🟦 參考自製（純 prose 風格系統；自訂商用授權不宜收錄檔案，原則可作日後 social-card／slide-deck 的自寫風格預設；非急件） |
| 2026-06-12 | hermes-graphiti-plugin（Hermes 記憶外掛） | github.com/p1s4/hermes-graphiti-plugin | p1s4 | 否（本專案無記憶簇） | 🟦 參考自製（屆時）（graphiti 接 Hermes 的薄包裝，出處單人短史；Muse 記憶層動工時自寫並參考其介面形狀，詳見當日本機稽核） |
| 2026-06-12 | graphiti（時間性知識圖譜框架，非技能） | github.com/getzep/graphiti | getzep（Zep） | 否（框架非技能） | 🟥 跳過（現階段）（成熟活躍、出處強；是 Muse 第二大腦記憶層的首選候選引擎，屆時再正式評估安裝） |
| 2026-06-12 | hermes-skill-registry（技能市集平臺） | github.com/Debarpan08/hermes-skill-registry | Debarpan08 | 部分（skill-finder 的發現角色） | 🟥 跳過（社群市集＋評分安裝的姿態與本專案安全評估流程相反；無授權條款；出處極早期） |
| 2026-06-14 | renwei-writing（人味寫作） | github.com/orange2ai/renwei-writing | orange2ai（橘子 & Cola） | 部分（重複 humanizer 語氣層） | 🟦 參考自製（編輯時保留作者人味的減法紀律；純 prose＋自訂商用限制授權不宜收錄＝萃取原則併入 `humanizer` 當「保留作者」護欄，不新建技能。資安純 prose SAFE；435★/6commit 極新。詳見當日本機日誌） |
| 2026-06-14 | effective-html（html／html-diagram／html-plan 三技能） | github.com/plannotator/effective-html | plannotator | 部分（html≈web-artifacts-builder/slide-deck；html-plan≈design-gate；html-diagram 為缺口） | 🟨 收錄＋客製（選擇性 vendor html-effectiveness 參考庫＋架構圖能力；MIT＋內嵌 Apache-2.0 可收錄。聚焦真缺口〔架構圖／有效技術 HTML 交付物〕，跳過純重複部分；收錄要補 attribution〔指向 plannotator 與原始 thariqs/html-effectiveness〕＋sources.lock。資安純 prose 無腳本 SAFE；755★。先 design-gate 設計再動工） |

| 2026-06-17 | ponytail | github.com/DietrichGebert/ponytail | DietrichGebert | 部分（重複 CLAUDE.md §2 Simplicity First＋§3 Surgical Changes 之常駐規則；為 caveman→`terse` 的程式碼極簡手足） | 🟦 參考自製（「懶惰資深工程師」程式碼極簡階梯：YAGNI→stdlib→原生→已裝相依→一行→最小可行；純 persona prose，兩個每回合 Node hook 僅旗標檔＋statusline 屬邊陲。資安 SAFE、MIT、v4.7.0 活躍。核心規則已被使用者全域 CLAUDE.md 每階段常駐涵蓋＝觸發式技能反而更弱；取三點加值〔明確階梯／`ponytail:` 捷徑註解慣例／非平凡邏輯留一個可跑檢查〕併進 CLAUDE.md §2/§3，或仿 terse 之於 caveman 建小技能。優先度低，不裝外掛） |
| 2026-06-21 | jianying-editor-skill（剪映自動剪輯） | github.com/luoluoluo22/jianying-editor-skill | luoluoluo22 | 否（無內建影片編輯） | 🟥 跳過（以 UI 自動化驅動中國版剪映 Pro 做端到端剪輯〔配音／字幕／特效／螢幕錄製／自動匯出〕，需 Windows＋舊版剪映 5.9＋中國版專屬 App，離使用者網路／系統守備；2k★／MIT／結構完整／單人。完整稽核見當日本機紀錄） |
| 2026-06-21 | daed（dae eBPF 路由引擎 Web 儀表板，非技能） | github.com/daeuniverse/daed | daeuniverse | 否（應用程式非技能；本專案無對應簇） | 🟥 跳過（現階段）（dae 的 eBPF 核心層分流技術對位使用者網路專長，但 daed 是 TS Web 儀表板、無可萃取技能素材；要用直接裝即可、不需技能中介。前端 MIT／後端 AGPL-3.0。日後若需 dae 設定／分流規則撰寫助手再評估自製，比照 graphiti 前例） |

| 2026-06-28 | 每日待辦日報提示（AI Chief of Staff／CEO brief／艾森豪矩陣類） | promptmagic.dev／tomsguide.com／github.com/0x2e-Tech/awesome-ai-prompts | 多方（廣傳 prose 提示，無單一正典） | 內容為缺口；送達層重疊內建 schedule/loop，優先級與 decision-lens Crux 相鄰但不同 cadence | 🟦 參考自製（最有名者皆純文字提示、無可維護正典；價值在優先級框架〔艾森豪為主＋Eat-the-Frog 排序〕＋日報輸出結構，複製成本≈0。強客製需求〔多語／PM 風格／與 schedule＋decision-lens 整合〕＝自製。送達用內建 schedule 不重造。語言：英文引擎＋輸出跟隨輸入語言，比照 decision-lens） |
| 2026-06-28 | OpenPaw（daxaur/openpaw） | github.com/daxaur/openpaw | daxaur | 部分（個人助理套件含 daily briefing；送達層重疊內建 schedule） | 🟥 跳過（38 技能個人助理套件，daily briefing 僅其一；含 Telegram／排程／kanban 整合，價值在整合非提示。為單一日報提示裝整套不划算；~107★ 未驗證、單人。取其日報觀念自製即可） |
| 2026-06-28 | geoffrey morning-briefing（krishagel/geoffrey） | github.com/krishagel/geoffrey | krishagel | 部分（morning briefing 整合行事曆/Email） | 🟥 跳過（訊號不一致：第三方市集頁稱已上線，原 repo 自稱「尚未實作、Phase 2 roadmap」；Bun CLI＋AppleScript/JXA 綁 macOS，與使用者 Linux/GCP 不合。~5★、MIT、單人。安裝前須核實程式） |
| 2026-06-28 | DailyBrief（leiting-eric/DailyBrief） | github.com/leiting-eric/DailyBrief | leiting-eric | 否（不同需求） | 🟥 跳過（AI 每日「新聞」簡報：GitHub 熱門＋行情技術分析，非個人待辦日報＝離題。~266★ 未驗證、TS／MIT、活躍，但需求不符） |
| 2026-06-28 | morning-digest（mshadmanrahman/morning-digest） | github.com/mshadmanrahman/morning-digest | mshadmanrahman | 部分（行事曆/Email/Slack/待辦合成晨報；送達層重疊 schedule） | 🟥 跳過（最貼近「個人晨間整合」，但價值在程式整合〔需串接各服務授權〕、~5★ 單人 Python。提示觀念自製、整合用內建 schedule） |

| 2026-06-28 | CLAUDE.md 自我稽核去重流程（bnext 90421，slug 誤標 code-fix） | bnext.com.tw/article/90421/claude-cowork-code-fix | 數位時代（文章，非 repo） | 是（內建 /memory＋schedule；既有 skill-evolve 同款週期偵察骨架） | 🟥 跳過（正文非 debug，是 CLAUDE.md 設定稽核去重：5 條判準揪重複/衝突/冗餘＋週期排程。純 prose＋內建排程，無可重現工程；排程被內建 schedule 涵蓋；使用者已手動在做〔d64bafd〕；skill-evolve 已是自我資產週期偵察者。不需建技能，最多存一段薄提示或小幅擴 skill-evolve 視野到 CLAUDE.md） |
| 2026-06-28 | claude-token-optimizer（nadimtuhin） | github.com/nadimtuhin/claude-token-optimizer | nadimtuhin | 部分（CLAUDE.md/context 稽核壓縮，與內建 /memory 相鄰） | 🟥 跳過（cto audit/compress/prune CLI 宣稱省 90% token；單人 481★、--break-system-packages 類自動裝＝安裝面要警覺。純 prose 路徑自寫即可，不裝；要裝須先 skill-auditor，本次未稽核） |

| 2026-07-02 | html-ppt-skill | github.com/lewislulu/html-ppt-skill | lewislulu | 是（slide-deck） | 🟥 跳過（範本驅動 HTML 簡報＋演講者模式；與 slide-deck 同域，範本依賴 CDN 與零資產原則相斥、渲染綁 macOS、內容簡體。演講者模式工程為日後可參考增量，MIT） |
| 2026-07-02 | baoyu-skills（整包 21 技能） | github.com/JimLiu/baoyu-skills | JimLiu（宝玉） | 部分 | 🟥 整包不裝＋逐項挖（MIT、37 貢獻者、活躍，出處強；多數綁簡體／中國平臺或需操控已登入瀏覽器；圖像類重精選資料。逐項裁決見下與本機日誌） |
| 2026-07-02 | baoyu-translate | github.com/JimLiu/baoyu-skills | JimLiu（宝玉） | 否 | 🟦 參考自製（三段式翻譯法〔初翻→自我批評→精翻〕純文字可自寫，改鎖 EN↔zh-TW＋臺灣用語、下游接 chinese-typography；使用者雙語技術寫作高對位） |
| 2026-07-02 | baoyu-url-to-markdown | github.com/JimLiu/baoyu-skills | JimLiu（宝玉） | 否 | 🟥 跳過（現階段）（自建 fetch＋站點配接器工程紮實；Muse 入庫管線動工時再正式評估，比照 graphiti 前例） |
| 2026-07-02 | guizang-ppt-skill | github.com/op7418/guizang-ppt-skill | op7418（歸藏） | 是（slide-deck） | 🟦 參考自製（低優先）（與 slide-deck 同域不裝；AGPL-3.0 不宜收錄檔案；可自寫其「版式登記表＋靜態校驗器」約束式品管原則進 slide-deck） |
| 2026-07-02 | huashu-design | github.com/alchaincyf/huashu-design | alchaincyf（花叔） | 部分（ui-design-advisor／slide-deck／內建 pptx） | 🟦 參考自製（風格顧問與簡報鏈重複既有管線；MIT；真缺口對位＝時間軸動畫→MP4/GIF 匯出鏈，列為日後 IG 影片技能候選參考；品牌資產協議原則可挑進 ui-design-advisor） |
| 2026-07-02 | frontend-slides | github.com/zarazhangrui/frontend-slides | zarazhangrui | 是（slide-deck） | 🟦 參考自製（低優先）（與 slide-deck 同域、CDN 字型路線與零資產原則相斥，範本庫不收；MIT、出處強；可挑「機讀選型索引＋漸進揭露＋3 預覽先看再選」機制進 slide-deck） |
| 2026-07-02 | agency-agents（233 人格合集） | github.com/msitarzewski/agency-agents | msitarzewski | 部分（工程紀律簇重疊 design-gate／systematic-debugging／verify-before-done＋內建 code-review） | 🟥 跳過（人格定義合集非技能；厚實的工程／資安／測試簇正是使用者本人守備、行銷簇較薄；MIT、治理成熟；日後可單檔參考自寫） |

| 2026-07-03 | qiaomu-anything-to-notebooklm | github.com/joeseesun/qiaomu-anything-to-notebooklm | joeseesun（向陽喬木） | 否（無「內容→NotebookLM 入庫」簇；與擱置的 Muse 入庫線相鄰） | 🟥 跳過（多源內容→NotebookLM 生成〔播客/PPT/心智圖/測驗〕；核心 NotebookLM 整合為薄包裝〔引擎在外部 notebooklm-py〕，實質工程集中在中國平臺內容擷取〔微信/小宇宙/飛書/得到〕，深綁簡中生態＋平臺帳號依賴、與使用者守備低相關；安裝面較重。5467★、MIT、單人 11 commit 3 月。Muse 入庫線動工時直接評估 notebooklm-py／graphiti，非此包裝） |
| 2026-07-03 | html-ppt-skill／baoyu-slide-deck／frontend-slides／huashu-design／guizang-ppt-skill／ppt-master（重貼） | 見 2026-07-02 各列 | 多方 | 見各列 | ♻️ Recall：六者於 2026-07-02 已評估或早已追蹤（前五者見上方 07-02 列；ppt-master 為 slide-deck 蒸餾來源、在其 sources.lock 追蹤、非安裝候選）。簡報機制已榨完，無上游改動故不重評 |

| 2026-07-03 | darwin-skill | github.com/alchaincyf/darwin-skill | alchaincyf（花叔） | 部分（skill-evolve／內建 skill-creator） | 🟦 參考自製（技能自我優化流程，9 維評分＋git revert 棘輪；價值在 prose，單人、~2 月、LICENSE 未證實） |
| 2026-07-03 | SkillOpt | github.com/microsoft/SkillOpt | microsoft | 部分（skill-evolve／內建 skill-creator） | 🟦 參考自製（官方研究框架，方法論參考：有界編輯＋held-out 驗證；非可直接裝的技能，附帶 skillopt-sleep 子技能日後另評） |

_由 `skill-curator` 維護。新評估在當日本機工作日誌完成後，把中性一列同步到這裡。_
