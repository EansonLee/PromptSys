# AI Agent 自动化操作指南

本指南说明如何使用新增的 AI Agent 自动化功能，包括四个操作按钮的使用方法和跨平台实现。

## 功能概述

系统新增了四个 AI Agent 自动化操作按钮：

1. **打开页面** - 自动打开 Claude CLI
2. **获取仓库** - 获取 GitLab 仓库信息
3. **获取任务** - 将选中的提示词传递给 Claude CLI
4. **执行任务** - 在 Claude CLI 中执行任务

## 使用流程

### 步骤 1: 生成提示词
1. 在前端界面输入 APP 名称、主题等参数
2. 点击"生成提示词"按钮
3. 等待生成多个版本的提示词文档

### 步骤 2: 选择提示词
1. 在生成结果的标签页中，使用单选按钮选择一个最满意的提示词
2. 选中的提示词会显示绿色对勾标记

### 步骤 3: 执行 AI Agent 操作
按照以下顺序使用四个操作按钮：

#### 3.1 打开页面
- **功能**: 自动在系统中打开 Claude CLI
- **支持平台**: Windows 10, macOS, Linux
- **实现**: 
  - Windows: 使用 PowerShell 打开新的 CMD 窗口并启动 Claude CLI
  - macOS: 使用 AppleScript 打开新的 Terminal 窗口
  - Linux: 使用 gnome-terminal 打开终端

#### 3.2 获取仓库 (可选)
- **功能**: 获取 GitLab 仓库信息
- **配置**: 需要在 `.env` 文件中配置 `GITLAB_TOKEN`
- **支持**: GitLab 仓库（公共或私有）

#### 3.3 获取任务
- **功能**: 将选中的提示词写入文件并传递给 Claude CLI
- **前提**: 必须先选择一个提示词
- **生成文件**: 在 `backend/temp_claude/` 目录下生成时间戳命名的文件

#### 3.4 执行任务
- **功能**: 在 Claude CLI 中执行最新的任务文件
- **前提**: 必须先完成"获取任务"步骤
- **实现**: 通过管道将任务文件内容传递给 Claude CLI

## 环境配置

### 前端配置
确保 `frontend/.env.local` 包含正确的后端 API 地址：
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 后端配置
在 `backend/.env` 文件中添加以下配置：

```bash
# 基础配置（必需）
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://192.168.38.226:3000

# GitLab 配置（可选）
GITLAB_TOKEN=your_gitlab_personal_access_token_here
GITLAB_URL=https://gitlab.com

# AI Agent 配置（可选）
CLAUDE_CLI_PATH=/path/to/claude/cli
TEMP_FILES_CLEANUP_HOURS=24
```

## 跨平台实现细节

### Windows 10
- 使用 PowerShell 执行命令
- 自动打开新的 CMD 窗口
- 支持 UTF-8 编码的文件处理

### macOS
- 使用 AppleScript 控制 Terminal 应用
- 通过 Bash 执行 Claude CLI 命令
- 原生支持 UTF-8 编码

### Linux
- 使用 gnome-terminal 打开终端
- 通过 Bash 执行命令
- 完整的 UTF-8 支持

## API 接口说明

### POST /open-claude-cli
打开 Claude CLI
- **请求**: 无参数
- **响应**: `{status: "success", message: "...", process_id: number}`

### POST /get-repository
获取 GitLab 仓库信息
- **请求**: `{repository_url: string}`
- **响应**: `{status: "success", repository_name: string, ...}`

### POST /get-tasks
传递选中的提示词
- **请求**: `{selected_prompt: {role, goal, function_output, ui_requirements}}`
- **响应**: `{status: "success", prompt_file: string, ...}`

### POST /execute-tasks
执行 Claude CLI 任务
- **请求**: 无参数
- **响应**: `{status: "success", process_id: number, ...}`

### POST /cleanup-temp-files
清理临时文件
- **请求**: 无参数
- **响应**: `{status: "success", cleaned_files: string[], ...}`

## 故障排除

### Claude CLI 未安装
确保系统已安装 Claude CLI 并可通过命令行访问：
```bash
# 测试 Claude CLI 是否可用
claude --version
```

### 权限问题
- **Windows**: 确保 PowerShell 执行权限正确
- **macOS**: 可能需要授予 Terminal 自动化权限
- **Linux**: 确保 gnome-terminal 已安装

### 文件编码问题
系统自动处理 UTF-8 编码，如遇到编码问题，检查：
1. 系统区域设置
2. 终端编码配置
3. Claude CLI 版本兼容性

### GitLab API 问题
1. 检查 `GITLAB_TOKEN` 是否有效
2. 确认仓库 URL 格式正确
3. 验证网络连接和防火墙设置

## 开发说明

### 目录结构
```
backend/
├── services/
│   ├── claude_cli_automation.py  # Claude CLI 自动化核心
│   ├── gitlab_integration.py     # GitLab API 集成
│   └── prompt_generator.py       # 原有提示词生成
├── temp_claude/                  # 临时文件存储目录
└── main.py                       # FastAPI 主应用
```

### 扩展开发
要添加新的 AI Agent 功能：

1. 在 `claude_cli_automation.py` 中添加新方法
2. 在 `main.py` 中添加对应的 API 端点
3. 在前端添加新的操作按钮
4. 更新此文档

### 测试建议
1. 在不同平台上测试跨平台功能
2. 测试各种错误情况和异常处理
3. 验证文件编码和路径处理
4. 测试并发操作和资源清理

---

**注意**: 此功能需要系统已正确安装和配置 Claude CLI。如遇问题，请检查 Claude CLI 安装和系统环境配置。