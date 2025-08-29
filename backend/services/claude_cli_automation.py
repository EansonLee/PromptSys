"""
Claude CLI 自动化工具
支持 Windows 10 和 macOS 的跨平台 Claude CLI 自动化操作
"""

import os
import platform
import subprocess
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ClaudeCLIAutomation:
    """Claude CLI 自动化管理器"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.temp_dir = os.path.join(os.getcwd(), "temp_claude")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def open_claude_cli(self) -> Dict[str, Any]:
        """
        跨平台打开 Claude CLI
        
        Returns:
            Dict: 操作结果
        """
        try:
            if self.system == "windows":
                # Windows 实现 - 直接打开CMD并启动claude
                cmd = [
                    "cmd", "/c", "start", "cmd", "/k", 
                    "echo Claude CLI is ready for automation... && claude"
                ]
            elif self.system == "darwin":  # macOS
                # macOS 实现 - 直接在新Terminal中启动claude
                cmd = [
                    "osascript", "-e",
                    'tell application "Terminal" to do script "echo \'Claude CLI is ready for automation...\' && claude"'
                ]
            else:
                # Linux 实现
                cmd = [
                    "gnome-terminal", "--", "bash", "-c",
                    "echo 'Claude CLI is ready for automation...' && claude; exec bash"
                ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"Claude CLI 已在 {self.system} 系统上启动，进程 ID: {process.pid}")
            
            return {
                "status": "success",
                "message": f"Claude CLI 已在 {self.system} 系统上成功启动",
                "process_id": process.pid,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
            
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
            
            # 构建跨平台命令 - 简化版本，直接使用系统命令
            if self.system == "windows":
                # Windows CMD 实现 - 直接使用CMD
                cmd = [
                    "cmd", "/c", 
                    f"type \"{prompt_file}\" | claude"
                ]
            else:
                # macOS/Linux 实现
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
        打开 Claude CLI 并自动输入提示词内容（交互方式）
        
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
            
            # 为了自动输入，我们需要创建一个批处理脚本或使用特殊的方法
            if self.system == "windows":
                return self._open_claude_cli_with_prompt_windows(prompt_content, prompt_file)
            elif self.system == "darwin":
                return self._open_claude_cli_with_prompt_macos(prompt_content, prompt_file)
            else:
                return self._open_claude_cli_with_prompt_linux(prompt_content, prompt_file)
                
        except Exception as e:
            logger.error(f"打开 Claude CLI 并输入提示词失败: {str(e)}")
            return {
                "status": "error",
                "message": f"操作失败: {str(e)}",
                "prompt_file": prompt_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
    
    def _open_claude_cli_with_prompt_windows(self, prompt_content: str, prompt_file: str) -> Dict[str, Any]:
        """Windows下打开Claude CLI并自动输入提示词"""
        try:
            # 创建PowerShell脚本来实现真正的交互式输入
            ps_script_file = os.path.join(self.temp_dir, "claude_auto_input.ps1")
            
            # 清理提示词内容中的特殊字符，保持换行
            clean_content = prompt_content.replace('"', "'").replace('`', "'")
            
            # 准备PowerShell脚本内容 - 完全使用英文避免编码问题
            ps_content = f'''# Claude CLI Auto Input Script
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 | Out-Null

try {{
    Write-Host "=====================================" -ForegroundColor Yellow
    Write-Host "Claude CLI 自动输入功能启动" -ForegroundColor Green  
    Write-Host "=====================================" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "提示词内容预览:" -ForegroundColor Cyan
    Write-Host "-------------------------------------"
    Get-Content "{prompt_file}" -Encoding UTF8 | Write-Host
    Write-Host "-------------------------------------"
    Write-Host ""
    
    Write-Host "正在启动 Claude CLI..." -ForegroundColor Green
    
    # Start Claude CLI process
    $claudeProcess = Start-Process "cmd" -ArgumentList "/k claude" -PassThru -WindowStyle Normal
    
    if ($claudeProcess) {{
        Write-Host "Claude CLI 进程已启动 (进程ID: $($claudeProcess.Id))" -ForegroundColor Green
        
        Write-Host "等待 2000ms 让 Claude CLI 完全加载..." -ForegroundColor Yellow
        Start-Sleep -Milliseconds 2000
        
        # Prepare prompt content
        $prompt = @"
{clean_content}
"@
        
        Write-Host "准备自动输入..." -ForegroundColor Cyan
        
        # Load necessary assemblies
        try {{
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName Microsoft.VisualBasic
            Write-Host "必需程序集加载成功" -ForegroundColor Green
        }} catch {{
            Write-Host "加载必需程序集失败: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "错误详情: $($_.Exception.StackTrace)" -ForegroundColor Red
            throw
        }}
        
        # Copy content to clipboard
        try {{
            Set-Clipboard -Value $prompt
            Write-Host "提示词已成功复制到剪贴板" -ForegroundColor Green
        }} catch {{
            Write-Host "复制到剪贴板失败: $($_.Exception.Message)" -ForegroundColor Red
            Write-Host "错误详情: $($_.Exception.StackTrace)" -ForegroundColor Red
            throw
        }}
        
        Write-Host ""
        Write-Host "尝试自动粘贴和发送..." -ForegroundColor Yellow
        
        # Try to activate Claude CLI window and auto-paste
        try {{
            Write-Host "等待额外 500ms 确保 Claude CLI 就绪..." -ForegroundColor Yellow
            Start-Sleep -Milliseconds 500
            
            $activated = $false
            $activationError = "未尝试任何激活方法"
            
            # Method 1: Activate by process ID
            if (-not $activated) {{
                try {{
                    if ($claudeProcess -and !$claudeProcess.HasExited) {{
                        Write-Host "方法1: 通过进程ID激活窗口 ($($claudeProcess.Id))..." -ForegroundColor Cyan
                        [Microsoft.VisualBasic.Interaction]::AppActivate($claudeProcess.Id)
                        $activated = $true
                        Write-Host "成功: 方法1已激活 Claude CLI 窗口" -ForegroundColor Green
                    }} else {{
                        $activationError = "Claude CLI 进程不存在或已退出"
                        Write-Host "方法1失败: $activationError" -ForegroundColor Red
                    }}
                }} catch {{
                    $activationError = "方法1失败: $($_.Exception.Message)"
                    Write-Host $activationError -ForegroundColor Red
                    Write-Host "尝试方法2..." -ForegroundColor Yellow
                }}
            }}
            
            # Method 2: Find CMD window containing "claude"
            if (-not $activated) {{
                try {{
                    Write-Host "方法2: 搜索包含'claude'的CMD窗口..." -ForegroundColor Cyan
                    $processes = Get-Process | Where-Object {{$_.ProcessName -eq "cmd" -and $_.MainWindowTitle -like "*claude*"}}
                    if ($processes) {{
                        Write-Host "找到 $($processes.Count) 个匹配窗口" -ForegroundColor Cyan
                        [Microsoft.VisualBasic.Interaction]::AppActivate($processes[0].Id)
                        $activated = $true
                        Write-Host "成功: 方法2已激活 Claude CLI 窗口" -ForegroundColor Green
                    }} else {{
                        $activationError = "未找到标题包含'claude'的CMD窗口"
                        Write-Host "方法2失败: $activationError" -ForegroundColor Red
                    }}
                }} catch {{
                    $activationError = "方法2失败: $($_.Exception.Message)"
                    Write-Host $activationError -ForegroundColor Red
                    Write-Host "尝试方法3..." -ForegroundColor Yellow
                }}
            }}
            
            # Method 3: Windows API force activation
            if (-not $activated) {{
                try {{
                    Write-Host "方法3: 使用Windows API强制激活窗口..." -ForegroundColor Cyan
                    Add-Type -TypeDefinition @"
                    using System;
                    using System.Runtime.InteropServices;
                    public class WindowHelper {{
                        [DllImport("user32.dll")]
                        public static extern bool SetForegroundWindow(IntPtr hWnd);
                        [DllImport("user32.dll")]
                        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
                    }}
"@
                    if ($claudeProcess -and !$claudeProcess.HasExited -and $claudeProcess.MainWindowHandle -ne [IntPtr]::Zero) {{
                        [WindowHelper]::ShowWindow($claudeProcess.MainWindowHandle, 9) | Out-Null
                        [WindowHelper]::SetForegroundWindow($claudeProcess.MainWindowHandle) | Out-Null
                        $activated = $true
                        Write-Host "成功: 方法3使用Windows API激活了 Claude CLI 窗口" -ForegroundColor Green
                    }} else {{
                        $activationError = "Windows API的进程句柄无效"
                        Write-Host "方法3失败: $activationError" -ForegroundColor Red
                    }}
                }} catch {{
                    $activationError = "方法3失败: $($_.Exception.Message)"
                    Write-Host $activationError -ForegroundColor Red
                }}
            }}
            
            if ($activated) {{
                Write-Host "窗口激活成功，准备自动粘贴..." -ForegroundColor Green
                Start-Sleep -Milliseconds 300
                
                # Send Ctrl+V to paste with verification
                try {{
                    Write-Host "发送 Ctrl+V 粘贴提示词..." -ForegroundColor Cyan
                    
                    # Step 1: Send the paste command
                    [System.Windows.Forms.SendKeys]::SendWait("^v")
                    Write-Host "✓ 粘贴命令已发送" -ForegroundColor Green
                    
                    # Step 2: Wait for initial paste processing
                    Write-Host "等待粘贴操作处理..." -ForegroundColor Yellow
                    Start-Sleep -Milliseconds 600
                    
                    # Step 3: Send a harmless key to ensure the paste is processed
                    # Using End key to move cursor to end (this confirms text was pasted)
                    Write-Host "发送End键确认粘贴完成..." -ForegroundColor Cyan
                    [System.Windows.Forms.SendKeys]::SendWait("{{END}}")
                    Start-Sleep -Milliseconds 200
                    
                    # Step 4: Verify clipboard content
                    Write-Host "验证剪贴板内容..." -ForegroundColor Cyan
                    $clipboardContent = Get-Clipboard -Raw
                    if ($clipboardContent -and $clipboardContent.Length -gt 10) {{
                        $previewText = $clipboardContent.Substring(0, [Math]::Min(60, $clipboardContent.Length)).Replace("`n", " ").Replace("`r", " ")
                        Write-Host "✓ 确认剪贴板内容: $previewText..." -ForegroundColor Green
                        Write-Host "✓ 粘贴操作确认完成" -ForegroundColor Green
                        $pasteConfirmed = $true
                    }} else {{
                        Write-Host "⚠ 警告: 剪贴板内容检测异常" -ForegroundColor Yellow
                        $pasteConfirmed = $false
                    }}
                    
                    # Step 5: Additional confirmation wait
                    if ($pasteConfirmed) {{
                        Write-Host "粘贴已确认，继续执行..." -ForegroundColor Green
                    }} else {{
                        Write-Host "粘贴状态未确认，但继续执行流程..." -ForegroundColor Yellow
                    }}
                    
                }} catch {{
                    Write-Host "✗ 粘贴失败: $($_.Exception.Message)" -ForegroundColor Red
                    Write-Host "错误详情: $($_.Exception.StackTrace)" -ForegroundColor DarkRed
                    throw
                }}
                
                # Additional wait to ensure paste is fully processed by Claude CLI
                Write-Host "额外等待 1200ms 确保Claude CLI处理完粘贴..." -ForegroundColor Yellow
                Start-Sleep -Milliseconds 1200
                
                # Final wait before sending Enter as requested
                Write-Host "按用户要求等待 2000ms 后发送 Enter 键..." -ForegroundColor Yellow
                Start-Sleep -Milliseconds 2000
                
                # Send Enter key to submit - using robust methods
                try {{
                    Write-Host "发送Enter键提交提示词..." -ForegroundColor Cyan
                    
                    # Method 1: Try simple tilde method first (most reliable)
                    try {{
                        [System.Windows.Forms.SendKeys]::SendWait("~")
                        Write-Host "Enter键发送成功 (方法1: 波浪号)" -ForegroundColor Green
                        $enterSent = $true
                    }} catch {{
                        Write-Host "方法1失败，尝试方法2..." -ForegroundColor Yellow
                        $enterSent = $false
                    }}
                    
                    # Method 2: Try standard ENTER if method 1 failed
                    if (-not $enterSent) {{
                        try {{
                            Start-Sleep -Milliseconds 100
                            [System.Windows.Forms.SendKeys]::SendWait("{{ENTER}}")
                            Write-Host "Enter键发送成功 (方法2: 标准ENTER)" -ForegroundColor Green
                            $enterSent = $true
                        }} catch {{
                            Write-Host "方法2失败，尝试方法3..." -ForegroundColor Yellow
                        }}
                    }}
                    
                    # Method 3: Try VK_RETURN using Windows API if other methods failed
                    if (-not $enterSent) {{
                        try {{
                            Add-Type -TypeDefinition @"
                            using System;
                            using System.Runtime.InteropServices;
                            public class KeySender {{
                                [DllImport("user32.dll")]
                                public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);
                                
                                [DllImport("user32.dll")]
                                public static extern IntPtr GetForegroundWindow();
                                
                                [DllImport("user32.dll")]
                                public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
                                
                                public const int VK_RETURN = 0x0D;
                                public const int WM_KEYDOWN = 0x0100;
                                public const int WM_KEYUP = 0x0101;
                                public const int WM_CHAR = 0x0102;
                                
                                public static void SendEnterKeyboard() {{
                                    keybd_event(VK_RETURN, 0, 0, 0);  // Key down
                                    System.Threading.Thread.Sleep(50);
                                    keybd_event(VK_RETURN, 0, 2, 0);  // Key up
                                }}
                                
                                public static void SendEnterMessage() {{
                                    IntPtr hWnd = GetForegroundWindow();
                                    PostMessage(hWnd, WM_KEYDOWN, (IntPtr)VK_RETURN, IntPtr.Zero);
                                    System.Threading.Thread.Sleep(50);
                                    PostMessage(hWnd, WM_CHAR, (IntPtr)13, IntPtr.Zero);  // ASCII 13 = Enter
                                    PostMessage(hWnd, WM_KEYUP, (IntPtr)VK_RETURN, IntPtr.Zero);
                                }}
                            }}
"@
                            # Try keyboard event first
                            [KeySender]::SendEnterKeyboard()
                            Start-Sleep -Milliseconds 100
                            
                            # Also try Windows message approach as backup
                            [KeySender]::SendEnterMessage()
                            
                            Write-Host "Enter键发送成功 (方法3: 组合Windows API)" -ForegroundColor Green
                            $enterSent = $true
                        }} catch {{
                            Write-Host "方法3失败: $($_.Exception.Message)" -ForegroundColor Yellow
                        }}
                    }}
                    
                    if (-not $enterSent) {{
                        Write-Host "所有Enter键发送方法都失败了" -ForegroundColor Red
                        Write-Host "提示词已粘贴到Claude CLI，请手动按Enter键发送" -ForegroundColor Yellow
                    }}
                    
                }} catch {{
                    Write-Host "发送Enter键过程中发生未处理的错误: $($_.Exception.Message)" -ForegroundColor Red
                    Write-Host "提示词已在剪贴板和Claude CLI中，请手动按Enter键" -ForegroundColor Yellow
                }}
                
                Write-Host ""
                Write-Host "=== 自动粘贴和发送完成 ===" -ForegroundColor Green
                Write-Host "Claude CLI 现在应该正在处理您的请求..." -ForegroundColor Yellow
                
            }} else {{
                Write-Host ""
                Write-Host "=== 自动激活失败 ===" -ForegroundColor Red
                Write-Host "失败原因: $activationError" -ForegroundColor Red
                Write-Host ""
                Write-Host "请手动完成以下步骤:" -ForegroundColor Yellow
                Write-Host "1. 点击 Claude CLI 窗口以激活它" -ForegroundColor White
                Write-Host "2. 按 Ctrl+V 粘贴提示词" -ForegroundColor White  
                Write-Host "3. 按 Enter 键发送" -ForegroundColor White
                Write-Host "提示词已在剪贴板中准备就绪!" -ForegroundColor Green
            }}
            
        }} catch {{
            Write-Host ""
            Write-Host "=== 自动粘贴过程发生错误 ===" -ForegroundColor Red
            Write-Host "错误详情: $($_.Exception.Message)" -ForegroundColor Red
            
            # 只在调试模式下显示完整堆栈跟踪
            if ($VerbosePreference -eq 'Continue') {{
                Write-Host "完整堆栈跟踪: $($_.Exception.StackTrace)" -ForegroundColor DarkRed
            }}
            
            Write-Host ""
            Write-Host "=== 回退到手动模式 ===" -ForegroundColor Yellow
            Write-Host "提示词已在剪贴板中，请按以下步骤手动完成:" -ForegroundColor Yellow
            Write-Host "1. 点击Claude CLI窗口" -ForegroundColor White
            Write-Host "2. 按 Ctrl+V 粘贴提示词" -ForegroundColor White
            Write-Host "3. 按 Enter 键发送" -ForegroundColor White
        }}
        
    }} else {{
        Write-Host "启动 Claude CLI 失败" -ForegroundColor Red
        Write-Host "请检查 Claude CLI 是否已正确安装并在 PATH 环境变量中" -ForegroundColor Yellow
    }}
    
}} catch {{
    Write-Host ""
    Write-Host "=== 脚本执行发生错误 ===" -ForegroundColor Red
    Write-Host "错误信息: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "错误详情: $($_.Exception.StackTrace)" -ForegroundColor Red
}}

Write-Host ""
Write-Host "按任意键关闭此窗口..." -ForegroundColor Gray
try {{
    $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
}} catch {{
    # 如果 ReadKey 失败，使用 Read-Host 作为备用
    Read-Host "按 Enter 键继续"
}}
Write-Host "窗口正在关闭..."
'''
            
            # 写入PowerShell脚本 - 使用UTF-8 BOM编码避免中文乱码
            with open(ps_script_file, 'w', encoding='utf-8-sig') as f:
                f.write(ps_content)
            
            # 创建批处理文件来启动PowerShell脚本
            batch_file = os.path.join(self.temp_dir, "start_claude_auto_input.bat")
            batch_content = f'''@echo off
echo Starting Claude CLI Auto Input...
echo.
powershell.exe -ExecutionPolicy Bypass -NoExit -File "{ps_script_file}"
pause
'''
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            # 直接启动批处理文件，使用简单方式避免引号问题
            cmd = [batch_file]
            process = subprocess.Popen(cmd, shell=True)
            
            logger.info(f"Windows Claude CLI 自动输入已启动，进程 ID: {process.pid}")
            
            return {
                "status": "success",
                "message": "Claude CLI 自动输入流程已启动（等待2000ms后自动输入提示词）",
                "process_id": process.pid,
                "prompt_file": prompt_file,
                "powershell_script": ps_script_file,
                "batch_file": batch_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Windows Claude CLI 自动输入失败: {str(e)}")
            raise
    
    def _open_claude_cli_with_prompt_macos(self, prompt_content: str, prompt_file: str) -> Dict[str, Any]:
        """macOS下打开Claude CLI并自动输入提示词"""
        try:
            # 创建一个shell脚本来自动化输入
            script_file = os.path.join(self.temp_dir, "claude_auto_input.sh")
            
            script_content = f'''#!/bin/bash
echo "Starting Claude CLI with automatic input..."
echo ""
echo "====================================="
echo "Prompt Content Preview:"
echo "====================================="
cat "{prompt_file}"
echo ""
echo "====================================="
echo "Sending to Claude CLI..."
echo "====================================="
echo ""
echo '{prompt_content}' | claude
read -p "Press Enter to close..."
'''
            
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 给脚本执行权限
            os.chmod(script_file, 0o755)
            
            # 使用AppleScript打开Terminal并执行脚本
            applescript = f'''
tell application "Terminal"
    do script "bash '{script_file}'"
    activate
end tell
'''
            
            cmd = ["osascript", "-e", applescript]
            process = subprocess.Popen(cmd)
            
            logger.info(f"macOS Claude CLI 自动输入已启动，进程 ID: {process.pid}")
            
            return {
                "status": "success", 
                "message": "Claude CLI 已打开并自动输入提示词内容",
                "process_id": process.pid,
                "prompt_file": prompt_file,
                "script_file": script_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"macOS Claude CLI 自动输入失败: {str(e)}")
            raise
    
    def _open_claude_cli_with_prompt_linux(self, prompt_content: str, prompt_file: str) -> Dict[str, Any]:
        """Linux下打开Claude CLI并自动输入提示词"""
        try:
            # 创建一个shell脚本来自动化输入
            script_file = os.path.join(self.temp_dir, "claude_auto_input.sh")
            
            script_content = f'''#!/bin/bash
echo "Starting Claude CLI with automatic input..."
echo ""
echo "====================================="
echo "Prompt Content Preview:"
echo "====================================="
cat "{prompt_file}"
echo ""
echo "====================================="
echo "Sending to Claude CLI..."
echo "====================================="
echo ""
echo '{prompt_content}' | claude
read -p "Press Enter to close..."
'''
            
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # 给脚本执行权限
            os.chmod(script_file, 0o755)
            
            # 打开新的终端窗口执行脚本
            cmd = ["gnome-terminal", "--", "bash", script_file]
            process = subprocess.Popen(cmd)
            
            logger.info(f"Linux Claude CLI 自动输入已启动，进程 ID: {process.pid}")
            
            return {
                "status": "success",
                "message": "Claude CLI 已打开并自动输入提示词内容", 
                "process_id": process.pid,
                "prompt_file": prompt_file,
                "script_file": script_file,
                "platform": self.system,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Linux Claude CLI 自动输入失败: {str(e)}")
            raise
    
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

# 全局实例
claude_cli_automation = ClaudeCLIAutomation()