#!/usr/bin/env python3
"""
测试中转站API的可用性
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(override=True)

def test_api():
    """测试中转站API"""
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print("=== 中转站API测试 ===")
    print(f"API Key: {api_key[:20] if api_key else 'None'}...")
    print(f"Base URL: {base_url}")
    
    # 测试不同的endpoint路径
    endpoints_to_test = [
        f"{base_url}/chat/completions",
        "https://api.free.fastapi.pro/v1/chat/completions",
        "https://api.free.fastapi.pro/chat/completions"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": "Hello, this is a test."}
        ],
        "max_tokens": 50
    }
    
    for endpoint in endpoints_to_test:
        print(f"\n--- 测试 endpoint: {endpoint} ---")
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS!")
                print(f"返回内容: {result.get('choices', [{}])[0].get('message', {}).get('content', '')}")
                return endpoint, True
            else:
                print(f"FAILED: {response.status_code}")
                print(f"错误信息: {response.text}")
                
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
    
    return None, False

def test_different_keys():
    """测试不同的API Key格式"""
    base_url = "https://api.free.fastapi.pro/v1"
    
    # 可能的API Key
    test_keys = [
        "sk-FastAPI1ZMbDl0KBg0KFp5G0EON1pGNSR0O5xMuuU8wa1ndq",  # 原始提供的key
        os.getenv("OPENAI_API_KEY"),  # 环境变量中的key
    ]
    
    print("\n=== 测试不同API Key ===")
    
    for i, key in enumerate(test_keys):
        if not key:
            continue
            
        print(f"\n--- 测试 Key #{i+1}: {key[:20]}... ---")
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=30)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("SUCCESS! 该Key有效!")
                return key
            else:
                print(f"FAILED Key无效: {response.text}")
                
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
    
    return None

if __name__ == "__main__":
    # 测试API endpoint
    working_endpoint, success = test_api()
    
    if not success:
        # 如果endpoint都失败，测试不同的key
        working_key = test_different_keys()
        if working_key:
            print(f"\nSUCCESS! 找到有效的API Key: {working_key[:20]}...")
        else:
            print("\nFAILED! 所有测试都失败了")
    else:
        print(f"\nSUCCESS! 找到可用的endpoint: {working_endpoint}")