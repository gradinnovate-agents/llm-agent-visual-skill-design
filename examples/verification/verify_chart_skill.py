#!/usr/bin/env python3
"""
圖表 SKILL 完整驗證測試

測試項目:
1. SKILL.md 文件存在性與格式
2. references/ 目錄下的參考文件
3. templates/ 目錄下的模板檔案
4. scripts/ 目錄下的腳本可執行性
5. 圖表生成功能正確性
"""

import os
import sys
import json
from pathlib import Path

# 設定項目路徑
PROJECT_ROOT = Path(__file__).parent.parent
SKILL_DIR = PROJECT_ROOT / "examples" / "chart_skill"


def check_file_exists(filepath: Path, description: str) -> bool:
    """檢查檔案是否存在"""
    if filepath.exists():
        print(f"  ✓ {description}: {filepath.name}")
        return True
    else:
        print(f"  ✗ {description}: 缺少 {filepath}")
        return False


def check_skill_md() -> bool:
    """檢查 SKILL.md 格式"""
    print("\n[1/5] 檢查 SKILL.md 文件...")
    
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.exists():
        print("  ✗ SKILL.md 不存在")
        return False
    
    content = skill_md.read_text()
    
    checks = {
        "YAML frontmatter": content.startswith("---"),
        "name 欄位": "name:" in content,
        "version 欄位": "version:" in content,
        "description 欄位": "description:" in content,
        "trigger 欄位": "trigger:" in content,
        "使用說明": "## 使用" in content or "## 工作流程" in content,
        "相關資源": "## 相關資源" in content
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass


def check_references() -> bool:
    """檢查 references 目錄"""
    print("\n[2/5] 檢查 references 目錄...")
    
    refs_dir = SKILL_DIR / "references"
    checks = [
        (refs_dir / "chart-selection-guide.md", "圖表選擇指南"),
        (refs_dir / "color-palettes.md", "配色方案")
    ]
    
    all_pass = True
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_pass = False
    
    return all_pass


def check_templates() -> bool:
    """檢查 templates 目錄"""
    print("\n[3/5] 檢查 templates 目錄...")
    
    templates_dir = SKILL_DIR / "templates"
    checks = [
        (templates_dir / "bar_chart.json", "柱狀圖模板"),
        (templates_dir / "line_chart.json", "折線圖模板")
    ]
    
    all_pass = True
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_pass = False
            continue
        
        # 檢查 JSON 格式
        try:
            with open(filepath) as f:
                json.load(f)
            print(f"    ✓ JSON 格式正確")
        except json.JSONDecodeError:
            print(f"    ✗ JSON 格式錯誤")
            all_pass = False
    
    return all_pass


def check_scripts() -> bool:
    """檢查 scripts 目錄"""
    print("\n[4/5] 檢查 scripts 目錄...")
    
    scripts_dir = SKILL_DIR / "scripts"
    checks = [
        (scripts_dir / "validate.py", "驗證腳本"),
        (scripts_dir / "generate.py", "生成腳本")
    ]
    
    all_pass = True
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_pass = False
    
    return all_pass


def check_functionality() -> bool:
    """檢查圖表生成功能"""
    print("\n[5/5] 檢查圖表生成功能...")
    
    sys.path.insert(0, str(PROJECT_ROOT / "examples"))
    
    try:
        from chart_skill.scripts.validate import validate_input
        
        # 測試有效輸入
        test_input = {
            "chartType": "bar",
            "data": [
                {"month": "1月", "sales": 100},
                {"month": "2月", "sales": 200}
            ],
            "xField": "month",
            "yField": "sales"
        }
        
        is_valid, message = validate_input(test_input)
        if is_valid:
            print("  ✓ 驗證功能正常")
        else:
            print(f"  ✗ 驗證功能異常: {message}")
            return False
        
        # 測試圖表生成
        from basic_chart_skill import ChartSkill
        
        skill = ChartSkill()
        result = skill.generate(test_input)
        
        if result["success"]:
            print("  ✓ 圖表生成功能正常")
            print(f"    輸出格式: {result['metadata']['format']}")
            print(f"    圖片大小: {len(result['imageBase64'])} 字元")
        else:
            print(f"  ✗ 圖表生成失敗: {result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ 功能測試異常: {e}")
        return False


def main():
    """主函數"""
    print("=" * 60)
    print("圖表 SKILL 完整驗證")
    print("=" * 60)
    
    results = []
    results.append(("SKILL.md 格式", check_skill_md()))
    results.append(("references 目錄", check_references()))
    results.append(("templates 目錄", check_templates()))
    results.append(("scripts 目錄", check_scripts()))
    results.append(("功能測試", check_functionality()))
    
    print("\n" + "=" * 60)
    print("驗證結果")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n總計: {passed} 通過, {failed} 失敗")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
