# slide-deck 機制升級實作計畫

> 依 `docs/specs/2026-07-02-slide-deck-mechanisms-design.md`。批次指令下自主執行。

## 任務 1：`scripts/check_deck.py` 版式鎖（核心程式）

常數區加：

```python
# Registered page roles (layouts.md). data-label is the hook that makes role checks
# possible; an unregistered label usually means an invented layout — the main source
# of unstable slides (constraints make generated decks more reliable).
ROLE_ALIASES = {"big-number": "bignumber", "section-divider": "section", "divider": "section"}
KNOWN_ROLES = {"cover", "agenda", "section", "content", "bignumber", "quote",
               "comparison", "timeline", "closing"}
# Near-empty roles (layouts.md density table): prose beyond this belongs on a Content slide.
SPARSE_ROLES = {"cover", "section", "closing", "bignumber", "quote"}
MAX_SPARSE_UNITS = 50
```

抽純函式 `slide_role_warns(attrs, frag, n)`（缺標 WARN／未登記 WARN／content-agenda bullet cap／稀疏角色 >50 單位 WARN），main 迴圈改呼叫它並移除原本內嵌的角色檢查；`_selftest()` 加四案（缺標、未登記、quote 超字、Big-Number 別名合法）。驗收：`--selftest` 印 selftest OK；對 examples 跑非 strict exit 0。

## 任務 2：`references/layouts.md`＋SKILL.md Phase 4 各補一句

「每張投影片 MUST 帶登記角色的 `data-label`（登記表＝本目錄九角色）——校驗器靠它做角色檢查，未登記＝自創版式警告。」驗收：兩檔 grep `data-label` 有新句。

## 任務 3：`references/style-presets.md` 開頭加選型表

六預設 × best_for × avoid_for（設計 §2 的表），註明「先查表再讀中選節」。驗收：`grep -c avoid_for` ≥1。

## 任務 4：SKILL.md Phase 2 預覽規則銳化

「2–3 個預設」→「1 穩（選型表最對位）＋1 大膽＋1 外卡；預覽用真實內容，MUST NOT 渲染內部流程字樣」。驗收：grep 外卡／wildcard。

## 任務 5：attribution.md＋sources.lock

attribution 補 guizang-ppt-skill（AGPL、原則非檔、版式鎖思想、WARN 化為刻意偏離）與 frontend-slides 本輪採納（avoid_for 表＋預覽組成）；lock 新增 guizang 條目（commit `21fee2c4a940` 以稽核當日 HEAD 為準——實作時以 scratchpad 複本 rev-parse 為準）＋更新 frontend-slides note。驗收：JSON 合法、8 源。

## 任務 6：evals 補一案 `role-lock-registered-labels`

產出簡報每張帶登記 data-label；校驗器抓自創角色。驗收：案數 +1。

## 任務 7：驗證＋提交

selftest／example exit 0／JSON 全過 → `✨ feat(slide-deck): 版式鎖＋選型表＋預覽組成規則（原則參考 guizang-ppt／frontend-slides）`；docs 另一提交。
