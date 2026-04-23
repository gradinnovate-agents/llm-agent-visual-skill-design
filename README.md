# LLM Agent 視覺化 SKILL 設計 v2

> 詳細探討如何設計完整的 SKILL 架構，讓 LLM Agent 能夠有系統性地輸出高品質圖表與圖像。

## 課程簡介

本課程不只是教學生如何"使用"工具，更重要的是教導如何"設計"一個完整的 SKILL 系統。

**核心學習目標：**
- 掌握 SKILL 架構設計的語法與語意
- 理解熱門開源專案的設計模式
- 能夠獨立設計並實作圖表/圖像生成 SKILL

## 研究基礎

本課程基於 GitHub 上熱門實作的深度分析：

| 專案 | Stars | 設計特色 |
|------|-------|---------|
| `antvis/mcp-server-chart` | ⭐ 3996+ | MCP Server 架構，Tool-based 設計 |
| `hustcc/mcp-echarts` | ⭐ 226+ | Structured Output + 渲染引擎分離 |
| `StructuredLabs/preswald` | ⭐ 4287+ | WASM 在瀏覽器執行，離線可用 |
| `JimLiu/baoyu-skills` | ⭐ 150+ | Layout × Style 雙維度設計 |
| `bnomei/nereid` | ⭐ 50+ | Mermaid + AI Agent 整合 |
| `AlexMikhalev/beautiful-mermaid` | ⭐ 1+ | 多主題渲染、SVG/ASCII 輸出 |
| `KillianLucas/open-interpreter` | ⭐ 59k+ | Code Interpreter 模式，通用能力 |

## 課程大綱

| 章節 | 標題 | 核心內容 |
|-----|------|---------|
| 01 | [SKILL 設計基礎](docs/01-skill-design-fundamentals.md) | SKILL vs Tool vs Function、YAML Frontmatter 語法 |
| 02 | [設計模式深度剖析](docs/02-design-patterns-deep-dive.md) | 四大模式對比、選型決策樹 |
| 03 | [圖表 SKILL 設計實戰](docs/03-chart-skill-implementation.md) | 完整 SKILL.md 架構、references/、templates/、scripts/ |
| 04 | [圖像生成 SKILL 設計實戰](docs/04-image-skill-implementation.md) | Prompt 設計、樣式系統、一致性保證 |
| 05 | [驗證與測試策略](docs/05-validation-testing.md) | JSON Schema、單元測試、E2E 驗證 |
| 06 | [案例研究：熱門實作剖析](docs/06-case-studies.md) | Preswald、baoyu-infographic、nereid 深度分析 |

## 完整 SKILL 架構範例

本課程提供兩個完整的 SKILL 實作：

```
examples/
├── chart_skill/
│   ├── SKILL.md              # 主技能文件 (YAML frontmatter + 使用說明)
│   ├── references/
│   │   ├── chart-types.md    # 圖表類型參考手冊
│   │   └── color-palettes.md # 配色方案參考
│   ├── templates/
│   │   ├── bar_chart.json    # 柱狀圖模板
│   │   └── line_chart.json   # 折線圖模板
│   └── scripts/
│       ├── validate.py       # 輸入驗證腳本
│       └── generate.py       # 圖表生成腳本
└── image_skill/
    ├── SKILL.md
    ├── references/
    ├── templates/
    └── scripts/
```

## 快速開始

```bash
# 複製儲存庫
git clone https://github.com/gradinnovate-agents/llm-agent-visual-skill-design.git
cd llm-agent-visual-skill-design

# 安裝依賴
pip install -r examples/requirements.txt

# 執行驗證
python examples/verification/verify_chart_skill.py
python examples/verification/verify_image_skill.py
```

## 授權

MIT License

---

<p align="center">
本課程由 <a href="https://github.com/gradinnovate-agents">gradinnovate-agents</a> 維護
</p>
