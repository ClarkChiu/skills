# 多模型分階段路由 — 操作參考（OpenCode 多階段才用得到）

> **狀態：參考存檔，非預設啟用。** 主力 Claude Code 用不到這頁。只有在 OpenCode
> 上跑多階段（SDD／design→apply→verify 之類）、且想用便宜模型分擔各階段時才看。
> 源自 Gentle-AI（github.com/Gentleman-Programming/gentle-ai）與 r/opencodeCLI 的
> 多模型工作流討論。

採用動機要放對：**不是為了省 token**（多 agent 互審通常更貴），是為了**降幻覺、
讓長專案的輸出更穩**。

## 1. 角色 failover cascade

每個角色給一條有序降級鏈。後端（如 OpenCode Go）每隔幾週輪替模型時，被輪掉的就
自動往下掉，不必手動重平衡。

```yaml
# 每個角色：primary + 有序 fallback。上一個不可用／被輪替就用下一個。
roles:
  reason:   [opus-4.8, qwen-3.7-max, glm-5.2]      # design / spec / verify
  bulk:     [deepseek-v4-flash, qwen-3.7-plus]      # explore / 大檔讀取 / apply
  default:  [deepseek-v4-pro, minimax-m3]           # 其餘
```

## 2. 2-3 模型分階段路由（最小版）

別學社群那篇的 11 段配置——共識是過度工程。砍到 3 級，階段對應上面三條鏈：

| 階段 | 用哪條鏈 | 理由 |
|---|---|---|
| design / spec / verify | `reason` | 要推理與互審，配最強 |
| explore / apply / 大 context 讀取 | `bulk` | 要便宜＋大視窗，推理弱沒關係 |
| 其餘 | `default` | 折衷 |
