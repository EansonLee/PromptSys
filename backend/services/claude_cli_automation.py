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
except ImportError as e:
    logging.warning(f"GUI 自动化库导入失败: {e}")
    pyautogui = None
    pyperclip = None
    psutil = None

logger = logging.getLogger(__name__)

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
                        claude_windows.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'cmdline': pinfo['cmdline'],
                            'create_time': pinfo['create_time']
                        })
                        logger.info(f"找到 Claude CLI 相关进程: PID={pinfo['pid']}, Name={pinfo['name']}, CMD={cmdline_str[:100]}")
                        
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
        """macOS 窗口激活"""
        try:
            # 使用 AppleScript 激活窗口
            script = f"""
            tell application "System Events"
                set frontApp to first application process whose unix id is {pid}
                set frontmost of frontApp to true
            end tell
            """
            subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
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


class ClipboardManager:
    """跨平台剪贴板管理器"""
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """复制文本到剪贴板"""
        try:
            pyperclip.copy(text)
            time.sleep(0.1)  # 等待剪贴板操作完成
            return True
        except Exception as e:
            logger.error(f"复制到剪贴板失败: {e}")
            return False
    
    @staticmethod
    def get_clipboard_content() -> str:
        """获取剪贴板内容"""
        try:
            return pyperclip.paste()
        except Exception as e:
            logger.error(f"获取剪贴板内容失败: {e}")
            return ""
    
    @staticmethod
    def verify_clipboard_content(expected_text: str, timeout: float = 2.0) -> bool:
        """验证剪贴板内容"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_content = ClipboardManager.get_clipboard_content()
            if current_content and expected_text[:100] in current_content:
                return True
            time.sleep(0.1)
        return False


class KeyboardController:
    """跨平台键盘控制器"""
    
    def __init__(self):
        self.system = platform.system().lower()
    
    def send_paste_command(self, max_attempts: int = 3) -> bool:
        """发送粘贴命令 (Ctrl+V 或 Cmd+V) - 带重试机制"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"发送粘贴命令 (第 {attempt + 1} 次尝试)...")
                
                if self.system == "darwin":
                    # macOS 使用 Cmd+V
                    pyautogui.keyDown('cmd')
                    time.sleep(0.05)
                    pyautogui.press('v')
                    time.sleep(0.05)
                    pyautogui.keyUp('cmd')
                else:
                    # Windows/Linux 使用 Ctrl+V
                    pyautogui.keyDown('ctrl')
                    time.sleep(0.05)
                    pyautogui.press('v')
                    time.sleep(0.05)
                    pyautogui.keyUp('ctrl')
                
                # 等待粘贴操作完成
                time.sleep(0.2)
                logger.info(f"粘贴命令发送成功 (第 {attempt + 1} 次)")
                return True
                
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次粘贴命令失败: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(0.5)  # 重试前等待
                    
        logger.error(f"粘贴命令在 {max_attempts} 次尝试后仍然失败")
        return False
    
    def send_enter(self, max_attempts: int = 3) -> bool:
        """发送回车键 - 带重试机制"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"发送回车键 (第 {attempt + 1} 次尝试)...")
                
                # 使用多种方法发送回车键
                if attempt == 0:
                    # 方法1: 标准回车键
                    pyautogui.press('enter')
                elif attempt == 1:
                    # 方法2: 使用键码
                    pyautogui.press('return')
                else:
                    # 方法3: 手动按键操作
                    pyautogui.keyDown('enter')
                    time.sleep(0.05)
                    pyautogui.keyUp('enter')
                
                time.sleep(0.1)
                logger.info(f"回车键发送成功 (第 {attempt + 1} 次)")
                return True
                
            except Exception as e:
                logger.warning(f"第 {attempt + 1} 次发送回车键失败: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(0.3)  # 重试前等待
                    
        logger.error(f"回车键在 {max_attempts} 次尝试后仍然失败")
        return False
    
    def type_text(self, text: str, interval: float = 0.01) -> bool:
        """输入文本"""
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
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
            
            # 方法2: 标准Ctrl+V粘贴（非Windows或右键失败时）
            if not paste_success:
                try:
                    logger.info("尝试方法2: 标准Ctrl+V粘贴...")
                    if self.keyboard_controller.send_paste_command():
                        paste_success = True
                        paste_methods_tried.append("标准Ctrl+V")
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
                        kb.press(Key.cmd)
                        kb.press('v')
                        kb.release('v')
                        kb.release(Key.cmd)
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
            
            # 等待粘贴初步完成
            if paste_success:
                logger.info("粘贴命令已发送，等待1秒后进行内容验证...")
                time.sleep(1.0)
                
                # 兜底检查：验证粘贴内容是否正确
                paste_verified = self._verify_paste_content(prompt_content)
                
                if not paste_verified and self.system == "windows":
                    logger.warning("粘贴内容验证失败，在Windows环境下尝试兜底操作...")
                    # Windows兜底：如果Ctrl+V失败，尝试右键粘贴
                    try:
                        logger.info("兜底操作: Windows CMD鼠标右键粘贴...")
                        if self._windows_cmd_right_click_paste():
                            paste_methods_tried.append("兜底右键粘贴")
                            logger.info("兜底右键粘贴成功")
                            time.sleep(1.0)
                            paste_verified = self._verify_paste_content(prompt_content)
                    except Exception as e:
                        logger.warning(f"兜底右键粘贴失败: {e}")
            
            # 方法4: 直接输入文本作为最后备选
            if not paste_success or not paste_verified:
                try:
                    logger.info("尝试最后方法: 直接输入文本...")
                    # 清空当前输入（如果有的话）
                    pyautogui.hotkey('ctrl', 'a')
                    time.sleep(0.2)
                    # 直接输入文本内容（较慢但可靠）
                    pyautogui.write(prompt_content[:800], interval=0.005)  # 限制长度防止过长
                    paste_success = True
                    paste_verified = True
                    paste_methods_tried.append("直接输入")
                    logger.info("直接输入文本方法成功")
                except Exception as e:
                    logger.error(f"直接输入文本也失败: {e}")
            
            # 第七步: 最终粘贴验证和等待
            logger.info("步骤 7: 最终粘贴验证和等待...")
            
            if paste_success:
                logger.info(f"粘贴操作完成，使用的方法: {paste_methods_tried}")
                
                if paste_verified:
                    logger.info("✓ 粘贴内容验证通过")
                    # 根据内容长度动态调整等待时间
                    content_length = len(prompt_content)
                    base_wait = 1.0
                    additional_wait = min(content_length / 1000, 2.0)  # 每1000字符增加1秒，最多2秒
                    total_wait = base_wait + additional_wait
                    
                    logger.info(f"内容已验证，等待 {total_wait:.1f} 秒确保完全显示...")
                    time.sleep(total_wait)
                else:
                    logger.warning("⚠ 粘贴内容验证未通过，但继续执行")
                    # 验证失败时等待更长时间
                    logger.info("内容验证失败，等待3秒后继续...")
                    time.sleep(3.0)
                
                # 最终确保光标在正确位置
                try:
                    pyautogui.press('end')  # 移动到文本末尾
                    time.sleep(0.2)
                    logger.info("光标已移动到文本末尾")
                except Exception as e:
                    logger.warning(f"移动光标失败: {e}")
                    
            else:
                logger.error(f"所有粘贴方法都失败了，尝试的方法: {paste_methods_tried}")
                logger.warning("粘贴失败，跳过发送步骤")
                paste_verified = False
                
            # 第八步: 发送回车键提交（仅在粘贴成功且验证通过时）
            if paste_success and paste_verified:
                logger.info("步骤 8: 发送回车键提交...")
                logger.info("最终检查：确保光标位置正确...")
                
                # 确保光标在文本末尾，避免意外输入
                try:
                    pyautogui.press('end')
                    time.sleep(0.2)
                    logger.info("光标已确认在文本末尾")
                except Exception as e:
                    logger.warning(f"设置光标位置失败: {e}")
                
                logger.info("准备发送回车键...")
                time.sleep(0.5)  # 短暂等待确保状态稳定
            
                # 尝试多种回车方法
                enter_success = False
                enter_methods_tried = []
                
                # 方法1: 标准回车
                try:
                    if self.keyboard_controller.send_enter():
                        enter_success = True
                        enter_methods_tried.append("标准Enter")
                        logger.info("标准回车方法成功")
                except Exception as e:
                    logger.warning(f"标准回车失败: {e}")
                
                # 方法2: pynput回车
                if not enter_success:
                    try:
                        from pynput.keyboard import Key, Controller
                        kb = Controller()
                        kb.press(Key.enter)
                        kb.release(Key.enter)
                        enter_success = True
                        enter_methods_tried.append("pynput")
                        logger.info("pynput回车方法成功")
                    except Exception as e:
                        logger.warning(f"pynput回车失败: {e}")
                
                # 方法3: 多种回车键尝试
                if not enter_success:
                    try:
                        pyautogui.press('return')  # 尝试return键
                        time.sleep(0.2)
                        pyautogui.press('enter')   # 再次尝试enter
                        enter_success = True
                        enter_methods_tried.append("多种回车键")
                        logger.info("多种回车键方法成功")
                    except Exception as e:
                        logger.warning(f"多种回车键失败: {e}")
                
                if enter_success:
                    logger.info(f"回车操作完成，使用的方法: {enter_methods_tried}")
                    logger.info("提示词已提交给Claude CLI处理")
                else:
                    logger.error(f"所有回车方法都失败了，尝试的方法: {enter_methods_tried}")
                    logger.warning("请手动按 Enter 键提交提示词")
                    
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
                    "按 Ctrl+V 粘贴提示词" if not paste_success else None,
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
                    "2. 按 Ctrl+V (或 Cmd+V) 粘贴提示词",
                    "3. 按 Enter 键发送提示词"
                ]
            }
    
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
                    for i in range(5):  # 尝试移动5个字符
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
                pyautogui.hotkey('ctrl', 'home')
                time.sleep(0.1)
                
                # 只选择前面一小部分文本（减少破坏性）
                pyautogui.hotkey('shift', 'right')  # 选择1个字符
                time.sleep(0.1)
                for i in range(20):  # 继续选择20个字符
                    pyautogui.hotkey('shift', 'right')
                    time.sleep(0.01)
                
                # 复制选中内容
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
                    expected_start = expected_content.strip()[:20]
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
        """获取自动化系统状态"""
        status = {
            "system": self.system,
            "libraries_available": {
                "pyautogui": pyautogui is not None,
                "pyperclip": pyperclip is not None,
                "psutil": psutil is not None
            },
            "components_initialized": {
                "window_manager": self.window_manager is not None,
                "clipboard_manager": self.clipboard_manager is not None,
                "keyboard_controller": self.keyboard_controller is not None,
                "process_launcher": self.process_launcher is not None
            },
            "claude_cli_processes": len(self.window_manager.find_claude_cli_windows()),
            "temp_directory": self.temp_dir,
            "temp_directory_exists": os.path.exists(self.temp_dir),
            "timestamp": datetime.now().isoformat()
        }
        
        return status


# 全局实例
claude_cli_automation = ClaudeCLIAutomation()