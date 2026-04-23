# 第二章：設計模式深度剖析

## 2.1 四大設計模式概覽

根據對熱門開源專案的分析，我們歸納出四大設計模式：

| 模式 | 代表專案 | 核心特徵 | 適用場景 |
|------|---------|---------|---------|
| **Tool Calling** | `antvis/mcp-server-chart` | 每個圖表類型是獨立 Tool | 需要精細控制時 |
| **Structured Output** | `hustcc/mcp-echarts` | LLM 輸出 JSON，渲染引擎轉換 | 需要結構化數據時 |
| **Code Interpreter** | `open-interpreter`, `e2b` | LLM 生成執行碼，沙盒執行 | 需要彈性和通用性時 |
| **Generative UI** | `preswald`, `baoyu-infographic` | 佈局×樣式雙維度控制 | 需要豐富視覺效果時 |

## 2.2 Tool Calling 模式

### 架構圖

```
┌────────────────────────────────────────────────┐
│              User Query              │
│   "畫一個顯示銷售趨勢的折線圖"      │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│              LLM Agent               │
│   分析需求 → 選擇适當的 Tool        │
│   "這個需要折線圖，使用 line_chart Tool" │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│            Tool Definition            │
│   {
    "name": "line_chart",
    "parameters": { ... }               │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│            Execution Result           │
│            PNG/SVG 圖片               │
└────────────────────────────────────────────────┘
```

### 實作範例

```python
# Tool Definition for LLM
LINE_CHART_TOOL = {
    "type": "function",
    "function": {
        "name": "generate_line_chart",
        "description": "生成折線圖顯示時間趨勢數據",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "string"},  # 時間點
                            "y": {"type": "number"}   # 數值
                        }
                    }
                },
                "title": {"type": "string"},
                "smooth": {"type": "boolean", "default": False}
            },
            "required": ["data"]
        }
    }
}
```

## 2.3 Structured Output 模式

### 架構圖

```
┌────────────────────────────────────────────────┐
│              User Query              │
│   "顯示各月份銷售額"                  │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│              LLM Agent               │
│   輸出結構化 JSON：                  │
│   {                                   │
│     "chartType": "line",              │
│     "title": "月度銷售趨勢",            │
│     "data": [...]                     │
│   }                                   │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│         Rendering Engine             │
│   JSON → ECharts/Plotly/Matplotlib    │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│            Output Image              │
└────────────────────────────────────────────────┘
```

### 優勢
- **解耦：** LLM 只負責輸出 JSON，不需知道如何渲染
- **可換：** 可以隨時更換底層渲染引擎
- **可測試：** JSON 輸出容易驗證

## 2.4 Code Interpreter 模式

### 架構圖

```
┌────────────────────────────────────────────────┐
│              User Query              │
│   "分析這個 CSV 並畫圖"              │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│              LLM Agent               │
│   生成 Python 程式碼：              │
│   ```python                           │
│   import pandas as pd                │
│   import matplotlib.pyplot as plt     │
│   df = pd.read_csv(...)              │
│   df.plot()                          │
│   plt.savefig('output.png')          │
│   ```                                 │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│           Sandbox Environment        │
│   (Docker / WASM / 雲端)             │
│   安全執行生成的代碼                 │
└────────────────────────────────────────────────┘
                   ▼
┌────────────────────────────────────────────────┐
│            Output Image              │
└────────────────────────────────────────────────┘
```

### 實作考量

```python
# 安全執行環境設定
RESTRICTED_MODULES = ['os', 'sys', 'subprocess', 'socket']
ALLOWED_IMPORTS = ['pandas', 'matplotlib', 'numpy', 'seaborn']
TIMEOUT_SECONDS = 30
MAX_MEMORY_MB = 512
```

## 2.5 模式選擇決策樹

```
需要什麼樣的圖表能力？
    │
    ├───→ 需要彈性/通用性 → Code Interpreter
    │
    ├───→ 需要精確控制每種圖表 → Tool Calling
    │
    ├───→ 需要結構化數據交換 → Structured Output
    │
    └───→ 需要豐富視覺效果 → Generative UI

數據敏感性？
    │
    ├───→ 高敏感 → 本地沙盒 / WASM
    └───→ 低敏感 → 雲端 API
```

## 2.6 小結

- 四大模式各有優勢，選擇取決於具體需求
- Tool Calling 適合精細控制，Structured Output 適合解耦
- Code Interpreter 提供最大彈性，但需注意安全
- Generative UI 適合需要豐富視覺效果的場景
