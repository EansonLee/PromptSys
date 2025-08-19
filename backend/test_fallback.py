#!/usr/bin/env python3
"""
测试降级策略的脚本
发送请求到本地API来验证500错误时的降级机制
"""

import requests
import json
import time

def test_api_request():
    """测试API请求和降级策略"""
    url = "http://localhost:8000/generate-prompt"
    
    data = {
        "app_name": "清理大师",
        "theme": "智能清理系统，通过AI分析设备使用情况",
        "variant_folder": "variant_clean123",
        "ui_color": "蓝色科技感"
    }
    
    print("=== 测试降级策略 ===")
    print(f"发送请求到: {url}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    print()
    
    try:
        print("发送请求中...")
        start_time = time.time()
        
        response = requests.post(
            url, 
            json=data, 
            headers={"Content-Type": "application/json"},
            timeout=60  # 延长超时时间
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"响应时间: {duration:.2f}秒")
        print(f"状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 请求成功！")
            print(f"角色: {result['role'][:100]}...")
            print(f"目标: {result['goal'][:100]}...")
            print(f"功能输出长度: {len(result['function_output'])} 字符")
            print(f"UI要求: {result['ui_requirements'][:100]}...")
            print(f"时间戳: {result['timestamp']}")
            
            # 检查内容是否包含创意元素
            content = result['function_output']
            has_bullets = '•' in content
            has_examples = ('示例展示' in content or '📊' in content or '🎯' in content)
            
            print(f"\n创意检查:")
            print(f"  - 包含项目符号: {'✅' if has_bullets else '❌'}")
            print(f"  - 包含示例展示: {'✅' if has_examples else '❌'}")
            
            return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

if __name__ == "__main__":
    print("开始测试降级策略...")
    print("注意：主要API可能会返回500错误，这时应该自动切换到SiliconFlow")
    print()
    
    success = test_api_request()
    
    print("\n=== 测试完成 ===")
    if success:
        print("✅ 降级策略测试成功！")
        print("请检查后端日志确认使用了哪个API")
    else:
        print("❌ 测试失败，请检查后端日志")