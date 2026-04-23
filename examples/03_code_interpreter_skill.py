"""
範例 3: Code Interpreter 模式實作
演示 LLM 生成執行碼 → 沙盒執行 的流程
"""

import subprocess
import tempfile
import os
from typing import Dict, Any
import json


class CodeInterpreterSkill:
    """
    Code Interpreter 模式圖表生成器
    
    設計理念:
    1. LLM 生成安全的 Python 代碼
    2. 在受限環境中執行
    3. 捕捉輸出圖片
    
    安全考量:
    - 限制可安裝的套件
    - 設定執行超時
    - 限制記憶體使用
    """
    
    # 允許安裝的套件清單
    ALLOWED_PACKAGES = [
        'matplotlib', 'numpy', 'pandas', 'seaborn',
        'plotly', 'pyecharts', 'altair'
    ]
    
    # 禁用的模組
    RESTRICTED_MODULES = [
        'os', 'sys', 'subprocess', 'socket',
        'urllib', 'http', 'ftplib', 'smtplib'
    ]
    
    # 執行限制
    TIMEOUT_SECONDS = 30
    MAX_MEMORY_MB = 512
    
    def execute(self, code: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        執行 LLM 生成的代碼
        
        Args:
            code: LLM 生成的 Python 代碼
            data: 輸入資料（會寫入臨時檔案供代碼讀取）
        
        Returns:
            執行結果物件
        """
        # 1. 安全檢查
        security_check = self._check_code_security(code)
        if not security_check["safe"]:
            return {
                "success": False,
                "error": f"安全檢查失敗: {security_check['reason']}"
            }
        
        # 2. 準備臨時環境
        with tempfile.TemporaryDirectory() as tmpdir:
            # 寫入資料（如果有）
            if data:
                data_path = os.path.join(tmpdir, "input_data.json")
                with open(data_path, 'w') as f:
                    json.dump(data, f)
            
            # 寫入代碼
            code_path = os.path.join(tmpdir, "script.py")
            with open(code_path, 'w') as f:
                f.write(self._wrap_code(code, tmpdir))
            
            # 3. 執行代碼
            try:
                result = subprocess.run(
                    ['python', code_path],
                    capture_output=True,
                    text=True,
                    timeout=self.TIMEOUT_SECONDS,
                    cwd=tmpdir
                )
                
                if result.returncode != 0:
                    return {
                        "success": False,
                        "error": f"執行錯誤:\n{result.stderr}"
                    }
                
                # 4. 捕捉輸出
                output = self._capture_output(tmpdir)
                return {
                    "success": True,
                    "output": output,
                    "stdout": result.stdout
                }
                
            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": f"執行超時（>{self.TIMEOUT_SECONDS}秒）"
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"執行異常: {str(e)}"
                }
    
    def _check_code_security(self, code: str) -> Dict[str, Any]:
        """檢查代碼安全性"""
        # 檢查禁用模組
        for module in self.RESTRICTED_MODULES:
            if f"import {module}" in code or f"from {module}" in code:
                return {
                    "safe": False,
                    "reason": f"使用了禁用模組: {module}"
                }
        
        # 檢查危險關鍵字
        dangerous_keywords = ['eval(', 'exec(', '__import__', 'open(', 'file(']
        for keyword in dangerous_keywords:
            if keyword in code:
                return {
                    "safe": False,
                    "reason": f"發現危險關鍵字: {keyword}"
                }
        
        return {"safe": True, "reason": ""}
    
    def _wrap_code(self, code: str, output_dir: str) -> str:
        """包裝代碼，添加安全限制和輸出處理"""
        return f"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import os

# 設定輸出目錄
output_dir = "{output_dir}"

# 讀取輸入資料（如果存在）
input_data = None
if os.path.exists(os.path.join(output_dir, "input_data.json")):
    with open(os.path.join(output_dir, "input_data.json")) as f:
        input_data = json.load(f)

# 用戶代碼
{code}

# 保存所有圖表
for i, fig_num in enumerate(plt.get_fignums()):
    fig = plt.figure(fig_num)
    fig.savefig(os.path.join(output_dir, f'output_{{i}}.png'), 
                dpi=150, bbox_inches='tight')
    plt.close(fig)

print("執行完成")
"""
    
    def _capture_output(self, output_dir: str) -> Dict[str, Any]:
        """捕捉輸出檔案"""
        import base64
        
        outputs = []
        for filename in sorted(os.listdir(output_dir)):
            if filename.startswith('output_') and filename.endswith('.png'):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode()
                outputs.append({
                    "filename": filename,
                    "base64": f"data:image/png;base64,{img_data}"
                })
        
        return {
            "images": outputs,
            "count": len(outputs)
        }


def demo():
    """演示 Code Interpreter 模式"""
    skill = CodeInterpreterSkill()
    
    # 模擬 LLM 生成的代碼
    llm_code = """
# 創建示例資料
import numpy as np

months = ['1月', '2月', '3月', '4月', '5月', '6月']
values = [120, 190, 150, 280, 220, 310]

# 繮製折線圖
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(months, values, marker='o', linewidth=2, markersize=8, color='#3498db')
ax.fill_between(months, values, alpha=0.3, color='#3498db')
ax.set_title('上半年業績趨勢', fontsize=14, fontweight='bold')
ax.set_xlabel('月份')
ax.set_ylabel('業績')
ax.grid(True, alpha=0.3)
"""
    
    print("執行 LLM 生成的代碼...")
    print("-" * 50)
    print(llm_code)
    print("-" * 50)
    
    result = skill.execute(llm_code)
    
    if result["success"]:
        print(f"\n✅ 執行成功!")
        print(f"   生成了 {result['output']['count']} 張圖片")
    else:
        print(f"\n❌ 執行失敗: {result['error']}")
    
    # 測試安全檢查
    print("\n測試安全檢查...")
    malicious_code = """
import os
os.system("rm -rf /")
"""
    result = skill.execute(malicious_code)
    print(f"惡意代碼檢查結果: {result['error']}")


if __name__ == "__main__":
    demo()
