# 第五章：驗證與測試策略

## 5.1 為什麼需要驗證？

SKILL 是 LLM Agent 的能力擴展，質量直接影響 Agent 的可靠性：

- **輸入驗證：** 确保使用者提供的參數正確
- **輸出驗證：** 確保生成的結果符合預期
- **邊界測試：** 處理異常情況
- **性能測試：** 確保响應速度

## 5.2 三層驗證體系

```
┌──────────────────────────────────────┐
│        第一層：JSON Schema 驗證         │
│   結構、類型、必填欄位檢查            │
└──────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────┐
│        第二層：業務邏輯驗證            │
│   數據範圍、業務規則、一致性檢查          │
└──────────────────────────────────────┘
                   ▼
┌──────────────────────────────────────┐
│        第三層：結果驗證                │
│   輸出格式、內容正確性、品質評估          │
└──────────────────────────────────────┘
```

## 5.3 JSON Schema 驗證實作

```python
import jsonschema
from typing import Dict, Any

class InputValidator:
    """輸入資料驗證器"""
    
    CHART_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "chartType": {
                "type": "string",
                "enum": ["bar", "line", "scatter", "histogram"]
            },
            "data": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "object"}
            },
            "xField": {"type": "string"},
            "yField": {"type": "string"},
            "title": {"type": "string"},
            "options": {"type": "object"}
        },
        "required": ["chartType", "data", "xField", "yField"]
    }
    
    def validate(self, input_data: Dict[str, Any]) -> tuple[bool, str]:
        """驗證輸入資料
        
        Returns:
            (is_valid, error_message)
        """
        try:
            jsonschema.validate(input_data, self.CHART_SCHEMA)
            
            # 業務邏輯驗證
            error = self._validate_business_logic(input_data)
            if error:
                return False, error
            
            return True, ""
            
        except jsonschema.ValidationError as e:
            return False, f"格式錯誤: {e.message}"
    
    def _validate_business_logic(self, data: Dict) -> str:
        """業務邏輯驗證"""
        # 檢查欄位存在性
        sample = data["data"][0]
        if data["xField"] not in sample:
            return f"缺少 X 軸欄位: {data['xField']}"
        if data["yField"] not in sample:
            return f"缺少 Y 軸欄位: {data['yField']}"
        
        # 檢查數值類型
        for i, item in enumerate(data["data"]):
            val = item.get(data["yField"])
            if not isinstance(val, (int, float)):
                return f"第 {i+1} 筆資料的 Y 值不是數字: {val}"
        
        return ""
```

## 5.4 單元測試實作

```python
import unittest
from chart_skill import ChartSkill

class TestChartSkill(unittest.TestCase):
    """圖表技能單元測試"""
    
    def setUp(self):
        self.skill = ChartSkill()
    
    def test_bar_chart_generation(self):
        """測試柱狀圖生成"""
        input_data = {
            "chartType": "bar",
            "data": [
                {"category": "A", "value": 100},
                {"category": "B", "value": 200}
            ],
            "xField": "category",
            "yField": "value",
            "title": "Test Chart"
        }
        
        result = self.skill.generate(input_data)
        
        self.assertTrue(result["success"])
        self.assertIn("imageBase64", result)
        self.assertEqual(result["metadata"]["format"], "png")
    
    def test_invalid_chart_type(self):
        """測試無效圖表類型"""
        input_data = {
            "chartType": "invalid_type",
            "data": [{"x": 1, "y": 2}],
            "xField": "x",
            "yField": "y"
        }
        
        with self.assertRaises(ValueError) as context:
            self.skill.generate(input_data)
        
        self.assertIn("圖表類型", str(context.exception))
    
    def test_empty_data(self):
        """測試空資料"""
        input_data = {
            "chartType": "bar",
            "data": [],
            "xField": "x",
            "yField": "y"
        }
        
        result = self.skill.generate(input_data)
        self.assertFalse(result["success"])
        self.assertIn("空", result["error"])

if __name__ == "__main__":
    unittest.main()
```

## 5.5 E2E 整合測試

```python
def test_end_to_end_workflow():
    """E2E 整合測試"""
    # 1. 模擬 LLM 呼叫
    llm_output = {
        "chartType": "line",
        "data": [
            {"month": "Jan", "sales": 100},
            {"month": "Feb", "sales": 150},
            {"month": "Mar", "sales": 200}
        ],
        "xField": "month",
        "yField": "sales",
        "title": "Q1 Sales Trend"
    }
    
    # 2. 驗證輸入
    validator = InputValidator()
    is_valid, error = validator.validate(llm_output)
    assert is_valid, f"驗證失敗: {error}"
    
    # 3. 生成圖表
    skill = ChartSkill()
    result = skill.generate(llm_output)
    
    # 4. 驗證結果
    assert result["success"], f"生成失敗: {result.get('error')}"
    assert "imageBase64" in result
    assert result["metadata"]["format"] == "png"
    
    # 5. 驗證圖片大小
    import base64
    img_data = base64.b64decode(result["imageBase64"].split(",")[1])
    assert len(img_data) > 1000, "圖片太小，可能生成失敗"
    
    print("✅ E2E 測試通過")
```

## 5.6 錯誤處理策略

| 錯誤類型 | 處理策略 | 回傳給 LLM 的資訊 |
|---------|---------|----------------|
| 驗證錯誤 | 立即失敗，回傳詳細錯誤 | 具體的警歧說明 |
| 渲染錯誤 | 重詥5.1實作參考、降級或切換方案 | 錯誤索引和建議 |
| 超時 | 設定合理超時，返回部分結果 | 狀態和已完成程度 |

## 5.7 小結

- 三層驗證保證可靠性：Schema → 業務邏輯 → 結果
- 自動化測試是 SKILL 的必要組成
- 良好的錯誤訊息幫助 LLM 理解問題
