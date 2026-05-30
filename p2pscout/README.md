# p2pscout

跨多個索引來源搜尋 BitTorrent 資源,依**實測的可下載性**(而非索引自報的數字)排序,讓自動化代理能直接拿到「現在真的抓得到」的那一筆。下載本身交給 [aria2](https://aria2.github.io/)。

合法用途範例:在多個來源間尋找體積最大、來源最健康的 Linux 發行版映像檔、公眾領域資料集、開源軟體散布檔。是否散布特定內容、是否取得授權,由使用者自行負責。

## 特色

- **多來源聚合**:一次查詢平行展開多個提供者(provider),再依資訊雜湊(infohash)去除重複並合併 —— 同一資源在不同來源的種子數、追蹤伺服器自動彙整。
- **分層探測**:`shallow`(分散式雜湊表加追蹤伺服器,數秒)足以批次排序;`full`(再加握手驗證,讀取對等節點的位元欄位)在下載前證明資源真的活著。
- **判讀結論**:每筆給出 `downloadable` / `live` / `dead` 的明確判定,代理可直接據以決策。
- **下載分離**:本工具只負責搜尋、探測、排序;實際傳輸委派給 aria2 的遠端程序呼叫介面。

## 致謝

「不信任自報數字、直接握手讀位元欄位來驗證對等節點」這個概念,啟發自 [`joway/gardener`](https://github.com/joway/gardener)。p2pscout 為從頭獨立實作:多來源聚合與去重、apibay JSON 來源、分層探測與判定皆為本專案自有設計與程式碼。

## 建置

> 需要 Go 1.25 以上。

```sh
cd p2pscout
go build -o p2pscout ./cmd/p2pscout
```

## 使用

```sh
# shallow:多來源搜尋並依可下載性排序(預設,數秒)
p2pscout "ubuntu 24.04"

# full:下載前用握手驗證確認資源真的活著(較慢)
p2pscout --full "ubuntu 24.04"

# 指定來源 / 機器可讀輸出
p2pscout --providers apibay --json "..."

# 挑最健康的交給 aria2(get 會自動啟用 full;非 downloadable 不下載)
aria2c --enable-rpc --rpc-secret=TOKEN &
p2pscout get --auto --aria2-secret=TOKEN --dir ~/Downloads "ubuntu 24.04"

# 驗證指定 magnet(跳過搜尋);'-' 從 stdin 讀,可被管道串接
p2pscout get --magnet "magnet:?xt=urn:btih:..." --auto
some-source | p2pscout get --magnet - --auto
```

未加 `--auto` 時,`get` 只印出磁力連結,不會真的下載。

## 提供者(第一版)

| 提供者 | 性質 | 取捨 |
|--------|------|------|
| `apibay` | 主機後端 JSON 介面 | 直接回資訊雜湊與種子數,不靠網頁解析,最穩,當主力。 |
| `torrentz2` | 元搜尋聚合(網頁解析) | 一次查詢間接涵蓋多個索引,覆蓋廣;但網站改版即失效。 |

兩者失敗模式互補(一個介面化、一個解析網頁;一個單源、一個聚合),跨來源去重後再以實測健康度排序,才是 p2pscout 的核心價值。

## 欄位

| 欄位 | 意義 |
|------|------|
| `verdict` | `downloadable`(full 模式下有確認的做種者)/ `live`(有對等節點但未確認,或 shallow 模式)/ `dead`(找不到任何對等節點) |
| `conf` | 完成握手且持有所有分塊的對等節點數;`-` 表示 shallow 模式未驗證 |
| `dht` | 分散式雜湊表回傳的不重複對等節點數 |
| `trk` | 有回應的追蹤伺服器平均種子數(自報) |
| `score` | 加權健康分數,full 模式由確認做種者主導 |

## 評分

```
score = 15 * 確認做種者數   (僅 full 模式;唯一證明可下載的訊號)
      +  2 * 分散式雜湊表對等節點數
      +  1.5 * 追蹤伺服器平均種子數
      +  時近度(0..1 平手時的微調)
```

## 擴充提供者

實作 `internal/search.Provider`(`Key()` 與 `Find()`),在檔案的 `init()` 裡呼叫 `register(key, factory)`,註冊表、命令列工具與聚合器就會自動發現它。所有回傳的磁力連結必須經 `search.CleanMagnet` 清洗(只保留 udp、http、https 追蹤伺服器,否則底層的 anacrolix/torrent 會當掉)。

## 注意

- 分散式雜湊表的啟動引導為盡力而為;網路阻擋 UDP 時退化成追蹤伺服器加握手。
- `torrentz2` 為網頁解析,網站改版即失效。
- `full` 模式會寫入暫存目錄但**不抓取分塊資料**,結束即清除。真正下載是 aria2 的事。
