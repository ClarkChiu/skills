# 來源與授權 (Attribution)

## 英文規則（rules-en.md）

原樣收錄自 **blader/humanizer**（MIT 授權，v2.8.0）。
- 儲存庫：https://github.com/blader/humanizer
- 它本身整理自維基百科 **「Signs of AI writing」**（WikiProject AI Cleanup 維護）：
  https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- v2.8.0 再同步（2026-06-08，由 `skill-evolve` 偵測）：新增 #31 製造戲劇感的短句連發、
  #32 格言公式、#33 對話式修辭開場三條痕跡，並擴充 #20 收進「Want me to…?／Should I
  continue?」這類「要不要我繼續」結尾。

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
