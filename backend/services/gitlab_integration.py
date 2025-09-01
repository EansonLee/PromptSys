"""
Git SSH 集成工具
用于通过SSH方式获取和管理 Git 仓库信息
"""

import os
import logging
import subprocess
from typing import Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class GitIntegration:
    """Git SSH 集成管理器 - 统一使用SSH方式访问Git仓库"""
    
    def __init__(self):
        # 从 .env 文件读取 SSH 密钥配置
        self.ssh_key_path = os.getenv("GIT_SSH_KEY_PATH", "~/.ssh/id_rsa")
        self.ssh_key_content = os.getenv("GIT_SSH_KEY_CONTENT")
        self.git_user_name = os.getenv("GIT_USER_NAME")
        self.git_user_email = os.getenv("GIT_USER_EMAIL")
        
        # 展开用户主目录路径
        if self.ssh_key_path.startswith("~"):
            self.ssh_key_path = os.path.expanduser(self.ssh_key_path)
        
        logger.info(f"使用SSH密钥方式访问Git仓库，密钥路径: {self.ssh_key_path}")
        
        # 检查SSH密钥配置
        self._validate_ssh_config()
    
    def _validate_ssh_config(self):
        """验证SSH密钥配置"""
        if self.ssh_key_content:
            logger.info("检测到SSH密钥内容配置，将使用环境变量中的密钥")
        elif os.path.exists(self.ssh_key_path):
            logger.info(f"SSH密钥文件存在: {self.ssh_key_path}")
        else:
            logger.warning(f"SSH密钥文件不存在: {self.ssh_key_path}")
            logger.warning("请在 .env 文件中配置正确的 GIT_SSH_KEY_PATH 或 GIT_SSH_KEY_CONTENT")
    
    def _setup_ssh_environment(self) -> Dict[str, str]:
        """设置SSH环境变量"""
        env = os.environ.copy()
        
        # 如果配置了SSH密钥内容，创建临时密钥文件
        if self.ssh_key_content:
            import tempfile
            import platform
            
            try:
                # 处理可能的换行符问题
                key_content = self.ssh_key_content.strip()
                # 确保私钥内容有正确的换行符
                # .env文件中的多行字符串可能被读取为单行，需要转换换行符
                if '\\n' in key_content and '\n' not in key_content:
                    key_content = key_content.replace('\\n', '\n')
                elif '\n' not in key_content and len(key_content.split()) > 10:
                    # 如果是单行但内容很长，可能需要手动添加换行符
                    logger.warning("SSH密钥似乎是单行格式，这可能导致问题")
                
                # 验证私钥格式
                if not (key_content.startswith('-----BEGIN') and key_content.endswith('-----')):
                    logger.error("SSH密钥格式不正确，必须包含完整的 BEGIN 和 END 标记")
                    raise ValueError("SSH密钥格式不正确")
                
                # 在Windows上需要特殊处理文件权限
                temp_key_file = tempfile.NamedTemporaryFile(mode='w', suffix='.key', delete=False, encoding='utf-8')
                temp_key_file.write(key_content)
                if not key_content.endswith('\n'):
                    temp_key_file.write('\n')
                temp_key_file.close()
                
                # 在Unix系统上设置文件权限
                if platform.system() != 'Windows':
                    os.chmod(temp_key_file.name, 0o600)
                else:
                    # Windows上也尝试设置权限，虽然可能无效
                    try:
                        os.chmod(temp_key_file.name, 0o600)
                    except:
                        pass
                
                env['GIT_SSH_COMMAND'] = f'ssh -i "{temp_key_file.name}" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
                logger.info(f"使用环境变量中的SSH密钥内容，临时文件: {temp_key_file.name}")
                
                # 验证临时文件内容
                with open(temp_key_file.name, 'r') as f:
                    file_content = f.read()
                    logger.debug(f"临时密钥文件前50字符: {file_content[:50]}")
                    
            except Exception as e:
                logger.error(f"创建临时SSH密钥文件失败: {str(e)}")
                # 回退到默认SSH配置
                env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no'
                logger.info("回退到默认SSH配置")
        elif os.path.exists(self.ssh_key_path):
            env['GIT_SSH_COMMAND'] = f'ssh -i "{self.ssh_key_path}" -o StrictHostKeyChecking=no'
            logger.info(f"使用SSH密钥文件: {self.ssh_key_path}")
        else:
            # 使用默认SSH配置
            env['GIT_SSH_COMMAND'] = 'ssh -o StrictHostKeyChecking=no'
            logger.info("使用默认SSH配置")
        
        return env
    
    def parse_repository_url(self, repo_url: str) -> Dict[str, str]:
        """
        解析 GitLab 仓库 URL
        
        Args:
            repo_url: GitLab 仓库 URL
            
        Returns:
            Dict: 解析结果包含域名、项目路径等
        """
        try:
            # 处理 SSH URL 格式 git@domain:user/repo.git
            if repo_url.startswith("git@"):
                # 将 SSH 格式转换为 HTTPS 格式进行解析
                ssh_parts = repo_url.replace("git@", "").replace(".git", "")
                if ":" in ssh_parts:
                    domain_part, path_part = ssh_parts.split(":", 1)
                    https_url = f"https://{domain_part}/{path_part}"
                    parsed = urlparse(https_url)
                else:
                    raise ValueError("无效的 SSH URL 格式")
            else:
                parsed = urlparse(repo_url)
            
            domain = f"{parsed.scheme}://{parsed.netloc}"
            
            # 移除 .git 后缀和前导斜杠
            path = parsed.path.strip('/').replace('.git', '')
            
            # GitLab API 需要的项目路径格式
            project_path = path.replace('/', '%2F')
            
            return {
                "domain": domain,
                "path": path,
                "project_path": project_path,
                "api_url": f"{domain}/api/v4/projects/{project_path}"
            }
            
        except Exception as e:
            logger.error(f"解析仓库 URL 失败: {str(e)}")
            raise ValueError(f"无效的 GitLab URL: {repo_url}")
    
    def get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """
        通过SSH获取Git仓库信息
        
        Args:
            repo_url: Git仓库 URL
            
        Returns:
            Dict: 仓库信息
        """
        try:
            logger.info(f"使用SSH方式获取仓库信息: {repo_url}")
            return self._get_git_info_via_ssh(repo_url)
            
        except Exception as e:
            logger.error(f"获取仓库信息失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取仓库信息失败: {str(e)}",
                "repository_url": repo_url,
                "auth_method": "ssh_key",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_git_info_via_ssh(self, repo_url: str) -> Dict[str, Any]:
        """
        通过SSH密钥和Git命令获取仓库信息
        
        Args:
            repo_url: Git仓库URL
            
        Returns:
            Dict: 仓库信息
        """
        try:
            # 临时克隆仓库获取信息
            temp_dir = f"/tmp/gitlab_temp_{os.getpid()}"
            
            # 使用git命令获取远程仓库信息
            cmd_remote_info = f"git ls-remote --heads {repo_url}"
            env = self._setup_ssh_environment()
            result = subprocess.run(cmd_remote_info.split(), capture_output=True, text=True, timeout=30, env=env)
            
            if result.returncode == 0:
                # 解析分支信息
                branches = []
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line and '\t' in line:
                        commit_id, ref = line.split('\t', 1)
                        branch_name = ref.replace('refs/heads/', '')
                        branches.append({
                            "name": branch_name,
                            "commit_id": commit_id[:8],
                            "default": branch_name == "main" or branch_name == "master"
                        })
                
                # 获取仓库名称
                repo_name = repo_url.split('/')[-1].replace('.git', '') if '/' in repo_url else repo_url
                
                return {
                    "status": "success",
                    "repository_name": repo_name,
                    "repository_url": repo_url,
                    "description": "通过SSH获取的仓库信息",
                    "default_branch": "main" if any(b["name"] == "main" for b in branches) else (branches[0]["name"] if branches else "master"),
                    "branches": branches,
                    "message": "通过SSH密钥获取仓库信息成功",
                    "auth_method": "ssh_key",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": f"SSH访问失败: {result.stderr}",
                    "repository_url": repo_url,
                    "auth_method": "ssh_key",
                    "timestamp": datetime.now().isoformat()
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "message": "SSH操作超时",
                "repository_url": repo_url,
                "auth_method": "ssh_key", 
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"SSH获取仓库信息失败: {str(e)}")
            return {
                "status": "error",
                "message": f"SSH获取仓库信息失败: {str(e)}",
                "repository_url": repo_url,
                "auth_method": "ssh_key",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_repository_branches(self, repo_url: str) -> Dict[str, Any]:
        """
        通过SSH获取仓库分支信息
        
        Args:
            repo_url: Git仓库 URL
            
        Returns:
            Dict: 分支信息
        """
        try:
            logger.info(f"使用SSH方式获取分支信息: {repo_url}")
            # 从SSH获取的仓库信息中提取分支信息
            repo_info = self._get_git_info_via_ssh(repo_url)
            if repo_info.get("status") == "success":
                branches = repo_info.get("branches", [])
                return {
                    "status": "success",
                    "branches": branches,
                    "message": "通过SSH密钥获取分支信息成功",
                    "auth_method": "ssh_key",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return repo_info
                
        except Exception as e:
            logger.error(f"获取分支信息失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取分支信息失败: {str(e)}",
                "auth_method": "ssh_key",
                "timestamp": datetime.now().isoformat()
            }

# 全局实例
gitlab_integration = GitIntegration()