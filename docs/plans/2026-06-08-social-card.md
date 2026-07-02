# social-card — 實作計畫

- 日期：2026-06-08
- 設計文件：`docs/specs/2026-06-08-social-card-design.md`（已核准）
- 慣例：gitmoji + Conventional Commits，**無** `Co-Authored-By`。每個任務一個 commit。
- 取捨：程式碼類任務給完整可跑碼；文字 reference 給內容規格 + 驗收標準（執行時依規格撰寫）。

---

## Phase A — 先把渲染器去風險（最先做）

### 任務 1：Spike — 實測 agent-browser 對固定尺寸元素的精確截圖

**目的**：釘死「固定像素卡片 → 精確尺寸 PNG」的指令；整條管線依賴它。

**建立** `/tmp/sc-spike/card.html`：
```html
<!doctype html><html><head><meta charset="utf-8"><style>
  html,body{margin:0;padding:0}
  .card{width:1080px;height:1350px;box-sizing:border-box;overflow:hidden;
    background:#f5f2ea;color:#111;display:flex;align-items:center;justify-content:center;
    font:700 96px/1.1 system-ui,sans-serif}
</style></head><body>
  <section class="card" id="ig-01">1080×1350</section>
</body></html>
```

**依序試這幾條，記錄哪條能輸出「正好 1080×1350」的 PNG**：
```bash
cd /tmp/sc-spike
# 方法 A：設 viewport 為卡片尺寸，截整頁
agent-browser open "file:///tmp/sc-spike/card.html"
agent-browser viewport 1080 1350 2>/dev/null || echo "（無 viewport 子指令則記下）"
agent-browser screenshot a.png
# 方法 B：元素 ref 截圖（若支援）
agent-browser snapshot -i
agent-browser screenshot b.png            # 視 snapshot 是否能鎖元素
# 方法 C：--full
agent-browser screenshot --full c.png
agent-browser close
# 驗尺寸
python3 - <<'PY'
from pathlib import Path
try:
    from PIL import Image
    for p in ("a.png","b.png","c.png"):
        f=Path("/tmp/sc-spike")/p
        if f.exists(): print(p, Image.open(f).size)
except ImportError:
    import subprocess
    for p in ("a.png","b.png","c.png"):
        f=Path("/tmp/sc-spike")/p
        if f.exists(): print(p, subprocess.run(["file",str(f)],capture_output=True,text=True).stdout.strip())
PY
```

**驗證**：至少一條方法輸出**正好 `1080×1350`** 的 PNG。
**產出**：把可行的指令序列記成兩三行，貼進任務 8（render-qa.md）的「Render」段。
**若全部都偏移**：退路是先 `agent-browser eval` 量元素 `getBoundingClientRect`，再用 viewport=元素尺寸截圖；把實測結論寫進 render-qa.md。
**Commit**：無（spike 用 `/tmp`，不進版控；結論寫進後續任務的檔案）。

---

## Phase B — 技能骨架 + 文字 references

### 任務 2：`social-card/SKILL.md`

**Frontmatter（完整，照抄）**：
```yaml
---
name: social-card
description: >-
  Generate polished IG / LinkedIn social card image sets (carousels + single cards)
  from an article, notes, outline, or screenshots — a principle-driven design engine
  (Swiss + Editorial systems, fixed-ratio frames) that renders to exact-size PNG via
  agent-browser. USE THIS SKILL when the user wants Instagram carousel images, IG
  4:5 / 1:1 / 9:16 posts, LinkedIn document-carousel or square cards, or 「社群卡片」
  「IG 輪播圖」「貼文圖」「LinkedIn 卡片」. Targets IG (4:5 primary, 1:1, 9:16) and
  LinkedIn (1:1, 1.91:1); FB gets a single 1.91:1 card. Do NOT use to POST or schedule
  to social media (no account management), for 16:9 slide decks (use slide-deck), or
  for Xiaohongshu 3:4 / WeChat 21:9 covers.
license: MIT
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(agent-browser:*)
---
```

