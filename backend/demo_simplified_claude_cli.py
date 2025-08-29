#!/usr/bin/env python3
"""
简化版 Claude CLI 自动化演示脚本
展示修改后的直接调用Claude CLI功能

使用方法:
python demo_simplified_claude_cli.py
"""

import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.claude_cli_automation import claude_cli_automation

def demo_open_claude_cli():
    """演示打开Claude CLI功能"""
    print("=== 演示: 打开Claude CLI ===")
    print("正在使用简化的方法打开Claude CLI...")
    
    result = claude_cli_automation.open_claude_cli()
    
    if result["status"] == "success":
        print(f"[成功] Claude CLI已启动")
        print(f"  平台: {result['platform']}")
        print(f"  进程ID: {result['process_id']}")
        print(f"  启动时间: {result['timestamp']}")
        print("  注意: 应该会看到一个新的CMD窗口打开并显示Claude CLI")
    else:
        print(f"[失败] {result['message']}")
    
    return result["status"] == "success"

def demo_execute_command():
    """演示执行Claude命令功能（直接自动输入，不单独打开Claude CLI）"""
    print("\n=== 演示: Claude CLI自动输入提示词 ===")
    
    # 创建测试提示词
    test_prompt = {
        "role": "你是一个简化测试助手",
        "goal": "验证Claude CLI自动化功能是否正常工作",
        "function_output": "请简单回复'系统工作正常'来确认功能",
        "ui_requirements": "无特殊UI要求"
    }
    
    print("正在创建测试提示词文件...")
    try:
        file_path = claude_cli_automation.write_prompt_to_file(test_prompt, "demo_test.txt")
        print(f"[成功] 提示词文件已创建: {os.path.basename(file_path)}")
        
        # 显示文件内容预览
        print("\n文件内容预览:")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("-" * 40)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("-" * 40)
        
        print("\n正在使用交互式方法执行Claude CLI命令...")
        print("注意: 这会打开Claude CLI窗口并自动输入提示词内容，然后按Enter发送")
        
        result = claude_cli_automation.open_claude_cli_with_prompt(file_path)
        
        if result["status"] == "success":
            print(f"[成功] 交互式Claude CLI已启动")
            print(f"  平台: {result['platform']}")
            print(f"  进程ID: {result['process_id']}")
            print(f"  提示词文件: {os.path.basename(result['prompt_file'])}")
            
            if claude_cli_automation.system == "windows":
                ps_script = result.get('powershell_script', '')
                if ps_script:
                    print(f"  PowerShell脚本: {os.path.basename(ps_script)}")
                    print("  执行流程: PowerShell窗口 → 显示提示词预览 → 启动Claude CLI → 等待2000ms → 自动粘贴输入 → 发送")
            else:
                script_file = result.get('script_file', '')
                if script_file:
                    print(f"  脚本文件: {os.path.basename(script_file)}")
                    print("  执行流程: Terminal窗口 → 显示提示词预览 → 自动输入到Claude CLI → 发送")
            
            print("\n期望行为:")
            print("  1. 打开PowerShell自动化窗口，显示提示词内容预览")
            print("  2. 自动启动Claude CLI（在新的CMD窗口中）")
            print("  3. 等待2000ms让Claude CLI完全加载")
            print("  4. 自动将提示词内容复制到剪贴板")
            print("  5. 尝试多种方法自动激活Claude CLI窗口")
            print("  6. 自动执行Ctrl+V粘贴操作")
            print("  7. 自动按Enter键发送提示词")
            print("  8. Claude CLI开始处理请求并返回AI响应")
            print("")
            print("  注意: 如果自动粘贴失败，会提示手动操作")
            
            return True
        else:
            print(f"[失败] {result['message']}")
            return False
            
    except Exception as e:
        print(f"[失败] 创建或执行失败: {e}")
        return False

def demo_platform_differences():
    """演示跨平台差异"""
    print("\n=== 演示: 跨平台实现差异 ===")
    
    system = claude_cli_automation.system
    print(f"当前系统: {system}")
    
    if system == "windows":
        print("Windows实现:")
        print("  - 打开Claude CLI: 使用 'cmd /c start cmd /k claude'")
        print("  - 执行命令: 使用 'cmd /c type file | claude'")
        print("  - 优势: 无需PowerShell，直接使用CMD")
    elif system == "darwin":
        print("macOS实现:")
        print("  - 打开Claude CLI: 使用 AppleScript 控制 Terminal")
        print("  - 执行命令: 使用 'sh -c cat file | claude'")
        print("  - 优势: 原生Terminal集成")
    else:
        print("Linux实现:")
        print("  - 打开Claude CLI: 使用 gnome-terminal")
        print("  - 执行命令: 使用 'sh -c cat file | claude'")
        print("  - 优势: 标准shell命令")
    
    print("\n主要改进:")
    print("  [OK] 移除了git-bash依赖")
    print("  [OK] 简化了Windows实现")
    print("  [OK] 统一了各平台的调用方式")
    print("  [OK] 减少了环境配置要求")

def demo_cleanup():
    """演示清理功能"""
    print("\n=== 演示: 临时文件清理 ===")
    
    print("正在清理演示产生的临时文件...")
    result = claude_cli_automation.cleanup_temp_files(older_than_hours=0)
    
    if result["status"] == "success":
        cleaned_files = result.get("cleaned_files", [])
        print(f"[成功] 清理完成，删除了 {len(cleaned_files)} 个文件")
        if cleaned_files:
            print("  清理的文件:")
            for file in cleaned_files:
                print(f"    - {file}")
    else:
        print(f"[失败] {result['message']}")

def main():
    """主演示函数"""
    print("Claude CLI 自动化 - 简化版功能演示")
    print("=" * 50)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"系统平台: {claude_cli_automation.system}")
    
    # 检查Claude CLI是否可用
    try:
        import subprocess
        result = subprocess.run(['claude', '--version'], 
                              capture_output=True, text=True, timeout=5)
        claude_available = result.returncode == 0
    except:
        claude_available = False
    
    if not claude_available:
        print("\n[WARNING]  注意: Claude CLI似乎未安装或不在PATH中")
        print("   以下演示将展示功能调用，但可能无法看到实际的Claude CLI界面")
    
    # 让用户选择演示类型
    print("\n选择演示类型:")
    print("1. 仅打开Claude CLI")
    print("2. 自动输入提示词到Claude CLI（推荐）")
    print("3. 显示平台差异说明")
    
    try:
        choice = input("请输入选择 (1-3, 默认2): ").strip() or "2"
    except (EOFError, KeyboardInterrupt):
        choice = "2"  # 默认选择选项2
    
    success_count = 0
    total_demos = 0
    
    if choice == "1":
        # 演示1: 打开Claude CLI
        total_demos += 1
        if demo_open_claude_cli():
            success_count += 1
    elif choice == "2":
        # 演示2: 自动输入命令（推荐，一步完成）
        total_demos += 1
        if demo_execute_command():
            success_count += 1
    elif choice == "3":
        # 演示3: 平台差异说明
        demo_platform_differences()
    else:
        print("无效选择，使用默认选项...")
        total_demos += 1
        if demo_execute_command():
            success_count += 1
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n\n演示执行出错: {e}")
    
    print("\n演示结束")