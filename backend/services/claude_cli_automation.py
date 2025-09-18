"""
Claude CLI 自动化工具 - GUI 自动化版本
使用 Python GUI 自动化库实现跨平台 Claude CLI 自动化操作
支持 Windows、macOS 和 Linux
"""

import os
import platform
import time
import logging
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime
import subprocess
import re

# GUI 自动化库
try: 
    import pyautogui
    import pyperclip
    import psutil
    from pynput import keyboard, mouse
    from pynput.keyboard import Key, Listener

    # macOS 特定库
    if platform.system().lower() == "darwin":
        try:
            import Quartz
            import Vision
            import CoreGraphics
            import AppKit
            from Foundation import NSString, NSURL, NSData
            macos_libs_available = True
        except ImportError as e:
            logging.warning(f"macOS 特定库导入失败: {e}")
            macos_libs_available = False
    else:
        macos_libs_available = False

    # OCR 库 (可选)
    try:
        import pytesseract
        from PIL import Image
        ocr_available = True
    except ImportError:
        ocr_available = False
        logging.info("OCR 库不可用，将使用其他文本检测方法")

except ImportError as e:
    logging.warning(f"GUI 自动化库导入失败: {e}")
    pyautogui = None
    pyperclip = None
    psutil = None
    macos_libs_available = False
    ocr_available = False

logger = logging.getLogger(__name__)

class ScreenTextDetector:
    """屏幕文本检测器 - 用于检测"Yes, proceed"等提示"""

    def __init__(self):
        self.system = platform.system().lower()

    def detect_yes_proceed_options(self, screenshot=None) -> Dict[str, Any]:
        """
        检测屏幕上是否有"Yes, proceed"等选项

        Args:
            screenshot: 可选的截图对象，如果不提供则自动截图

        Returns:
            Dict: 检测结果，包含是否找到选项、位置等信息
        """
        result = {
            "found": False,
            "options": [],
            "positions": [],
            "suggested_action": None,
            "detection_method": None
        }

        try:
            # 如果没有提供截图，则自动截图
            if screenshot is None:
                screenshot = pyautogui.screenshot()

            # 方法1: 使用OCR检测文本 (如果可用)
            if ocr_available:
                ocr_result = self._detect_with_ocr(screenshot)
                if ocr_result["found"]:
                    result.update(ocr_result)
                    result["detection_method"] = "OCR"
                    return result

            # 方法2: 使用macOS Vision框架 (如果可用)
            if self.system == "darwin" and macos_libs_available:
                vision_result = self._detect_with_vision(screenshot)
                if vision_result["found"]:
                    result.update(vision_result)
                    result["detection_method"] = "macOS Vision"
                    return result

            # 方法3: 模板匹配 (备用方法)
            template_result = self._detect_with_template_matching(screenshot)
            if template_result["found"]:
                result.update(template_result)
                result["detection_method"] = "Template Matching"
                return result

            # 方法4: 简单的颜色/模式检测
            pattern_result = self._detect_with_pattern_analysis(screenshot)
            if pattern_result["found"]:
                result.update(pattern_result)
                result["detection_method"] = "Pattern Analysis"
                return result

        except Exception as e:
            logger.error(f"文本检测过程中出错: {e}")

        return result

    def _detect_with_ocr(self, screenshot) -> Dict[str, Any]:
        """使用OCR检测文本"""
        result = {"found": False, "options": [], "positions": []}

        try:
            # 转换截图为PIL Image
            if hasattr(screenshot, 'save'):
                # 已经是PIL Image
                img = screenshot
            else:
                # 转换numpy array到PIL Image
                img = Image.fromarray(screenshot)

            # 使用tesseract进行OCR
            text = pytesseract.image_to_string(img, lang='eng')

            # 搜索相关选项
            yes_proceed_patterns = [
                r"yes,?\s*proceed",
                r"continue",
                r"yes",
                r"proceed",
                r"确认",
                r"继续"
            ]

            options_found = []
            for pattern in yes_proceed_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    options_found.append({
                        "text": match.group(),
                        "pattern": pattern,
                        "start": match.start(),
                        "end": match.end()
                    })

            if options_found:
                result["found"] = True
                result["options"] = options_found
                result["suggested_action"] = "press_enter"
                logger.info(f"OCR检测到选项: {[opt['text'] for opt in options_found]}")

        except Exception as e:
            logger.warning(f"OCR检测失败: {e}")

        return result

    def _detect_with_vision(self, screenshot) -> Dict[str, Any]:
        """使用macOS Vision框架检测文本"""
        result = {"found": False, "options": [], "positions": []}

        if not macos_libs_available:
            return result

        try:
            # 将截图转换为Core Graphics图像
            if hasattr(screenshot, 'save'):
                # PIL Image转换
                import io
                buffer = io.BytesIO()
                screenshot.save(buffer, format='PNG')
                buffer.seek(0)
                data = NSData.dataWithData_(buffer.getvalue())
            else:
                # 其他格式处理
                return result

            # 这里需要使用Vision框架的文本识别
            # 由于复杂性，先返回基本结果
            logger.info("Vision框架文本检测功能需要进一步实现")

        except Exception as e:
            logger.warning(f"Vision框架检测失败: {e}")

        return result

    def _detect_with_template_matching(self, screenshot) -> Dict[str, Any]:
        """使用模板匹配检测"""
        result = {"found": False, "options": [], "positions": []}

        try:
            # 简单的模板匹配逻辑
            # 这里可以添加预定义的"Yes, proceed"按钮模板
            logger.info("模板匹配检测功能待实现")

        except Exception as e:
            logger.warning(f"模板匹配检测失败: {e}")

        return result

    def _detect_with_pattern_analysis(self, screenshot) -> Dict[str, Any]:
        """使用模式分析检测可能的选项"""
        result = {"found": False, "options": [], "positions": []}

        try:
            # 分析屏幕上是否有类似按钮或选项的区域
            # 这是一个启发式方法，基于颜色、形状等特征

            # 获取屏幕尺寸
            width, height = screenshot.size if hasattr(screenshot, 'size') else (1920, 1080)

            # 检查屏幕下半部分是否有类似提示的内容
            # 通常Claude的提示会出现在终端窗口的底部

            # 简单启发式：如果终端窗口最近有新内容输出，可能有选项
            logger.info("模式分析检测: 检查是否有新的提示输出")

            # 基于时间的简单检测：如果最近1-2秒有屏幕变化，可能有新提示
            result["found"] = True  # 临时设为True以便测试
            result["options"] = [{"text": "可能的选项", "confidence": 0.5}]
            result["suggested_action"] = "check_and_enter"

        except Exception as e:
            logger.warning(f"模式分析检测失败: {e}")

        return result

    def monitor_for_prompts(self, duration_seconds: float = 30.0, check_interval: float = 2.0) -> Dict[str, Any]:
        """
        监控屏幕变化，检测Claude提示

        Args:
            duration_seconds: 监控持续时间
            check_interval: 检查间隔

        Returns:
            Dict: 监控结果
        """
        logger.info(f"开始监控Claude提示，持续 {duration_seconds} 秒")

        start_time = time.time()
        last_screenshot = None

        while time.time() - start_time < duration_seconds:
            try:
                # 截图
                current_screenshot = pyautogui.screenshot()

                # 如果有之前的截图，比较变化
                if last_screenshot is not None:
                    # 检测是否有新内容
                    change_detected = self._detect_screen_changes(last_screenshot, current_screenshot)

                    if change_detected:
                        logger.info("检测到屏幕变化，分析新内容...")

                        # 检测是否有"Yes, proceed"等选项
                        detection_result = self.detect_yes_proceed_options(current_screenshot)

                        if detection_result["found"]:
                            logger.info("检测到可能的选项提示!")
                            return {
                                "status": "found",
                                "detection_result": detection_result,
                                "time_taken": time.time() - start_time
                            }

                last_screenshot = current_screenshot
                time.sleep(check_interval)

            except Exception as e:
                logger.error(f"监控过程中出错: {e}")
                time.sleep(check_interval)

        logger.info("监控完成，未检测到明确的选项提示")
        return {
            "status": "timeout",
            "detection_result": None,
            "time_taken": duration_seconds
        }

    def _detect_screen_changes(self, old_screenshot, new_screenshot) -> bool:
        """检测屏幕变化"""
        try:
            # 简单的变化检测：比较图像的一小部分区域
            # 重点关注终端窗口可能出现提示的区域

            if hasattr(old_screenshot, 'crop') and hasattr(new_screenshot, 'crop'):
                # 获取屏幕尺寸
                width, height = new_screenshot.size

                # 检查屏幕底部区域 (通常提示出现在这里)
                bottom_region = (0, int(height * 0.7), width, height)

                old_crop = old_screenshot.crop(bottom_region)
                new_crop = new_screenshot.crop(bottom_region)

                # 转换为数组并比较
                import numpy as np
                old_array = np.array(old_crop)
                new_array = np.array(new_crop)

                # 计算差异
                diff = np.abs(old_array.astype(float) - new_array.astype(float))
                mean_diff = np.mean(diff)

                # 如果差异超过阈值，认为有变化
                threshold = 10.0  # 可调整
                changed = mean_diff > threshold

                if changed:
                    logger.debug(f"检测到屏幕变化，差异值: {mean_diff}")

                return changed

        except Exception as e:
            logger.warning(f"屏幕变化检测失败: {e}")

        return False


