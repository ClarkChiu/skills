#!/usr/bin/env python3
"""
normalize.py 的回歸測試 (regression tests).

執行：python3 test_normalize.py
每一條都鎖住一個曾經出錯、或容易再出錯的行為。
"""
import contextlib
import io
import json
import os
import sys
import tempfile
from unittest import mock

import normalize as N
from normalize import normalize


def n(s, **kw):
    kw.setdefault('convert', False)  # 預設關閉 OpenCC，讓測試不依賴外部套件
    out, _ = normalize(s, **kw)
    return out


CASES = [
    # (說明, 輸入, 期望輸出, kwargs)
    ("盤古之白：中英之間補空格", "使用Python3寫程式", "使用 Python3 寫程式", {}),
    ("標點全形化", "他說,對吧?", "他說，對吧？", {}),
    ("引號轉直角", '他說"你好"', "他說「你好」", {}),
    # 這是最重要的回歸：佔位符曾用裸數字，還原時會把內文的數字毀掉。
    ("數字不被佔位符汙染（曾經的嚴重 bug）",
     "我有100台手機跟3.14版,共1000元", "我有 100 台手機跟 3.14 版，共 1000 元", {}),
    ("版本號被保護、後面句點轉全形",
     "版本是2.31.0.然後呢", "版本是 2.31.0。然後呢", {}),
    ("Markdown 有序清單標記不被破壞", "1. 記得設定", "1. 記得設定", {}),
    ("純英文句子不被動到", "This is fine, really.", "This is fine, really.", {}),
    ("--no-punct：半形逗號原地不動、不長出空格",
     "好用多了,推薦", "好用多了,推薦", dict(punct=False, quotes=False, fixes=False)),
    ("冪等：已正規化的文字再跑一次不變",
     "使用 Python 寫程式，很開心。", "使用 Python 寫程式，很開心。", {}),
    ("code span 內的引號不轉", "執行`git -m \"x\"`完成", "執行 `git -m \"x\"` 完成", {}),
    # 雙階段還原：行內 code 含中文時，內部逐字不被 pangu 拆，只有外緣加空格
    ("行內 code 含中文：內部逐字、外緣加空格",
     "執行`會議6月25日`完成", "執行 `會議6月25日` 完成", {}),
    # code 在所有規則跑完後才還原 → casing 碰不到，`github` 不變 GitHub
    ("行內 code 不被 casing 改寫", "看`github`設定", "看 `github` 設定", {}),
    # 對照組：同樣的 github 在 code 外仍會被 casing 正規化
    ("code 外的 github 仍正規化（對照）", "用github跑", "用 GitHub 跑", {}),
    # 省略號曾被句點規則咬成 "。.。"，這是嚴重 bug 的回歸鎖
    ("省略號 ... → ……（台灣六點），不可變 。.。",
     "然後...就這樣", "然後……就這樣", {}),
    ("破折號 -- → ——（中文間）", "就這樣--結束", "就這樣——結束", {}),
    ("純英文省略號不動", "wait... what", "wait... what", {}),
    # 數字+中文日期/時間單位：使用者偏好「加空格」(與 zhlint skipZhUnits 慣例相反)
    ("數字+中文單位仍加盤古之白（使用者偏好）",
     "我5月要去,共12時30分", "我 5 月要去，共 12 時 30 分", {}),
    ("專有名詞大小寫 github→GitHub、ios→iOS",
     "用github跑在ios上", "用 GitHub 跑在 iOS 上", {}),
    ("全形英數 → 半形", "全形ＡＢＣ１２３", "全形 ABC123", {}),
    ("--no-casing 關閉大小寫", "用github", "用 github", dict(casing=False)),
    # 網址／email／路徑在 pangu 前就還原，曾被之後的 casing 改寫（2026-10-22：
    # max-api.maicoin.com/api/v3 → max-API.maicoin.com/API/v3，網址就壞了）。
    ("網址不被大小寫規則改寫",
     "[MAX 公開 API](https://max-api.maicoin.com/api/v3/currencies)",
     "[MAX 公開 API](https://max-api.maicoin.com/api/v3/currencies)", {}),
    ("email 不被大小寫規則改寫", "寄到api@example.com", "寄到 api@example.com", {}),
    ("路徑不被大小寫規則改寫", "設定檔在config/api/settings.json",
     "設定檔在 config/api/settings.json", {}),
    # 沒有 https:// 的網域、底線變數名不在保護片段裡，casing 只擋了前面的句點
    # （2026-10-22：06 號報告的 open.er-api.com 被改成 open.er-API.com）。
    ("網域名稱裡的 api 不被改大寫", "改用open.er-api.com的匯率",
     "改用 open.er-api.com 的匯率", {}),
    ("底線變數名裡的 api 不被改大寫", "把api_key填進設定", "把 api_key 填進設定", {}),
    # 空白清理曾把行首縮排一起壓成一格，巢狀清單就變成同一層（2026-10-22）。
    ("巢狀清單的行首縮排保留",
     "- 第一層\n  - 第二層\n    - 第三層", "- 第一層\n  - 第二層\n    - 第三層", {}),
    ("行首以外的連續空白照樣壓成一格（對照）", "  中文  與   空白", "  中文 與 空白", {}),
    # 網址樣式遇到逗號就停，查詢字串 usd,twd 的逗號被轉成全形，連 Markdown 連結的
    # ]( ) 也一起變全形，整條連結失效（2026-10-22，06 號報告的 CoinGecko 連結）。
    ("網址裡的逗號不轉全形",
     "[價格](https://x.com/p?c=usd,twd)、[幣種](https://x.com/q)",
     "[價格](https://x.com/p?c=usd,twd)、[幣種](https://x.com/q)", {}),
    ("網址後面的逗號仍當標點（對照）", "見https://example.com/a,然後再看",
     "見 https://example.com/a，然後再看", {}),
    # CJK 字元類別最後一段的起點 U+F900 被 NFC 正規化成同形的 U+8C48，範圍變成
    # U+8C48–U+FAFF，把韓文和私用區（哨符）都當成漢字（2026-10-22）。韓文地名要原樣
    # 才查得到地圖；括號裡只有被保護的 email 時，哨符也不該讓括號變全形。
    ("韓文地名裡的數字不補空格", "→ 토산2리마을회관 前", "→ 토산2리마을회관 前", {}),
    ("韓文外的半形括號不轉全形", "到「화순환승정류장(안덕농협)」",
     "到「화순환승정류장(안덕농협)」", {}),
    ("括號裡只有 email 時不轉全形", "作者：Alex (alex@example.com)",
     "作者：Alex (alex@example.com)", {}),
    # 標點規則用 \s* 吃空白，連換行一起吃：標題、分隔線、下一段被併成一行（2026-10-22，
    # 分析專案有 6 份筆記因此少行）。標點轉換不可跨行。
    ("Markdown 分隔線不被併成破折號", "## 標題\n\n---\n\n內容", "## 標題\n\n---\n\n內容", {}),
    ("下一行開頭的標點不把兩行併起來", "第一行中文\n:第二行", "第一行中文\n：第二行", {}),
    ("西文縮寫句點不轉 。（Fig./e.g.）",
     "見Fig.3跟e.g.這個", "見 Fig.3 跟 e.g.這個", {}),
    # 個人字典：權限最高，逐字替換凌駕一切
    ("個人字典 replacements 蓋過規則",
     "敝公司很棒", "本團隊很棒", dict(user_dict={"replacements": {"敝公司": "本團隊"}})),
    ("逐字替換長鍵先套：短鍵寫在前面也不會把長鍵咬掉半截",
     "快快閃記憶體儲器", "快閃記憶體",
     dict(user_dict={"replacements": {"快快閃記憶體儲": "快閃記憶體",
                                      "快快閃記憶體儲器": "快閃記憶體"}})),
    ("個人字典 formal_tai 覆寫預設→臺",
     "在台北", "在臺北", dict(user_dict={"formal_tai": True})),
    # s2twp 漏掉的台灣在地用詞修正（defaults.json，OpenCC 之後套用；輸入用已轉繁形）
    ("賬→帳（撞 Beancount 記帳）", "記賬", "記帳", {}),
    ("vocab_fixes 攝像頭→攝影機", "攝像頭", "攝影機", {}),
    ("vocab_fixes 不誤傷 識別證（只收人臉識別）", "員工識別證", "員工識別證", {}),
    # 祕（2026-10-05 使用者選定，依教育部標準；上游 OpenCC 已從 TWVariants.txt 移除 祕→秘，
    # 凍結的 0.1.7 仍吐 秘）。always_fixes 先把 秘 一律轉 祕，vocab_fixes 再把音譯字
    # 祕魯 改回 秘魯。不能用「秘魯→秘魯」同字鍵保護：_apply_map 每個鍵都重掃全文，
    # 長鍵先套擋不住後面的短鍵。
    ("秘→祕：秘書", "秘書處", "祕書處", {}),
    ("秘→祕：神秘", "很神秘", "很神祕", {}),
    ("秘→祕：便秘", "便秘困擾", "便祕困擾", {}),
    ("秘魯 是音譯（讀ㄅㄧˋ），維持 秘", "去秘魯旅行", "去秘魯旅行", {}),
    ("秘魯 與 祕 同句：各自正確", "秘魯的神秘遺跡", "秘魯的神祕遺跡", {}),
    ("祕魯 寫錯也改回 秘魯", "祕魯人", "秘魯人", {}),
    ("祕 冪等：已是 祕 的文字再跑不變", "神祕的祕書去秘魯", "神祕的祕書去秘魯", {}),
    # markdown 強調符號：空格補在標記外側，絕不插進標記與內容之間
    ("Markdown 粗體不被撐破（曾經的 bug：**來源** → ** 來源 **）",
     "**來源**：後面的內容", "**來源**：後面的內容", {}),
    ("粗體外側補空格、內側不插：中文**bold**中文",
     "中文**bold**中文", "中文 **bold** 中文", {}),
    ("底線強調同理：中文__bold__中文",
     "中文__bold__中文", "中文 __bold__ 中文", {}),
    ("星號數學式仍有 CJK 邊界空格", "答案是3*4啦", "答案是 3*4 啦", {}),
    # 孤立 NBSP 轉一般空格、連續 NBSP 保留。源自 pangu.js v8.0.0 SOLITARY_NBSP，但上游
    # v8.1.0 已反轉；2026-09-17 使用者決定維持這裡的行為，所以這兩條鎖的是我們自己的選擇。
    ("孤立 NBSP → 一般空格", "中文\u00a0abc", "中文 abc", {}),
    ("連續 NBSP 是刻意版面，保留", "縮排\u00a0\u00a0\u00a0內容", "縮排\u00a0\u00a0\u00a0內容", {}),
    # pangu.js v10 斜線規則（使用者 2026-09-17 選定）：斜線緊貼中文時兩側都不補空格，
    # 原有空格保留。舊的單斜線規則曾把「中文/English」排成單邊空格「中文 /English」。
    ("含中文的路徑不被拆", "/home/用戶/文件", "/home/用戶/文件", {}),
    ("並列分隔符不加空格", "選甲/乙/丙其一", "選甲/乙/丙其一", {}),
    ("中文二擇一斜線貼緊", "上行/下行", "上行/下行", {}),
    ("中英混合斜線不出現單邊空格", "中文/English", "中文/English", {}),
    ("英中混合斜線不出現單邊空格", "English/中文", "English/中文", {}),
    ("原文已有的斜線空格保留", "上行 / 下行", "上行 / 下行", {}),
    ("斜線日期內部不拆、外側照補盤古之白", "截止06/11前", "截止 06/11 前", {}),
    # 以下來自 2026-11-03 的變異測試：這些行為之前沒有測試守住，或只守住一部分。
    # 保護片段分兩階段還原。文字裡同時有行內程式碼和網址／版本號時，還原迴圈若提早結束，
    # 行內程式碼會整段消失（當天試驗的 115 個案例壞了 90 個，原有測試卻全過）。
    ("行內程式碼與網址並存，兩者都還原",
     "看`a.md`跟https://example.com/x 的說明", "看 `a.md` 跟 https://example.com/x 的說明", {}),
    ("行內程式碼與版本號並存，兩者都還原",
     "看`a.md`的2.31.0版", "看 `a.md` 的 2.31.0 版", {}),
    # 全形化：SKILL.md 列出的標點都要有人守。分號、驚嘆號、括號原本沒有測試，
    # 冒號和句點只測到部分情況。
    ("分號轉全形", "好;走", "好；走", {}),
    ("驚嘆號轉全形", "太好了!走吧", "太好了！走吧", {}),
    ("冒號轉全形", "注意:走吧", "注意：走吧", {}),
    ("中文後的句點轉全形", "結束了.", "結束了。", {}),
    ("含中文的括號轉全形", "這是(範例)喔", "這是（範例）喔", {}),
    ("單個全形省略號收斂成六點", "等一下…走", "等一下……走", {}),
    ("多個全形省略號也收斂成六點", "等一下………走", "等一下……走", {}),
    ("中文前的半形省略號", "...好的", "……好的", {}),
    ("連打句號轉省略號", "等等。。。好", "等等……好", {}),
    # 彎引號常見於從網頁貼上的文字，原本只測了直引號。
    ("彎雙引號轉直角", "他說“你好”", "他說「你好」", {}),
    ("彎單引號轉雙直角", "他說‘你好’", "他說『你好』", {}),
    ("標點前的空白移除", "好 ,走 。", "好，走。", {}),
    ("括號內側的空白移除", "（ 範例 ）「 你好 」", "（範例）「你好」", {}),
    # 預設值本身就是規則：程式預設 台，個人字典才翻成 臺。
    ("預設 臺→台（未設 formal_tai）", "在臺北", "在台北", {}),
    # 個人字典是權限最高的一層，protect 與 casing 原本完全沒有測試。
    # 要用會被轉換的詞：沒有 protect 時，這句會變成 臺灣大哥大在臺北。
    ("個人字典 protect 保住品牌的 台", "台灣大哥大在台北", "台灣大哥大在臺北",
     dict(user_dict={"formal_tai": True, "protect": ["台灣大哥大"]})),
    # 短詞先抽的話，長詞剩下的 台 會曝露出來被轉成 臺，輸出才會不同。
    ("個人字典 protect 最長優先", "台灣大哥大台北店在台北", "台灣大哥大台北店在臺北",
     dict(user_dict={"formal_tai": True, "protect": ["台灣", "台灣大哥大台北店"]})),
    ("個人字典新增 casing", "用foobar寫", "用 FooBar 寫",
     dict(user_dict={"casing": {"foobar": "FooBar"}})),
    ("個人字典覆寫內建 casing", "用github寫", "用 GITHUB 寫",
     dict(user_dict={"casing": {"github": "GITHUB"}})),
    # protect 詞曾先被換成哨符、才連同程式碼一起抽走，還原程式碼後哨符就留在輸出裡，
    # 原文從此消失，--in-place 還會寫進檔案（2026-11-03）。
    ("protect 詞在行內程式碼裡原樣保留", "見`台積電`的股價", "見 `台積電` 的股價",
     dict(user_dict={"protect": ["台積電"]})),
    # 圍欄外的 台積電v1 會被加空格，所以沒變才證明圍欄有保護到。
    ("protect 詞在圍欄式程式碼裡原樣保留", "```\n台積電v1\n```", "```\n台積電v1\n```",
     dict(user_dict={"protect": ["台積電"]})),
    ("protect 詞在網址裡的程式碼也原樣保留", "`https://a.tw/台積電`", "`https://a.tw/台積電`",
     dict(user_dict={"protect": ["台積電"]})),
    # 程式碼外面照舊要擋住規則：沒有 protect 時 台灣 會被改成 臺灣。
    ("protect 詞同時在程式碼內外，外面照樣不被改",
     "台灣大哥大和`台灣大哥大`", "台灣大哥大和 `台灣大哥大`",
     dict(formal_tai=True, user_dict={"protect": ["台灣大哥大"]})),
    # 詞有包含關係時要先抽長的。短的先被抽走，長的就對不上，沒保護到的 台灣 會被改掉。
    ("protect 詞長的優先", "台灣大哥大", "台灣大哥大",
     dict(formal_tai=True, user_dict={"protect": ["大哥大", "台灣大哥大"]})),
    # 鍵盤打的 " 分不出開頭結尾，只能照順序配。前面多一個 "，後面就全部錯開一格，
    # 「」會括在錯的字上（2026-11-03）。配不起來的行寧可不轉，也不要轉錯。
    ("引句跨行：配不起來的那一行不轉",
     '老師說"今天的作業是\n第一章",還有"第二章"也要看',
     '老師說"今天的作業是\n第一章"，還有"第二章"也要看', {}),
    # 接在數字後面、又沒有開著的引號，才是英吋。
    ("英吋在引句前面", '這台是 19" 機櫃,他說"很重"', '這台是 19" 機櫃，他說「很重」', {}),
    ("英吋在引句後面", '他說"很重",這台是 8" 平板', '他說「很重」，這台是 8" 平板', {}),
    ("兩個英吋都不當引號", '19" 和 23" 機櫃', '19" 和 23" 機櫃', {}),
    # 小數在這一步之前已被抽成哨符，引號前面看不到數字，要查回原文。
    ("小數英吋", '這台是 2.5" 硬碟,他說"很輕"', '這台是 2.5" 硬碟，他說「很輕」', {}),
    # 有開著的引號時，數字後面的 " 是結尾。把它也當英吋，"IPv6" 這類引句就轉不了。
    ("引句以數字結尾不算英吋", '規格是"RFC 5389"，尺寸是 19"', '規格是「RFC 5389」，尺寸是 19"', {}),
    # 編號後面接引句比英吋常見：自家文件換成直引號後有 5 行，英吋 0 行（2026-11-03）。
    ("編號後面的引句不算英吋", '見 §3"兩軸字體"，還有 Phase 4"A 版"',
     '見 §3「兩軸字體」，還有 Phase 4「A 版」', {}),
    # 沒空格時，靠後面的 " 分辨：下一個也接在數字後面，或根本沒有下一個，就是英吋。
    ("沒空格的兩個英吋", '19"和23"機櫃', '19"和 23"機櫃', {}),
    ("沒空格的英吋在引句後面", '他說"很重"，這台是19"機櫃', '他說「很重」，這台是 19"機櫃', {}),
    # 英吋後面緊接著文字時只是猜的。猜了之後又碰到引號，就可能配錯，不如整行不轉。
    ("猜成英吋後又碰到引號：內容以數字結尾",
     'IPv6"RFC 8200"和"RFC 4291"', 'IPv6"RFC 8200"和"RFC 4291"', {}),
    ("猜成英吋後又碰到引號：內容以括號開頭",
     '步驟3"(a)"是 19" 機櫃', '步驟 3"(a)"是 19" 機櫃', {}),
    ("標點後面的英吋不是猜的，後面的引句照轉", '19",他說"很重"', '19"，他說「很重」', {}),
    # Markdown 記號和範圍符號也是標點，接在英吋後面不算猜的（2026-11-04 審查）。
    ("粗體裡的英吋，後面的引句照轉", '**19"** 機櫃,他說"很重"', '**19"** 機櫃，他說「很重」', {}),
    ("連結文字裡的英吋，後面的引句照轉", '[19"](#a) 機櫃,他說"很重"', '[19"](#a) 機櫃，他說「很重」', {}),
    *[(f"英吋範圍用 {c} 連接，後面的引句照轉",
       f'19"{c}27" 機櫃,他說"很重"', f'19"{c}27" 機櫃，他說「很重」', {}) for c in '-~～×'],
    # ’ 也是英文的撇號，曾被一律轉成 』：It’s 變成 It』s（2026-11-04）。
    ("撇號不是引號：字母中間", "It’s fine, don’t worry.", "It’s fine, don’t worry.", {}),
    ("撇號不是引號：後面接中文", "iPhone’s 螢幕很大", "iPhone’s 螢幕很大", {}),
    ("撇號不是引號：空格後面", "the ’90s 音樂", "the ’90s 音樂", {}),
    ("撇號不是引號：字尾", "dogs’ 玩具", "dogs’ 玩具", {}),
    ("彎單引號在彎雙引號裡", "“他說‘你好’”", "「他說『你好』」", {}),
    # 引號裡的撇號不能把引號提早關掉。
    ("引號裡的撇號：字母中間", "‘It’s fine’", "『It’s fine』", {}),
    ("引號裡的撇號：重音字母後面", "‘café’s 菜單’", "『café’s 菜單』", {}),
    ("引號裡的撇號：數字後面", "‘1990’s 音樂’", "『1990’s 音樂』", {}),
    ("引號裡的撇號：空格後面、數字前面", "‘the ’90s 音樂’", "『the ’90s 音樂』", {}),
    # 後面接英文時，要前面也是英文才算撇號。
    ("中文後面的 ’ 是結尾，後面接英文也一樣", "他說‘你好’abc", "他說『你好』abc", {}),
    ("同一行兩組彎單引號各配各的", "‘甲’和‘乙’", "『甲』和『乙』", {}),
    # 配不起來的不轉，和直引號同一個立場。
    ("彎單引號只有開頭：不轉", "他說‘你好", "他說‘你好", {}),
    ("彎單引號後面只有撇號：不轉", "‘It’s", "‘It’s", {}),
    ("彎單引號跨行：不轉", "‘第一\n第二’", "‘第一\n第二’", {}),
    ("引號裡的撇號：版本號後面", "‘Python 3.14’s features’", "『Python 3.14’s features』", {}),
    # 跑第二次結果不能變：第一次留下的 ‘ 不能跨過轉好的 『 配到後面的 ’，
    # 否則對處理過的檔案再跑一次，括錯的引號會默默出現（2026-11-04 審查）。
    ("彎單引號：外層配不到，內層照轉", "‘a ‘b’ c’", "‘a 『b』 c’", {}),
    ("彎單引號：上一條的結果再跑一次不變", "‘a 『b』 c’", "‘a 『b』 c’", {}),
    ("彎單引號：年代撇號配不到老歌的結尾，再跑一次不變",
     "他用 ‘90s 的『老歌』,dogs’ 玩具", "他用 ‘90s 的『老歌』,dogs’ 玩具", {}),
    # 屬性值不是給人讀的文字，引號或空格一動就壞：href="x" 曾變成 href=「x」（2026-11-04）。
    ("HTML 屬性裡的網址", '<a href="https://x.com">連結</a>', '<a href="https://x.com">連結</a>', {}),
    ("HTML 標籤有多個屬性", '<img src="a.png" alt="圖">', '<img src="a.png" alt="圖">', {}),
    ("HTML 屬性裡的中英文不加空格", '<a href="台積電v1">連結</a>', '<a href="台積電v1">連結</a>', {}),
    ("HTML 標籤跨行", '<img\n  src="a.png"\n  alt="圖">', '<img\n  src="a.png"\n  alt="圖">', {}),
    # 這個空格在頁面上看得到，中文和中文之間不該有。
    ("HTML 標籤外緣不加空格", '見<a href="x">連結</a>的', '見<a href="x">連結</a>的', {}),
    ("HTML 標籤旁邊的引句照轉", '他說"你好"<a href="x">連結</a>', '他說「你好」<a href="x">連結</a>', {}),
    ("沒有屬性的標籤旁邊的引句照轉", '他說"你好"<br>她說"再見"', '他說「你好」<br>她說「再見」', {}),
    ("HTML 標籤外面的大小寫照改", '<a href="github">github</a>', '<a href="github">GitHub</a>', {}),
    # 先抽 protect 詞的話，哨符會鎖在標籤裡，原文從此消失（同程式碼那條）。
    ("protect 詞在 HTML 屬性裡原樣保留", '<a title="台積電">連結</a>', '<a title="台積電">連結</a>',
     dict(user_dict={"protect": ["台積電"]})),
    # 先抽標籤的話，哨符會鎖在程式碼裡。
    ("HTML 標籤在行內程式碼裡原樣保留", '見`<a href="x">`的', '見 `<a href="x">` 的', {}),
    # 值裡的 < 和 > 不算標籤的邊界，只算到第一個 > 的話引號會落單或配錯。
    ("HTML 屬性值裡有 >", '<a title="a>b">和<a title="c>d">', '<a title="a>b">和<a title="c>d">', {}),
    ("HTML 屬性值裡有 <", '<a title="a<b" href="x">', '<a title="a<b" href="x">', {}),
    ("HTML 標籤名有冒號、自我關閉", '<xsl:value-of select="a"/>', '<xsl:value-of select="a"/>', {}),
    # 比較式不是標籤，被當成標籤的話裡面就不會處理。曾經連著等號和後面的 > 吞掉好幾段
    # （2026-11-04 審查）。
    ("比較式和等號隔了幾段：整段照常處理", '若 i<n 的話,令k=0。\n\n下一段english混中文,半形.\n\n1 -> 2',
     '若 i<n 的話，令 k=0。\n\n下一段 english 混中文，半形。\n\n1 -> 2', {}),
    ("標籤名後面沒有空白：比較式照常處理", 'a<b，且c=1>d', 'a<b，且 c=1>d', {}),
    ("沒有等號：比較式照常處理", 'x<y 且z>w', 'x<y 且 z>w', {}),
    ("有等號但不是屬性語法：比較式照常處理", 'x<y 且z=1>w', 'x<y 且 z=1>w', {}),
    ("等號後面的值有中文：比較式照常處理", 'i<n m=k，且j>0', 'i<n m=k，且 j>0', {}),
    # 連結目標和標題一動，連結就壞了：[連結](https://x.com "標題") 曾變成
    # [連結]（https://x.com 「標題」）（2026-11-04）。
    ("Markdown 連結：雙引號標題", '[連結](https://x.com "標題")', '[連結](https://x.com "標題")', {}),
    ("Markdown 連結：單引號標題", "[連結](https://x.com '標題')", "[連結](https://x.com '標題')", {}),
    ("Markdown 連結：括號標題", '[連結](https://x.com (標題))', '[連結](https://x.com (標題))', {}),
    ("Markdown 連結：中文檔名", '[說明](./說明.md)', '[說明](./說明.md)', {}),
    ("Markdown 連結：目標有空白要用尖括號", '[說明](<有 空格.md>)', '[說明](<有 空格.md>)', {}),
    ("Markdown 連結：網址裡有括號", '[維基](https://x.com/a_(b) "標題")', '[維基](https://x.com/a_(b) "標題")', {}),
    ("Markdown 圖片", '![圖](./圖片.png "說明")', '![圖](./圖片.png "說明")', {}),
    # 目標要和檔名一字不差：字形修正、盤古之白、個人字典都不能動。
    ("Markdown 連結：目標不做字形修正", '[連結](臺灣.md)', '[連結](臺灣.md)', {}),
    ("Markdown 連結：目標裡的中英文不加空格", '[連結](說明v2.md)', '[連結](說明v2.md)', {}),
    ("Markdown 連結：個人字典只換連結文字", '[文件](文件.md)', '[檔案](文件.md)',
     dict(user_dict={"replacements": {"文件": "檔案"}})),
    # 先抽 protect 詞的話，哨符會鎖在連結裡，原文從此消失（同 HTML 標籤那條）。
    ("protect 詞在連結標題裡原樣保留", '[連結](https://x.com "台積電")', '[連結](https://x.com "台積電")',
     dict(user_dict={"protect": ["台積電"]})),
    # 保護的只有括號這一段，連結文字和前後的文字照常處理。
    ("Markdown 連結文字照常處理", '[中文abc](https://x.com "標題")', '[中文 abc](https://x.com "標題")', {}),
    ("Markdown 連結前後照常處理", '見[連結](https://x.com "標題"),然後"引用"',
     '見[連結](https://x.com "標題")，然後「引用」', {}),
    ("Markdown 連結在括號裡", '(見[連結](https://x.com "標題"))', '（見[連結](https://x.com "標題")）', {}),
    # 不是連結的括號照常轉，保護範圍不能放大到一般文字。
    ("方括號後面的括號有空白：不是連結", '[註](見下方 說明)', '[註]（見下方 說明）', {}),
    ("前面沒有方括號：不是連結", '(https://x.com "標題")', '（https://x.com 「標題」）', {}),
    # 括號裡沒有 . / # : 也沒有標題，多半是一般文字，不能因為前面剛好有 ] 就不排版
    # （2026-11-04 審查）。貼上的文字和 .txt 也會進來，不是每份都是 Markdown。
    ("方括號後面的括號沒有路徑符號：照常處理", '[註](見下方,第3頁)', '[註]（見下方，第 3 頁）', {}),
    ("區間的括號：照常處理", '區間(0,1](含上界),然後abc', '區間(0,1]（含上界），然後 abc', {}),
    ("跳脫的方括號：照常處理", '\\[註\\](他說"你好")', '\\[註\\]（他說「你好」）', {}),
    # 中文後面的 ! 曾被轉成 ！，圖片就變成一般連結，而且不會報錯（2026-11-04 審查）。
    ("Markdown 圖片前面緊接中文", '見下圖![圖](a.png "說明")', '見下圖![圖](a.png "說明")', {}),
    ("Markdown 圖片前面有空格", '見下圖 ![圖](a.png)', '見下圖 ![圖](a.png)', {}),
    ("Markdown 圖片的替代文字照常處理", '見下圖![中文abc](a.png)', '見下圖![中文 abc](a.png)', {}),
    ("驚嘆號後面的方括號不是圖片：照常轉全形", '太好了![註]', '太好了！[註]', {}),
    ("Markdown 連結：目標只有斜線也算路徑", '[說明](文件/說明abc)', '[說明](文件/說明abc)', {}),
    ("Markdown 連結：目標只有井字號也算錨點", '[章節](#第3節)', '[章節](#第3節)', {}),
    ("Markdown 連結：目標只有冒號也算網址", '[信箱](mailto:王小明)', '[信箱](mailto:王小明)', {}),
]

