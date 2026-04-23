"""
範例 4: 圖像生成 SKILL
演示如何實作一個結構化的圖像生成 SKILL
"""

import jsonschema
from typing import Dict, Any, Optional


class ImageGenerationSkill:
    """
    圖像生成 SKILL
    
    支援多種風格控制和輸出格式
    """
    
    INPUT_SCHEMA = {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000,
                "description": "圖像描述 prompt"
            },
            "style": {
                "type": "string",
                "enum": ["photorealistic", "illustration", "sketch", "3d-render", "anime", "minimalist"],
                "default": "illustration",
                "description": "風格"
            },
            "size": {
                "type": "string",
                "enum": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"],
                "default": "1024x1024"
            },
            "seed": {
                "type": "integer",
                "description": "隨機種子，用於可複現"
            },
            "negative_prompt": {
                "type": "string",
                "description": "負面描述，避免的內容"
            },
            "format": {
                "type": "string",
                "enum": ["url", "base64"],
                "default": "url"
            }
        },
        "required": ["prompt"]
    }
    
    # 風格修飾詞
    STYLE_MODIFIERS = {
        "photorealistic": "professional photography, high detail, 8k, photorealistic",
        "illustration": "digital art, clean lines, vibrant colors, professional illustration",
        "sketch": "pencil sketch, monochrome, artistic drawing, hand-drawn",
        "3d-render": "3d render, blender, octane render, professional 3d modeling",
        "anime": "anime style, studio ghibli, cel shading, japanese animation",
        "minimalist": "minimal design, flat colors, geometric shapes, clean"
    }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """驗證輸入"""
        try:
            jsonschema.validate(input_data, self.INPUT_SCHEMA)
            return True
        except jsonschema.ValidationError as e:
            raise ValueError(f"輸入驗證失敗: {e.message}")
    
    def generate_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        生成完整的 prompt
        
        結構: [主體描述] + [風格修飾] + [負面描述]
        """
        base_prompt = input_data["prompt"]
        style = input_data.get("style", "illustration")
        style_modifier = self.STYLE_MODIFIERS.get(style, "")
        negative = input_data.get("negative_prompt", "")
        
        # 組合完整 prompt
        full_prompt = f"{base_prompt}, {style_modifier}"
        
        if negative:
            full_prompt += f" | negative: {negative}"
        
        return full_prompt
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成圖像
        
        注意: 這是演示版本，實際使用時需要整合 DALL-E 或 Stable Diffusion API
        """
        # 1. 驗證輸入
        self.validate_input(input_data)
        
        # 2. 生成完整 prompt
        full_prompt = self.generate_prompt(input_data)
        
        # 3. 模擬輸出（實際使用時接入真實 API）
        # 這裡演示結構化的輸出
        return {
            "success": True,
            "prompt": full_prompt,
            "enhanced_prompt": full_prompt,
            "style": input_data.get("style", "illustration"),
            "size": input_data.get("size", "1024x1024"),
            "seed": input_data.get("seed"),
            "metadata": {
                "model": "dall-e-3",  # 或 "stable-diffusion-xl"
                "format": input_data.get("format", "url")
            },
            "note": "這是演示版本。實際使用時請整合 OpenAI DALL-E 或 Stability AI API。"
        }
    
    def get_style_guide(self) -> Dict[str, str]:
        """獲取風格指南"""
        return {
            "photorealistic": "寫實攝影風格，適合產品照、人物写真",
            "illustration": "數位插畫風格，適合文章插圖、說明圖",
            "sketch": "手繪風格，適合草圖、概念圖",
            "3d-render": "3D 渲染風格，適合產品展示、建範",
            "anime": "動漫風格，適合卡通、角色設計",
            "minimalist": "極簡風格，適合簡報、網頁設計"
        }


def demo():
    """演示圖像生成 SKILL"""
    skill = ImageGenerationSkill()
    
    print("圖像生成 SKILL 演示")
    print("=" * 50)
    
    # 範例 1: 商業插畫
    print("\n範例 1: 商業插畫")
    result = skill.generate({
        "prompt": "一個商人在現代辦公室中使用電腦工作",
        "style": "illustration",
        "size": "1024x1024"
    })
    print(f"生成的 prompt: {result['enhanced_prompt']}")
    
    # 範例 2: 寫實風格
    print("\n範例 2: 寫實風格")
    result = skill.generate({
        "prompt": "日落時分的山景",
        "style": "photorealistic",
        "size": "1792x1024",
        "negative_prompt": "blurry, low quality, watermark"
    })
    print(f"生成的 prompt: {result['enhanced_prompt']}")
    
    # 範例 3: 一致性保證
    print("\n範例 3: 一致性保證（使用 seed）")
    result = skill.generate({
        "prompt": "可愛的貓咪",
        "style": "anime",
        "seed": 42,
        "size": "512x512"
    })
    print(f"使用 seed=42 以保證可複現")
    
    # 顯示風格指南
    print("\n風格指南:")
    for style, desc in skill.get_style_guide().items():
        print(f"  {style}: {desc}")


if __name__ == "__main__":
    demo()
