# ig-reel 技能設計（庫存素材 → IG 9:16 直式短片）

> 2026-07-02。依 `research/2026-06-21-video-editing-projects-for-ig.md` 的研究結論與建議路線實作；記憶 `ig-video-skill-idea` 標記的真缺口（social-card 明寫不做影片）。
> **流程備註**：使用者批次指令「三項依序做完」（＝IG 影片正式動工的明示），離線中自主執行，假設標明、獨立提交可撤銷。

## 1. 目標與範圍

**目標**：把使用者**自己的影音庫存**變成 IG 直式短片（Reel，1080×1920、≤60 秒為預設目標），終端機優先、批次可量產。核心引擎是 **ffmpeg**（系統已在、使用者本行）；auto-editor（剪廢秒）與 whisper（字幕）為**選用外部 CLI**——裝了自動用、沒裝優雅降級，絕不自動安裝（比照 agent-browser／rtk 前例，記進 README 外部 CLI 節）。

**範圍內**：素材盤點（ffprobe）→ 粗剪 → 9:16 重構圖 → 字幕 → 混音 → 合成輸出 → 批次；每支輸出必過 ffprobe 驗證（fail loud）。

**非目標**（硬邊界）：
- **不做一鍵生成**：不抓 Pexels 等網路庫存、不 AI 編題——素材與想法都是使用者的（研究檔核心判斷）。
- 不發文、不排程（與 social-card 同界線；發布屬另案）。
- 不做 HTML 卡片動畫→MP4 線（huashu 路線）——列為日後擴充，先服務實拍庫存這個主需求（YAGNI）。
- 不裝 MoviePy／Remotion：ffmpeg 直驅已夠；範本化量產真的痛了再評估 Remotion（授權注意：個人免費、公司規模付費）。
- 零腳本：全部是 ffmpeg 指令配方（prose recipes），可跑檢查＝每支輸出的 ffprobe 驗證步。

## 2. 管線（六階段，研究檔架構、第 2 格換成掃自己素材夾）

1. **盤點（ingest）**：`ffprobe` 掃素材夾出清單（時長、解析度、橫直、有無音軌），與使用者確認選片與敘事順序。MUST NOT 憑檔名猜內容——不確定就問或抽影格看。
2. **粗剪**：有 auto-editor → 先剪靜音廢秒；沒有 → `-ss/-t` 手動進出點。能 stream copy 就不重編碼。
3. **9:16 重構圖**（決策規則見 references）：直式源→直接縮放；橫式源→二選一：**主體置中裁切**（人物／主體明確）或**模糊墊底**（畫面不可裁：風景、全景、文字畫面）。MUST 問或看畫面決定，不默默裁掉主體。
4. **字幕**：有 whisper → 轉錄出 SRT →校對→燒錄；沒有→使用者給 SRT 或跳過。燒錄樣式有字級地板與**安全區**（Reels 上下 UI 帶：上 ~250px、下 ~420px @1920——與 social-card 9:16 安全區同源）。研究檔提醒：IG 字幕是互動率主力，預設建議加。
5. **混音**：配樂墊底＋人聲時自動壓低（sidechaincompress 或分段 volume）；輸出前 `loudnorm` 響度正規化。
6. **合成輸出**：concat →1080×1920、H.264、`yuv420p`、`+faststart`、30fps、≤60s 提醒（超長警告但不硬擋）。批次＝一份簡單清單（來源、進出點、字幕檔、配樂）跑迴圈。

## 3. 鐵則

1. **素材是使用者的**：任何步驟 MUST NOT 引入外部庫存畫面。
2. **fail loud**：每支輸出跑 ffprobe 驗證（尺寸 1080×1920、時長、音軌存在），不符合就報錯不交付；批次結束回報成功／失敗清單，MUST NOT 靜默跳過失敗項。
3. **字幕在安全區內**、字級不低於地板（1920 高畫布上 ≥48px 級）。
4. **最少重編碼**：剪切能 copy 就 copy，只在濾鏡步重編碼一次。
5. 檔案不進版控：產出寫使用者指定目錄，暫存進系統暫存區。

## 4. 檔案結構與登錄

```
ig-reel/
  SKILL.md                      # 英文（工程主題），description 帶中文觸發語
  references/
    pipeline.md                 # 六階段＋完整 ffmpeg 指令配方＋批次迴圈＋ffprobe 驗證
    reframe.md                  # 9:16 決策規則＋裁切／模糊墊底濾鏡配方＋安全區數字
    subtitles-audio.md          # whisper→SRT→燒錄樣式；混音／ducking／loudnorm 配方
    attribution.md              # 原創建構；管線形狀參考 MoneyPrinterTurbo/ShortGPT（經研究檔）；huashu 動畫線列日後擴充
  sources.lock                  # 釘 alchaincyf/huashu-design（0e7ec8aca005，動畫線候選）；MoneyPrinterTurbo 未直接稽核故不釘、僅 attribution 記載
  evals/evals.json
```

登錄四件套＋README 外部 CLI 節補 ffmpeg（必備）／auto-editor／whisper（選用）。skill-map：獨立工具；邊界 vs social-card（影 vs 圖，同屬「圖＋影」家族）、vs slide-deck（影片 vs 簡報）。

## 5. 驗收（Given/When/Then）

1. Given 一支 1280×720 橫式測試片，When 走模糊墊底配方，Then 輸出 ffprobe 驗為 1080×1920、H.264、yuv420p、有音軌。
2. Given 素材夾有直式與橫式混合，When 盤點，Then 清單列出每支的解析度／橫直／時長，且重構圖策略逐支確認而非一律裁切。
3. Given whisper 未安裝，When 使用者要字幕，Then 明說降級選項（給 SRT 或跳過），不嘗試安裝。
4. Given 使用者說「順便發到 IG」，When 執行，Then 明說發布超出範圍。
5. Given 批次三支其中一支來源損壞，When 跑批次，Then 結束回報 2 成功 1 失敗＋原因，exit 非零。

## 6. 自我審查

- 與研究檔建議路線的偏差只有一處：暫不引入 MoviePy／editly（研究說「要 Python/MIT 純淨」才用；ffmpeg 直驅對代理更透明、零相依）——記為天花板：若配方複雜到難維護，再上 MoviePy。
- 安全區數字與 social-card 同源但各自記載（跨技能指標易碎）；來源註記一致。
- 無佔位符；六階段每階段在 references 都有對應配方段。
