# 第四章：圖像生成 SKILL 設計實戰

## 4.1 圖像生成 SKILL 的特殊性

相比於圖表 SKILL，圖像生成 SKILL 有以下特點：

1. **不確定性：** 同一個 prompt 可能產生不同結果
2. **風格控制：** 需要明確的風格系統
3. **一致性：** 多張圖片需要維持相同風格
4. **質量評估：** 難以程式化判斷好壞

## 4.2 完整 SKILL 架構範例

```yaml
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
| `outpainting` | 延伸補圖 | 擴展畫面 |

## 風格系統

為了保持一致性，本技能提供預設風格模板：

### 預設風格

| 風格名稱 | 描述 | 配置參數 |
|---------|------|---------|
| `photorealistic` | 写實攝影 | high detail, 8k, professional photography |
| `illustration` | 插畫 | digital art, clean lines, vibrant colors |
| `sketch` | 手繪 | pencil sketch, monochrome, artistic |
| `3d-render` | 3D 渲染 | 3d render, blender, octane render |
| `anime` | 動漫風 | anime style, studio ghibli, cel shading |
| `minimalist` | 極簡 | minimal design, flat colors, geometric |

### 風格一致性保證

```python
# 使用 seed 確保可複現
{
  "prompt": "...",
  "style": "illustration",
  "seed": 42,  # 固定 seed
  "negative_prompt": "blurry, low quality"
}
```

## Prompt Engineering 指南

### 結構化 Prompt 模板

```
[主體描述], [風格修飾詞], [技術參數]

例如：
"一隻橘色的貓坐在窗邊, 數位藝術風格, 高細節, 8k"
```

### 重要要素

| 要素 | 作用 | 範例 |
|------|------|------|
| Subject | 主體 | a cat, a landscape, a character |
| Style | 風格 | digital art, oil painting, photo |
| Quality | 品質 | high quality, detailed, 8k |
| Lighting | 光照 | natural light, dramatic lighting |
| Composition | 構圖 | rule of thirds, centered |

## 輸入驗證

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "prompt": {
      "type": "string",
      "minLength": 1,
      "maxLength": 1000
    },
    "style": {
      "type": "string",
      "enum": ["photorealistic", "illustration", "sketch", "3d-render", "anime", "minimalist"]
    },
    "size": {
      "type": "string",
      "enum": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"]
    },
    "seed": {"type": "integer"},
    "negative_prompt": {"type": "string"},
    "format": {
      "type": "string",
      "enum": ["url", "base64"],
      "default": "url"
    }
  },
  "required": ["prompt"]
}
```

## 安全與合規

### 內容過濾

- 自動檢港並過濾不適當內容
- 提供透明的過濾原因

### 版權標註

```python
{
  "watermark": "AI Generated",
  "metadata": {
    "generator": "DALL-E 3",
    "prompt_hash": "sha256_of_prompt"
  }
}
```

## 相關資源

- `references/style-gallery.md` - 風格參考手冊
- `references/prompt-templates/` - 預設 prompt 模板
- `templates/standard-config.json` - 標準配置
- `scripts/validate.py` - 輸入驗證腳本
- `scripts/generate.py` - 圖像生成腳本