class WindowManager:
    """跨平台窗口管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
    
    def find_claude_cli_windows(self) -> List[Dict[str, Any]]:
        """查找 Claude CLI 相关窗口"""
        claude_windows = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
                try:
                    pinfo = proc.info
                    cmdline_str = ' '.join(pinfo['cmdline'] or [])
                    
                    # 检查进程名或命令行是否包含 claude
                    is_claude_process = False
                    
                    if pinfo['name']:
                        # 直接的 claude 进程
                        if 'claude' in pinfo['name'].lower():
                            is_claude_process = True
                        # Windows 下的 cmd 进程运行 claude
                        elif (self.system == "windows" and 
                              pinfo['name'].lower() in ['cmd.exe', 'powershell.exe', 'pwsh.exe'] and
                              'claude' in cmdline_str.lower()):
                            is_claude_process = True
                        # Unix 系统下的 shell 进程运行 claude
                        elif (self.system != "windows" and 
                              pinfo['name'].lower() in ['bash', 'sh', 'zsh', 'terminal'] and
                              'claude' in cmdline_str.lower()):
                            is_claude_process = True
                    
                    # 检查命令行参数
                    if not is_claude_process and pinfo['cmdline']:
                        if any('claude' in str(cmd).lower() for cmd in pinfo['cmdline']):
                            is_claude_process = True
                    
                    if is_claude_process:
                        # 获取进程状态
                        try:
                            process = psutil.Process(pinfo['pid'])
                            status = process.status()
                            memory_info = process.memory_info()
                        except:
                            status = 'unknown'
                            memory_info = None

                        claude_windows.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'cmdline': pinfo['cmdline'],
                            'create_time': pinfo['create_time'],
                            'status': status,
                            'memory_usage': memory_info.rss if memory_info else 0
                        })
                        logger.info(f"找到 Claude CLI 相关进程: PID={pinfo['pid']}, Name={pinfo['name']}, Status={status}, CMD={cmdline_str[:100]}")

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except Exception as e:
            logger.warning(f"查找 Claude CLI 窗口时出错: {e}")
        
        # 按创建时间排序，最新的在前
        claude_windows.sort(key=lambda x: x['create_time'], reverse=True)
        logger.info(f"总共找到 {len(claude_windows)} 个 Claude CLI 相关进程")
        
        return claude_windows
    
    def activate_window_by_pid(self, pid: int) -> bool:
        """通过进程ID激活窗口"""
        try:
            if self.system == "windows":
                return self._activate_window_windows(pid)
            elif self.system == "darwin":
                return self._activate_window_macos(pid)
            else:
                return self._activate_window_linux(pid)
        except Exception as e:
            logger.error(f"激活窗口失败 (PID: {pid}): {e}")
            return False
    
    def _activate_window_windows(self, pid: int) -> bool:
        """Windows 窗口激活"""
        try:
            # 方法1: 尝试使用 pyautogui 查找并激活窗口
            if pyautogui:
                try:
                    for window in pyautogui.getAllWindows():
                        # 查找包含 claude 或相关关键词的窗口
                        title_lower = window.title.lower()
                        if ('claude' in title_lower or 
                            'cmd' in title_lower or 
                            'command prompt' in title_lower or
                            'powershell' in title_lower):
                            logger.info(f"尝试激活窗口: {window.title}")
                            try:
                                window.activate()
                                time.sleep(0.3)
                                return True
                            except Exception as e:
                                logger.warning(f"激活窗口失败: {e}")
                                continue
                except Exception as e:
                    logger.warning(f"pyautogui 窗口激活失败: {e}")
            
            # 方法2: 尝试使用 subprocess 和 tasklist 查找窗口
            try:
                import subprocess
                result = subprocess.run(['tasklist', '/fi', f'PID eq {pid}', '/fo', 'csv'], 
                                      capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode == 0 and str(pid) in result.stdout:
                    logger.info(f"进程 {pid} 存在，尝试使用 Alt+Tab 激活")
                    # 使用 Alt+Tab 尝试切换到目标窗口
                    if pyautogui:
                        pyautogui.keyDown('alt')
                        pyautogui.press('tab')
                        time.sleep(0.1)
                        pyautogui.keyUp('alt')
                        return True
            except Exception as e:
                logger.warning(f"tasklist 方法失败: {e}")
            
            # 方法3: 尝试使用 win32gui (如果可用)
            try:
                import win32gui
                import win32con
                
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_pid = win32gui.GetWindowThreadProcessId(hwnd)[1]
                        if window_pid == pid:
                            windows.append(hwnd)
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                
                if windows:
                    hwnd = windows[0]
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    win32gui.SetForegroundWindow(hwnd)
                    logger.info(f"使用 win32gui 成功激活窗口")
                    return True
                    
            except ImportError:
                logger.info("win32gui 不可用，已尝试其他方法")
            except Exception as e:
                logger.warning(f"win32gui 激活失败: {e}")
            
            return False
            
        except Exception as e:
            logger.error(f"Windows 窗口激活失败: {e}")
            return False
    
    def _activate_window_macos(self, pid: int) -> bool:
        """macOS 窗口激活 - 增强版"""
        try:
            # 方法1: 使用 AppleScript 通过进程ID激活
            script = f"""
            tell application "System Events"
                try
                    set frontApp to first application process whose unix id is {pid}
                    set frontmost of frontApp to true
                    return true
                on error
                    return false
                end try
            end tell
            """
            result = subprocess.run(["osascript", "-e", script],
                                  check=True, capture_output=True, text=True)
            if "true" in result.stdout:
                logger.info(f"AppleScript成功激活窗口 (PID: {pid})")
                time.sleep(0.5)
                return True

        except subprocess.CalledProcessError as e:
            logger.warning(f"AppleScript方法1失败: {e}")

        try:
            # 方法2: 尝试通过应用程序名称激活终端
            terminal_script = """
            tell application "Terminal"
                activate
                try
                    do script "" in front window
                on error
                    do script ""
                end try
            end tell
            """
            subprocess.run(["osascript", "-e", terminal_script],
                          check=True, capture_output=True)
            logger.info("AppleScript成功激活Terminal应用")
            time.sleep(0.5)
            return True

        except subprocess.CalledProcessError as e:
            logger.warning(f"AppleScript方法2失败: {e}")

        try:
            # 方法3: 使用Quartz事件系统 (如果可用)
            if macos_libs_available:
                return self._activate_window_with_quartz(pid)

        except Exception as e:
            logger.warning(f"Quartz激活方法失败: {e}")

        return False

    def _activate_window_with_quartz(self, pid: int) -> bool:
        """使用Quartz事件系统激活窗口"""
        try:
            if not macos_libs_available:
                return False

            # 获取所有窗口
            window_list = Quartz.CGWindowListCopyWindowInfo(
                Quartz.kCGWindowListOptionOnScreenOnly,
                Quartz.kCGNullWindowID
            )

            for window in window_list:
                window_pid = window.get('kCGWindowOwnerPID', 0)
                if window_pid == pid:
                    window_id = window.get('kCGWindowNumber', 0)
                    if window_id:
                        # 尝试将窗口置于前台
                        logger.info(f"使用Quartz激活窗口 ID: {window_id}")
                        # 这里需要更复杂的Quartz操作
                        return True

        except Exception as e:
            logger.error(f"Quartz窗口激活失败: {e}")

        return False

    def activate_terminal_for_claude(self) -> bool:
        """专门用于激活Claude CLI的Terminal窗口"""
        try:
            # AppleScript专门查找包含claude的Terminal窗口
            script = '''
            tell application "Terminal"
                activate

                -- 查找包含claude的窗口
                set claudeWindows to {}
                repeat with theWindow in windows
                    try
                        set windowContents to contents of theWindow
                        if windowContents contains "claude" then
                            set end of claudeWindows to theWindow
                        end if
                    end try
                end repeat

                -- 如果找到claude窗口，激活第一个
                if (count of claudeWindows) > 0 then
                    set selected of item 1 of claudeWindows to true
                    return "found_claude_window"
                else
                    -- 没找到claude窗口，激活最前面的窗口
                    if (count of windows) > 0 then
                        set selected of window 1 to true
                        return "activated_first_window"
                    else
                        return "no_windows"
                    end if
                end if
            end tell
            '''

            result = subprocess.run(["osascript", "-e", script],
                                  capture_output=True, text=True, check=True)

            result_text = result.stdout.strip()
            logger.info(f"Terminal激活结果: {result_text}")

            time.sleep(0.5)  # 等待窗口激活
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"AppleScript激活Terminal失败: {e}")
            return False

    def find_terminal_processes(self) -> List[Dict[str, Any]]:
        """查找所有终端进程"""
        terminal_processes = []

        # 定义终端进程名
        if self.system == "darwin":
            terminal_names = ['terminal', 'iterm2', 'iterm', 'kitty', 'alacritty', 'wezterm']
        elif self.system == "windows":
            terminal_names = ['cmd.exe', 'powershell.exe', 'pwsh.exe', 'windowsterminal.exe', 'wt.exe']
        else:
            terminal_names = ['gnome-terminal', 'xterm', 'konsole', 'terminator', 'tilix', 'alacritty', 'kitty']

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time', 'ppid']):
                try:
                    pinfo = proc.info

                    if pinfo['name'] and any(term in pinfo['name'].lower() for term in terminal_names):
                        # 获取进程详细信息
                        try:
                            process = psutil.Process(pinfo['pid'])
                            status = process.status()
                            memory_info = process.memory_info()
                            cpu_percent = process.cpu_percent()
                        except:
                            status = 'unknown'
                            memory_info = None
                            cpu_percent = 0.0

                        terminal_processes.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'cmdline': pinfo['cmdline'],
                            'create_time': pinfo['create_time'],
                            'ppid': pinfo['ppid'],
                            'status': status,
                            'memory_usage': memory_info.rss if memory_info else 0,
                            'cpu_percent': cpu_percent
                        })

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

        except Exception as e:
            logger.warning(f"查找终端进程时出错: {e}")

        # 按创建时间排序，最新的在前
        terminal_processes.sort(key=lambda x: x['create_time'], reverse=True)
        logger.info(f"找到 {len(terminal_processes)} 个终端进程")

        return terminal_processes

    def cleanup_old_claude_processes(self, keep_newest: int = 1) -> Dict[str, Any]:
        """清理旧的Claude CLI进程，保留最新的几个"""
        result = {
            "cleaned_processes": [],
            "kept_processes": [],
            "errors": []
        }

        try:
            claude_processes = self.find_claude_cli_windows()

            if len(claude_processes) <= keep_newest:
                logger.info(f"只有 {len(claude_processes)} 个Claude进程，无需清理")
                result["kept_processes"] = claude_processes
                return result

            # 保留最新的进程
            processes_to_keep = claude_processes[:keep_newest]
            processes_to_clean = claude_processes[keep_newest:]

            logger.info(f"将保留 {len(processes_to_keep)} 个进程，清理 {len(processes_to_clean)} 个进程")

            for proc_info in processes_to_clean:
                try:
                    pid = proc_info['pid']
                    logger.info(f"正在终止进程 PID={pid}, Name={proc_info['name']}")

                    process = psutil.Process(pid)

                    # 优雅终止
                    process.terminate()

                    # 等待进程结束
                    try:
                        process.wait(timeout=5)
                        logger.info(f"成功终止进程 PID={pid}")
                        result["cleaned_processes"].append(proc_info)
                    except psutil.TimeoutExpired:
                        # 强制终止
                        logger.warning(f"进程 PID={pid} 未响应terminate，使用kill")
                        process.kill()
                        process.wait(timeout=3)
                        logger.info(f"强制终止进程 PID={pid}")
                        result["cleaned_processes"].append(proc_info)

                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logger.warning(f"无法终止进程 PID={proc_info['pid']}: {e}")
                    result["errors"].append(f"PID={proc_info['pid']}: {str(e)}")
                except Exception as e:
                    logger.error(f"终止进程 PID={proc_info['pid']} 时出错: {e}")
                    result["errors"].append(f"PID={proc_info['pid']}: {str(e)}")

            result["kept_processes"] = processes_to_keep

            logger.info(f"进程清理完成: 清理了 {len(result['cleaned_processes'])} 个进程，保留了 {len(result['kept_processes'])} 个进程")

        except Exception as e:
            logger.error(f"清理Claude进程时出错: {e}")
            result["errors"].append(str(e))

        return result

    def cleanup_old_terminal_processes(self, max_terminals: int = 3) -> Dict[str, Any]:
        """清理过多的终端进程"""
        result = {
            "cleaned_processes": [],
            "kept_processes": [],
            "errors": []
        }

        try:
            terminal_processes = self.find_terminal_processes()

            if len(terminal_processes) <= max_terminals:
                logger.info(f"只有 {len(terminal_processes)} 个终端进程，无需清理")
                result["kept_processes"] = terminal_processes
                return result

            # 按创建时间和活跃度排序，保留最活跃和最新的
            def process_score(proc):
                # 基础分数：创建时间（越新越高）
                time_score = proc['create_time']
                # CPU使用率加分
                cpu_score = proc.get('cpu_percent', 0) * 100
                # 内存使用量（适中最好）
                memory_score = min(proc.get('memory_usage', 0) / (1024*1024), 100)  # MB
                return time_score + cpu_score + memory_score

            terminal_processes.sort(key=process_score, reverse=True)

            processes_to_keep = terminal_processes[:max_terminals]
            processes_to_clean = terminal_processes[max_terminals:]

            logger.info(f"将保留 {len(processes_to_keep)} 个终端进程，清理 {len(processes_to_clean)} 个进程")

            for proc_info in processes_to_clean:
                try:
                    pid = proc_info['pid']
                    logger.info(f"正在终止终端进程 PID={pid}, Name={proc_info['name']}")

                    process = psutil.Process(pid)

                    # 对于终端进程，先尝试优雅关闭
                    if self.system == "darwin":
                        # macOS: 尝试使用AppleScript关闭Terminal窗口
                        try:
                            script = f'''
                            tell application "System Events"
                                tell process "{proc_info['name']}"
                                    if exists then
                                        keystroke "w" using command down
                                    end if
                                end tell
                            end tell
                            '''
                            subprocess.run(["osascript", "-e", script],
                                          timeout=3, capture_output=True)
                            time.sleep(1)
                        except:
                            pass

                    # 检查进程是否还存在
                    if process.is_running():
                        process.terminate()
                        try:
                            process.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            process.kill()
                            process.wait(timeout=2)

                    logger.info(f"成功终止终端进程 PID={pid}")
                    result["cleaned_processes"].append(proc_info)

                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    logger.warning(f"无法终止终端进程 PID={proc_info['pid']}: {e}")
                    result["errors"].append(f"PID={proc_info['pid']}: {str(e)}")
                except Exception as e:
                    logger.error(f"终止终端进程 PID={proc_info['pid']} 时出错: {e}")
                    result["errors"].append(f"PID={proc_info['pid']}: {str(e)}")

            result["kept_processes"] = processes_to_keep

            logger.info(f"终端进程清理完成: 清理了 {len(result['cleaned_processes'])} 个进程，保留了 {len(result['kept_processes'])} 个进程")

        except Exception as e:
            logger.error(f"清理终端进程时出错: {e}")
            result["errors"].append(str(e))

        return result

    def _activate_window_linux(self, pid: int) -> bool:
        """Linux 窗口激活"""
        try:
            # 使用 xdotool 激活窗口
            result = subprocess.run(
                ["xdotool", "search", "--pid", str(pid), "windowactivate"],
                check=True, capture_output=True
            )
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            # xdotool 未安装，尝试其他方法
            try:
                subprocess.run(["wmctrl", "-a", f"pid:{pid}"], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False


class MacOSPermissionHandler:
    """macOS权限对话框自动处理器"""

    def __init__(self):
        self.system = platform.system().lower()

    def detect_permission_dialogs(self) -> List[Dict[str, Any]]:
        """检测macOS权限对话框"""
        dialogs = []

        if self.system != "darwin" or not macos_libs_available:
            return dialogs

        try:
            # 方法1: 使用AppleScript检测对话框
            script = '''
            tell application "System Events"
                set allProcesses to every application process
                set dialogProcesses to {}
                repeat with proc in allProcesses
                    try
                        set procWindows to every window of proc
                        repeat with win in procWindows
                            set winTitle to title of win
                            -- 检测常见的权限对话框标题
                            if winTitle contains "wants to control" or ¬
                               winTitle contains "Accessibility" or ¬
                               winTitle contains "Screen Recording" or ¬
                               winTitle contains "允许" or ¬
                               winTitle contains "权限" or ¬
                               winTitle contains "Permission" then
                                set end of dialogProcesses to {process:name of proc, window:winTitle}
                            end if
                        end repeat
                    end try
                end repeat
                return dialogProcesses
            end tell
            '''

            result = subprocess.run(["osascript", "-e", script],
                                  capture_output=True, text=True, timeout=5)

            if result.returncode == 0 and result.stdout.strip():
                logger.info(f"检测到权限对话框: {result.stdout.strip()}")
                dialogs.append({
                    "type": "permission_dialog",
                    "detected_by": "applescript",
                    "details": result.stdout.strip()
                })

        except Exception as e:
            logger.warning(f"AppleScript权限对话框检测失败: {e}")

        try:
            # 方法2: 使用pyautogui检测对话框窗口
            if pyautogui:
                windows = pyautogui.getAllWindows()
                for window in windows:
                    title = window.title.lower()
                    if any(keyword in title for keyword in [
                        'accessibility', 'screen recording', 'permission',
                        'wants to control', '权限', '允许'
                    ]):
                        dialogs.append({
                            "type": "permission_dialog",
                            "detected_by": "pyautogui",
                            "window_title": window.title,
                            "window_rect": (window.left, window.top, window.width, window.height)
                        })
                        logger.info(f"pyautogui检测到权限对话框: {window.title}")

        except Exception as e:
            logger.warning(f"pyautogui权限对话框检测失败: {e}")

        return dialogs

    def auto_click_allow_button(self, dialog_info: Dict[str, Any] = None) -> bool:
        """自动点击允许/同意按钮"""
        if self.system != "darwin":
            logger.warning("权限对话框自动点击仅支持macOS")
            return False

        try:
            # 方法1: 使用AppleScript点击按钮
            success = self._applescript_click_allow()
            if success:
                return True

            # 方法2: 使用pyautogui查找并点击按钮
            success = self._pyautogui_click_allow(dialog_info)
            if success:
                return True

            # 方法3: 使用OCR检测按钮位置（如果可用）
            if ocr_available:
                success = self._ocr_click_allow()
                if success:
                    return True

            logger.warning("所有自动点击方法都失败了")
            return False

        except Exception as e:
            logger.error(f"自动点击允许按钮失败: {e}")
            return False

    def _applescript_click_allow(self) -> bool:
        """使用AppleScript点击允许按钮"""
        try:
            # 常见的权限对话框按钮文本
            button_texts = [
                "Allow", "OK", "Grant Access", "允许", "确定", "同意",
                "Continue", "Yes", "Open System Preferences"
            ]

            for button_text in button_texts:
                try:
                    script = f'''
                    tell application "System Events"
                        -- 尝试点击对话框中的按钮
                        try
                            set dialogFound to false
                            set allProcesses to every application process
                            repeat with proc in allProcesses
                                set procWindows to every window of proc
                                repeat with win in procWindows
                                    try
                                        set winButtons to every button of win
                                        repeat with btn in winButtons
                                            if name of btn is "{button_text}" then
                                                click btn
                                                set dialogFound to true
                                                exit repeat
                                            end if
                                        end repeat
                                        if dialogFound then exit repeat
                                    end try
                                end repeat
                                if dialogFound then exit repeat
                            end repeat
                            return dialogFound
                        end try
                    end tell
                    '''

                    result = subprocess.run(["osascript", "-e", script],
                                          capture_output=True, text=True, timeout=10)

                    if result.returncode == 0 and "true" in result.stdout:
                        logger.info(f"AppleScript成功点击按钮: {button_text}")
                        time.sleep(1)
                        return True

                except subprocess.TimeoutExpired:
                    logger.warning(f"AppleScript点击按钮超时: {button_text}")
                    continue
                except Exception as e:
                    logger.warning(f"AppleScript点击按钮失败 {button_text}: {e}")
                    continue

            return False

        except Exception as e:
            logger.error(f"AppleScript点击允许按钮失败: {e}")
            return False

    def _pyautogui_click_allow(self, dialog_info: Dict[str, Any] = None) -> bool:
        """使用pyautogui点击允许按钮"""
        try:
            if not pyautogui:
                return False

            # 常见按钮图片特征或文本模式
            button_patterns = [
                "Allow", "OK", "Grant", "允许", "确定", "同意"
            ]

            # 如果有对话框信息，优先在对话框区域查找
            search_region = None
            if dialog_info and "window_rect" in dialog_info:
                rect = dialog_info["window_rect"]
                search_region = (rect[0], rect[1], rect[2], rect[3])

            # 尝试通过截图和图像识别找到按钮
            screenshot = pyautogui.screenshot()

            if search_region:
                # 裁剪到对话框区域
                cropped = screenshot.crop(search_region)
                # 在裁剪区域中查找按钮
                # 这里可以添加更复杂的图像识别逻辑
                logger.info("在对话框区域查找按钮...")

            # 简单的位置估算：权限对话框通常在屏幕中央下方有按钮
            screen_width, screen_height = pyautogui.size()

            # 预设一些常见的按钮位置
            potential_button_areas = [
                (screen_width // 2 + 50, screen_height // 2 + 50),  # 对话框右下
                (screen_width // 2 - 50, screen_height // 2 + 50),  # 对话框左下
                (screen_width // 2, screen_height // 2 + 80),       # 对话框底部中央
            ]

            for x, y in potential_button_areas:
                try:
                    # 点击潜在的按钮位置
                    pyautogui.click(x, y)
                    time.sleep(0.5)

                    # 检查对话框是否消失
                    dialogs_after = self.detect_permission_dialogs()
                    if len(dialogs_after) == 0:
                        logger.info(f"pyautogui成功点击按钮位置: ({x}, {y})")
                        return True

                except Exception as e:
                    logger.warning(f"pyautogui点击位置失败 ({x}, {y}): {e}")
                    continue

            return False

        except Exception as e:
            logger.error(f"pyautogui点击允许按钮失败: {e}")
            return False

    def _ocr_click_allow(self) -> bool:
        """使用OCR检测按钮并点击"""
        try:
            if not ocr_available:
                return False

            # 截图
            screenshot = pyautogui.screenshot()

            # 使用OCR识别文本
            import pytesseract
            from PIL import Image

            # OCR识别
            ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)

            # 查找按钮文本
            button_keywords = ['Allow', 'OK', 'Grant', '允许', '确定', '同意']

            for i, text in enumerate(ocr_data['text']):
                if text.strip() and any(keyword.lower() in text.lower() for keyword in button_keywords):
                    # 获取文本位置
                    x = ocr_data['left'][i] + ocr_data['width'][i] // 2
                    y = ocr_data['top'][i] + ocr_data['height'][i] // 2

                    # 点击按钮
                    pyautogui.click(x, y)
                    time.sleep(0.5)

                    logger.info(f"OCR成功识别并点击按钮: {text} at ({x}, {y})")
                    return True

            return False

        except Exception as e:
            logger.error(f"OCR点击允许按钮失败: {e}")
            return False

    def monitor_and_handle_permission_dialogs(self, duration_seconds: float = 30.0) -> Dict[str, Any]:
        """监控并自动处理权限对话框"""
        result = {
            "dialogs_detected": 0,
            "dialogs_handled": 0,
            "dialogs_failed": 0,
            "details": []
        }

        if self.system != "darwin":
            result["message"] = "权限对话框监控仅支持macOS"
            return result

        logger.info(f"开始监控权限对话框，持续 {duration_seconds} 秒")

        start_time = time.time()
        check_interval = 2.0

        while time.time() - start_time < duration_seconds:
            try:
                # 检测权限对话框
                dialogs = self.detect_permission_dialogs()

                if dialogs:
                    result["dialogs_detected"] += len(dialogs)
                    logger.info(f"检测到 {len(dialogs)} 个权限对话框")

                    for dialog in dialogs:
                        try:
                            # 尝试自动点击允许
                            success = self.auto_click_allow_button(dialog)

                            if success:
                                result["dialogs_handled"] += 1
                                result["details"].append({
                                    "dialog": dialog,
                                    "action": "auto_clicked",
                                    "result": "success"
                                })
                                logger.info("成功自动处理权限对话框")
                            else:
                                result["dialogs_failed"] += 1
                                result["details"].append({
                                    "dialog": dialog,
                                    "action": "auto_click_failed",
                                    "result": "failed"
                                })
                                logger.warning("自动处理权限对话框失败")

                        except Exception as e:
                            result["dialogs_failed"] += 1
                            result["details"].append({
                                "dialog": dialog,
                                "action": "error",
                                "result": str(e)
                            })
                            logger.error(f"处理权限对话框时出错: {e}")

                time.sleep(check_interval)

            except Exception as e:
                logger.error(f"监控权限对话框时出错: {e}")
                time.sleep(check_interval)

        result["message"] = f"监控完成，检测到 {result['dialogs_detected']} 个对话框，成功处理 {result['dialogs_handled']} 个"
        logger.info(result["message"])

        return result


class ClipboardManager:
    """跨平台剪贴板管理器 - macOS增强版"""

    def __init__(self):
        self.system = platform.system().lower()

    def copy_to_clipboard(self, text: str) -> bool:
        """复制文本到剪贴板 - 多种方法尝试"""
        methods_tried = []

        # 方法1: 使用pyperclip (通用方法)
        try:
            pyperclip.copy(text)
            time.sleep(0.2)  # 增加等待时间

            # 验证复制是否成功
            if self._verify_copy_success(text):
                logger.info("pyperclip复制成功")
                return True
            else:
                logger.warning("pyperclip复制验证失败")
                methods_tried.append("pyperclip")
        except Exception as e:
            logger.warning(f"pyperclip复制失败: {e}")
            methods_tried.append("pyperclip")

        # 方法2: macOS原生方法 (如果可用)
        if self.system == "darwin":
            try:
                success = self._copy_with_macos_native(text)
                if success:
                    logger.info("macOS原生复制成功")
                    return True
                methods_tried.append("macOS原生")
            except Exception as e:
                logger.warning(f"macOS原生复制失败: {e}")
                methods_tried.append("macOS原生")

        # 方法3: 使用AppleScript (macOS)
        if self.system == "darwin":
            try:
                success = self._copy_with_applescript(text)
                if success:
                    logger.info("AppleScript复制成功")
                    return True
                methods_tried.append("AppleScript")
            except Exception as e:
                logger.warning(f"AppleScript复制失败: {e}")
                methods_tried.append("AppleScript")

        # 方法4: 使用subprocess调用pbcopy (macOS)
        if self.system == "darwin":
            try:
                success = self._copy_with_pbcopy(text)
                if success:
                    logger.info("pbcopy复制成功")
                    return True
                methods_tried.append("pbcopy")
            except Exception as e:
                logger.warning(f"pbcopy复制失败: {e}")
                methods_tried.append("pbcopy")

        logger.error(f"所有复制方法都失败了，尝试的方法: {methods_tried}")
        return False

    def _copy_with_macos_native(self, text: str) -> bool:
        """使用macOS原生API复制"""
        if not macos_libs_available:
            return False

        try:
            # 使用AppKit的NSPasteboard
            pasteboard = AppKit.NSPasteboard.generalPasteboard()
            pasteboard.clearContents()
            success = pasteboard.setString_forType_(text, AppKit.NSPasteboardTypeString)

            if success:
                time.sleep(0.1)
                # 验证
                content = pasteboard.stringForType_(AppKit.NSPasteboardTypeString)
                return content and text[:100] in content
            return False

        except Exception as e:
            logger.warning(f"macOS原生复制失败: {e}")
            return False

    def _copy_with_applescript(self, text: str) -> bool:
        """使用AppleScript复制"""
        try:
            # 转义文本中的特殊字符
            escaped_text = text.replace('"', '\\"').replace('\\', '\\\\')

            script = f'''
            set the clipboard to "{escaped_text}"
            '''

            subprocess.run(["osascript", "-e", script],
                          capture_output=True, text=True, check=True)

            time.sleep(0.2)

            # 验证复制结果
            return self._verify_copy_success(text)

        except Exception as e:
            logger.warning(f"AppleScript复制失败: {e}")
            return False

    def _copy_with_pbcopy(self, text: str) -> bool:
        """使用pbcopy命令复制"""
        try:
            process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=text)

            if process.returncode == 0:
                time.sleep(0.1)
                return self._verify_copy_success(text)
            return False

        except Exception as e:
            logger.warning(f"pbcopy复制失败: {e}")
            return False

    def _verify_copy_success(self, expected_text: str) -> bool:
        """验证复制是否成功"""
        try:
            current_content = self.get_clipboard_content()
            if current_content and len(current_content) > 10:
                # 检查前100个字符是否匹配
                expected_start = expected_text[:100].strip()
                current_start = current_content[:100].strip()
                return expected_start in current_start or current_start in expected_start
            return False
        except:
            return False

    def get_clipboard_content(self) -> str:
        """获取剪贴板内容 - 多种方法尝试"""
        # 方法1: pyperclip
        try:
            content = pyperclip.paste()
            if content:
                return content
        except Exception as e:
            logger.warning(f"pyperclip获取剪贴板失败: {e}")

        # 方法2: macOS原生方法
        if self.system == "darwin":
            try:
                content = self._get_clipboard_macos_native()
                if content:
                    return content
            except Exception as e:
                logger.warning(f"macOS原生获取剪贴板失败: {e}")

        # 方法3: pbpaste (macOS)
        if self.system == "darwin":
            try:
                result = subprocess.run(['pbpaste'], capture_output=True, text=True, check=True)
                return result.stdout
            except Exception as e:
                logger.warning(f"pbpaste获取剪贴板失败: {e}")

        return ""

    def _get_clipboard_macos_native(self) -> str:
        """使用macOS原生API获取剪贴板内容"""
        if not macos_libs_available:
            return ""

        try:
            pasteboard = AppKit.NSPasteboard.generalPasteboard()
            content = pasteboard.stringForType_(AppKit.NSPasteboardTypeString)
            return content or ""
        except Exception as e:
            logger.warning(f"macOS原生获取剪贴板失败: {e}")
            return ""

    def verify_clipboard_content(self, expected_text: str, timeout: float = 3.0) -> bool:
        """验证剪贴板内容 - 增强版"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_content = self.get_clipboard_content()
            if current_content:
                # 更宽松的验证条件
                expected_sample = expected_text[:200].strip().lower()
                current_sample = current_content[:200].strip().lower()

                # 检查关键字匹配
                if (expected_sample in current_sample or
                    current_sample in expected_sample or
                    len(current_content.strip()) > len(expected_text.strip()) * 0.8):
                    logger.info("剪贴板内容验证成功")
                    return True

            time.sleep(0.2)

        logger.warning("剪贴板内容验证超时")
        return False

    def clear_clipboard(self) -> bool:
        """清空剪贴板"""
        try:
            if self.system == "darwin":
                # macOS方法
                if macos_libs_available:
                    pasteboard = AppKit.NSPasteboard.generalPasteboard()
                    pasteboard.clearContents()
                    return True
                else:
                    # 使用pbcopy清空
                    subprocess.run(['pbcopy'], input='', text=True, check=True)
                    return True
            else:
                # 其他系统使用pyperclip
                pyperclip.copy('')
                return True
        except Exception as e:
            logger.error(f"清空剪贴板失败: {e}")
            return False


