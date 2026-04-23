"""
範例 1: 基本圖表生成 SKILL
演示如何實作一個簡單的圖表生成器，支援多種圖表類型
"""

import matplotlib.pyplot as plt
import jsonschema
from typing import List, Dict, Optional, Union, Any
import base64
from io import BytesIO


class ChartSkill:
    """
    圖表生成 SKILL - 支援多種圖表類型
    
    使用範例:
        skill = ChartSkill()
        result = skill.generate({
            "chartType": "bar",
            "data": [
                {"month": "1月", "sales": 120},
                {"month": "2月", "sales": 200}
            ],
            "xField": "month",
            "yField": "sales",
            "title": "月度銷售額"
        })
    """
    
    INPUT_SCHEMA = {
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
    
    def __init__(self, theme: str = "default"):
        self.theme = theme
        self._setup_style()
    
    def _setup_style(self):
        """設定圖表樣式 - 遵循 Tufte 原則"""
        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.edgecolor'] = '#333333'
        plt.rcParams['axes.labelcolor'] = '#333333'
        plt.rcParams['xtick.color'] = '#333333'
        plt.rcParams['ytick.color'] = '#333333'
        # 移除上方和右方邊框
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """驗證輸入資料"""
        try:
            jsonschema.validate(input_data, self.INPUT_SCHEMA)
            
            # 業務邏輯驗證
            if not input_data["data"]:
                raise ValueError("資料不能為空")
            
            sample = input_data["data"][0]
            if input_data["xField"] not in sample:
                raise ValueError(f"缺少 X 軸欄位: {input_data['xField']}")
            if input_data["yField"] not in sample:
                raise ValueError(f"缺少 Y 軸欄位: {input_data['yField']}")
            
            return True
            
        except jsonschema.ValidationError as e:
            raise ValueError(f"輸入驗證失敗: {e.message}")
    
    def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """主入口：生成圖表"""
        # 1. 驗證輸入
        self.validate_input(input_data)
        
        # 2. 根據類型分派
        chart_type = input_data["chartType"]
        generator_method = getattr(self, f"_generate_{chart_type}", None)
        
        if not generator_method:
            raise ValueError(f"不支援的圖表類型: {chart_type}")
        
        # 3. 生成圖表
        fig = generator_method(input_data)
        
        # 4. 轉換為輸出格式
        options = input_data.get("options", {})
        result = self._format_output(fig, options)
        
        plt.close(fig)
        return result
    
    def _generate_bar(self, input_data: Dict) -> plt.Figure:
        """生成柱狀圖"""
        data = input_data["data"]
        x_field = input_data["xField"]
        y_field = input_data["yField"]
        
        categories = [d[x_field] for d in data]
        values = [d[y_field] for d in data]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, values, color='#2c3e50', alpha=0.8)
        
        # 添加數值標籤（direct label）
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
        
        # 標題和軸標籤
        if "title" in input_data:
            ax.set_title(input_data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(x_field)
        ax.set_ylabel(y_field)
        ax.grid(False)
        
        return fig
    
    def _generate_line(self, input_data: Dict) -> plt.Figure:
        """生成折線圖"""
        data = input_data["data"]
        x_field = input_data["xField"]
        y_field = input_data["yField"]
        
        x_values = [d[x_field] for d in data]
        y_values = [d[y_field] for d in data]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_values, y_values, marker='o', linewidth=2, color='#2980b9')
        
        if "title" in input_data:
            ax.set_title(input_data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(x_field)
        ax.set_ylabel(y_field)
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _generate_scatter(self, input_data: Dict) -> plt.Figure:
        """生成散佈圖"""
        data = input_data["data"]
        x_field = input_data["xField"]
        y_field = input_data["yField"]
        
        x_values = [d[x_field] for d in data]
        y_values = [d[y_field] for d in data]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(x_values, y_values, alpha=0.6, s=100, color='#e74c3c')
        
        if "title" in input_data:
            ax.set_title(input_data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(x_field)
        ax.set_ylabel(y_field)
        
        return fig
    
    def _generate_histogram(self, input_data: Dict) -> plt.Figure:
        """生成直方圖"""
        data = input_data["data"]
        y_field = input_data["yField"]
        
        values = [d[y_field] for d in data]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(values, bins=10, color='#27ae60', alpha=0.7, edgecolor='white')
        
        if "title" in input_data:
            ax.set_title(input_data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(y_field)
        ax.set_ylabel("頻率")
        
        return fig
    
    def _format_output(self, fig: plt.Figure, options: Dict) -> Dict[str, Any]:
        """格式化輸出"""
        format_type = options.get("format", "png")
        dpi = options.get("dpi", 150)
        
        buffer = BytesIO()
        fig.savefig(buffer, format=format_type, dpi=dpi, bbox_inches='tight')
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "imageBase64": f"data:image/{format_type};base64,{image_base64}",
            "metadata": {
                "format": format_type,
                "dpi": dpi,
                "width": fig.get_figwidth() * dpi,
                "height": fig.get_figheight() * dpi
            }
        }


def demo():
    """演示使用"""
    skill = ChartSkill()
    
    # 示例資料
    data = [
        {"month": "1月", "sales": 120, "profit": 30},
        {"month": "2月", "sales": 200, "profit": 50},
        {"month": "3月", "sales": 150, "profit": 40},
        {"month": "4月", "sales": 280, "profit": 70},
        {"month": "5月", "sales": 220, "profit": 55}
    ]
    
    # 測試柱狀圖
    print("生成柱狀圖...")
    result = skill.generate({
        "chartType": "bar",
        "data": data,
        "xField": "month",
        "yField": "sales",
        "title": "月度銷售額",
        "options": {"format": "png", "dpi": 150}
    })
    print(f"✓ 柱狀圖生成成功: {result['metadata']}")
    
    # 測試折線圖
    print("\n生成折線圖...")
    result = skill.generate({
        "chartType": "line",
        "data": data,
        "xField": "month",
        "yField": "profit",
        "title": "月度利潤趨勢"
    })
    print(f"✓ 折線圖生成成功: {result['metadata']}")


if __name__ == "__main__":
    demo()
