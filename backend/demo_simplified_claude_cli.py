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
    """演示GUI自动化执行Claude命令功能 - macOS优化版"""
    print("\n=== 演示: macOS优化GUI自动化Claude CLI提示词输入 ===")

    # 创建测试提示词
    test_prompt = {
        "role": "你是一个macOS自动化测试助手",
        "goal": "验证macOS优化的Claude CLI自动化功能，包括'Yes, proceed'检测",
        "function_output": "请回复包含'Yes, proceed'选项的内容来测试自动检测功能",
        "ui_requirements": "测试macOS原生剪贴板、AppleScript窗口激活、Cmd键映射等功能"
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
        
        print("\n=== macOS自动化功能测试 ===")

        # 1. 测试系统状态
        print("1. 检查macOS优化功能状态...")
        status = claude_cli_automation.get_automation_status()

        if status['system'] == 'darwin':
            print("   ✅ 运行在macOS系统")
            macos_features = status.get('macos_specific_features', {})
            print(f"   - AppleScript支持: {'✅' if macos_features.get('applescript_support') else '❌'}")
            print(f"   - Terminal激活: {'✅' if macos_features.get('terminal_activation') else '❌'}")
            print(f"   - Cmd键映射: {'✅' if macos_features.get('cmd_key_mapping') else '❌'}")
            print(f"   - 原生剪贴板: {'✅' if macos_features.get('native_clipboard') else '❌'}")

            detection_caps = status.get('detection_capabilities', {})
            print(f"   - Yes/Proceed检测: {'✅' if detection_caps.get('yes_proceed_detection') else '❌'}")
            print(f"   - 屏幕变化监控: {'✅' if detection_caps.get('screen_change_monitoring') else '❌'}")
        else:
            print("   ⚠️  非macOS系统，将使用通用功能")

        # 2. 测试剪贴板功能
        print("\n2. 测试macOS剪贴板功能...")
        with open(file_path, 'r', encoding='utf-8') as f:
            test_content = f.read()

        clipboard_success = claude_cli_automation.clipboard_manager.copy_to_clipboard(test_content)
        if clipboard_success:
            print("   ✅ macOS剪贴板复制成功")
            verify_success = claude_cli_automation.clipboard_manager.verify_clipboard_content(test_content)
            print(f"   ✅ 剪贴板验证: {'成功' if verify_success else '失败'}")
        else:
            print("   ❌ 剪贴板复制失败")

        # 3. 进程管理演示
        print("\n3. 进程管理和清理演示...")

        # 显示当前终端进程
        terminals = claude_cli_automation.list_terminal_processes()
        print(f"   📱 当前终端进程: {len(terminals)} 个")
        for i, terminal in enumerate(terminals[:3]):  # 只显示前3个
            memory_mb = terminal.get('memory_usage', 0) / (1024*1024)
            print(f"     {i+1}. PID={terminal['pid']}, Name={terminal['name']}, Memory={memory_mb:.1f}MB")

        # 显示Claude进程
        claude_processes = claude_cli_automation.window_manager.find_claude_cli_windows()
        print(f"   🤖 当前Claude进程: {len(claude_processes)} 个")

        # 如果有多个Claude进程，进行清理
        if len(claude_processes) > 1:
            print(f"   🧹 检测到多个Claude进程，执行清理...")
            cleanup_result = claude_cli_automation.cleanup_claude_processes(keep_newest=1)
            print(f"   ✅ 清理了 {len(cleanup_result['cleaned_processes'])} 个旧Claude进程")
        else:
            print(f"   ✅ Claude进程数量正常，无需清理")

        # 如果有过多终端，可选择清理（演示用途，通常不自动清理）
        if len(terminals) > 5:
            print(f"   🧹 检测到过多终端进程({len(terminals)}个)，可执行清理")
            print(f"   ℹ️  演示模式：跳过终端清理以保护用户环境")

        print("\n4. 正在使用完整自动化工作流执行Claude CLI命令...")
        print("   📋 包含: 进程管理 + macOS权限处理 + 自动化操作")

        # 使用新的完整工作流（包含进程管理和权限处理）
        result = claude_cli_automation.complete_workflow_with_cleanup(
            file_path,
            monitor_duration=30.0,
            max_terminals=5,  # 保守设置，避免过度清理
            keep_claude_processes=1
        )
        
        if result["status"] in ["success", "partial_success"]:
            print(f"[成功] 完整自动化工作流已完成")
            print(f"  最终状态: {result['status']}")
            print(f"  消息: {result.get('message', '')}")

            # 显示清理结果
            cleanup_results = result.get('cleanup_results', {})
            if cleanup_results:
                print(f"\n==== 进程清理结果 ====")

                terminal_cleanup = cleanup_results.get('terminals', {})
                if terminal_cleanup:
                    cleaned_terminals = len(terminal_cleanup.get('cleaned_processes', []))
                    kept_terminals = len(terminal_cleanup.get('kept_processes', []))
                    print(f"  终端进程: 清理 {cleaned_terminals} 个，保留 {kept_terminals} 个")

                claude_cleanup = cleanup_results.get('claude_processes', {})
                if claude_cleanup:
                    cleaned_claude = len(claude_cleanup.get('cleaned_processes', []))
                    kept_claude = len(claude_cleanup.get('kept_processes', []))
                    print(f"  Claude进程: 清理 {cleaned_claude} 个，保留 {kept_claude} 个")

            # 显示自动化工作流结果
            automation_results = result.get('automation_results', {})
            if automation_results:
                steps = automation_results.get('steps', {})

                # 检查权限监控结果
                if 'permission_monitor' in steps:
                    perm_result = steps['permission_monitor']
                    print(f"\n==== macOS权限处理 ====")
                    print(f"  权限监控: {perm_result.get('status', 'unknown')}")
                    print(f"  消息: {perm_result.get('message', 'N/A')}")

                # 检查进程清理结果
                if 'process_cleanup' in steps:
                    proc_result = steps['process_cleanup']
                    cleaned = len(proc_result.get('cleaned_processes', []))
                    if cleaned > 0:
                        print(f"\n==== 预清理结果 ====")
                        print(f"  清理的Claude进程: {cleaned} 个")

            if automation_results and 'send_prompt' in automation_results.get('steps', {}):
                send_result = steps['send_prompt']
                print(f"\n==== 步骤1: 发送提示词 ====")
                print(f"  状态: {'✅ 成功' if send_result.get('status') == 'success' else '❌ 失败'}")

                if send_result.get('status') == 'success':
                    # 显示macOS特定的自动化状态
                    automation_summary = send_result.get('automation_summary', {})
                    print(f"  窗口激活: {automation_summary.get('window_activation', 'N/A')}")
                    print(f"  输入焦点: {automation_summary.get('input_focus', 'N/A')}")
                    print(f"  粘贴操作: {automation_summary.get('paste_operation', 'N/A')}")
                    print(f"  内容验证: {automation_summary.get('content_verification', 'N/A')}")
                    print(f"  回车提交: {automation_summary.get('enter_submission', 'N/A')}")

                    # 显示使用的方法
                    methods_used = send_result.get('methods_used', {})
                    if methods_used:
                        print(f"  使用的方法:")
                        if methods_used.get('paste_methods'):
                            print(f"    粘贴: {', '.join(methods_used['paste_methods'])}")
                        if methods_used.get('enter_methods'):
                            print(f"    回车: {', '.join(methods_used['enter_methods'])}")

            if 'monitor_response' in steps:
                monitor_result = steps['monitor_response']
                print(f"\n==== 步骤2: 监控Claude响应 ====")
                print(f"  监控状态: {monitor_result.get('status', 'unknown')}")

                if monitor_result.get('status') == 'handled':
                    print("  🎉 检测到Claude提示并自动处理!")
                    print(f"  执行的操作: {monitor_result.get('action_taken', 'N/A')}")
                    detection_result = monitor_result.get('detection_result', {})
                    if detection_result:
                        print(f"  检测方法: {detection_result.get('detection_method', 'N/A')}")
                        print(f"  检测到的选项: {len(detection_result.get('options', []))}")
                elif monitor_result.get('status') == 'no_prompts_detected':
                    print("  📝 未检测到需要自动处理的提示")
                elif monitor_result.get('status') == 'detected_no_action':
                    print("  👁️ 检测到提示但无需自动处理")
                else:
                    print(f"  ⚠️ 监控结果: {monitor_result.get('message', '未知')}")

            # 显示总结信息
            summary = result.get('summary', {})
            if summary:
                print(f"\n==== 工作流总结 ====")
                print(f"  提示词已发送: {'✅' if summary.get('prompt_sent') else '❌'}")
                print(f"  检测到提示: {'✅' if summary.get('prompts_detected') else '❌'}")
                print(f"  自动处理: {'✅' if summary.get('auto_handled') else '❌'}")
                print(f"  总耗时: {summary.get('total_time', 0):.1f}秒")

            print(f"\n==== 增强功能技术特点 ====")
            print("  🍎 AppleScript窗口激活和Terminal检测")
            print("  📋 多重剪贴板方案(NSPasteboard/AppleScript/pbcopy)")
            print("  ⌨️ Cmd键自动映射(Cmd+V而非Ctrl+V)")
            print("  👁️ 智能屏幕文本检测('Yes, proceed')")
            print("  🔄 自动Enter键响应")
            print("  🧹 多进程管理和自动清理")
            print("  🔐 macOS权限对话框自动处理")
            print("  📱 智能终端进程管理")
            print("  🛡️ 多重备用方案和容错机制")
            print("  📊 实时状态监控和反馈")

            # 如果有手动步骤提示
            if 'send_prompt' in steps and steps['send_prompt'].get('next_manual_steps'):
                manual_steps = steps['send_prompt']['next_manual_steps']
                print(f"\n[INFO] 如需手动操作:")
                for i, step in enumerate(manual_steps, 1):
                    print(f"  {i}. {step}")

            return True
        else:
            print(f"[失败] {result['message']}")
            return False
            
    except Exception as e:
        print(f"[失败] 创建或执行失败: {e}")
        return False

def demo_platform_differences():
    """演示macOS优化的GUI自动化实现"""
    print("\n=== 演示: macOS优化GUI自动化技术说明 ===")

    system = claude_cli_automation.system
    print(f"当前系统: {system}")

    # 获取系统状态
    status = claude_cli_automation.get_automation_status()

    print("\n=== 核心功能架构 ===")
    print("基础GUI自动化库:")
    print("  - 窗口管理: psutil + pyautogui (跨平台)")
    print("  - 剪贴板操作: pyperclip + 平台原生API")
    print("  - 键盘模拟: pynput.keyboard + 平台优化")
    print("  - 屏幕检测: pyautogui + OCR + Vision (macOS)")
    print("  - 进程管理: subprocess + psutil")

    if system == "darwin":
        print("\n=== macOS深度优化 ===")

        # macOS特定功能
        macos_features = status.get('macos_specific_features', {})
        print("🍎 AppleScript集成:")
        print(f"  - 智能窗口激活: {'✅ 可用' if macos_features.get('applescript_support') else '❌ 不可用'}")
        print("  - Terminal自动检测和激活")
        print("  - 键盘事件模拟 (key code级别)")

        print("\n📋 原生剪贴板支持:")
        print(f"  - NSPasteboard API: {'✅ 可用' if macos_features.get('native_clipboard') else '❌ 不可用'}")
        print("  - AppleScript剪贴板操作")
        print("  - pbcopy/pbpaste命令行工具")
        print("  - 智能降级机制")

        print("\n⌨️ 键盘输入优化:")
        print(f"  - Cmd键自动映射: {'✅ 启用' if macos_features.get('cmd_key_mapping') else '❌ 禁用'}")
        print("  - 多重按键发送方法")
        print("  - AppleScript键盘事件")

        detection_caps = status.get('detection_capabilities', {})
        print("\n👁️ 智能检测系统:")
        print(f"  - 屏幕文本检测: {'✅ 启用' if detection_caps.get('screen_text_detection') else '❌ 禁用'}")
        print(f"  - 'Yes, proceed'检测: {'✅ 启用' if detection_caps.get('yes_proceed_detection') else '❌ 禁用'}")
        print(f"  - OCR文本识别: {'✅ 可用' if detection_caps.get('ocr_detection') else '❌ 不可用'}")
        print(f"  - macOS Vision框架: {'✅ 可用' if detection_caps.get('macos_vision') else '❌ 不可用'}")
        print(f"  - 屏幕变化监控: {'✅ 启用' if detection_caps.get('screen_change_monitoring') else '❌ 禁用'}")

        print("\n🔄 自动化工作流:")
        print("  - 完整工作流: 发送 → 监控 → 响应")
        print("  - 实时屏幕监控")
        print("  - 自动Enter键响应")
        print("  - 智能状态反馈")

        print("\n🛡️ 容错和备用机制:")
        enhanced_features = status.get('enhanced_features', [])
        for feature in enhanced_features:
            print(f"  - {feature}")

    elif system == "windows":
        print("\nWindows特定优化:")
        print("  - 窗口激活: win32gui API")
        print("  - 右键粘贴支持 (CMD环境)")
        print("  - 进程启动: cmd /c start")
        print("  - 编码处理: UTF-8 BOM")
    else:
        print("\nLinux特定优化:")
        print("  - 窗口激活: X11/Wayland")
        print("  - 进程启动: gnome-terminal/xterm")
        print("  - 桌面环境: GNOME/KDE/XFCE兼容")

    print(f"\n=== 技术优势 ===")
    if system == "darwin":
        print("  ✅ 深度macOS集成 (AppleScript/Quartz/Vision)")
        print("  ✅ 智能文本检测和自动响应")
        print("  ✅ 原生剪贴板多重备用方案")
        print("  ✅ 完整的自动化工作流")
    print("  ✅ 纯Python实现，无外部依赖")
    print("  ✅ 跨平台兼容性")
    print("  ✅ 智能重试和容错机制")
    print("  ✅ 详细的状态反馈和调试")
    print("  ✅ 模块化设计便于扩展")

    if system == "darwin":
        print(f"\n=== macOS权限要求 ===")
        print("  📋 辅助功能权限 (系统偏好设置 > 安全性与隐私)")
        print("  📱 屏幕录制权限 (用于屏幕检测)")
        print("  🔐 输入监控权限 (用于键盘自动化)")

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
    print("2. 完整增强版自动化工作流（推荐）")
    print("   - 智能多进程管理和清理")
    print("   - macOS权限对话框自动处理")
    print("   - 'Yes, proceed'检测和自动处理")
    print("   - AppleScript窗口激活")
    print("   - 原生剪贴板操作和Cmd键映射")
    print("3. 显示macOS优化技术说明")
    
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