# 需要 OpenCC 才能跑的案例（s2twp 逐行偵測）。缺套件時整段跳過並大聲說，
# 不假裝通過 —— 與 normalize.py 對 OpenCC 缺席的 fail-loud 立場一致。
OPENCC_CASES = [
    # (說明, 輸入, 期望輸出, kwargs)  —— 這裡 convert 預設「開」
    ("簡體輸入照轉（软件→軟體）", "这个软件很好用", "這個軟體很好用", {}),
    ("已是繁體：文件 不被二次轉成 檔案", "請看這份文件", "請看這份文件", {}),
    ("已是繁體：登錄／聲明 不被改成 登入／宣告",
     "登錄資訊與授權聲明", "登錄資訊與授權聲明", {}),
    ("已是繁體：英文本體 不被切成 英文字體（曾經的切詞災難）",
     "英文本體很重要", "英文本體很重要", {}),
    # 偵測器拿 OpenCC 標準繁體判斷簡體專用字，群床峰灶痴粽 的標準繁體是 羣牀峯竈癡糉，
    # 但臺灣用前者（s2tw 原樣保留）。含這些字的繁體行曾被整行重轉，姓氏 范 變 範（2026-10-22）。
    ("已是繁體：含 群 的行不被整行重轉（范 是姓）",
     "社群推薦：查理‧范多倫", "社群推薦：查理‧范多倫", {}),
    ("混排：簡體行照轉、繁體行不動",
     "繁體的文件\n简体的软件", "繁體的文件\n簡體的軟體", {}),
    ("--force-convert 回到整篇轉換（文件→檔案）",
     "請看這份文件", "請看這份檔案", dict(force_convert=True)),
    # opencc-python-reimplemented 0.1.7 的 s2twp 有貪婪比對錯字（BYVoid/OpenCC 1.4.1
    # 已修，但那份修正流不進這個被釘住的套件），補在 data/defaults.json 的 vocab_fixes。
    # 這幾條鎖的是「出貨的預設表真的補上了」，不是「替換機制會動」。
    ("s2twp 貪婪錯字：互联网络 不吐出 網際網路絡", "互联网络技术", "網際網路技術", {}),
    ("s2twp 貪婪錯字：快闪存储器 不吐出 快快閃記憶體儲器（短鍵是長鍵前綴，順序會咬人）",
     "快闪存储器很小", "快閃記憶體很小", {}),
    ("s2twp 貪婪錯字：快闪存储 單獨出現也要對", "快闪存储技术", "快閃記憶體技術", {}),
    ("老挝 官方國名（跟進 OpenCC 1.4.1）",
     "老挝人民民主共和国", "寮人民民主共和國", {}),
    # 網路術語（2026-09-17 使用者選定）：s2twp 留下 掩碼；輸出不含任何鍵，跑兩次結果一樣。
    # 單獨的「組播」「丟包」會撞一般文字，只記在 glossary.md，不在這一層替換。
    ("網路術語 子网掩码 → 子網路遮罩", "设置子网掩码", "設定子網路遮罩", {}),
    ("網路術語 掩碼 → 遮罩（繁體輸入也修）", "網路掩碼長度", "網路遮罩長度", {}),
    ("OpenCC 1.4.2 補的 内存条 → 記憶體模組（凍結版只給 記憶體條）", "换一根内存条", "換一根記憶體模組", {}),
    ("秘→祕 經 OpenCC 後套用：神秘", "神秘的秘书", "神祕的祕書", {}),
    ("秘鲁 經 OpenCC 後仍是 秘魯", "秘鲁首都", "秘魯首都", {}),
    ("Markdown 連結：簡轉繁只轉連結文字，檔名才對得上", "[说明](说明.md)", "[說明](说明.md)", {}),
    ("方括號後面的一般文字照常簡轉繁", "[链接](见下方)", "[連結]（見下方）", {}),
    # 中國用語→臺灣用語（取自 sysprog21/zhtw-mcp 5b385b3d66b1；鍵是凍結版 s2twp 的輸出）。
    # 都是無歧義的完整術語；會撞詞的（回歸、身份、零假設…）記在 glossary.md，不在這一層。
    ("請求頭 → 請求標頭", "设置请求头", "設定請求標頭", {}),
    ("請求頭部 → 請求標頭（長鍵先套，不吐 請求標頭部）", "读取请求头部", "讀取請求標頭", {}),
    ("虛擬現實 → 虛擬實境", "虚拟现实设备", "虛擬實境裝置", {}),
    ("置信區間 → 信賴區間", "95%置信区间", "95% 信賴區間", {}),
    ("置信水平 → 信賴水準", "置信水平为0.95", "信賴水準為 0.95", {}),
    ("協方差 → 共變異數", "协方差矩阵", "共變異數矩陣", {}),
    # 輸出用教育部的 分布。舊的偵測器把共用字 布 當簡體、整行重轉；改成逐字看簡體專用字後才可行。
    ("正態分布 → 常態分布", "服从正态分布", "服從常態分布", {}),
    ("常態分佈 → 常態分布（繁體輸入也統一）", "服從常態分佈", "服從常態分布", {}),
    ("共用字 布、干 不讓繁體行被重轉", "常態分布的文件不受干擾", "常態分布的文件不受干擾", {}),
    ("秘魯 行不被重轉（detector_traditional_ok）", "秘魯的文件", "秘魯的文件", {}),
    ("祕魯 行冪等", "祕魯的文件", "秘魯的文件", {}),
    ("最大似然估計 → 最大概似估計", "最大似然估计", "最大概似估計", {}),
    ("似然函數：引擎吐 似然函式，要 概似函數", "对数似然函数", "對數概似函數", {}),
    ("備擇假設 → 對立假設", "备择假设成立", "對立假設成立", {}),
    ("顯著性水平 → 顯著水準", "显著性水平", "顯著水準", {}),
    ("馬爾可夫 → 馬可夫", "马尔可夫链", "馬可夫鏈", {}),
    ("馬爾科夫 → 馬可夫", "马尔科夫过程", "馬可夫過程", {}),
    ("艾滋病 → 愛滋病", "艾滋病防治", "愛滋病防治", {}),
    ("艾滋 跨詞不誤傷", "方興未艾滋長的產業", "方興未艾滋長的產業", {}),
    ("腦卒中 → 腦中風", "脑卒中患者", "腦中風患者", {}),
    ("靶向治療 → 標靶治療", "靶向治疗药物", "標靶治療藥物", {}),
    ("論文答辯 → 論文口試", "下周论文答辩", "下週論文口試", {}),
    ("新增術語冪等：輸出再跑一次不變",
     "請求標頭、信賴區間、常態分布、馬可夫鏈、愛滋病、概似函數",
     "請求標頭、信賴區間、常態分布、馬可夫鏈、愛滋病、概似函數", {}),
    ("祕 冪等（經 OpenCC）：祕 不會讓偵測器把整行當簡體重轉",
     "神祕的祕書看這份文件", "神祕的祕書看這份文件", {}),
    # 凍結版 s2twp 的錯轉（2026-10-19 實測；上游 OpenCC 已修 高級，#1509，凍結版拿不到）。
    # 鍵是凍結版的輸出，都是無歧義的完整詞；單獨的 高階 不能動（見下一條和 glossary.md）。
    ("高级中学 → 高級中學（凍結版吐 高階中學）", "他在高级中学教书", "他在高級中學教書", {}),
    ("信息安全 → 資訊安全（凍結版吐港式的 資訊保安）", "这门信息安全课", "這門資訊安全課", {}),
    ("笔记本电脑 → 筆記型電腦（凍結版吐 膝上型電腦）", "买了笔记本电脑", "買了筆記型電腦", {}),
    ("字符集 → 字元集", "字符集设置", "字元集設定", {}),
    ("高階主管 不被改成 高級主管（高級／高階不能一律替換）", "高阶主管开会", "高階主管開會", {}),
    ("這四條冪等：輸出再跑一次不變",
     "高級中學、資訊安全、筆記型電腦、字元集", "高級中學、資訊安全、筆記型電腦、字元集", {}),
    # 刻意不收 数字人文→數位人文：這一層沒有詞界線，「數字」＋「人文…」跨小句會被咬。
    # 這條鎖的是「別再把它加回出貨的 defaults.json」（使用者自己的 user-dictionary.json
    # 不在測試載入範圍，那是他的檔案）。理由見 references/glossary.md。
    ("數字人文 不進 defaults.json（跨小句會誤傷）",
     "報表上的數字人文科系的學生未必看得懂", "報表上的數字人文科系的學生未必看得懂", {}),
    # 逐行偵測不可弄丟行結構（2026-11-03 變異測試）。
    ("簡轉繁保留行結構",
     "软件\nhello world\n视频", "軟體\nhello world\n影片", {}),
]