**Body 內容規格**：開場「為什麼準則導向、不是套模板」（仿 slide-deck）；非協商鐵則 3–5 條（一卡一想法、先砍字不縮字、安全區、零授權資產）；每次流程：吃輸入 → 選平台/版式 → 生成單一 HTML（固定尺寸 frame）→ agent-browser render → eval QA → 修正；指向各 reference。

**驗證**：`python3 -c "import yaml,sys; d=yaml.safe_load(open('social-card/SKILL.md').read().split('---')[1]); assert d['name']=='social-card' and 'allowed-tools' in d; print('frontmatter OK')"`
**Commit**：`✨ feat(social-card): SKILL.md — IG/LinkedIn social card engine, agent-browser render`

### 任務 3：`social-card/references/platform-specs.md`
**規格**：設計文件 §2 的像素表（IG 4:5/1:1/9:16、LinkedIn 1:1/1.91:1、FB 1.91:1）逐一寫尺寸、用途、安全區；CSS class 命名對照（`.ig-45 .ig-11 .ig-916 .li-11 .li-191 .fb-191`）與固定 `width/height`；高解析與命名規則。
**驗證**：`grep -qE "1080.?1350" social-card/references/platform-specs.md && grep -qE "1080.?1920" social-card/references/platform-specs.md && echo OK`
**Commit**：`📝 docs(social-card): platform-specs — IG/LinkedIn pixel specs + safe areas`

### 任務 4：`social-card/references/principles.md`
**規格**：一卡一想法；先砍字不縮字（最高鐵則，仿 slide-deck §2）；標題字數/行數上限；CJK 行高（大標 1.08–1.22、內文 1.35–1.55）；安全區；對比；不在雜亂照片壓長文。每條附「為什麼」。
**驗證**：`grep -qi "shorten\|砍字\|never shrink\|不縮" social-card/references/principles.md && echo OK`
**Commit**：`📝 docs(social-card): principles — one idea per card, shorten-not-shrink`

### 任務 5：`social-card/references/style-system.md`
**規格**：2 風格家族（Swiss：網格/髮絲線/無陰影/直角/型階；Editorial：雜誌/非對稱/細紋理/重點線）各自的視覺規則；3–4 套原創主題色盤（每套附 hex、用途）；何時用哪個風格。零授權資產聲明。
**驗證**：`grep -qi "swiss" social-card/references/style-system.md && grep -qi "editorial" social-card/references/style-system.md && grep -qcE "#[0-9a-fA-F]{6}" social-card/references/style-system.md && echo OK`
**Commit**：`📝 docs(social-card): style-system — Swiss + Editorial, original palettes`

### 任務 6：`social-card/references/layouts.md`
**規格**：6–8 個頁面角色（封面/重點/清單・checklist/比較/引言/截圖框/總結），每個寫：用途、結構、標題字數上限、適用比例、常見錯誤。
**驗證**：`grep -cE "^##|^###" social-card/references/layouts.md`（≥6）
**Commit**：`📝 docs(social-card): layouts — 7 page roles with caps and recipes`

### 任務 7：`social-card/references/screenshot-treatment.md`
**規格**：移植 guizang 原則——UI/密集文字/程式碼/表格用 `object-fit:contain`，物件/可裁切用 `cover`；`object-position` 依內容；安全內距；不加透視/傾斜；Swiss 直角無陰影 vs Editorial 小圓角細陰影。
**驗證**：`grep -q "object-fit" social-card/references/screenshot-treatment.md && echo OK`
**Commit**：`📝 docs(social-card): screenshot-treatment — object-fit rules by content type`

