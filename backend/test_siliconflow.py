#!/usr/bin/env python3
"""
SiliconFlow API 测试脚本
用于验证SiliconFlow API的连接和模型调用
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_siliconflow_api():
    """测试SiliconFlow API调用"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    model = os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen2.5-32B-Instruct")
    
    print("=== SiliconFlow API 测试 ===")
    print(f"API Key: {api_key[:20] if api_key else 'None'}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print()
    
    if not api_key:
        print("ERROR: SILICONFLOW_API_KEY 未设置")
        return False
    
    # 构建请求
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "user", 
                "content": "你好，请简单介绍一下你自己"
            }
        ],
        "temperature": 0.7
    }
    
    try:
        print("发送测试请求...")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print()
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: 请求成功!")
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 提取回复内容
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"\nAI回复: {content}")
            
            return True
        else:
            print(f"FAILED: 请求失败: {response.status_code}")
            print(f"错误响应: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: 网络请求错误: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON解析错误: {e}")
        print(f"原始响应: {response.text}")
        return False
    except Exception as e:
        print(f"ERROR: 未知错误: {e}")
        return False

def test_available_models():
    """测试可用模型列表"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    base_url = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
    
    if not api_key:
        print("❌ SILICONFLOW_API_KEY 未设置，跳过模型列表测试")
        return
    
    print("\n=== 测试可用模型列表 ===")
    
    url = f"{base_url}/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            models = response.json()
            print("✅ 模型列表获取成功:")
            
            if 'data' in models:
                qwen_models = [m for m in models['data'] if 'Qwen' in m.get('id', '')]
                print(f"\n🔍 找到 {len(qwen_models)} 个Qwen模型:")
                for model in qwen_models[:10]:  # 只显示前10个
                    print(f"  - {model.get('id', 'Unknown')}")
            else:
                print(f"模型数据: {json.dumps(models, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ 模型列表获取失败: {response.status_code}")
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 模型列表请求错误: {e}")

if __name__ == "__main__":
    print("开始测试 SiliconFlow API...")
    print()
    
    # 测试API调用
    success = test_siliconflow_api()
    
    # 测试模型列表
    test_available_models()
    
    print("\n=== 测试完成 ===")
    if success:
        print("✅ SiliconFlow API 工作正常，可以用作降级策略")
    else:
        print("❌ SiliconFlow API 测试失败，需要检查配置")
        sys.exit(1)