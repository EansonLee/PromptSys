# 提示词生成系统

基于 LangChain + Next.js 的前后端分离创意提示词生成系统，支持 GPT-4 主线 + SiliconFlow 降级双API架构，具备智能错误处理和高可用性保障。

## 系统架构

```
prompt_sys/
├── frontend/          # Next.js 前端应用
├── backend/           # FastAPI 后端服务
│   ├── main.py        # 主应用入口
│   ├── services/      # 核心服务
│   │   └── prompt_generator.py  # 提示词生成器
│   ├── requirements.txt
│   └── .env.example
├── prompt/            # 原始需求文档
├── start.bat          # Windows启动脚本  
└── start.sh           # Linux/Mac启动脚本
```

## 功能特性

- **前后端分离**：前端负责输入和展示，后端负责生成逻辑
- **创意增强**：专注生成富有创意和创新性的提示词内容
- **模板化输出**：严格遵循指定模板结构
- **智能降级策略**：GPT-4主线 + SiliconFlow Qwen降级，自动处理429/500错误
- **增强创意输出**：详细的功能描述、真实数据示例、emoji视觉元素
- **智能主题匹配**：改进的prompt确保生成内容与用户主题高度契合
- **可编辑固定内容**：前端支持自定义数据采集等固定逻辑
- **详细日志记录**：显示API使用情况、模型调用状态等完整流程
- **环境变量配置**：统一的.env配置管理，支持多环境部署
- **远程部署支持**：配置化CORS，支持远程服务器部署

## 快速开始

### 1. 环境准备

确保已安装：
- Node.js 18+
- Python 3.9+
- OpenAI API Key（主要API）
- SiliconFlow API Key（降级API，可选但推荐）

### 2. 后端启动

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置API密钥和服务器设置

# 启动服务
python main.py
```

后端服务将在 http://localhost:8000 启动

### 3. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
# 创建 .env.local 文件，设置后端API地址

# 启动开发服务器
npm run dev
```

前端应用将在 http://localhost:3000 启动

## 使用说明

1. 在前端页面输入：
   - **APP 名称**：如"清理大师"
   - **主题**：如"智能清理系统，通过AI分析设备使用情况"
   - **变体文件夹**：如"variant_clean123"
   - **UI主色调**：如"蓝色科技感"

2. 点击"生成提示词"按钮

3. 系统将：
   - 优先调用 GPT-4 生成创意内容
   - 遇到429/500错误时自动切换到SiliconFlow
   - 生成详细的功能描述、数据示例和UI规范
   - 按模板格式封装输出
   - 实时返回结果（无数据库存储）

4. 可选择"编辑固定内容"自定义技术要求（第5-13条）

5. 点击"生成最终模板"查看包含固定内容的完整模板

6. 使用"复制到剪贴板"功能获取最终结果

## API 接口

### POST /generate-prompt

生成提示词

**请求体：**
```json
{
  "app_name": "清理大师",
  "theme": "智能清理系统，通过AI分析设备使用情况",
  "variant_folder": "variant_clean123",
  "ui_color": "蓝色科技感"
}
```

**响应：**
```json
{
  "role": "角色描述...",
  "goal": "目标描述...", 
  "function_output": "功能模块详细描述...",
  "ui_requirements": "UI规范要求...",
  "raw_gpt_output": "原始GPT输出",
  "timestamp": "2024-01-01T00:00:00"
}
```

## 配置说明

### 后端配置 (`backend/.env`)

```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.free.fastapi.pro/v1
OPENAI_MODEL=gpt-4

# SiliconFlow 降级API配置
SILICONFLOW_API_KEY=your_siliconflow_api_key
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
SILICONFLOW_MODEL=Qwen/Qwen2.5-32B-Instruct

# LLM 通用配置
LLM_TEMPERATURE=0.7

# 服务器配置
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS 配置 (用逗号分隔多个源)
CORS_ORIGINS=http://localhost:3000,http://192.168.38.226:3000
```

### 前端配置 (`frontend/.env.local`)

```env
# Frontend API 配置
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# 生产环境时需要修改为实际的后端服务器地址
# NEXT_PUBLIC_API_BASE_URL=http://192.168.38.226:8000
```

### 降级策略

系统优先使用GPT-4 API，当遇到以下错误时自动切换到SiliconFlow：
- 429错误（配额不足/速率限制）
- 500错误（服务器内部错误）
- 其他网络连接问题

### 技术栈

**后端：**
- FastAPI - Web框架
- LangChain - AI编排框架
- OpenAI API - GPT-4模型调用
- SiliconFlow API - Qwen降级模型
- Python Logging - 详细日志记录
- Python dotenv - 环境变量管理

**前端：**
- Next.js 15 - React框架 
- React 19 - 用户界面库
- TypeScript 5 - 类型安全
- Tailwind CSS 4 - 样式框架
- 环境变量配置 - 多环境支持

## 开发调试

### API接口文档
- 查看后端API文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 日志查看
后端会输出详细的日志信息，包括：
- 请求接收和参数验证
- 主要API和降级API调用状态
- 模板解析和格式化过程
- 错误处理和降级策略触发
- API切换和使用情况统计

### 一键启动
- Windows: 双击 `start.bat`
- Linux/Mac: 运行 `./start.sh`

### 测试API功能
```bash
# 测试SiliconFlow API连接
cd backend
python test_siliconflow.py

# 测试降级策略
python test_fallback.py
```

## 依赖安装问题

如果遇到依赖版本冲突，请按以下步骤解决：

```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 安装依赖（忽略冲突警告）
cd backend
pip install -r requirements.txt

# 3. 验证安装
python main.py
```

依赖冲突警告不影响核心功能使用。

## 远程部署

### 部署到远程服务器

1. **后端部署**：
   ```bash
   # 修改后端 .env 配置
   BACKEND_HOST=0.0.0.0  # 监听所有接口
   CORS_ORIGINS=http://localhost:3000,http://your-server-ip:3000
   ```

2. **前端部署**：
   ```bash
   # 修改前端 .env.local 配置
   NEXT_PUBLIC_API_BASE_URL=http://your-server-ip:8000
   ```

3. **网络配置**：
   - 确保服务器防火墙开放8000和3000端口
   - 如使用云服务器，配置安全组规则

## 注意事项

1. **API Key**: 建议配置主要API和降级API双重保障
2. **网络连接**: 支持多API源，提高网络连接稳定性
3. **依赖版本**: 可能存在版本冲突警告，但不影响核心功能
4. **固定内容**: 数据采集等固定逻辑由前端管理，支持自定义编辑
5. **创意输出**: 增强的prompt模板，生成更详细和创意的内容
6. **高可用性**: 智能降级策略确保服务连续性
7. **轻量化**: 无数据库依赖，纯生成式服务

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 查看后端日志确认降级策略是否触发
   - 验证网络连接

2. **CORS错误**
   - 确认后端.env中CORS_ORIGINS包含前端地址
   - 检查前端.env.local中API地址配置

3. **生成内容不够创意**
   - 系统已优化prompt模板，生成更详细内容
   - 支持emoji、数据示例和技术规范

4. **降级策略未生效**
   - 运行`python test_fallback.py`测试降级功能
   - 检查SiliconFlow API配置和连接