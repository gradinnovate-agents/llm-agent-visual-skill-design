# 第六章：案例研究：熱門實作剖析

## 6.1 Preswald: WASM 資料應用框架

### 專案概覽

- **Repo:** `StructuredLabs/preswald`
- **Stars:** ⭐ 4,287+
- **核心特色:** 在瀏覽器中執行完整的 Python 資料工作流

### 設計亮點

```
┌────────────────────────────────────┐
│     Python 代碼 (伺服器端)      │
│   - Pandas, Plotly, Matplotlib      │
│   - DuckDB 查詢                    │
└────────────────────────────────────┘
                   ▼
┌────────────────────────────────────┐
│        WASM 編譯/打包              │
└────────────────────────────────────┘
                   ▼
┌────────────────────────────────────┐
│   瀏覽器執行 (Pyodide)            │
│   - 完全離線可用                  │
│   - 無需後端伺服器                  │
└────────────────────────────────────┘
```

### 對 SKILL 設計的啟發

1. **沙盒化執行:** 可以安全地執行任意用戶代碼
2. **一體式部署:** 單一文件即可分享
3. **離線能力:** 不依賴網路連接

## 6.2 baoyu-infographic: 雙維度設計

### 專案概覽

- **Repo:** `JimLiu/baoyu-skills`
- **核心特色:** Layout × Style 雙維度設計

### 設計亮點

```
         Layout (佈局)
              │
    ┌─────────┼─────────┐
    │         │         │
←───→   ←───→   ←───→
linear   bento    hub-
progress grid     spoke

              ×

         Style (樣式)
              │
    ┌─────────┼─────────┐
    │         │         │
🎨        ✏️        🖼️
craft-   chalkboard pixel
handmade           art
```

### 應用於圖表 SKILL

```yaml
# 可以採用的設計
chart_generation:
  layout:  # 圖表佈局
    - single-chart      # 單圖
    - comparison        # 並列比較
    - dashboard         # 儀表板
    
  style:  # 視覺樣式
    - minimal           # 極簡
    - corporate         # 商業
    - colorful          # 色彩
```

## 6.3 nereid: AI + Mermaid 整合

### 專案概覽

- **Repo:** `bnomei/nereid`
- **Stars:** ⭐ 50+
- **核心特色:** 與 AI Agent 協作創建 Mermaid 圖表

### 交互流程

```
用戶: "幫我畫一個系統架構圖"
         │
         ▼
LLM Agent: "我來為您創建一個系統架構圖"
         │
         ▼
      生成 Mermaid 語法
         │
         ▼
    graph TD
    A[前端] --> B[API 層]
    B --> C[數據層]
         │
         ▼
      渲染為 SVG/PNG
         │
         ▼
    顯示給用戶
         │
         ▼
用戶: "把 API 層改成微服務架構"
         │
    (重複上述流程)
```

### 啟發

- **人機協作:** AI 輔助，人類檢視和修改
- **迭代改進:** 快速迭代圖表設計
- **文本基礎:** 方便版本控制和復原

## 6.4 beautiful-mermaid: 多主題渲染

### 專案概覽

- **Repo:** `AlexMikhalev/beautiful-mermaid`
- **特色:** 15 種內建主題

### 主題系統設計

```python
THEMES = {
    "default": {"bg": "#ffffff", "primary": "#1e1e1e"},
    "dark": {"bg": "#1e1e1e", "primary": "#ffffff"},
    "forest": {"bg": "#f0fdf4", "primary": "#166534"},
    "ocean": {"bg": "#eff6ff", "primary": "#1e40af"},
    # ... 更多主題
}
```

### 應用於圖表 SKILL

```yaml
# 設計一個可擴展的主題系統
theme_system:
  base_themes:
    - default
    - dark
    - colorful
  
  customization:
    - primary_color
    - secondary_color
    - background
    - font_family
```

## 6.5 綜合比較

| 專案 | 核心特色 | 學習重點 | 應用場景 |
|-----|---------|---------|---------|
| Preswald | WASM 執行 | 沙盒化、離線能力 | 資料應用 |
| baoyu | 雙維度設計 | 分層抽象 | 豐富視覺 |
| nereid | 人機協作 | 迭代工作流 | 文本圖表 |
| beautiful-mermaid | 主題系統 | 可擴展設計 | 多樣式輸出 |

## 6.6 小結

- 每個專案都有其獨特的設計思想
- 可以根據需求組合不同專案的優點
- 關鍵是找到適合自己場景的設計模式
