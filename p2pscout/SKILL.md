---
name: p2pscout
description: >
  跨多個索引來源搜尋 BitTorrent 資源,依實測可下載性(分散式雜湊表 + 追蹤伺服器,可選握手驗證)排序,
  挑出現在真的抓得到的那一筆。當使用者要「找某資源的種子 / 磁力連結」、「確認資源還活著」、
  或「下載前先驗證可下載性」時使用。本工具不傳輸資料 —— 下載交給 aria2。
---

# p2pscout — agent 使用指南

跨多來源搜尋,依**實測**可下載性排序。索引自報的種子數常過期或灌水,p2pscout 自己探測 swarm:
分散式雜湊表查詢、追蹤伺服器查詢,並可選擇真的握手、讀取對等節點的位元欄位來確認它持有所有分塊。

## 何時呼叫

- 使用者要「找 X 的種子 / 磁力連結」、「X 還有人做種嗎」。
- 下載前要確認資源是否真的活著。
- **不要**用於:抓任意網址、傳輸非種子內容。傳輸由 `p2pscout get` 委派 aria2。

## 前置

需本機有 Go 1.25+。**無需手動建置** —— 直接用 `go run` 呼叫(首次編譯後進快取,之後即時)。
所有指令都從**本技能目錄**(這份 SKILL.md 所在的資料夾)執行,因為 Go 原始碼就在這裡。
`get --auto` 另需 aria2c 以遠端程序呼叫模式執行。

## 呼叫

從本技能目錄執行(把 `<query>` 換成關鍵字):

```sh
go run ./cmd/p2pscout <query>                      # shallow:多來源 + 可下載性排序(數秒)
go run ./cmd/p2pscout --full <query>               # full:加握手驗證(數十秒)
go run ./cmd/p2pscout --json <query>               # 機器可讀;腳本請用這個
go run ./cmd/p2pscout --providers apibay,torrentz2 <query>   # 指定來源(逗號分隔,或 all)
go run ./cmd/p2pscout get --auto --aria2-secret=TOKEN --dir ~/Downloads <query>
```

> 想要常駐 binary 免每次編譯:`go build -o p2pscout ./cmd/p2pscout` 後改用 `./p2pscout <query>`。

| flag | 預設 | 意義 |
|------|------|------|
| `-n, --limit` | 20 | 每個提供者最多取幾筆 |
| `--providers` | all | 逗號分隔的提供者,或 `all` |
| `--full` | false | 加握手驗證(慢但能證明可下載) |
| `--json` | false | 輸出 JSON |
| `-v, --verbose` | false | 加上索引自報的種子/對等節點數 |
| `--timeout` | 90s | 整體預算 |
| `--concurrency` | 4 | 同時探測幾筆 |

## 判讀

- `verdict=downloadable`(僅 full 模式):現在抓得下來,推薦排名第一。
- `verdict=live`:有對等節點但未經握手確認(或 shallow 模式)。要下載前先跑 `--full`。
- `verdict=dead`:找不到任何對等節點,別推薦。
- `--json` 的 `score` 已降序排序;`magnet` 欄可直接交給種子用戶端或 `p2pscout get`。

## 下載委派

`p2pscout get <query>` 會自動啟用 `--full`,挑判定為 `downloadable` 的最高分項目。
若已知確切資源,用 `p2pscout get --magnet "<magnet>"` 跳過搜尋、直接驗證該 magnet。
`--magnet -` 則從標準輸入讀 magnet,便於管道串接(上游只負責吐 magnet、本工具負責驗證下載,彼此不相依):
`p2p-ranking-board get <id> | p2pscout get --magnet - --auto`。

行為:
- 不帶 `--auto`:只印磁力連結,不下載(讓使用者決定)。
- 帶 `--auto`:呼叫 aria2 遠端程序呼叫排入下載,印出工作識別碼。
- 最高分非 `downloadable`:拒絕排入,回明確訊息。
- aria2 沒在跑 / 連不上:回明確錯誤(`is aria2c running with --enable-rpc?`),不靜默失敗。

## 失敗模式

- 無結果:非零退出 `no results`。換關鍵字。
- 網路阻擋 UDP:分散式雜湊表退化為零;追蹤伺服器加握手仍可用,排序壓縮但仍有意義。
- `torrentz2` 改版:該提供者回零筆,需更新解析。其他提供者不受影響。

## 別做

- 別在密集迴圈裡跑(每次都加入分散式雜湊表、開大量連線),一個查詢跑一次。
- 別把磁力連結直接餵下載器而不給使用者看 —— 他們可能要挑非第一名。
- 別用表格輸出做下游解析,用 `--json`。
