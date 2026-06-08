# social-card — 設計文件

- 日期：2026-06-08
- 狀態：**待核准（design-gate 硬閘門）**
- 參考來源：op7418/guizang-social-card-skill（取設計系統「原則」，不收檔；研究見 `research/audits/2026-06-08-guizang-social-card-skill.md`）

## 1. 目的與範圍

**做什麼**：把文章／筆記／大綱／截圖，生成一組精緻的 **IG／LinkedIn 社群卡片圖**（輪播 + 單張）。
準則導向的設計引擎（與 `slide-deck` 同血緣），輸出固定比例的卡片畫面，經 **agent-browser** 渲染成 PNG。

**不做什麼（v1 out of scope）**：
- **發文／排程／數據／回覆**（這是「管理」軌，屬 Meta Graph API 整合的另案，不是 skill）。
- 小紅書 3:4／微信公眾號 21:9（guizang 的原平台，不沿用）。
- Reels/Story 動畫、影片。
- 生成式配圖的「產生」（可擺放使用者提供或既有素材，但不主打生圖）。

## 2. 目標平台與精確像素規格

高解析輸出（2× 友善），固定尺寸：

| 平台／比例 | 像素 | 用途 | 安全區重點 |
|---|---|---|---|
| **IG 直式 4:5** ⭐ | 1080×1350 | 主打：輪播／動態 | 側邊 64–96px |
| **IG 方形 1:1** | 1080×1080 | 單張／封面 | 側邊 64–96px |
| **IG 限動 9:16** | 1080×1920 | Stories／Reels 封面 | 上 ~250px、下 ~340px 留給 UI（頭像／字幕／CTA），正文壓在中間安全帶 |
| **LinkedIn 方形 1:1** | 1080×1080 | 文件輪播／動態 | 邊距放寬 |
| **LinkedIn 橫式 1.91:1** | 1200×627 | 連結／分享卡 | 中央偏左標題帶 |
| **FB 單張 1.91:1** 🔻 | 1200×630 | 降級：單張連結圖，**沿用 LinkedIn 橫式幾何**，不另做整套 | — |

## 3. 設計系統（精簡 v1）

- **2 風格家族**：
  - **Swiss**（網格、髮絲線、無陰影、直角、強型階）
  - **Editorial**（雜誌、非對稱、細微紋理、重點線）
- **3–4 套原創主題色盤**（如 紙上墨黑／單色重點／另兩套）——零授權資產，全部原創。
- **6–8 個核心版式（頁面角色）**：封面 / 重點（單句陳述）/ 清單・checklist / 比較 / 引言（pull-quote）/ 截圖框 / 總結。

**承載原則（取自 guizang，跨平台通用）**：
- 一張卡一個想法；標題字數上限（依版式）。
- **先砍字、不縮字**（內容溢出時切頁或刪字，絕不把字級壓到地板）。
- 截圖處理：UI／密集文字／程式碼用 `object-fit:contain`；物件／可裁切用 `cover`；`object-position` 依內容設。
- 安全邊距、CJK 行高（大標 1.08–1.22、內文 1.35–1.55）、不在雜亂照片上壓長文。

## 4. 渲染 + QA 管線（agent-browser，取代 playwright）

**單一 HTML 含所有卡片**，每張是固定尺寸節點：
```html
<main class="sheet">
  <section class="card ig-45" id="ig-01">…</section>
  <section class="card ig-45" id="ig-02">…</section>
  <section class="card li-191" id="li-01">…</section>
</main>
```
每個 `.card` 用 `box-sizing:border-box`、固定 `width/height`、`overflow:hidden`。