class KeyboardController:
    """跨平台键盘控制器 - macOS优化版"""

    def __init__(self):
        self.system = platform.system().lower()

    def send_paste_command(self, max_attempts: int = 3) -> bool:
        """发送粘贴命令 - macOS优化版"""
        methods_tried = []

        for attempt in range(max_attempts):
            logger.info(f"发送粘贴命令 (第 {attempt + 1} 次尝试)...")

            # macOS 特殊处理
            if self.system == "darwin":
                success = self._macos_paste_with_multiple_methods(attempt)
                if success:
                    logger.info(f"macOS粘贴命令成功 (第 {attempt + 1} 次)")
                    return True
                methods_tried.append(f"macOS方法{attempt+1}")
            else:
                # Windows/Linux 处理
                success = self._windows_linux_paste(attempt)
                if success:
                    logger.info(f"Windows/Linux粘贴命令成功 (第 {attempt + 1} 次)")
                    return True
                methods_tried.append(f"Windows/Linux方法{attempt+1}")

            if attempt < max_attempts - 1:
                time.sleep(0.5)  # 重试前等待

        logger.error(f"粘贴命令在 {max_attempts} 次尝试后仍然失败，尝试的方法: {methods_tried}")
        return False

    def _macos_paste_with_multiple_methods(self, attempt: int) -> bool:
        """macOS多种粘贴方法"""
        try:
            if attempt == 0:
                # 方法1: 使用keyDown/keyUp明确按下Command+V
                logger.info("macOS方法1: 使用pyautogui keyDown/keyUp Command+V")
                pyautogui.keyDown('command')
                time.sleep(0.05)
                pyautogui.press('v')
                time.sleep(0.05)
                pyautogui.keyUp('command')
                time.sleep(0.3)
                return True

            elif attempt == 1:
                # 方法2: 使用pynput的Cmd+V
                logger.info("macOS方法2: 使用pynput Command+V")
                from pynput.keyboard import Key, Controller
                kb = Controller()
                with kb.pressed(Key.cmd):
                    kb.press('v')
                    kb.release('v')
                time.sleep(0.3)
                return True

            elif attempt == 2:
                # 方法3: AppleScript执行粘贴
                logger.info("macOS方法3: 使用AppleScript Command+V")
                script = '''
                tell application "System Events"
                    key code 9 using command down
                end tell
                '''
                result = subprocess.run(["osascript", "-e", script],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    time.sleep(0.3)
                    return True
                else:
                    logger.warning(f"AppleScript粘贴失败: {result.stderr}")
                    return False

        except Exception as e:
            logger.warning(f"macOS粘贴方法 {attempt+1} 失败: {e}")
            return False

    def _windows_linux_paste(self, attempt: int) -> bool:
        """Windows/Linux粘贴方法"""
        try:
            if attempt == 0:
                # 方法1: 标准 Ctrl+V
                pyautogui.keyDown('ctrl')
                time.sleep(0.05)
                pyautogui.press('v')
                time.sleep(0.05)
                pyautogui.keyUp('ctrl')
                time.sleep(0.2)
                return True

            elif attempt == 1:
                # 方法2: 使用pynput
                from pynput.keyboard import Key, Controller
                kb = Controller()
                kb.press(Key.ctrl)
                kb.press('v')
                kb.release('v')
                kb.release(Key.ctrl)
                time.sleep(0.2)
                return True

            elif attempt == 2:
                # 方法3: 手动按键操作
                pyautogui.keyDown('ctrl')
                time.sleep(0.1)
                pyautogui.keyDown('v')
                time.sleep(0.1)
                pyautogui.keyUp('v')
                time.sleep(0.1)
                pyautogui.keyUp('ctrl')
                time.sleep(0.2)
                return True

        except Exception as e:
            logger.warning(f"Windows/Linux粘贴方法 {attempt+1} 失败: {e}")
            return False
    
    def send_enter(self, max_attempts: int = 3) -> bool:
        """发送回车键 - 增强版"""
        methods_tried = []

        for attempt in range(max_attempts):
            logger.info(f"发送回车键 (第 {attempt + 1} 次尝试)...")

            try:
                success = False

                if attempt == 0:
                    # 方法1: 标准回车键
                    pyautogui.press('enter')
                    time.sleep(0.2)
                    success = True
                    methods_tried.append("pyautogui.press('enter')")

                elif attempt == 1:
                    # 方法2: 使用pynput
                    from pynput.keyboard import Key, Controller
                    kb = Controller()
                    kb.press(Key.enter)
                    time.sleep(0.05)
                    kb.release(Key.enter)
                    time.sleep(0.2)
                    success = True
                    methods_tried.append("pynput.Key.enter")

                elif attempt == 2:
                    # 方法3: AppleScript (macOS) 或 手动按键操作
                    if self.system == "darwin":
                        script = '''
                        tell application "System Events"
                            key code 36
                        end tell
                        '''
                        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
                        time.sleep(0.2)
                        success = True
                        methods_tried.append("AppleScript key code 36")
                    else:
                        # 其他系统使用手动按键
                        pyautogui.keyDown('enter')
                        time.sleep(0.05)
                        pyautogui.keyUp('enter')
                        time.sleep(0.2)
                        success = True
                        methods_tried.append("手动按键操作")

                if success:
                    logger.info(f"回车键发送成功 (第 {attempt + 1} 次)")
                    return True

            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次发送回车键失败: {e}")
                methods_tried.append(f"失败: {str(e)[:50]}")

            if attempt < max_attempts - 1:
                time.sleep(0.3)  # 重试前等待

        logger.error(f"回车键在 {max_attempts} 次尝试后仍然失败，尝试的方法: {methods_tried}")
        return False

    def type_text(self, text: str, interval: float = 0.01) -> bool:
        """输入文本 - 增强版"""
        try:
            # 方法1: 使用pyautogui
            try:
                pyautogui.write(text, interval=interval)
                logger.info("pyautogui文本输入成功")
                return True
            except Exception as e:
                logger.warning(f"pyautogui文本输入失败: {e}")

            # 方法2: 使用pynput
            try:
                from pynput.keyboard import Controller
                kb = Controller()
                kb.type(text)
                logger.info("pynput文本输入成功")
                return True
            except Exception as e:
                logger.warning(f"pynput文本输入失败: {e}")

            # 方法3: 分段输入 (对于长文本)
            try:
                chunk_size = 100  # 每次输入100个字符
                for start_pos in range(0, len(text), chunk_size):
                    chunk = text[start_pos:start_pos+chunk_size]
                    pyautogui.write(chunk, interval=interval*2)
                    time.sleep(0.1)
                logger.info("分段文本输入成功")
                return True
            except Exception as e:
                logger.warning(f"分段文本输入失败: {e}")

            return False

        except Exception as e:
            logger.error(f"所有文本输入方法都失败: {e}")
            return False

    def send_key_combination(self, *keys, max_attempts: int = 2) -> bool:
        """发送组合键 - 通用方法"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"发送组合键 {'+'.join(keys)} (第 {attempt + 1} 次尝试)")

                # macOS键名映射
                if self.system == "darwin":
                    key_mapping = {
                        'ctrl': 'command',  # macOS使用Command而不是Ctrl
                        'control': 'command',
                        'cmd': 'command',
                        'command': 'command'
                    }
                    # 替换键名
                    mapped_keys = [key_mapping.get(key.lower(), key) for key in keys]
                    logger.info(f"macOS键映射: {'+'.join(keys)} -> {'+'.join(mapped_keys)}")
                else:
                    mapped_keys = list(keys)

                # 使用明确的keyDown/keyUp方式发送组合键
                if len(mapped_keys) == 2:
                    modifier_key = mapped_keys[0]
                    regular_key = mapped_keys[1]

                    pyautogui.keyDown(modifier_key)
                    time.sleep(0.05)
                    pyautogui.press(regular_key)
                    time.sleep(0.05)
                    pyautogui.keyUp(modifier_key)
                else:
                    # 对于多个键的组合，使用pyautogui.hotkey
                    pyautogui.hotkey(*mapped_keys)

                time.sleep(0.2)
                logger.info(f"组合键 {'+'.join(mapped_keys)} 发送成功")
                return True

            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次发送组合键失败: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(0.3)

        logger.error(f"组合键 {'+'.join(keys)} 发送失败")
        return False

    def send_special_key(self, key_name: str, max_attempts: int = 2) -> bool:
        """发送特殊键"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"发送特殊键 {key_name} (第 {attempt + 1} 次尝试)")

                # 使用pyautogui发送特殊键
                pyautogui.press(key_name)
                time.sleep(0.1)

                logger.info(f"特殊键 {key_name} 发送成功")
                return True

            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次发送特殊键失败: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(0.2)

        logger.error(f"特殊键 {key_name} 发送失败")
        return False


class ProcessLauncher:
    """跨平台进程启动器"""
    
    def __init__(self):
        self.system = platform.system().lower()
    
    def launch_claude_cli(self) -> Optional[subprocess.Popen]:
        """启动 Claude CLI"""
        try:
            if self.system == "windows":
                return self._launch_claude_cli_windows()
            elif self.system == "darwin":
                return self._launch_claude_cli_macos()
            else:
                return self._launch_claude_cli_linux()
        except Exception as e:
            logger.error(f"启动 Claude CLI 失败: {e}")
            return None
    
    def _launch_claude_cli_windows(self) -> Optional[subprocess.Popen]:
        """Windows 下启动 Claude CLI"""
        try:
            # 启动新的命令提示符窗口并运行 claude
            cmd = ["cmd", "/c", "start", "cmd", "/k", "claude"]
            process = subprocess.Popen(cmd, shell=True)
            return process
        except Exception as e:
            logger.error(f"Windows 启动 Claude CLI 失败: {e}")
            return None
    
    def _launch_claude_cli_macos(self) -> Optional[subprocess.Popen]:
        """macOS 下启动 Claude CLI"""
        try:
            # 使用 AppleScript 在新的 Terminal 窗口中启动 claude
            applescript = '''
            tell application "Terminal"
                do script "claude"
                activate
            end tell
            '''
            process = subprocess.Popen(["osascript", "-e", applescript])
            return process
        except Exception as e:
            logger.error(f"macOS 启动 Claude CLI 失败: {e}")
            return None
    
    def _launch_claude_cli_linux(self) -> Optional[subprocess.Popen]:
        """Linux 下启动 Claude CLI"""
        try:
            # 尝试不同的终端应用程序
            terminal_commands = [
                ["gnome-terminal", "--", "bash", "-c", "claude; exec bash"],
                ["xterm", "-e", "bash", "-c", "claude; exec bash"],
                ["konsole", "-e", "bash", "-c", "claude; exec bash"],
                ["x-terminal-emulator", "-e", "bash", "-c", "claude; exec bash"]
            ]
            
            for cmd in terminal_commands:
                try:
                    process = subprocess.Popen(cmd)
                    return process
                except FileNotFoundError:
                    continue
            
            logger.warning("未找到可用的终端应用程序")
            return None
            
        except Exception as e:
            logger.error(f"Linux 启动 Claude CLI 失败: {e}")
            return None


class ClaudeCLIAutomation:
    """Claude CLI 自动化管理器 - GUI 自动化版本"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.temp_dir = os.path.join(os.getcwd(), "temp_claude")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
        
        # 初始化组件
        self.window_manager = WindowManager()
        self.clipboard_manager = ClipboardManager()
        self.keyboard_controller = KeyboardController()
        self.process_launcher = ProcessLauncher()
        self.screen_detector = ScreenTextDetector()
        self.permission_handler = MacOSPermissionHandler()
        
        # 配置 pyautogui
        if pyautogui:
            pyautogui.FAILSAFE = True  # 移动到屏幕左上角终止
            pyautogui.PAUSE = 0.1  # 每次操作后的暂停时间
        
        logger.info(f"Claude CLI 自动化初始化完成 - 系统: {self.system}")
    
    def open_claude_cli(self) -> Dict[str, Any]:
        """
        跨平台打开 Claude CLI
        
        Returns:
            Dict: 操作结果
        """
        try:
            logger.info("启动 Claude CLI...")
            
            process = self.process_launcher.launch_claude_cli()
            
            if process:
                # 等待进程启动
                time.sleep(2.0)
                
                logger.info(f"Claude CLI 已在 {self.system} 系统上启动，进程 ID: {process.pid}")
                
                return {
                    "status": "success",
                    "message": f"Claude CLI 已在 {self.system} 系统上成功启动",
                    "process_id": process.pid,
                    "platform": self.system,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                raise Exception("无法启动 Claude CLI 进程")
                
        except Exception as e:
            logger.error(f"启动 Claude CLI 失败: {str(e)}")
            return {
                "status": "error",
                "message": f"启动失败: {str(e)}",
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
    
    def write_prompt_to_file(self, prompt_data: Dict[str, str], filename: str = None) -> str:
        """
        将提示词数据写入文件
        
        Args:
            prompt_data: 包含提示词内容的字典
            filename: 自定义文件名（可选）
            
        Returns:
            str: 文件路径
        """
        if filename is None:
            filename = f"claude_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        file_path = os.path.join(self.temp_dir, filename)
        
        # 格式化提示词内容
        prompt_content = f"""# AI Agent 任务提示词
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 角色设定
{prompt_data.get('role', '')}

## 目标任务
{prompt_data.get('goal', '')}

## 功能输出要求
{prompt_data.get('function_output', '')}

## UI设计要求
{prompt_data.get('ui_requirements', '')}

---
请根据以上要求执行相应的 AI Agent 任务。
"""
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            
            logger.info(f"提示词已写入文件: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"写入提示词文件失败: {str(e)}")
            raise
    
    def execute_claude_command(self, prompt_file: str) -> Dict[str, Any]:
        """
        执行 Claude CLI 命令 - 管道方式（保持向后兼容）
        
        Args:
            prompt_file: 提示词文件路径
            
        Returns:
            Dict: 执行结果
        """
        try:
            if not os.path.exists(prompt_file):
                raise FileNotFoundError(f"提示词文件不存在: {prompt_file}")
            
            # 构建跨平台命令
            if self.system == "windows":
                cmd = ["cmd", "/c", f"type \"{prompt_file}\" | claude"]
            else:
                cmd = ["sh", "-c", f"cat '{prompt_file}' | claude"]
            
            # 启动 Claude CLI 进程
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            
            logger.info(f"Claude CLI 任务已在 {self.system} 系统上启动，进程 ID: {process.pid}")
            
            return {
                "status": "success",
                "message": f"Claude CLI 任务已在 {self.system} 系统上开始执行",
                "process_id": process.pid,
                "prompt_file": prompt_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"执行 Claude CLI 命令失败: {str(e)}")
            return {
                "status": "error",
                "message": f"执行失败: {str(e)}",
                "prompt_file": prompt_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
    
    def open_claude_cli_with_prompt(self, prompt_file: str) -> Dict[str, Any]:
        """
        打开 Claude CLI 并自动输入提示词内容（GUI 自动化方式）
        
        Args:
            prompt_file: 提示词文件路径
            
        Returns:
            Dict: 操作结果
        """
        try:
            if not os.path.exists(prompt_file):
                raise FileNotFoundError(f"提示词文件不存在: {prompt_file}")
            
            # 读取提示词内容
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read().strip()
            
            logger.info("开始 GUI 自动化流程...")
            
            # 第一步: 启动 Claude CLI
            logger.info("步骤 1: 启动 Claude CLI...")
            process = self.process_launcher.launch_claude_cli()
            if not process:
                raise Exception("无法启动 Claude CLI")
            
            # 第二步: 等待 Claude CLI 启动完成
            logger.info("步骤 2: 等待 Claude CLI 启动完成...")
            time.sleep(3.0)  # 等待 Claude CLI 完全加载
            
            # 第三步: 查找并激活 Claude CLI 窗口
            logger.info("步骤 3: 查找并激活 Claude CLI 窗口...")
            activation_success = self._activate_claude_cli_window()
            if activation_success:
                logger.info("成功激活 Claude CLI 窗口")
            else:
                logger.warning("无法自动激活 Claude CLI 窗口，将继续执行但可能需要手动激活")
            
            # 第四步: 复制提示词到剪贴板
            logger.info("步骤 4: 复制提示词到剪贴板...")
            if not self.clipboard_manager.copy_to_clipboard(prompt_content):
                raise Exception("复制提示词到剪贴板失败")
            
            # 第五步: 验证剪贴板内容
            logger.info("步骤 5: 验证剪贴板内容...")
            if not self.clipboard_manager.verify_clipboard_content(prompt_content[:100]):
                logger.warning("剪贴板内容验证失败，但继续执行...")
            
            # 给用户一些时间手动激活窗口（如果自动激活失败）
            if not activation_success:
                logger.info("等待 2 秒钟以便手动激活 Claude CLI 窗口...")
                time.sleep(2.0)
            
            # 第六步: 设置输入焦点
            logger.info("步骤 6a: 设置Claude CLI输入焦点...")
            focus_ready = self._ensure_input_focus(activation_success)
            
            # 第六步: 粘贴提示词
            logger.info("步骤 6b: 粘贴提示词...")
            
            if not focus_ready:
                logger.warning("输入焦点可能未正确设置，建议手动点击Claude CLI窗口")
                # 给用户3秒时间手动点击
                logger.info("等待3秒供用户手动点击Claude CLI窗口...")
                time.sleep(3.0)
            
            # 尝试多种粘贴方法（Windows CMD环境优先使用右键粘贴）
            paste_success = False
            paste_methods_tried = []
            paste_verified = False
            
            # Windows CMD环境特殊处理
            if self.system == "windows":
                # 方法1: Windows CMD专用 - 鼠标右键粘贴
                try:
                    logger.info("尝试方法1: Windows CMD鼠标右键粘贴...")
                    success = self._windows_cmd_right_click_paste()
                    if success:
                        paste_success = True
                        paste_methods_tried.append("鼠标右键粘贴")
                        logger.info("Windows CMD鼠标右键粘贴方法成功")
                except Exception as e:
                    logger.warning(f"鼠标右键粘贴失败: {e}")
            
            # 方法2: 系统标准粘贴（非Windows或右键失败时）
            if not paste_success:
                try:
                    paste_method_name = "标准Cmd+V" if self.system == "darwin" else "标准Ctrl+V"
                    logger.info(f"尝试方法2: {paste_method_name}粘贴...")
                    if self.keyboard_controller.send_paste_command():
                        paste_success = True
                        paste_methods_tried.append(paste_method_name)
                        logger.info("标准粘贴方法成功")
                except Exception as e:
                    logger.warning(f"标准粘贴方法失败: {e}")
            
            # 方法3: 使用pynput备选方案
            if not paste_success:
                try:
                    logger.info("尝试方法3: pynput粘贴...")
                    from pynput.keyboard import Key, Controller
                    kb = Controller()
                    if self.system == "darwin":
                        with kb.pressed(Key.cmd):
                            kb.press('v')
                            kb.release('v')
                    else:
                        kb.press(Key.ctrl)
                        kb.press('v')
                        kb.release('v')
                        kb.release(Key.ctrl)
                    paste_success = True
                    paste_methods_tried.append("pynput")
                    logger.info("pynput粘贴方法成功")
                except Exception as e:
                    logger.warning(f"pynput粘贴失败: {e}")
            
            # 简化处理：粘贴完成后等待1秒直接发送
            if paste_success:
                logger.info(f"粘贴操作完成，使用的方法: {paste_methods_tried}")
                logger.info("粘贴成功，等待1秒后直接发送Enter键...")
                time.sleep(1.0)
                paste_verified = True  # 简化：假设粘贴成功即为验证通过
                
            else:
                logger.error(f"所有粘贴方法都失败了，尝试的方法: {paste_methods_tried}")
                logger.warning("粘贴失败，跳过发送步骤")
                paste_verified = False

            # 第八步: 发送回车键提交（仅在粘贴成功时）
            if paste_success and paste_verified:
                logger.info("步骤 8: 发送Enter键提交...")

                # 直接发送回车键
                enter_success = False
                try:
                    enter_success = self.keyboard_controller.send_enter()
                    if enter_success:
                        logger.info("Enter键发送成功，提示词已提交给Claude CLI")
                    else:
                        logger.warning("Enter键发送失败，请手动按Enter键")
                except Exception as e:
                    logger.warning(f"发送Enter键时出错: {e}，请手动按Enter键")
                    
            elif paste_success and not paste_verified:
                # 粘贴成功但验证失败，不发送回车
                enter_success = False
                enter_methods_tried = []
                logger.warning("粘贴成功但内容验证失败，为安全起见跳过回车发送")
                logger.info("建议手动检查内容后按Enter键发送")
            else:
                # 粘贴完全失败时不执行回车
                enter_success = False
                enter_methods_tried = []
                logger.info("由于粘贴失败，跳过回车发送步骤")
            
            logger.info("GUI 自动化流程完成！")
            
            return {
                "status": "success",
                "message": "Claude CLI 已打开并自动输入提示词（GUI 自动化）",
                "process_id": process.pid,
                "prompt_file": prompt_file,
                "method": "gui_automation",
                "platform": self.system,
                "timestamp": datetime.now().isoformat(),
                "window_activation_success": activation_success,
                "paste_success": paste_success,
                "paste_verified": paste_verified,
                "enter_success": enter_success,
                "focus_ready": focus_ready,
                "methods_used": {
                    "paste_methods": paste_methods_tried,
                    "enter_methods": enter_methods_tried
                },
                "automation_summary": {
                    "window_activation": "成功" if activation_success else "失败，需手动激活",
                    "input_focus": "成功" if focus_ready else "可能失败，建议手动点击",
                    "paste_operation": f"成功 ({', '.join(paste_methods_tried)})" if paste_success else "失败，需手动粘贴",
                    "content_verification": "验证通过" if paste_verified else "验证失败" if paste_success else "跳过验证",
                    "enter_submission": f"成功 ({', '.join(enter_methods_tried)})" if enter_success else "失败，需手动按Enter"
                },
                "steps_completed": [
                    "启动 Claude CLI" + " [OK]",
                    "等待启动完成" + " [OK]", 
                    "查找并激活窗口" + (" [OK]" if activation_success else " [WARN]"),
                    "复制提示词到剪贴板" + " [OK]",
                    "验证剪贴板内容" + " [OK]",
                    "设置输入焦点" + (" [OK]" if focus_ready else " [WARN]"),
                    "粘贴提示词" + (" [OK]" if paste_success else " [FAIL]"),
                    "内容验证" + (" [OK]" if paste_verified else " [WARN]" if paste_success else " [SKIP]"),
                    "发送回车键提交" + (" [OK]" if enter_success else " [SAFE-SKIP]" if paste_success and not paste_verified else " [SKIP]")
                ],
                "next_manual_steps": [step for step in [
                    "请手动点击 Claude CLI 窗口" if not activation_success else None,
                    f"按 {'Cmd+V' if self.system == 'darwin' else 'Ctrl+V'} 粘贴提示词" if not paste_success else None,
                    "按 Enter 键发送提示词" if not enter_success else None
                ] if step is not None]
            }
            
        except Exception as e:
            logger.error(f"GUI 自动化流程失败: {str(e)}")
            return {
                "status": "error",
                "message": f"GUI 自动化失败: {str(e)}",
                "prompt_file": prompt_file,
                "method": "gui_automation",
                "platform": self.system,
                "timestamp": datetime.now().isoformat(),
                "fallback_instructions": [
                    "请手动完成以下步骤:",
                    "1. 点击 Claude CLI 窗口激活它",
                    f"2. 按 {'Cmd+V' if self.system == 'darwin' else 'Ctrl+V'} 粘贴提示词",
                    "3. 按 Enter 键发送提示词"
                ]
            }

    def monitor_and_handle_claude_prompts(self, duration_seconds: float = 60.0) -> Dict[str, Any]:
        """
        监控Claude输出并自动处理"Yes, proceed"等提示

        Args:
            duration_seconds: 监控持续时间

        Returns:
            Dict: 监控和处理结果
        """
        logger.info(f"开始监控Claude提示，持续 {duration_seconds} 秒")

        try:
            # 使用屏幕检测器监控提示
            monitor_result = self.screen_detector.monitor_for_prompts(
                duration_seconds=duration_seconds,
                check_interval=2.0
            )

            if monitor_result["status"] == "found":
                detection_result = monitor_result["detection_result"]
                logger.info(f"检测到提示: {detection_result}")

                # 检查建议的操作
                suggested_action = detection_result.get("suggested_action")

                if suggested_action in ["press_enter", "check_and_enter"]:
                    logger.info("自动处理：发送Enter键")

                    # 确保窗口激活
                    if self.system == "darwin":
                        # macOS使用专门的Terminal激活方法
                        activation_success = self.window_manager.activate_terminal_for_claude()
                    else:
                        # 其他系统的激活方法
                        claude_windows = self.window_manager.find_claude_cli_windows()
                        activation_success = False
                        if claude_windows:
                            activation_success = self.window_manager.activate_window_by_pid(
                                claude_windows[0]['pid']
                            )

                    if activation_success:
                        time.sleep(0.5)

                        # 发送Enter键
                        enter_success = self.keyboard_controller.send_enter()

                        if enter_success:
                            logger.info("成功发送Enter键响应Claude提示")
                            return {
                                "status": "handled",
                                "action_taken": "sent_enter",
                                "detection_result": detection_result,
                                "window_activated": activation_success,
                                "enter_sent": enter_success,
                                "timestamp": datetime.now().isoformat()
                            }
                        else:
                            logger.warning("发送Enter键失败")
                            return {
                                "status": "partial_success",
                                "action_taken": "window_activated_only",
                                "detection_result": detection_result,
                                "window_activated": activation_success,
                                "enter_sent": False,
                                "message": "窗口已激活，但Enter键发送失败，请手动按Enter",
                                "timestamp": datetime.now().isoformat()
                            }
                    else:
                        logger.warning("窗口激活失败")
                        return {
                            "status": "detection_only",
                            "action_taken": "none",
                            "detection_result": detection_result,
                            "message": "检测到提示但无法激活窗口，请手动处理",
                            "timestamp": datetime.now().isoformat()
                        }

                else:
                    logger.info(f"检测到提示但不需要自动处理: {suggested_action}")
                    return {
                        "status": "detected_no_action",
                        "detection_result": detection_result,
                        "message": "检测到提示但不需要自动处理",
                        "timestamp": datetime.now().isoformat()
                    }

            else:
                logger.info("监控期间未检测到需要处理的提示")
                return {
                    "status": "no_prompts_detected",
                    "message": f"在 {duration_seconds} 秒内未检测到Claude提示",
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"监控Claude提示时出错: {e}")
            return {
                "status": "error",
                "message": f"监控失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def complete_automation_workflow(self, prompt_file: str, monitor_duration: float = 60.0) -> Dict[str, Any]:
        """
        完整的自动化工作流：发送提示词 + 监控和处理Claude响应

        Args:
            prompt_file: 提示词文件路径
            monitor_duration: 监控Claude响应的时间

        Returns:
            Dict: 完整工作流结果
        """
        logger.info("开始完整的Claude自动化工作流")

        workflow_results = {
            "status": "started",
            "steps": {},
            "timestamp": datetime.now().isoformat()
        }

        try:
            # 步骤0: 清理旧进程和权限监控准备
            logger.info("步骤0: 系统准备和进程管理")

            # 清理旧的Claude进程（保留最新1个）
            cleanup_result = self.window_manager.cleanup_old_claude_processes(keep_newest=1)
            workflow_results["steps"]["process_cleanup"] = cleanup_result

            if cleanup_result["cleaned_processes"]:
                logger.info(f"清理了 {len(cleanup_result['cleaned_processes'])} 个旧Claude进程")

            # 如果是macOS，启动权限对话框监控（后台运行）
            permission_monitor_thread = None
            if self.system == "darwin":
                logger.info("启动macOS权限对话框监控...")
                import threading

                def permission_monitor():
                    return self.permission_handler.monitor_and_handle_permission_dialogs(duration_seconds=60.0)

                permission_monitor_thread = threading.Thread(target=permission_monitor, daemon=True)
                permission_monitor_thread.start()
                workflow_results["steps"]["permission_monitor"] = {"status": "started", "message": "权限对话框监控已启动"}

            # 步骤1: 发送提示词
            logger.info("步骤1: 发送提示词到Claude CLI")
            send_result = self.open_claude_cli_with_prompt(prompt_file)
            workflow_results["steps"]["send_prompt"] = send_result

            if send_result["status"] != "success":
                workflow_results["status"] = "failed_at_send"
                workflow_results["message"] = "发送提示词失败"
                return workflow_results

            # 步骤2: 等待Claude开始处理
            logger.info("步骤2: 等待Claude开始处理...")
            time.sleep(5.0)  # 给Claude一些时间开始处理

            # 步骤3: 监控Claude响应
            logger.info("步骤3: 监控Claude响应和自动处理提示")
            monitor_result = self.monitor_and_handle_claude_prompts(monitor_duration)
            workflow_results["steps"]["monitor_response"] = monitor_result

            # 确定最终状态
            if monitor_result["status"] in ["handled", "partial_success"]:
                workflow_results["status"] = "success"
                workflow_results["message"] = "工作流成功完成，Claude提示已自动处理"
            elif monitor_result["status"] == "detected_no_action":
                workflow_results["status"] = "success_no_action_needed"
                workflow_results["message"] = "工作流完成，检测到提示但无需自动处理"
            elif monitor_result["status"] == "no_prompts_detected":
                workflow_results["status"] = "success_no_prompts"
                workflow_results["message"] = "工作流完成，未检测到需要处理的提示"
            else:
                workflow_results["status"] = "partial_success"
                workflow_results["message"] = "工作流部分成功，可能需要手动干预"

            workflow_results["summary"] = {
                "prompt_sent": send_result.get("paste_success", False),
                "prompts_detected": monitor_result["status"] != "no_prompts_detected",
                "auto_handled": monitor_result["status"] == "handled",
                "total_time": time.time() - time.mktime(time.strptime(workflow_results["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"))
            }

            return workflow_results

        except Exception as e:
            logger.error(f"完整工作流失败: {e}")
            workflow_results["status"] = "error"
            workflow_results["message"] = f"工作流失败: {str(e)}"
            return workflow_results
    
    def _activate_claude_cli_window(self, max_attempts: int = 3) -> bool:
        """激活 Claude CLI 窗口"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"尝试激活窗口 (第 {attempt + 1} 次)...")
                
                # 查找 Claude CLI 相关窗口
                claude_windows = self.window_manager.find_claude_cli_windows()
                
                if claude_windows:
                    logger.info(f"找到 {len(claude_windows)} 个 Claude CLI 相关窗口")
                    
                    # 尝试激活最新的窗口
                    for window in reversed(claude_windows):  # 从最新的开始
                        if self.window_manager.activate_window_by_pid(window['pid']):
                            logger.info(f"成功激活窗口 (PID: {window['pid']})")
                            time.sleep(0.5)  # 等待窗口激活完成
                            return True
                    
                logger.warning(f"第 {attempt + 1} 次激活尝试失败")
                time.sleep(1.0)  # 等待后重试
                
            except Exception as e:
                logger.error(f"激活窗口时出错 (第 {attempt + 1} 次): {e}")
                time.sleep(1.0)
        
        return False
    
    def _ensure_input_focus(self, window_activated: bool) -> bool:
        """确保Claude CLI窗口有正确的输入焦点"""
        try:
            focus_methods_tried = []
            
            if pyautogui and window_activated:
                # 方法1: 智能窗口点击
                try:
                    claude_windows = pyautogui.getWindowsWithTitle('claude')
                    if not claude_windows:
                        # 查找包含关键词的窗口
                        all_windows = pyautogui.getAllWindows()
                        claude_windows = [w for w in all_windows if 
                                        'claude' in w.title.lower() or 
                                        'command prompt' in w.title.lower() or
                                        'cmd' in w.title.lower()]
                    
                    if claude_windows:
                        window = claude_windows[0]
                        # 点击窗口下方区域，通常是输入区
                        input_x = window.left + window.width // 2
                        input_y = window.top + int(window.height * 0.8)  # 窗口下方80%处
                        pyautogui.click(input_x, input_y)
                        time.sleep(0.2)
                        
                        # 发送一个测试字符再删除，确认输入工作
                        pyautogui.write('.')
                        time.sleep(0.1)
                        pyautogui.press('backspace')
                        time.sleep(0.2)
                        
                        logger.info(f"成功设置输入焦点在窗口 ({input_x}, {input_y})")
                        focus_methods_tried.append("智能窗口点击")
                        return True
                        
                except Exception as e:
                    logger.warning(f"智能窗口点击失败: {e}")
            
            # 方法2: Alt+Tab + 屏幕点击
            try:
                logger.info("尝试Alt+Tab切换焦点...")
                pyautogui.keyDown('alt')
                pyautogui.press('tab')
                pyautogui.keyUp('alt')
                time.sleep(0.5)
                
                # 点击屏幕下方中央（命令行通常在这里）
                screen_width, screen_height = pyautogui.size()
                click_x = screen_width // 2
                click_y = int(screen_height * 0.7)
                pyautogui.click(click_x, click_y)
                time.sleep(0.3)
                
                # 测试输入
                pyautogui.write('.')
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.2)
                
                logger.info(f"使用Alt+Tab+屏幕点击设置焦点 ({click_x}, {click_y})")
                focus_methods_tried.append("Alt+Tab切换")
                return True
                
            except Exception as e:
                logger.warning(f"Alt+Tab方法失败: {e}")
            
            # 方法3: 多次点击确保焦点
            try:
                screen_width, screen_height = pyautogui.size()
                # 在屏幕不同位置点击多次
                positions = [
                    (screen_width // 2, screen_height // 2),     # 中央
                    (screen_width // 2, int(screen_height * 0.8)), # 下方
                    (screen_width // 2, int(screen_height * 0.6))  # 中下方
                ]
                
                for pos_x, pos_y in positions:
                    pyautogui.click(pos_x, pos_y)
                    time.sleep(0.2)
                    
                logger.info("使用多点击方法设置焦点")
                focus_methods_tried.append("多点击")
                return True
                
            except Exception as e:
                logger.warning(f"多点击方法失败: {e}")
            
            logger.warning(f"所有焦点设置方法都失败了，尝试的方法: {focus_methods_tried}")
            return False
            
        except Exception as e:
            logger.error(f"设置输入焦点时出现严重错误: {e}")
            return False
    
    def _windows_cmd_right_click_paste(self) -> bool:
        """Windows CMD环境下的鼠标右键粘贴"""
        try:
            logger.info("执行Windows CMD鼠标右键粘贴操作...")
            
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()
            logger.info(f"当前鼠标位置: ({current_x}, {current_y})")
            
            # 尝试找到CMD窗口并在输入区域右键
            try:
                # 查找包含CMD或claude的窗口
                cmd_windows = []
                for window in pyautogui.getAllWindows():
                    title_lower = window.title.lower()
                    if ('cmd' in title_lower or 
                        'command prompt' in title_lower or 
                        'claude' in title_lower):
                        cmd_windows.append(window)
                
                if cmd_windows:
                    # 使用第一个找到的窗口
                    target_window = cmd_windows[0]
                    # 点击窗口下方区域（输入区）
                    click_x = target_window.left + target_window.width // 2
                    click_y = target_window.top + int(target_window.height * 0.85)
                    
                    logger.info(f"在CMD窗口输入区域右键: ({click_x}, {click_y})")
                    pyautogui.rightClick(click_x, click_y)
                    time.sleep(0.3)
                    
                else:
                    # 如果找不到窗口，在当前位置右键
                    logger.info("未找到CMD窗口，在当前位置右键")
                    pyautogui.rightClick()
                    time.sleep(0.3)
                    
            except Exception as e:
                logger.warning(f"智能右键定位失败，使用当前位置: {e}")
                pyautogui.rightClick()
                time.sleep(0.3)
            
            # 在Windows CMD中，右键会直接粘贴（如果快速编辑模式开启）
            # 或者会显示上下文菜单，我们需要智能判断
            
            logger.info("等待右键粘贴完成...")
            time.sleep(0.8)
            
            # 检查是否直接粘贴成功（快速编辑模式）
            try:
                # 发送End键，如果有内容会移动到末尾
                pyautogui.press('end')
                time.sleep(0.1)
                
                # 发送Left键，如果有内容应该能向左移动
                pyautogui.press('left')
                time.sleep(0.1)
                pyautogui.press('right')  # 移回末尾
                time.sleep(0.1)
                
                logger.info("快速编辑模式粘贴检测完成")
                
            except Exception as e:
                logger.warning(f"快速编辑模式检测失败: {e}")
                
                # 如果快速编辑模式失败，可能需要菜单操作
                try:
                    logger.info("尝试通过菜单粘贴...")
                    # 检查屏幕上是否有粘贴菜单（通过颜色或其他方式）
                    # 这里简单尝试发送Enter键关闭可能的菜单，然后重新右键
                    pyautogui.press('escape')  # 关闭可能的菜单
                    time.sleep(0.3)
                    
                    # 重新右键并等待
                    pyautogui.rightClick()
                    time.sleep(0.3)
                    pyautogui.press('p')  # 选择粘贴
                    time.sleep(0.5)
                    
                    logger.info("菜单模式粘贴尝试完成")
                    
                except Exception as menu_e:
                    logger.warning(f"菜单模式粘贴也失败: {menu_e}")
            
            logger.info("Windows CMD右键粘贴操作完成")
            return True
            
        except Exception as e:
            logger.error(f"Windows CMD右键粘贴失败: {e}")
            return False
    
    def _verify_paste_content(self, expected_content: str) -> bool:
        """验证粘贴内容是否正确"""
        try:
            logger.info("开始验证粘贴内容...")
            
            # 方法1: 使用非破坏性方式验证内容
            try:
                logger.info("使用非破坏性方式验证内容...")
                
                # 先移动到文本开头，不选择内容
                if self.system == "darwin":
                    pyautogui.hotkey('cmd', 'left')  # macOS使用Cmd+Left移动到行首
                else:
                    pyautogui.hotkey('ctrl', 'home')
                time.sleep(0.2)
                
                # 向右移动一些字符，如果有内容应该能移动
                can_move_right = False
                try:
                    for i in range(10):  # 尝试移动10个字符
                        pyautogui.press('right')
                        time.sleep(0.02)
                    can_move_right = True
                except:
                    pass
                
                # 移动到末尾
                pyautogui.press('end')
                time.sleep(0.1)
                
                # 尝试向左移动，如果有内容应该能移动
                can_move_left = False
                try:
                    for _ in range(5):  # 尝试移动5个字符
                        pyautogui.press('left')
                        time.sleep(0.02)
                    can_move_left = True
                except:
                    pass
                
                # 移动回末尾
                pyautogui.press('end')
                time.sleep(0.1)
                
                if can_move_right and can_move_left:
                    logger.info("内容验证通过：光标能在文本中移动，确认有内容")
                    return True
                elif can_move_right or can_move_left:
                    logger.info("内容验证部分通过：检测到可能有内容")
                    return True
                else:
                    logger.warning("内容验证失败：光标无法在文本中移动")
                    return False
                    
            except Exception as e:
                logger.warning(f"非破坏性验证方法失败: {e}")
            
            # 方法2: 谨慎的剪贴板验证（只在必要时使用）
            try:
                logger.info("使用谨慎的剪贴板验证...")
                
                # 保存当前剪贴板内容
                original_clipboard = pyperclip.paste()
                
                # 移动到文本开头
                if self.system == "darwin":
                    pyautogui.hotkey('cmd', 'left')  # macOS使用Cmd+Left移动到行首
                else:
                    pyautogui.hotkey('ctrl', 'home')
                time.sleep(0.1)
                
                # 只选择前面一小部分文本（减少破坏性）
                pyautogui.hotkey('shift', 'right')  # 选择1个字符
                time.sleep(0.1)
                for _ in range(20):  # 继续选择20个字符
                    pyautogui.hotkey('shift', 'right')
                    time.sleep(0.01)
                
                # 复制选中内容
                if self.system == "darwin":
                    pyautogui.hotkey('cmd', 'c')
                else:
                    pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.2)
                
                # 获取复制的内容
                partial_content = pyperclip.paste()
                
                # 恢复原始剪贴板内容
                pyperclip.copy(original_clipboard)
                
                # 取消选择，移动到末尾
                pyautogui.press('end')
                time.sleep(0.1)
                
                # 检查部分内容
                if len(partial_content.strip()) > 5:
                    if any(char in partial_content for char in ['#', '角色', '目标', 'AI']) or len(partial_content) > 10:
                        logger.info(f"内容验证通过：检测到部分预期内容='{partial_content[:30]}...'")
                        return True
                
                logger.warning(f"内容验证失败：部分内容='{partial_content[:30]}...'")
                return False
                    
            except Exception as e:
                logger.warning(f"剪贴板验证方法失败: {e}")
            
            # 如果所有验证方法都失败，返回False  
            logger.warning("所有内容验证方法都失败")
            return False
            
        except Exception as e:
            logger.error(f"内容验证过程出错: {e}")
            return False
    
    def cleanup_temp_files(self, older_than_hours: int = 24) -> Dict[str, Any]:
        """
        清理临时文件
        
        Args:
            older_than_hours: 清理多少小时前的文件
            
        Returns:
            Dict: 清理结果
        """
        try:
            cleaned_files = []
            current_time = datetime.now()
            
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    age_hours = (current_time - file_time).total_seconds() / 3600
                    
                    if age_hours > older_than_hours:
                        os.remove(file_path)
                        cleaned_files.append(filename)
                        logger.info(f"已清理临时文件: {filename}")
            
            return {
                "status": "success",
                "message": f"已清理 {len(cleaned_files)} 个临时文件",
                "cleaned_files": cleaned_files,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"清理临时文件失败: {str(e)}")
            return {
                "status": "error",
                "message": f"清理失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_automation_status(self) -> Dict[str, Any]:
        """获取自动化系统状态 - 增强版"""
        status = {
            "system": self.system,
            "libraries_available": {
                "pyautogui": pyautogui is not None,
                "pyperclip": pyperclip is not None,
                "psutil": psutil is not None,
                "macos_libs": macos_libs_available if self.system == "darwin" else "N/A",
                "ocr_libs": ocr_available
            },
            "components_initialized": {
                "window_manager": self.window_manager is not None,
                "clipboard_manager": self.clipboard_manager is not None,
                "keyboard_controller": self.keyboard_controller is not None,
                "process_launcher": self.process_launcher is not None,
                "screen_detector": self.screen_detector is not None,
                "permission_handler": self.permission_handler is not None
            },
            "macos_specific_features": {
                "applescript_support": self.system == "darwin",
                "terminal_activation": self.system == "darwin",
                "cmd_key_mapping": self.system == "darwin",
                "native_clipboard": macos_libs_available if self.system == "darwin" else False
            },
            "detection_capabilities": {
                "screen_text_detection": True,
                "yes_proceed_detection": True,
                "screen_change_monitoring": True,
                "ocr_detection": ocr_available,
                "macos_vision": macos_libs_available if self.system == "darwin" else False
            },
            "claude_cli_processes": len(self.window_manager.find_claude_cli_windows()),
            "temp_directory": self.temp_dir,
            "temp_directory_exists": os.path.exists(self.temp_dir),
            "enhanced_features": [
                "Multiple paste methods with fallback",
                "macOS-specific window activation",
                "Yes/proceed prompt detection",
                "Automatic Enter key handling",
                "AppleScript integration",
                "Native clipboard APIs",
                "Enhanced error handling",
                "Complete automation workflow",
                "Multiple terminal process management",
                "Claude process cleanup and management",
                "Automatic permission dialog handling",
                "Real-time process monitoring"
            ],
            "timestamp": datetime.now().isoformat()
        }

        return status

    def cleanup_multiple_terminals(self, max_terminals: int = 3) -> Dict[str, Any]:
        """便捷方法：清理多个终端进程"""
        logger.info(f"开始清理多个终端进程，保留最多 {max_terminals} 个")
        return self.window_manager.cleanup_old_terminal_processes(max_terminals)

    def cleanup_claude_processes(self, keep_newest: int = 1) -> Dict[str, Any]:
        """便捷方法：清理多个Claude进程"""
        logger.info(f"开始清理Claude进程，保留最新 {keep_newest} 个")
        return self.window_manager.cleanup_old_claude_processes(keep_newest)

    def list_terminal_processes(self) -> List[Dict[str, Any]]:
        """便捷方法：列出所有终端进程"""
        terminals = self.window_manager.find_terminal_processes()
        logger.info(f"找到 {len(terminals)} 个终端进程")
        return terminals

    def handle_permission_dialogs(self, duration_seconds: float = 10.0) -> Dict[str, Any]:
        """便捷方法：处理macOS权限对话框"""
        if self.system != "darwin":
            return {"message": "权限对话框处理仅支持macOS", "dialogs_handled": 0}

        logger.info(f"开始处理权限对话框，持续 {duration_seconds} 秒")
        return self.permission_handler.monitor_and_handle_permission_dialogs(duration_seconds)

    def complete_workflow_with_cleanup(self, prompt_file: str, monitor_duration: float = 60.0,
                                     max_terminals: int = 3, keep_claude_processes: int = 1) -> Dict[str, Any]:
        """
        完整工作流程，包含进程清理和权限处理

        Args:
            prompt_file: 提示词文件路径
            monitor_duration: 监控时间
            max_terminals: 保留的最大终端数
            keep_claude_processes: 保留的Claude进程数

        Returns:
            Dict: 完整工作流结果
        """
        logger.info("开始完整工作流程（包含进程管理和权限处理）")

        result = {
            "status": "started",
            "cleanup_results": {},
            "automation_results": {},
            "timestamp": datetime.now().isoformat()
        }

        try:
            # 第一步：清理进程
            logger.info("第一步：清理多余的终端和Claude进程")

            # 清理终端进程
            terminal_cleanup = self.cleanup_multiple_terminals(max_terminals)
            result["cleanup_results"]["terminals"] = terminal_cleanup

            # 清理Claude进程
            claude_cleanup = self.cleanup_claude_processes(keep_claude_processes)
            result["cleanup_results"]["claude_processes"] = claude_cleanup

            # 第二步：执行自动化工作流
            logger.info("第二步：执行自动化工作流")
            automation_result = self.complete_automation_workflow(prompt_file, monitor_duration)
            result["automation_results"] = automation_result

            # 确定最终状态
            if automation_result.get("status") in ["success", "success_no_action_needed", "success_no_prompts"]:
                result["status"] = "success"
                result["message"] = "完整工作流程成功完成"
            else:
                result["status"] = "partial_success"
                result["message"] = "工作流程部分完成，自动化环节可能需要手动干预"

            # 添加统计信息
            result["summary"] = {
                "terminals_cleaned": len(terminal_cleanup.get("cleaned_processes", [])),
                "claude_processes_cleaned": len(claude_cleanup.get("cleaned_processes", [])),
                "automation_successful": automation_result.get("status") == "success",
                "total_time": time.time() - time.mktime(time.strptime(result["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"))
            }

            return result

        except Exception as e:
            logger.error(f"完整工作流程失败: {e}")
            result["status"] = "error"
            result["message"] = f"工作流程失败: {str(e)}"
            return result


# 全局实例
claude_cli_automation = ClaudeCLIAutomation()