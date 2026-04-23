"""
範例 2: Structured Output 模式實作
演示 LLM 輸出 JSON → 渲染引擎轉換 的流程
"""

import json
import matplotlib.pyplot as plt
from typing import Dict, Any
import base64
from io import BytesIO


class StructuredChartSkill:
    """
    Structured Output 模式圖表生成器
    
    設計理念:
    1. LLM 只負責輸出結構化的 JSON
    2. 渲染引擎負責轉換為圖片
    3. 兩者解耦，可獨立更新
    """
    
    # 輸出 JSON 的結構定義
    OUTPUT_SCHEMA = {
        "type": "object",
        "properties": {
            "chart_type": {"type": "string", "enum": ["bar", "line", "pie"]},
            "title": {"type": "string"},
            "x_label": {"type": "string"},
            "y_label": {"type": "string"},
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string"},
                        "value": {"type": "number"},
                        "color": {"type": "string"}
                    }
                }
            }
        },
        "required": ["chart_type", "title", "data"]
    }
    
    def render(self, structured_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        將結構化數據渲染為圖表
        
        Args:
            structured_data: LLM 輸出的 JSON 物件
        
        Returns:
            包含 base64 圖片的結果物件
        """
        chart_type = structured_data["chart_type"]
        
        if chart_type == "bar":
            fig = self._render_bar(structured_data)
        elif chart_type == "line":
            fig = self._render_line(structured_data)
        elif chart_type == "pie":
            fig = self._render_pie(structured_data)
        else:
            raise ValueError(f"不支援的圖表類型: {chart_type}")
        
        return self._to_output(fig, structured_data)
    
    def _render_bar(self, data: Dict) -> plt.Figure:
        """渲染柱狀圖"""
        labels = [d["label"] for d in data["data"]]
        values = [d["value"] for d in data["data"]]
        colors = [d.get("color", "#3498db") for d in data["data"]]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(labels, values, color=colors, alpha=0.8)
        
        # 添加數值標籤
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
        
        ax.set_title(data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(data.get("x_label", ""))
        ax.set_ylabel(data.get("y_label", ""))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        return fig
    
    def _render_line(self, data: Dict) -> plt.Figure:
        """渲染折線圖"""
        labels = [d["label"] for d in data["data"]]
        values = [d["value"] for d in data["data"]]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(labels, values, marker='o', linewidth=2, markersize=8, color='#e74c3c')
        
        ax.set_title(data["title"], fontsize=14, fontweight='bold')
        ax.set_xlabel(data.get("x_label", ""))
        ax.set_ylabel(data.get("y_label", ""))
        ax.grid(True, alpha=0.3)
        
        return fig
    
    def _render_pie(self, data: Dict) -> plt.Figure:
        """渲染圓餅圖"""
        labels = [d["label"] for d in data["data"]]
        values = [d["value"] for d in data["data"]]
        colors = [d.get("color", None) for d in data["data"]]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title(data["title"], fontsize=14, fontweight='bold')
        
        return fig
    
    def _to_output(self, fig: plt.Figure, original_data: Dict) -> Dict[str, Any]:
        """轉換為輸出格式"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "success": True,
            "imageBase64": f"data:image/png;base64,{image_base64}",
            "structured_data": original_data,
            "metadata": {
                "format": "png",
                "chart_type": original_data["chart_type"]
            }
        }


def demo_llm_output():
    """演示 LLM 輸出的結構化數據"""
    
    # 模擬 LLM 輸出的 JSON
    llm_output = {
        "chart_type": "bar",
        "title": "2024 年 Q1 各部門收益",
        "x_label": "部門",
        "y_label": "收益 (萬元)",
        "data": [
            {"label": "銷售部", "value": 450, "color": "#3498db"},
            {"label": "市場部", "value": 320, "color": "#2ecc71"},
            {"label": "技術部", "value": 280, "color": "#e74c3c"},
            {"label": "人資部", "value": 150, "color": "#f39c12"},
            {"label": "財務部", "value": 200, "color": "#9b59b6"}
        ]
    }
    
    print("LLM 輸出的結構化數據:")
    print(json.dumps(llm_output, indent=2, ensure_ascii=False))
    
    # 使用 StructuredChartSkill 渲染
    skill = StructuredChartSkill()
    result = skill.render(llm_output)
    
    print(f"\n渲染結果:")
    print(f"  成功: {result['success']}")
    print(f"  圖表類型: {result['metadata']['chart_type']}")
    print(f"  圖片大小: {len(result['imageBase64'])} 字元")


if __name__ == "__main__":
    demo_llm_output()