### 任務 8：`social-card/references/render-qa.md`
**規格**：用任務 1 釘死的指令寫「Render」段（agent-browser open → 逐 frame 精確截圖 → 驗尺寸）；「QA」段說明 `agent-browser eval --stdin < scripts/qa-rules.js` 怎麼跑、怎麼讀結果、失敗如何修（切頁/砍字不縮字）；輸出資料夾結構與命名。
**驗證**：`grep -q "agent-browser" social-card/references/render-qa.md && grep -q "qa-rules.js" social-card/references/render-qa.md && echo OK`
**Commit**：`📝 docs(social-card): render-qa — agent-browser render + eval QA pipeline`

---

## Phase C — 原創骨架 + QA 腳本

### 任務 9：`social-card/assets/template-swiss.html`
**規格**：原創、零 guizang 資產。含 `.sheet` 容器 + 各比例 class 的固定尺寸 CSS（`.ig-45{width:1080px;height:1350px}` 等全部六個）+ `box-sizing:border-box;overflow:hidden`；Swiss 風格基底（網格變數、型階變數、髮絲線、無陰影）；範例放幾個 frame（封面 + 重點 + 清單）。CSS 變數驅動主題色。
**驗證**：`grep -qE "1080px" social-card/assets/template-swiss.html && grep -qiE "box-sizing:\s*border-box" social-card/assets/template-swiss.html && echo OK`
**Commit**：`✨ feat(social-card): template-swiss.html — original fixed-frame skeleton`

### 任務 10：`social-card/assets/template-editorial.html`
**規格**：同上骨架，Editorial 風格基底（非對稱欄、重點線、細微紙紋、可選細陰影）。
**驗證**：`grep -qE "1080px" social-card/assets/template-editorial.html && echo OK`
**Commit**：`✨ feat(social-card): template-editorial.html — magazine-style skeleton`

### 任務 11：`social-card/scripts/qa-rules.js`（完整碼，餵 agent-browser eval --stdin）
```javascript
// social-card QA rules — piped into `agent-browser eval --stdin`.
// Runs in the rendered page DOM; returns a findings array. Empty = pass.
(() => {
  const FLOOR = 28;                       // min readable body px on a 1080-wide canvas
  const TITLE_MAX_LINES = 4;              // display-title hard cap
  const SAFE = { 'ig-916': { top: 250, bottom: 340 } };  // Stories/Reels UI bands
  const out = [];
  for (const card of document.querySelectorAll('.card')) {
    const id = card.id || '(no-id)';
    // R1 overflow
    if (card.scrollHeight > card.clientHeight + 1)
      out.push({ card: id, rule: 'R1-overflow', fix: 'split the card or cut copy — never shrink the font' });
    // R3 min font floor on body/lead/caption
    for (const el of card.querySelectorAll('.body,.lead,.caption,.meta,.label')) {
      const px = parseFloat(getComputedStyle(el).fontSize);
      if (px && px < FLOOR)
        out.push({ card: id, rule: 'R3-font-floor', detail: `${el.className} ${px}px < ${FLOOR}px` });
    }
    // Title line cap
    for (const t of card.querySelectorAll('.title,.h-hero,.h-xl')) {
      const lh = parseFloat(getComputedStyle(t).lineHeight) || 1.1 * parseFloat(getComputedStyle(t).fontSize);
      const lines = Math.round(t.scrollHeight / lh);
      if (lines > TITLE_MAX_LINES)
        out.push({ card: id, rule: 'title-cap', detail: `${lines} lines > ${TITLE_MAX_LINES}`, fix: 'shorten the title' });
    }
    // Safe-area for Stories/Reels
    for (const [cls, band] of Object.entries(SAFE)) {
      if (!card.classList.contains(cls)) continue;
      const cr = card.getBoundingClientRect();
      for (const el of card.querySelectorAll('.title,.body,.lead,.cta')) {
        const r = el.getBoundingClientRect();
        if (r.top - cr.top < band.top || cr.bottom - r.bottom < band.bottom)
          out.push({ card: id, rule: 'safe-area', detail: `${el.className} enters the UI band`, fix: 'pull content into the central safe band' });
      }
    }
  }
  return out;
})();
```
**驗證**：`node -e "const s=require('fs').readFileSync('social-card/scripts/qa-rules.js','utf8'); new Function(s); console.log('qa-rules.js parses OK')"`
**Commit**：`✨ feat(social-card): qa-rules.js — DOM checks for overflow/font/title/safe-area`

