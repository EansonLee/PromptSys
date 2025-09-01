#!/usr/bin/env python3
"""
Git SSH 集成功能测试脚本
测试 gitlab_integration 模块是否能正确通过SSH获取仓库和分支信息
"""

import os
import sys
import json
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加 backend 目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.gitlab_integration import gitlab_integration

def print_separator(title: str):
    """打印分隔符"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_result(title: str, result: Dict[str, Any]):
    """打印测试结果"""
    print(f"\n{title}:")
    print("-" * 40)
    print(json.dumps(result, indent=2, ensure_ascii=False))

def test_repository_info(repo_url: str):
    """测试仓库信息获取"""
    print_separator("测试仓库信息获取")
    print(f"仓库URL: {repo_url}")
    
    try:
        result = gitlab_integration.get_repository_info(repo_url)
        print_result("仓库信息", result)
        
        # 检查关键字段
        if result.get("status") == "success":
            print("\n[SUCCESS] 仓库信息获取成功")
            print(f"   - 仓库名称: {result.get('repository_name')}")
            print(f"   - 默认分支: {result.get('default_branch')}")
            print(f"   - 描述: {result.get('description')}")
            print(f"   - SSH URL: {result.get('ssh_url')}")
        else:
            print("\n[ERROR] 仓库信息获取失败")
            print(f"   - 错误信息: {result.get('message')}")
            
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {str(e)}")

def test_repository_branches(repo_url: str):
    """测试分支信息获取"""
    print_separator("测试分支信息获取")
    print(f"仓库URL: {repo_url}")
    
    try:
        result = gitlab_integration.get_repository_branches(repo_url)
        # print_result("分支信息", result)
        
        # 检查关键字段
        if result.get("status") == "success":
            branches = result.get("branches", [])
            print(f"\n[SUCCESS] 分支信息获取成功 (共 {len(branches)} 个分支)")
            for branch in branches:
                default_flag = " (默认)" if branch.get("default") else ""
                commit_info = f" [{branch.get('last_commit', 'N/A')}]" if branch.get('last_commit') else ""
                print(f"   - {branch.get('name')}{default_flag}{commit_info}")
        else:
            print("\n[ERROR] 分支信息获取失败")
            print(f"   - 错误信息: {result.get('message')}")
            
    except Exception as e:
        print(f"\n[ERROR] 测试异常: {str(e)}")

def test_url_parsing():
    """测试URL解析功能"""
    print_separator("测试URL解析功能")
    
    test_urls = [
        "git@git.yingzhongshare.com:starbaba/android/traffic_android.git"
    ]
    
    for url in test_urls:
        print(f"\n测试URL: {url}")
        try:
            parsed = gitlab_integration.parse_repository_url(url)
            print(f"  - 域名: {parsed.get('domain')}")
            print(f"  - 路径: {parsed.get('path')}")
            print(f"  - 项目路径: {parsed.get('project_path')}")
            print(f"  - API URL: {parsed.get('api_url')}")
            print("  [SUCCESS] URL解析成功")
        except Exception as e:
            print(f"  [ERROR] URL解析失败: {str(e)}")

def check_environment():
    """检查环境配置"""
    print_separator("环境配置检查")
    
    # 从 .env 文件读取SSH密钥配置
    ssh_key_path = os.getenv("GIT_SSH_KEY_PATH", "~/.ssh/id_rsa")
    ssh_key_content = os.getenv("GIT_SSH_KEY_CONTENT")
    git_user_name = os.getenv("GIT_USER_NAME")
    git_user_email = os.getenv("GIT_USER_EMAIL")
    
    # 展开用户主目录路径
    if ssh_key_path.startswith("~"):
        ssh_key_path = os.path.expanduser(ssh_key_path)
    
    print("认证方式: SSH密钥 (通过 .env 文件配置)")
    print(f"SSH密钥路径: {ssh_key_path}")
    print(f"SSH密钥存在: {'是' if os.path.exists(ssh_key_path) else '否'}")
    print(f"SSH密钥内容: {'已配置' if ssh_key_content else '未配置'}")
    print(f"Git用户名: {git_user_name if git_user_name else '未配置'}")
    print(f"Git邮箱: {git_user_email if git_user_email else '未配置'}")
    
    print("\n说明: 使用 .env 文件配置SSH密钥访问Git仓库")
    print("   配置项: GIT_SSH_KEY_PATH 或 GIT_SSH_KEY_CONTENT")
    print("   通过git ls-remote命令获取仓库和分支信息")
    
    if not os.path.exists(ssh_key_path) and not ssh_key_content:
        print("\n⚠️ 警告: SSH密钥未正确配置")
        print("   请在 backend/.env 文件中设置:")
        print("   GIT_SSH_KEY_PATH=你的SSH密钥文件路径")
        print("   或")
        print("   GIT_SSH_KEY_CONTENT=你的SSH密钥内容")

def main():
    """主测试函数"""
    print("Git SSH 集成功能测试")
    print("=" * 60)
    
    # 检查环境配置
    check_environment()
    
    # 测试仓库URL
    repo_url = "git@git.yingzhongshare.com:starbaba/android/traffic_android.git"
    
    # 测试URL解析
    test_url_parsing()
    
    # 测试仓库信息获取
    test_repository_info(repo_url)
    
    # 测试分支信息获取
    test_repository_branches(repo_url)
    
    print_separator("测试完成")
    print("请查看上述测试结果，确认Git SSH集成功能是否正常工作。")
    print("统一使用SSH密钥方式通过Git命令获取仓库信息。")

if __name__ == "__main__":
    main()