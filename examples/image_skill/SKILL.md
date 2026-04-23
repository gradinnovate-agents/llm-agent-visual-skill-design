---
name: image-generation-skill
version: "1.0.0"
description: |
  生成 AI 圖像的技能，支援多種風格控制和輸出格式。
  整合 DALL-E、Stable Diffusion 等模型。
trigger: |
  當用戶需要生成、創建、製作圖片時使用，如：
  - "生成一張...的圖片"
  - "創建...風格的插圖"
  - "畫一張..."
  - "為...製作視覺素材"
metadata:
  hermes:
    tags: [image-generation, ai-art, dalle, stable-diffusion]
    related_skills: [content-creation, marketing]
    category: creative
---

# 圖像生成技能

## 支援的生成模式

| 模式 | 說明 | 適用場景 |
|-----|------|---------|
| `text-to-image` | 文字生成圖片 | 一般場景 |
| `image-to-image` | 圖片轉換 | 風格迄移、修改 |
| `inpainting` | 局部重繪 | 修復、替換部分內容 |

## 風格系統

### 預設風格

| 風格名稱 | 描述 |
|---------|------|
| `photorealistic` | 寫實攝影風格，適合產品照、人物写真 |
| `illustration` | 數位插畫風格，適合文章插圖、說明圖 |
| `sketch` | 手繪風格，適合草圖、概念圖 |
| `3d-render` | 3D 渲染風格，適合產品展示、建範 |
| `anime` | 動漫風格，適合卡通、角色設計 |
| `minimalist` | 極簡風格，適合簡報、網頁設計 |

### 風格一致性保證

使用 `seed` 參數確保可複現的結果：

```json
{
  "prompt": "...",
  "style": "illustration",
  "seed": 42
}
```

## Prompt Engineering 指南

### 結構化 Prompt 模板

```
[主體描述], [風格修飾詞], [技術參數]

例如：
"一隻橘色的貓坐在窗邊, 數位藝術風格, 高細節, 8k"
```

## 輸入驗證

所有輸入都會經過 JSON Schema 驗證，見 `scripts/validate.py`。

## 相關資源

- `references/style-gallery.md` - 風格參考手冊
- `templates/standard-config.json` - 標準配置
- `scripts/validate.py` - 輸入驗證腳本
