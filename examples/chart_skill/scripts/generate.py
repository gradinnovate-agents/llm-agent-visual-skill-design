#!/usr/bin/env python3
"""
圖表生成腳本

使用方式:
    python generate.py <input.json> <output.png>
"""

import json
import sys
import os

# 添加父目錄到路徑，以便匯入主模組
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from examples_01_basic_chart_skill import ChartSkill


def main():
    if len(sys.argv) < 3:
        print("使用方式: python generate.py <input.json> <output.png>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # 讀取輸入
    with open(input_file) as f:
        input_data = json.load(f)
    
    # 生成圖表
    skill = ChartSkill()
    result = skill.generate(input_data)
    
    if result["success"]:
        # 保存圖片
        import base64
        img_data = base64.b64decode(result["imageBase64"].split(",")[1])
        with open(output_file, "wb") as f:
            f.write(img_data)
        print(f"圖表已保存至: {output_file}")
    else:
        print(f"生成失敗: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