**渲染**：`agent-browser open file://…/index.html` → 等字體 →逐張 frame 以**精確像素**輸出 PNG 到 `output/`。
> ⚠️ 技術風險（計畫階段第一個要驗的）：agent-browser 對「單一元素精確尺寸截圖」的支援方式。
> **已解決（2026-06-08 執行階段）**：實測發現 agent-browser 預設視窗約 1280×577、`viewport`
> 指令不改截圖表面；`screenshot "#id"` 給對的尺寸但不繪製摺線以下（高卡半空白）。最終採
> **隔離單卡 → `screenshot --full` 繪製全高 → `convert` 裁切到精確尺寸**，封裝成
> `scripts/render-frames.sh`，跨兩主題兩版式驗證出圖正確（見 render-qa.md）。

**QA**：`agent-browser eval --stdin` 餵入 `scripts/qa-rules.js`，對渲染後 DOM 跑檢查（移植 guizang R1–R7、改成本專案規格）：
- R1 溢出（`scrollHeight > clientHeight`）
- R3 最小字級地板（1080 寬上，內文不低於 ~28–32px）
- 標題字數／行數上限（依版式）
- **安全區合規**（Stories 正文須在安全帶內）
- 對比度
- 失敗 → 回報，agent 改文案／切頁修正，**不縮字**。

整條 render/QA 都跑在 agent-browser（使用者已裝、已稽核），**不引入 playwright/chromium**。

## 5. 輸入與輸出

**輸入**：文章／筆記／大綱／截圖／產品說明 → 一組卡片。
**輸出結構**：
```
social-card-<slug>/
  index.html          # 所有 frame
  assets/             # 使用者截圖／既有素材
  output/             # 匯出 PNG：ig45-01-cover.png, ig45-02-point.png, li191-cover.png …
```

## 6. 檔案結構（鏡像 slide-deck 慣例）

```
social-card/
  SKILL.md                       # frontmatter：name、帶 IG/LinkedIn/輪播 觸發語的 description、allowed-tools: Read/Write/Edit + Bash(agent-browser:*)
  references/
    principles.md                # 一卡一想法、先砍字不縮字、安全區
    platform-specs.md            # 本文件 §2 的像素規格與安全區
    style-system.md              # Swiss / Editorial + 主題色盤
    layouts.md                   # 6–8 個頁面角色
    screenshot-treatment.md      # object-fit / 框 / 安全內距
    render-qa.md                 # agent-browser 渲染 + eval QA 指令
    attribution.md               # 參考 guizang「原則」非檔；AGPL/ISC 不收檔；render 改 agent-browser
  assets/
    template-swiss.html          # 原創骨架
    template-editorial.html      # 原創骨架
  scripts/
    qa-rules.js                  # 餵 agent-browser eval --stdin 的 DOM 檢查
  evals/evals.json
  sources.lock                   # 釘 guizang 基準（供 skill-evolve）
```

**登錄**：apm.yml、README 自建表、skill-curator/references/skill-map.md（Standalone tools，附與 slide-deck 邊界）、全域 symlink。

## 7. 與 slide-deck 的邊界

| | slide-deck | social-card |
|---|---|---|
| 輸出 | 16:9 簡報 HTML，螢幕自適應 → PDF | 固定比例社群卡（4:5/1:1/9:16/1.91:1）→ PNG |
| 渲染 | 自含 HTML（瀏覽器開） | agent-browser 截圖 |
| 用途 | 簡報／talk | IG/LinkedIn 貼文卡 |

共用 DNA：準則導向、一 frame 一想法、先砍字不縮字、零授權模板資產。

## 8. 撰寫語言

**英文**（工程／工具技能，照「語言看主題」房規，同 slide-deck／design-gate）；description 帶中文觸發語。

## 9. 成功標準（驗證用）

1. 給一篇文章 → 產出一組 IG 4:5 輪播卡 HTML，agent-browser 截圖出**精確 1080×1350** PNG。
2. 內容過長時，QA 抓到溢出，agent **切頁或砍字**而非縮字。
3. Stories 9:16 的正文落在安全帶內（上下 UI 區不壓字）。
4. 截圖卡：UI 截圖用 `contain`、不裁切。
5. FB 只出單張 1.91:1，不另做整套。
6. 全程不裝 playwright；render/QA 都過 agent-browser。
