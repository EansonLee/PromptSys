import requests
import json

# 测试API调用
url = "http://localhost:8000/generate-prompt"
data = {
    "theme": "WiFi探索测试",
    "app_name": "WiFi联通",
    "variant_folder": "variant_137158",
    "ui_color": "蓝色科技感",
    "reference_file": "HomeFragment"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("\n=== 角色 ===")
        print(result.get('role', 'Empty'))
        print("\n=== 功能输出 ===")
        function_output = result.get('function_output', 'Empty')
        try:
            # 检查是否包含#符号
            has_hash = '#' in function_output
            print(f"包含#符号: {has_hash}")
            
            # 检查开头字符
            if function_output:
                first_chars = function_output[:20]
                try:
                    print(f"开头20字符: {first_chars.encode('utf-8').decode('utf-8')[:20]}")
                except:
                    print(f"开头20字符(repr): {repr(first_chars)}")
                
            # 检查是否包含示例展示部分
            has_example = '示例展示' in function_output
            print(f"包含示例展示: {has_example}")
            
            if has_example:
                # 提取示例展示部分
                import re
                example_part = re.search(r'示例展示.*?(?=---|\n\n|\Z)', function_output, re.DOTALL)
                if example_part:
                    example_text = example_part.group(0)[:200]
                    print(f"示例展示部分前200字符: {repr(example_text)}")
                    
        except Exception as e:
            print(f"处理功能输出时出错: {e}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")