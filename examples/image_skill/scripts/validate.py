#!/usr/bin/env python3
"""
圖像生成 SKILL 輸入驗證腳本

使用方式:
    python validate.py <input.json>
    或
    python validate.py  # 使用內建測試案例
"""

import json
import jsonschema
import sys
from typing import Dict, Any, Tuple


IMAGE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
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
            "default": "illustration"
        },
        "size": {
            "type": "string",
            "enum": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"],
            "default": "1024x1024"
        },
        "seed": {
            "type": "integer",
            "description": "隨機種子"
        },
        "negative_prompt": {
            "type": "string"
        },
        "format": {
            "type": "string",
            "enum": ["url", "base64"],
            "default": "url"
        }
    },
    "required": ["prompt"]
}


def validate_input(input_data: Dict[str, Any]) -> Tuple[bool, str]:
    """驗證輸入資料"""
    try:
        # Schema 驗證
        jsonschema.validate(input_data, IMAGE_SCHEMA)
        
        # 業務邏輯驗證
        prompt = input_data.get("prompt", "")
        
        # 提示詞長度檢查
        if len(prompt) < 3:
            return False, "prompt 太短，請提供更詳細的描述"
        
        # 提示詞內容檢查（簡單版）
        dangerous_keywords = ["violence", "hate", "illegal"]
        for keyword in dangerous_keywords:
            if keyword in prompt.lower():
                return False, f"發現不適當關鍵字: {keyword}"
        
        return True, "驗證通過"
        
    except jsonschema.ValidationError as e:
        return False, f"格式錯誤: {e.message}"


def run_tests():
    """執行測試案例"""
    test_cases = [
        {
            "name": "有效輸入 - 基本提示詞",
            "input": {
                "prompt": "一隻可愛的貓咪"
            },
            "expected_valid": True
        },
        {
            "name": "有效輸入 - 完整參數",
            "input": {
                "prompt": "商人在辦公室使用電腦",
                "style": "illustration",
                "size": "1024x1024",
                "seed": 42
            },
            "expected_valid": True
        },
        {
            "name": "無效輸入 - 缺少 prompt",
            "input": {
                "style": "anime"
            },
            "expected_valid": False
        },
        {
            "name": "無效輸入 - prompt 過短",
            "input": {
                "prompt": "ab"
            },
            "expected_valid": False
        }
    ]
    
    print("圖像生成 SKILL 輸入驗證測試")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        is_valid, message = validate_input(test["input"])
        success = is_valid == test["expected_valid"]
        
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"\n{status}: {test['name']}")
        print(f"    驗證結果: {message}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'=' * 50}")
    print(f"結果: {passed} 通過, {failed} 失敗")
    return failed == 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 從檔案讀取輸入
        with open(sys.argv[1]) as f:
            input_data = json.load(f)
        is_valid, message = validate_input(input_data)
        print(f"驗證結果: {message}")
        sys.exit(0 if is_valid else 1)
    else:
        # 執行測試
        success = run_tests()
        sys.exit(0 if success else 1)
