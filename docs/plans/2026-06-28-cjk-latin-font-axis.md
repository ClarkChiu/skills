# slide-deck — CJK／Latin 字體軸 任務計畫

- 日期：2026-06-28
- 設計文件：`docs/specs/2026-06-28-cjk-latin-font-axis-design.md`（已核准）
- 內容真相來源：完整的規則文字與 linter 規格在設計文件 §4／§5，本計畫只負責**執行順序、
  驗證閘門、提交邊界**，不重複內文。

執行順序刻意「先程式、後文件、最後 bump」：linter 先到位且 `--selftest` 綠，後面文件改完
可立刻用它驗證既有範例不誤報。

---

## 任務 1 — check_deck.py：抽純函式 ＋ 第 8 條兩個 WARN ＋ `--selftest`

- 檔案：`slide-deck/scripts/check_deck.py`
- 內容依設計文件 §5：
  1. 新增模組級常數 `CJK_FAMILIES`（§5.1 黑名單，小寫）。
  2. 新增純函式 `font_axis_warns(doc: str) -> list[str]`：解析 `font-family:` 宣告做順序
     檢查、再做「載入 CJK webfont 但無 Han 字」檢查，回傳英文 WARN 清單（§5.2）。抽成純
     函式讓 `audit()` 與 `--selftest` 共用。
  3. 在現有第 7 條（overflow）之後呼叫 `warns.extend(font_axis_warns(doc))`。
  4. `main()` 加 `--selftest` 分支（§5.3）：對三段內嵌樣本 A/B/C assert，全過印
     `selftest OK` 回 0，否則回 1。
- 驗證：
  ```bash
  python3 slide-deck/scripts/check_deck.py --selftest
  ```
  預期：印 `selftest OK`，exit 0。
- 提交：`✨ feat(slide-deck): check_deck 新增 CJK/Latin 字體軸檢查（順序＋載入未用）＋--selftest`

## 任務 2 — principles.md §3：新增「兩軸字體」一段

- 檔案：`slide-deck/references/principles.md`
- 內容：設計文件 §4.1 的整段，插在 §3 現有「Webfont discipline（esp. CJK）」項之後。
- 驗證：
  ```bash
  grep -c "兩軸字體" slide-deck/references/principles.md          # 預期 1
  python3 slide-deck/scripts/check_deck.py --selftest             # 仍綠（未碰程式）
  ```
- 提交：與任務 3、4 合併（見下，三個文件改動是同一條原則的落實，併一個 commit）。

## 任務 3 — style-presets.md：131–133 行改寫

- 檔案：`slide-deck/references/style-presets.md`
- 內容：設計文件 §4.2，把「add Noto to the stack」改為 Latin 優先有序堆疊＋依語言載入，
  指回 §3。
- 驗證：`grep -n "兩軸\|Latin face\|principles.md §3\|排第一" slide-deck/references/style-presets.md` 有命中。

## 任務 4 — SKILL.md：Phase 4 補半行

- 檔案：`slide-deck/SKILL.md`
- 內容：設計文件 §4.3，在 Phase 4「Replace the `:root` variables…」後補一句兩軸順序提醒。
- 驗證：`grep -n "兩軸" slide-deck/SKILL.md` 有命中。
- 任務 2＋3＋4 合併提交：
  `📝 docs(slide-deck): formalize CJK/Latin 兩軸字體原則（principles §3／presets／SKILL）`

## 任務 5 — 整合驗證（不誤報既有範例）

- 驗證（設計文件 §6）：
  ```bash
  # 既有 CJK 範例：第 8 條不該產生新 WARN
  python3 slide-deck/scripts/check_deck.py slide-deck/examples/txone-profile.zh-TW.html
  ```
  預期：輸出不含兩條新 WARN（font stack 順序、CJK webfont 未用）。若誤報 → 回任務 1 修
  偵測邏輯（很可能是該範例的合法 Latin-first 堆疊被錯判），不是改範例。
- 若範例本身其實有 Latin 字排在 CJK 之後的真問題 → 那是 linter 抓到的真實缺陷，據實回報
  並修範例（Rule 12 失敗要大聲）。

## 任務 6 — sources.lock：bump 兩個 pending 源

- 檔案：`slide-deck/sources.lock`
- 內容：把 `zarazhangrui/frontend-slides` 與 `hugohe3/ppt-master` 從 pending 推進到現狀
  commit，註記採納結果：
  - frontend-slides → 9906a34d640d（v2.1.0, 2026-06-23）：密度雙檔觀念 slide-deck 已由
    §9/§10 覆蓋，無新增採納；本次無實質。
  - ppt-master → 13a25616e635（v2.11.0, 2026-06-27）：採納其「CJK/Latin 字體獨立軸」觀念，
    以原創方式寫進 principles §3 ＋ check_deck 第 8 條（借觀念、零相依實作）。
- 驗證：
  ```bash
  python3 -c "import json;json.load(open('slide-deck/sources.lock'));print('JSON ok')"
  GITHUB_TOKEN=$GITHUB_TOKEN python3 /root/.claude/skills/skill-evolve/scripts/check_updates.py slide-deck | grep "need a look"
  ```
  預期：JSON ok；`0 source(s) need a look`。
- 提交：`📌 chore(slide-deck): bump frontend-slides／ppt-master 基準，記載字體軸採納`

---

## 完工定義（Definition of Done）

- [ ] `check_deck.py --selftest` 綠。
- [ ] 既有 `txone-profile.zh-TW.html` 不被第 8 條誤報（或誤報已查明為真實缺陷並處理）。
- [ ] principles §3／style-presets／SKILL 三處文件到位、彼此指向一致。
- [ ] slide-deck `check_updates` 歸零、sources.lock JSON 合法。
- [ ] 三個 commit（程式／文件／lock）落地。
