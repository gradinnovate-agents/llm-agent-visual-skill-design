# 第一章：SKILL 設計基礎

## 1.1 為什麼要學習 SKILL 設計？

在開始實作之前，我們需要先理解一個核心問題：

> **SKILL 和 Tool 有什麼不同？**

### 層級對比

| 概念 | 層級 | 定義 | 範例 |
|------|------|------|------|
| **Function** | 低 | 單一可調用的程式函數 | `generate_bar_chart(data)` |
| **Tool** | 中 | 多個 Function 的組合 + 使用說明 | Chart Tool (含多種圖表類型) |
| **SKILL** | 高 | 完整的能力系統，含設計原則、範例、驗證 | 「數據可視化 SKILL」 |

### SKILL 的三大特徵

1. **自描述性 (Self-Describing)**
   - SKILL 文件本身就說明了什麼時候該用它
   - 包含 `trigger` 條件、`description` 描述

2. **結構化 (Structured)**
   - YAML frontmatter 定義元資料
   - Markdown body 說明使用方式
   - Linked files 提供參考資源

3. **可驗證 (Verifiable)**
   - 內建驗證機制
   - 提供測試案例

## 1.2 SKILL.md 語法詳解

### 基本結構

```yaml
---
name: chart-generation-skill          # 技能的唯一識別名
version: "1.0.0"                      # 遵循 SemVer
description: |                        # 詳細描述（支援換行）
  生成專業級圖表的技能。
  支援柱狀圖、折線圖、散佈圖等多種類型。
trigger: |                            # 觸發條件（關鍵！）
  當用戶說"生成圖表"、"畫圖"、"可視化數據"時
metadata:                             # 額外元資料
  hermes:
    tags: [chart, data-viz, matplotlib]
    related_skills: [data-analysis, report-generation]
---

# 圖表生成技能

## 使用場景

當需要將數據轉換為視覺化圖表時...

## 工作流程

1. **分析需求** → 確定圖表類型、資料格式
2. **驗證輸入** → 使用 JSON Schema 檢查
3. **生成圖表** → 調用渲染引擎
4. **格式輸出** → PNG/SVG/HTML 格式選擇

## 常見問題

### Q: 圖表類型如何選擇？
**A**: 參考 `references/chart-selection-guide.md`
```

### 關鍵欄位說明

| 欄位 | 必填 | 說明 |
|------|------|------|
| `name` | ✓ | 小寫、用 hyphens 連接 |
| `version` | ✓ | 遵循 SemVer (major.minor.patch) |
| `description` | ✓ | 一句話說清楚這個 SKILL 做什麼 |
| `trigger` | ✓ | 什麼情境下該啟用這個 SKILL |
| `metadata` | × | tags, related_skills, author 等 |

## 1.3 Linked Files 結構

完整的 SKILL 通常會有以下目錄結構：

```
skill-name/
├── SKILL.md                 # 主技能文件
├── references/              # 參考資料
│   ├── api-reference.md      # API 文件
│   ├── best-practices.md     # 最佳實踐
│   └── examples/             # 使用範例
├── templates/               # 模板檔案
│   ├── config.yaml          # 配置模板
│   └── sample-input.json    # 範例輸入
└── scripts/                 # 輔助腳本
    ├── validate.py           # 驗證腳本
    └── setup.sh              # 初始化腳本
```

## 1.4 小結

- SKILL 是比 Tool 更高階的抽象，包含完整使用說明
- YAML frontmatter 定義元資料，Markdown 說明使用方式
- Linked files 提供參考資源，讓 SKILL 更加自包含

---

> **認識 Check**✓ 能夠解釋 SKILL 和 Tool 的差異
✓ 能夠寫出符合規範的 SKILL.md 前置資料
✓ 理解 linked files 的目錄結構
