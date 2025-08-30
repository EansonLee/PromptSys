#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude CLI GUI自动化演示脚本
展示基于Python GUI自动化库的Claude CLI功能

使用方法:
python demo_simplified_claude_cli.py

注意: 需要安装GUI自动化依赖:
pip install pyautogui pyperclip psutil pynput
"""

import os
import sys
from datetime import datetime

# 设置控制台编码
if sys.platform.startswith('win'):
    import locale
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.claude_cli_automation import claude_cli_automation

def demo_open_claude_cli():
    """演示打开Claude CLI功能"""
    print("=== 演示: 打开Claude CLI (GUI自动化) ===")
    print("正在使用GUI自动化方法启动Claude CLI...")
    
    result = claude_cli_automation.open_claude_cli()
    
    if result["status"] == "success":
        print(f"[成功] Claude CLI已通过GUI自动化启动")
        print(f"  平台: {result['platform']}")
        print(f"  进程ID: {result['process_id']}")
        print(f"  启动时间: {result['timestamp']}")
        print("  注意: Claude CLI将在新窗口中启动，准备接受GUI自动化输入")
    else:
        print(f"[失败] {result['message']}")
    
    return result["status"] == "success"

def demo_execute_command():
    """演示GUI自动化执行Claude命令功能"""
    print("\n=== 演示: GUI自动化Claude CLI提示词输入 ===")
    
    # 创建测试提示词
    test_prompt = {
        "role": "你是一个GUI自动化测试助手",
        "goal": "验证基于Python GUI库的Claude CLI自动化功能",
        "function_output": "请简单回复'GUI自动化系统工作正常'来确认功能",
        "ui_requirements": "无特殊UI要求"
    }
    
    print("正在创建测试提示词文件...")
    try:
        file_path = claude_cli_automation.write_prompt_to_file(test_prompt, "gui_automation_test.txt")
        print(f"[成功] 提示词文件已创建: {os.path.basename(file_path)}")
        
        # 显示文件内容预览
        print("\n文件内容预览:")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print("-" * 40)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("-" * 40)
        
        print("\n正在使用GUI自动化方法执行Claude CLI命令...")
        print("注意: 系统将使用pyautogui等Python库自动操作Claude CLI界面")
        
        result = claude_cli_automation.open_claude_cli_with_prompt(file_path)
        
        if result["status"] == "success":
            print(f"[成功] GUI自动化Claude CLI已启动")
            print(f"  平台: {result['platform']}")
            print(f"  进程ID: {result['process_id']}")
            print(f"  提示词文件: {os.path.basename(result['prompt_file'])}")
            
            # 显示自动化操作状态
            activation_success = result.get('window_activation_success', False)
            paste_success = result.get('paste_success', False)
            paste_verified = result.get('paste_verified', False)
            enter_success = result.get('enter_success', False)
            focus_ready = result.get('focus_ready', False)
            automation_summary = result.get('automation_summary', {})
            methods_used = result.get('methods_used', {})
            
            print("\n自动化操作状态:")
            print(f"  窗口激活: {'[OK]' if activation_success else '[WARN]'} {automation_summary.get('window_activation', '')}")
            print(f"  输入焦点: {'[OK]' if focus_ready else '[WARN]'} {automation_summary.get('input_focus', '')}")
            print(f"  粘贴操作: {'[OK]' if paste_success else '[WARN]'} {automation_summary.get('paste_operation', '')}")
            print(f"  内容验证: {'[OK]' if paste_verified else '[WARN]' if paste_success else '[SKIP]'} {automation_summary.get('content_verification', '')}")
            print(f"  回车发送: {'[OK]' if enter_success else '[WARN]'} {automation_summary.get('enter_submission', '')}")
            
            # 显示使用的方法
            if methods_used:
                print("\n使用的自动化方法:")
                paste_methods = methods_used.get('paste_methods', [])
                enter_methods = methods_used.get('enter_methods', [])
                if paste_methods:
                    print(f"  粘贴方法: {', '.join(paste_methods)}")
                if enter_methods:
                    print(f"  回车方法: {', '.join(enter_methods)}")
            
            print("\n执行步骤:")
            steps = result.get('steps_completed', [])
            for i, step in enumerate(steps, 1):
                print(f"  {i}. {step}")
            
            # 显示需要手动完成的步骤
            manual_steps = result.get('next_manual_steps', [])
            if manual_steps:
                print(f"\n[WARN] 需要手动完成的步骤:")
                for i, step in enumerate(manual_steps, 1):
                    print(f"  {i}. {step}")
            else:
                print(f"\n[SUCCESS] 所有步骤都已自动完成！Claude CLI应该已经开始处理你的请求了。")
            
            print("\n技术特点:")
            print("  [+] 纯Python实现，无需PowerShell脚本")
            print("  [+] 跨平台兼容(Windows/macOS/Linux)")
            print("  [+] 双重备份机制(pyautogui + pynput)")
            print("  [+] 智能重试和容错机制")
            print("  [+] 详细的状态反馈和手动指引")
            
            return True
        else:
            print(f"[失败] {result['message']}")
            return False
            
    except Exception as e:
        print(f"[失败] 创建或执行失败: {e}")
        return False

def demo_platform_differences():
    """演示GUI自动化跨平台实现"""
    print("\n=== 演示: GUI自动化跨平台实现 ===")
    
    system = claude_cli_automation.system
    print(f"当前系统: {system}")
    
    print("\nGUI自动化统一实现:")
    print("  - 窗口管理: psutil + pyautogui (跨平台)")
    print("  - 剪贴板操作: pyperclip (跨平台)")
    print("  - 键盘模拟: pynput.keyboard (跨平台)")
    print("  - 鼠标模拟: pynput.mouse (跨平台)")
    print("  - 进程管理: subprocess + psutil (跨平台)")
    
    if system == "windows":
        print("\nWindows特定优化:")
        print("  - 窗口激活: win32gui API (通过pynput)")
        print("  - 进程启动: cmd /c start")
        print("  - 编码处理: UTF-8 BOM")
    elif system == "darwin":
        print("\nmacOS特定优化:")
        print("  - 窗口激活: Quartz API (通过pynput)")
        print("  - 进程启动: open -a Terminal")
        print("  - 权限处理: 辅助功能权限")
    else:
        print("\nLinux特定优化:")
        print("  - 窗口激活: X11/Wayland (通过pynput)")
        print("  - 进程启动: gnome-terminal")
        print("  - 桌面环境: GNOME/KDE/XFCE兼容")
    
    print("\n技术优势:")
    print("  [✓] 完全移除PowerShell/AppleScript依赖")
    print("  [✓] 统一的Python API接口")
    print("  [✓] 可靠的窗口检测和激活")
    print("  [✓] 智能重试和容错机制")
    print("  [✓] 详细的日志记录和调试")
    print("  [✓] 模块化设计便于维护")

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

def demo_dependency_check():
    """检查GUI自动化依赖库"""
    print("\n=== 依赖库检查 ===")
    dependencies = {
        'pyautogui': 'GUI自动化核心库',
        'pyperclip': '剪贴板操作库', 
        'psutil': '进程管理库',
        'pynput': '键盘鼠标控制库'
    }
    
    missing_deps = []
    for lib, desc in dependencies.items():
        try:
            __import__(lib)
            print(f"  [✓] {lib}: {desc}")
        except ImportError:
            print(f"  [✗] {lib}: {desc} - 缺失")
            missing_deps.append(lib)
    
    if missing_deps:
        print(f"\n[WARNING] 缺失依赖库: {', '.join(missing_deps)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    else:
        print("\n[✓] 所有GUI自动化依赖库已就绪")
        return True

def main():
    """主演示函数"""
    print("Claude CLI GUI自动化功能演示")
    print("=" * 50)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"系统平台: {claude_cli_automation.system}")
    
    # 检查GUI自动化依赖
    deps_ok = demo_dependency_check()
    
    # 检查Claude CLI是否可用
    try:
        import subprocess
        result = subprocess.run(['claude', '--version'], 
                              capture_output=True, text=True, timeout=5)
        claude_available = result.returncode == 0
    except:
        claude_available = False
    
    if not claude_available:
        print("\n[WARNING] 注意: Claude CLI似乎未安装或不在PATH中")
        print("   以下演示将展示功能调用，但可能无法看到实际的Claude CLI界面")
    
    if not deps_ok:
        print("\n[ERROR] 依赖库不完整，演示可能失败")
    
    # 让用户选择演示类型
    print("\n选择演示类型:")
    print("1. 仅启动Claude CLI (GUI自动化)")
    print("2. GUI自动化输入提示词到Claude CLI（推荐）")
    print("3. 显示GUI自动化技术说明")
    
    try:
        choice = input("请输入选择 (1-3, 默认2): ").strip() or "2"
    except (EOFError, KeyboardInterrupt):
        choice = "2"  # 默认选择选项2
    
    success_count = 0
    total_demos = 0
    
    if choice == "1":
        # 演示1: 仅启动Claude CLI
        total_demos += 1
        if demo_open_claude_cli():
            success_count += 1
    elif choice == "2":
        # 演示2: GUI自动化完整流程
        total_demos += 1
        if demo_execute_command():
            success_count += 1
    elif choice == "3":
        # 演示3: 技术说明
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