# 第三章：圖表 SKILL 設計實戰

## 3.1 完整 SKILL 架構範例

以下是一個符合 Hermes Agent SKILL 規範的圖表生成技能完整實作：

```yaml
---
name: chart-generation-skill
version: "1.0.0"
description: |
  生成專業級資料可視化圖表的技能。
  支援柱狀圖、折線圖、散佈圖、直方圖等多種類型，
  遵循 Tufte 資料可視化原則。
trigger: |
  當用戶需要將數據轉換為圖表時使用，如：
  - "畫一個顯示...的圖"
  - "生成...的可視化"
  - "把這些數據變成圖表"
  - "顯示趨勢圖"
metadata:
  hermes:
    tags: [chart, data-viz, matplotlib, visualization]
    related_skills: [data-analysis, report-generation]
    category: data-science
---

# 圖表生成技能

## 概述

本技能提供完整的資料可視化能力，從數據到圖片的一站式解決方案。

## 支援的圖表類型

| 類型 | 說明 | 適用場景 |
|-----|------|---------|
| `bar` | 柱狀圖 | 比較不同類別的數值 |
| `line` | 折線圖 | 顯示時間趨勢 |
| `scatter` | 散佈圖 | 探索變數關係 |
| `histogram` | 直方圖 | 顯示數據分佈 |
| `pie` | 圓餅圖 | 顯示占比（謹慎使用） |

## 使用流程

### Step 1: 準備輸入資料

資料格式：列表的列表，每個元素是包含資料欄位的字典

```json
[
  {"month": "1月", "sales": 120, "profit": 30},
  {"month": "2月", "sales": 200, "profit": 50},
  {"month": "3月", "sales": 150, "profit": 40}
]
```

### Step 2: 選擇圖表類型

參考 `references/chart-selection-guide.md` 了解如何選擇合適的圖表類型。

### Step 3: 設定參數

```python
{
  "chartType": "bar",
  "data": [...],
  "xField": "month",
  "yField": "sales",
  "title": "月度銷售額",
  "options": {
    "format": "png",
    "dpi": 150
  }
}
```

### Step 4: 執行生成

調用 `scripts/generate.py` 或使用 Python API。

## 輸入驗證

所有輸入都會經過 JSON Schema 驗證：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "chartType": {
      "type": "string",
      "enum": ["bar", "line", "scatter", "histogram", "pie"]
    },
    "data": {
      "type": "array",
      "minItems": 1
    },
    "xField": {"type": "string"},
    "yField": {"type": "string"},
    "title": {"type": "string"},
    "options": {"type": "object"}
  },
  "required": ["chartType", "data", "xField", "yField"]
}
```

## 錯誤處理

| 錯誤類型 | 說明 | 處理方式 |
|---------|------|---------|
| ValidationError | 輸入資料不符合 schema | 返回詳細錯誤訊息 |
| EmptyDataError | 資料為空 | 提示检查輸入 |
| RenderError | 渲染失敗 | 重試或降級 dpi |

## 最佳實踐

- 遵循 Tufte 資料可視化原則
- 使用直接標籤 (direct labels)
- 移除不必要的裝飾
- 選擇合適的圖表類型

## 相關資源

- `references/chart-selection-guide.md` - 圖表選擇指南
- `references/color-palettes.md` - 推薦配色方案
- `templates/bar_chart.json` - 柱狀圖模板
- `templates/line_chart.json` - 折線圖模板
- `scripts/validate.py` - 輸入驗證腳本
- `scripts/generate.py` - 圖表生成腳本
