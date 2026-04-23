"""
範例 5: LLM 整合示例
演示如何將圖表/圖像生成 SKILL 整合到 LLM Agent 中
"""

import json
from typing import Dict, Any, List


class LLMIntegrationDemo:
    """
    LLM 整合示例
    
    演示如何為 LLM 提供 Tool Definition，
    讓 LLM 能夠使用圖表/圖像生成能力
    """
    
    @staticmethod
    def get_chart_tool_definition() -> Dict[str, Any]:
        """
        圖表生成 Tool 定義
        
        這個定義會被提供給 LLM，讓 LLM 知道如何使用圖表生成功能
        """
        return {
            "type": "function",
            "function": {
                "name": "generate_chart",
                "description": """生成資料可視化圖表。支援柱狀圖、折線圖、散佈圖、直方圖。

使用指南:
- 比較不同類別的數值 → 使用 "bar" 類型
- 顯示時間趨勢 → 使用 "line" 類型
- 探索變數關係 → 使用 "scatter" 類型
- 數據應為列表格式，每個元素是包含欄位值的字典

範例:
{
  "chartType": "bar",
  "data": [
    {"month": "1月", "sales": 100},
    {"month": "2月", "sales": 150}
  ],
  "xField": "month",
  "yField": "sales",
  "title": "月度銷售額"
}""",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chartType": {
                            "type": "string",
                            "enum": ["bar", "line", "scatter", "histogram"],
                            "description": "圖表類型"
                        },
                        "data": {
                            "type": "array",
                            "description": "圖表數據，每個元素是包含欄位值的字典"
                        },
                        "xField": {
                            "type": "string",
                            "description": "X 軸對應的資料欄位名稱"
                        },
                        "yField": {
                            "type": "string",
                            "description": "Y 軸對應的資料欄位名稱"
                        },
                        "title": {
                            "type": "string",
                            "description": "圖表標題"
                        }
                    },
                    "required": ["chartType", "data", "xField", "yField"]
                }
            }
        }
    
    @staticmethod
    def get_image_tool_definition() -> Dict[str, Any]:
        """
        圖像生成 Tool 定義
        """
        return {
            "type": "function",
            "function": {
                "name": "generate_image",
                "description": "生成 AI 圖像。支援多種風格控制。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "圖像描述 prompt"
                        },
                        "style": {
                            "type": "string",
                            "enum": ["photorealistic", "illustration", "sketch", "3d-render", "anime", "minimalist"],
                            "description": "圖像風格"
                        },
                        "size": {
                            "type": "string",
                            "enum": ["256x256", "512x512", "1024x1024"],
                            "description": "圖像尺寸"
                        }
                    },
                    "required": ["prompt"]
                }
            }
        }
    
    @staticmethod
    def simulate_llm_conversation():
        """模擬 LLM 使用 Tool 的對話流程"""
        
        print("模擬 LLM Agent 對話")
        print("=" * 60)
        
        # 用戶輸入
        user_message = "請幫我畫一個顯示上半年各月份銷售額的圖表"
        print(f"\n用戶: {user_message}")
        
        # LLM 分析，決定使用哪個 Tool
        print("\nLLM 思考:")
        print("  1. 用戶想要可視化數據 → 需要圖表生成")
        print("  2. 顯示時間趨勢 → 選擇 line 圖表")
        print("  3. 準備調用 generate_chart Tool")
        
        # LLM 生成的參數
        tool_call = {
            "name": "generate_chart",
            "arguments": {
                "chartType": "line",
                "data": [
                    {"month": "1月", "sales": 120},
                    {"month": "2月", "sales": 190},
                    {"month": "3月", "sales": 150},
                    {"month": "4月", "sales": 280},
                    {"month": "5月", "sales": 220},
                    {"month": "6月", "sales": 310}
                ],
                "xField": "month",
                "yField": "sales",
                "title": "上半年銷售趨勢"
            }
        }
        
        print(f"\nLLM Tool 呼叫:")
        print(json.dumps(tool_call, indent=2, ensure_ascii=False))
        
        # 執行 Tool
        print("\n執行結果:")
        print("  ✓ 圖表生成成功")
        print("  ✓ 返回 base64 編碼的圖片")
        
        # LLM 回覆用戶
        print("\nLLM 回覆: 已為您生成上半年銷售趨勢圖。6 月的銷售額達到 310 萬，
是今年以來的最高點。")


def demo():
    """演示 LLM 整合"""
    demo_obj = LLMIntegrationDemo()
    
    print("LLM 整合示例")
    print("=" * 60)
    
    # 顯示 Tool 定義
    print("\n1. 圖表生成 Tool 定義:")
    chart_tool = demo_obj.get_chart_tool_definition()
    print(json.dumps(chart_tool, indent=2, ensure_ascii=False))
    
    print("\n2. 圖像生成 Tool 定義:")
    image_tool = demo_obj.get_image_tool_definition()
    print(json.dumps(image_tool, indent=2, ensure_ascii=False))
    
    # 模擬對話
    print("\n")
    demo_obj.simulate_llm_conversation()


if __name__ == "__main__":
    demo()
