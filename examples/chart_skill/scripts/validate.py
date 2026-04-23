#!/usr/bin/env python3
"""
圖表 SKILL 輸入驗證腳本

使用方式:
    python validate.py <input.json>
    或
    python validate.py  # 使用內建測試案例
"""

import json
import jsonschema
import sys
from typing import Dict, Any, Tuple


CHART_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "chartType": {
            "type": "string",
            "enum": ["bar", "line", "scatter", "histogram", "pie"],
            "description": "圖表類型"
        },
        "data": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "object"},
            "description": "圖表資料"
        },
        "xField": {
            "type": "string",
            "description": "X 軸欄位"
        },
        "yField": {
            "type": "string",
            "description": "Y 軸欄位"
        },
        "title": {
            "type": "string",
            "description": "圖表標題"
        },
        "options": {
            "type": "object",
            "description": "選項"
        }
    },
    "required": ["chartType", "data", "xField", "yField"]
}


def validate_input(input_data: Dict[str, Any]) -> Tuple[bool, str]:
    """驗證輸入資料"""
    try:
        # Schema 驗證
        jsonschema.validate(input_data, CHART_SCHEMA)
        
        # 業務邏輯驗證
        if not input_data["data"]:
            return False, "資料不能為空"
        
        sample = input_data["data"][0]
        if input_data["xField"] not in sample:
            return False, f"缺少 X 軸欄位: {input_data['xField']}"
        if input_data["yField"] not in sample:
            return False, f"缺少 Y 軸欄位: {input_data['yField']}"
        
        # 檢查數值類型
        for i, item in enumerate(input_data["data"]):
            val = item.get(input_data["yField"])
            if not isinstance(val, (int, float)):
                return False, f"第 {i+1} 筆資料的 Y 值不是數字: {val}"
        
        return True, "驗證通過"
        
    except jsonschema.ValidationError as e:
        return False, f"格式錯誤: {e.message}"


def run_tests():
    """執行測試案例"""
    test_cases = [
        {
            "name": "有效輸入 - 柱狀圖",
            "input": {
                "chartType": "bar",
                "data": [
                    {"month": "1月", "sales": 100},
                    {"month": "2月", "sales": 200}
                ],
                "xField": "month",
                "yField": "sales",
                "title": "銷售額"
            },
            "expected_valid": True
        },
        {
            "name": "無效輸入 - 缺少必填欄位",
            "input": {
                "chartType": "bar",
                "data": [{"x": 1}]
                # 缺少 xField, yField
            },
            "expected_valid": False
        },
        {
            "name": "無效輸入 - 空資料",
            "input": {
                "chartType": "bar",
                "data": [],
                "xField": "x",
                "yField": "y"
            },
            "expected_valid": False
        },
        {
            "name": "無效輸入 - 錯誤的圖表類型",
            "input": {
                "chartType": "invalid_type",
                "data": [{"x": 1, "y": 2}],
                "xField": "x",
                "yField": "y"
            },
            "expected_valid": False
        }
    ]
    
    print("圖表 SKILL 輸入驗證測試")
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
