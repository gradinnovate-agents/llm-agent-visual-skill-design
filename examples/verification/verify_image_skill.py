#!/usr/bin/env python3
"""
圖像生成 SKILL 完整驗證測試
"""

import os
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SKILL_DIR = PROJECT_ROOT / "examples" / "image_skill"


def check_file_exists(filepath: Path, description: str) -> bool:
    if filepath.exists():
        print(f"  ✓ {description}: {filepath.name}")
        return True
    else:
        print(f"  ✗ {description}: 缺少 {filepath}")
        return False


def check_skill_md() -> bool:
    print("\n[1/4] 檢查 SKILL.md 文件...")
    
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
        "風格系統": "風格" in content,
        "相關資源": "## 相關資源" in content
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass


def check_references() -> bool:
    print("\n[2/4] 檢查 references 目錄...")
    
    refs_dir = SKILL_DIR / "references"
    filepath = refs_dir / "style-gallery.md"
    
    if not check_file_exists(filepath, "風格參考手冊"):
        return False
    
    # 檢查內容
    content = filepath.read_text()
    if "## " in content:
        print(f"    ✓ 包含多個風格章節")
    
    return True


def check_templates() -> bool:
    print("\n[3/4] 檢查 templates 目錄...")
    
    templates_dir = SKILL_DIR / "templates"
    filepath = templates_dir / "standard-config.json"
    
    if not check_file_exists(filepath, "標準配置"):
        return False
    
    try:
        with open(filepath) as f:
            config = json.load(f)
        
        checks = [
            ("style_presets" in config, "style_presets 配置"),
            ("quality_modifiers" in config, "quality_modifiers 配置"),
            ("negative_prompts" in config, "negative_prompts 配置")
        ]
        
        for result, desc in checks:
            status = "✓" if result else "✗"
            print(f"    {status} {desc}")
        
        return all(r for r, _ in checks)
        
    except json.JSONDecodeError:
        print("    ✗ JSON 格式錯誤")
        return False


def check_scripts() -> bool:
    print("\n[4/4] 檢查 scripts 目錄...")
    
    scripts_dir = SKILL_DIR / "scripts"
    filepath = scripts_dir / "validate.py"
    
    if not check_file_exists(filepath, "驗證腳本"):
        return False
    
    return True


def main():
    print("=" * 60)
    print("圖像生成 SKILL 完整驗證")
    print("=" * 60)
    
    results = []
    results.append(("SKILL.md 格式", check_skill_md()))
    results.append(("references 目錄", check_references()))
    results.append(("templates 目錄", check_templates()))
    results.append(("scripts 目錄", check_scripts()))
    
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