---

## Phase D — 評測 + 來源追蹤

### 任務 12：`social-card/evals/evals.json`
**規格**：測意圖非僅行為。案例：①給文章→產 IG 4:5 輪播且截圖正好 1080×1350（deterministic 尺寸）；②內容過長→QA 抓溢出且「切頁/砍字非縮字」（行為主觀 + 尺寸確定）；③Stories 9:16 正文在安全帶內；④UI 截圖用 contain 不裁切；⑤FB 只出單張 1.91:1 不做整套；⑥不誤觸發去做發文/排程（範圍）。能確定性判斷的標 `deterministic:true`。
**驗證**：`python3 -c "import json; d=json.load(open('social-card/evals/evals.json')); assert len(d['evals'])>=5; print('evals OK', len(d['evals']))"`
**Commit**：`✅ test(social-card): evals — platform dims, shorten-not-shrink, safe-area, scope`

### 任務 13：`social-card/references/attribution.md` + `social-card/sources.lock`
**attribution 規格**：參考 op7418/guizang-social-card-skill 的**設計系統原則**（一卡一想法、先砍字不縮字、object-fit、安全區、Swiss/Editorial 雙系統）；**未收任何檔**（授權 AGPL/ISC 不一致，避免污染）；平台改 IG/LinkedIn；render 由 playwright 換成 agent-browser。
**sources.lock 規格**：釘 guizang commit（取目前 HEAD 完整 SHA）+ 日期 2026-06-08 + note「取原則非檔；render 改 agent-browser」，供 skill-evolve 比對。
**驗證**：`python3 -c "import json; json.load(open('social-card/sources.lock')); print('lock OK')" && grep -qi "agent-browser" social-card/references/attribution.md && echo OK`
**Commit**：`📝 docs(social-card): attribution + sources.lock — guizang principles, agent-browser render`

---

## Phase E — 登錄 + 部署

### 任務 14：登錄三處
- `apm.yml`：dependencies.apm 加 `- ./social-card/`（接在 `- ./roleplay-coach/` 之後）。
- `README.md`：自建技能表加一列 social-card（描述：IG/LinkedIn 社群卡片引擎，agent-browser 渲染，取 guizang 原則自製）。
- `skill-curator/references/skill-map.md`：Standalone tools 區加一條，附與 slide-deck 邊界（簡報 PDF vs 社群卡 PNG）。
**驗證**：`python3 -c "import yaml; assert './social-card/' in yaml.safe_load(open('apm.yml'))['dependencies']['apm']; print('apm.yml OK')" && grep -q "social-card" README.md skill-curator/references/skill-map.md && echo OK`
**Commit**：`📝 docs(social-card): register in apm.yml, README, skill-map`

### 任務 15：全域 symlink
```bash
ln -sfn /mnt/d/project/skills/social-card ~/.claude/skills/social-card
ls -ld ~/.claude/skills/social-card
```
**驗證**：`test -L ~/.claude/skills/social-card && echo "symlink OK"`
**Commit**：無（本機部署動作，不進版控）。後續 `apm install` 會把它部署進 `.claude/skills`、`.agents/skills`。

---

## 收尾驗證（全部任務完成後）

1. `python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('social-card/**/*.json',recursive=True)]; print('all JSON valid')"`
2. `node -e "new Function(require('fs').readFileSync('social-card/scripts/qa-rules.js','utf8'))"`（QA 腳本可解析）
3. 端到端煙霧測試：拿一段範例文字，產 IG 4:5 輪播 HTML → agent-browser 截圖 → 確認 PNG 正好 1080×1350、QA 回空陣列。
4. `git log --oneline` 應見任務 2–14 各一個 commit。
