# 來源與授權 (Attribution)

## 英文規則（rules-en.md）

原樣收錄自 **blader/humanizer**（MIT 授權，v3.1.0）。
- 儲存庫：https://github.com/blader/humanizer
- 它本身整理自維基百科 **「Signs of AI writing」**（WikiProject AI Cleanup 維護）：
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- v2.8.0 再同步（2026-06-08，由 `skill-evolve` 偵測）：新增 #31 製造戲劇感的短句連發、
  #32 格言公式、#33 對話式修辭開場三條痕跡，並擴充 #20 收進「Want me to…?／Should I
  continue?」這類「要不要我繼續」結尾。
- v3.0.0 整份換新（2026-09-17，由 `skill-evolve` 偵測、使用者決定）：上游把規則重寫成
  五類 25 條、由強到弱排序；依維基百科現況刪掉「假範圍」與「同義詞輪替」，新增模糊關聯、
  跟不存在的人爭辯、句首重複、限定詞疊太多等痕跡；弱痕跡標「單獨出現不算」。編號全部改變，
  `rules-zh-tw.md` 已按內容重新對應（上游的新舊編號表是從 35 條版本算的，不適用於我們收錄的 33 條版）。
  同時採用到 SKILL.md（原創重述）：強痕跡出現一次就改、不得編造事實、三種回傳方式。
- v3.1.0 同步（2026-10-05，由 `skill-evolve` 偵測）：新增 F 類第 26 條「替讀者重講他早就知道的事」
  （回覆訊息先講決定）；第 25 條從「寫上一版」放寬成「寫文件本身、不寫它要講的東西」（交代做法與來源、
  描述讀者看得到的版面）；第 2 條補上「替讀者解讀剛看完的例子」。`rules-zh-tw.md` 已對應補上這三處。

`sources.lock` 追蹤 blader/humanizer 的版本；上游出新規則時由 `skill-evolve` 提醒重新同步。
**rules-en.md 的規則內容請保持原樣、不要修改**，這樣才能讓 `skill-evolve` 比對上游更新。

## 中文規則（rules-zh-tw.md）

由本專案自寫（清楚簡單的臺灣繁體中文），不是直接翻譯哪一個現成專案。參考了：

- 維基百科「AI 味」整理（經理人）：https://www.managertoday.com.tw/articles/view/71293
- 老編輯 AI 味 5 特徵（數位時代）：https://www.bnext.com.tw/article/90761/how-to-fix-ai-writing-style
- AI 文「假真誠」特徵（數位時代 / LINE TODAY）：https://today.line.me/tw/v3/article/oqPOvYq
- 翻譯腔（維基百科）：https://zh.wikipedia.org/zh-tw/翻譯腔
- 十大常見翻譯腔（VoiceTube）：https://tw.blog.voicetube.com/archives/19126
- 中國網路術語表 ali-words（賦能/抓手/閉環/顆粒度）：https://github.com/justjavac/ali-words
- 為什麼互聯網公司不說人話（網易）：https://www.163.com/dy/article/G6JJQTMR05148UNS.html
- 簡繁地區用詞比較（ByVoid）：https://byvoid.com/zht/blog/region-phrases-comparison-information/
- ChatGPT 破折號習慣（經理人 / 科技新報）：https://www.managertoday.com.tw/articles/view/71260
- 既有繁中 fork 參考結構：kevintsai1202/Humanizer-zh-TW、op7418/Humanizer-zh

註：簡轉繁與地區用詞替換（視頻→影片等）交給 chinese-typography 的 OpenCC s2twp，本 skill 不重複。

## 「保留作者人味」減法紀律（SKILL.md）

SKILL.md 的「改的是 AI 痕跡，不是作者本人」一段，原則參考 **orange2ai/renwei-writing**（人味寫作）：
- 儲存庫：https://github.com/orange2ai/renwei-writing
- 取其核心姿態——「改完之後，那個人還在」：減法優先、把粗糙當風格簽名、保留承載情緒的語助詞、編輯隱形、作者保有最終裁量權。
- 它本身的收尾檢查清單也整理自維基百科「Signs of AI writing」（與 rules-en.md 同源）。
- **原創重述，未逐字收錄**。原因：renwei 為自訂雙授權（閉源商用須付費），不宜把原檔收進本公開儲存庫；且原則用清楚臺灣繁體中文重寫、接進既有 humanizer 管線，貼合本專案。
- 由 `sources.lock` 追蹤其 commit，上游若新增編輯原則由 `skill-evolve` 提醒評估是否併入。