def _write(directory, name, content):
    path = os.path.join(directory, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def _cli(*argv):
    """在同一個行程跑命令列，回傳 (結束碼, stdout, stderr)。"""
    out, err = io.StringIO(), io.StringIO()
    code = 0
    with mock.patch.object(sys, 'argv', ['normalize.py', *argv]):
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                N.main()
        except SystemExit as e:
            code = e.code or 0
    return code, out.getvalue(), err.getvalue()


def _without_opencc():
    # sys.modules 設成 None，import opencc 就會丟 ImportError。
    return mock.patch.dict(sys.modules, {'opencc': None})


def check_opencc_missing_fails_loud():
    # Rule 12：沒轉換就要讓呼叫端知道，不可默默讓簡體溜過去。
    err = io.StringIO()
    with _without_opencc(), contextlib.redirect_stderr(err):
        out, ok = normalize("软件", convert=True)
    return out == "软件" and ok is False and "NOT converted" in err.getvalue()


def check_cli_exits_2_when_conversion_skipped():
    # 命令列參數寫錯時 argparse 也會結束碼 2，所以還要看警告。
    with _without_opencc():
        code, _, err = _cli('--text', '软件')
    return code == 2 and 'NOT converted' in err


def check_unpaired_quote_lines_are_reported():
    # Rule 12：整行不轉的行如果沒有其他改動，連差異都看不到，所以要明說略過幾行。
    skipped, clean = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(skipped):      # 配到最後落單、猜了英吋又碰到引號
        normalize('老師說"今天\nIPv6"RFC 8200"和"RFC 4291"\n他說"很重"', convert=False)
    with contextlib.redirect_stderr(clean):        # 引句配得起來、英吋本來就不轉，都不算略過
        normalize('他說"很重"\n19" 和 23" 機櫃', convert=False)
    return 'NOTE: 2 行' in skipped.getvalue() and clean.getvalue() == ''


def check_unpaired_curly_single_quotes_are_reported():
    # 只有 ‘ 要回報：落單的 ’ 多半是撇號，回報只會是雜訊。
    skipped, clean = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(skipped):
        normalize('他說‘你好\n‘It’s', convert=False)
    with contextlib.redirect_stderr(clean):
        normalize('他說‘你好’\nIt’s fine，dogs’ 玩具', convert=False)
    return 'NOTE: 2 個' in skipped.getvalue() and clean.getvalue() == ''


def check_user_dict_file_loaded():
    with tempfile.TemporaryDirectory() as d:
        data = {"replacements": {"鐳射": "雷射"}}
        return N._load_user_dict(_write(d, 'd.json', json.dumps(data))) == data


def check_user_dict_missing_file_ignored():
    with tempfile.TemporaryDirectory() as d:
        return N._load_user_dict(os.path.join(d, 'none.json')) == {}


def check_user_dict_unreadable_warns():
    err = io.StringIO()
    with tempfile.TemporaryDirectory() as d, contextlib.redirect_stderr(err):
        loaded = N._load_user_dict(_write(d, 'bad.json', '{not json'))
    return loaded == {} and 'unreadable' in err.getvalue()


def check_default_dict_found_by_walking_up():
    with tempfile.TemporaryDirectory() as d:
        nested = os.path.join(d, 'a', 'b')
        os.makedirs(nested)
        path = _write(d, 'user-dictionary.json', '{}')
        with mock.patch.object(N, '__file__', os.path.join(nested, 'normalize.py')):
            return N._find_default_dict() == path


def check_default_dict_absent_returns_none():
    # 假造「檔案都不存在」，不然上層目錄剛好有同名檔，結果就會因機器而異。
    with mock.patch.object(os.path, 'exists', return_value=False):
        return N._find_default_dict() is None


def check_cli_applies_personal_dictionary():
    with tempfile.TemporaryDirectory() as d:
        path = _write(d, 'd.json', json.dumps({"replacements": {"鐳射": "雷射"}}))
        code, out, _ = _cli('--text', '使用Python3的鐳射', '--no-convert', '--dict', path)
    return code == 0 and out.strip() == '使用 Python3 的雷射'


def check_cli_in_place_rewrites_file():
    with tempfile.TemporaryDirectory() as d:
        path = _write(d, 'a.md', '使用Python3')
        # 指定不存在的字典，輸出才不受使用者自己的 user-dictionary.json 影響。
        code = _cli(path, '--in-place', '--no-convert',
                    '--dict', os.path.join(d, 'none.json'))[0]
        with open(path, encoding='utf-8') as f:
            return code == 0 and f.read().strip() == '使用 Python3'


# 需要呼叫內部函式、模擬環境或跑命令列的檢查，寫不成 (輸入, 期望輸出) 的表格。
CHECKS = [
    ("OpenCC 不在：原文不變、回報 False、印警告", check_opencc_missing_fails_loud),
    ("命令列：簡轉繁被跳過時結束碼 2", check_cli_exits_2_when_conversion_skipped),
    ("直引號配不起來：回報略過的行數", check_unpaired_quote_lines_are_reported),
    ("彎單引號配不起來：回報略過的個數", check_unpaired_curly_single_quotes_are_reported),
    ("個人字典：讀得到檔案", check_user_dict_file_loaded),
    ("個人字典：檔案不存在就當空字典", check_user_dict_missing_file_ignored),
    ("個人字典：內容壞掉就警告並忽略", check_user_dict_unreadable_warns),
    ("個人字典：從腳本位置逐層往上找", check_default_dict_found_by_walking_up),
    ("個人字典：找到根目錄都沒有就回傳 None", check_default_dict_absent_returns_none),
    ("命令列：--dict 的個人字典有套用", check_cli_applies_personal_dictionary),
    ("命令列：--in-place 改寫檔案", check_cli_in_place_rewrites_file),
]


def main():
    fails = total = 0

    def check(desc, fn):
        nonlocal fails, total
        total += 1
        ok = fn()
        if not ok:
            fails += 1
        print(f"{'PASS' if ok else 'FAIL'}  {desc}")

    def run(desc, src, want, kw):
        nonlocal fails, total
        total += 1
        got = n(src, **kw)
        ok = got == want
        if not ok:
            fails += 1
        print(f"{'PASS' if ok else 'FAIL'}  {desc}")
        if not ok:
            print(f"      input:  {src!r}")
            print(f"      want:   {want!r}")
            print(f"      got:    {got!r}")

    for desc, src, want, kw in CASES:
        run(desc, src, want, kw)

    for desc, fn in CHECKS:
        check(desc, fn)

    try:
        import opencc  # noqa: F401
        for desc, src, want, kw in OPENCC_CASES:
            run(desc, src, want, {**kw, 'convert': True})
        check("簡轉繁成功時回報 True（逐行與整篇兩條路徑）",
              lambda: normalize("软件")[1] is True
              and normalize("软件", force_convert=True)[1] is True)
    except ImportError:
        print(f"SKIP  OpenCC not installed — {len(OPENCC_CASES) + 1} 條 s2twp 逐行偵測案例未跑")

    print(f"\n{total-fails}/{total} passed")
    raise SystemExit(1 if fails else 0)


if __name__ == '__main__':
    main()
