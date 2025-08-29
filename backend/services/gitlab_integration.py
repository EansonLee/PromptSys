"""
GitLab API 集成工具
用于获取和管理 GitLab 仓库信息
"""

import os
import requests
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class GitLabIntegration:
    """GitLab API 集成管理器"""
    
    def __init__(self):
        self.gitlab_token = os.getenv("GITLAB_TOKEN")
        self.default_gitlab_url = os.getenv("GITLAB_URL", "https://gitlab.com")
        
        if not self.gitlab_token:
            logger.warning("GITLAB_TOKEN 未配置，将使用模拟数据")
    
    def parse_repository_url(self, repo_url: str) -> Dict[str, str]:
        """
        解析 GitLab 仓库 URL
        
        Args:
            repo_url: GitLab 仓库 URL
            
        Returns:
            Dict: 解析结果包含域名、项目路径等
        """
        try:
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
        获取 GitLab 仓库信息
        
        Args:
            repo_url: GitLab 仓库 URL
            
        Returns:
            Dict: 仓库信息
        """
        try:
            # 验证是否为 GitLab URL
            if "gitlab" not in repo_url.lower():
                raise ValueError("只支持 GitLab 仓库")
            
            url_info = self.parse_repository_url(repo_url)
            
            # 如果没有配置 GitLab Token，返回模拟数据
            if not self.gitlab_token:
                return self._get_mock_repository_info(url_info, repo_url)
            
            # 使用实际 GitLab API
            headers = {
                "Authorization": f"Bearer {self.gitlab_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url_info["api_url"], headers=headers, timeout=10)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                return {
                    "status": "success",
                    "repository_name": repo_data.get("name", ""),
                    "repository_url": repo_url,
                    "description": repo_data.get("description", ""),
                    "default_branch": repo_data.get("default_branch", "main"),
                    "last_activity": repo_data.get("last_activity_at", ""),
                    "visibility": repo_data.get("visibility", "private"),
                    "stars_count": repo_data.get("star_count", 0),
                    "forks_count": repo_data.get("forks_count", 0),
                    "open_issues_count": repo_data.get("open_issues_count", 0),
                    "web_url": repo_data.get("web_url", ""),
                    "clone_url": repo_data.get("http_url_to_repo", ""),
                    "ssh_url": repo_data.get("ssh_url_to_repo", ""),
                    "message": "仓库信息获取成功",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"GitLab API 请求失败: {response.status_code} - {response.text}")
                return {
                    "status": "error",
                    "message": f"API 请求失败: HTTP {response.status_code}",
                    "repository_url": repo_url,
                    "timestamp": datetime.now().isoformat()
                }
                
        except requests.exceptions.Timeout:
            logger.error("GitLab API 请求超时")
            return {
                "status": "error",
                "message": "API 请求超时",
                "repository_url": repo_url,
                "timestamp": datetime.now().isoformat()
            }
        except requests.exceptions.ConnectionError:
            logger.error("无法连接到 GitLab API")
            return {
                "status": "error",
                "message": "无法连接到 GitLab 服务器",
                "repository_url": repo_url,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取仓库信息失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取仓库信息失败: {str(e)}",
                "repository_url": repo_url,
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_mock_repository_info(self, url_info: Dict[str, str], repo_url: str) -> Dict[str, Any]:
        """
        返回模拟的仓库信息（当没有配置 GitLab Token 时使用）
        
        Args:
            url_info: 解析的 URL 信息
            repo_url: 原始仓库 URL
            
        Returns:
            Dict: 模拟的仓库信息
        """
        repo_name = url_info["path"].split('/')[-1] if '/' in url_info["path"] else url_info["path"]
        
        return {
            "status": "success",
            "repository_name": repo_name,
            "repository_url": repo_url,
            "description": "这是一个示例仓库（模拟数据）",
            "default_branch": "main",
            "last_activity": datetime.now().isoformat(),
            "visibility": "private",
            "stars_count": 5,
            "forks_count": 2,
            "open_issues_count": 3,
            "web_url": repo_url,
            "clone_url": repo_url,
            "ssh_url": repo_url.replace("https://", "git@").replace(".com/", ".com:") + ".git",
            "message": "仓库信息获取成功（模拟数据）",
            "note": "请配置 GITLAB_TOKEN 环境变量以获取真实数据",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_repository_branches(self, repo_url: str) -> Dict[str, Any]:
        """
        获取仓库分支信息
        
        Args:
            repo_url: GitLab 仓库 URL
            
        Returns:
            Dict: 分支信息
        """
        try:
            if not self.gitlab_token:
                return {
                    "status": "success",
                    "branches": [
                        {"name": "main", "default": True},
                        {"name": "develop", "default": False},
                        {"name": "feature/example", "default": False}
                    ],
                    "message": "分支信息获取成功（模拟数据）",
                    "timestamp": datetime.now().isoformat()
                }
            
            url_info = self.parse_repository_url(repo_url)
            branches_url = f"{url_info['api_url']}/repository/branches"
            
            headers = {
                "Authorization": f"Bearer {self.gitlab_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(branches_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                branches_data = response.json()
                branches = [
                    {
                        "name": branch.get("name", ""),
                        "default": branch.get("default", False),
                        "last_commit": branch.get("commit", {}).get("id", "")[:8]
                    }
                    for branch in branches_data
                ]
                
                return {
                    "status": "success",
                    "branches": branches,
                    "message": "分支信息获取成功",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": f"获取分支信息失败: HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"获取分支信息失败: {str(e)}")
            return {
                "status": "error",
                "message": f"获取分支信息失败: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

# 全局实例
gitlab_integration = GitLabIntegration()