# 在其他项目中使用 Awesome Copilot 资源的完整指南

本文档将详细介绍如何在您的新项目中使用 Awesome GitHub Copilot 仓库中的各种资源，包括 Collections、Prompts、Instructions 和 Chat Modes。

## 目录

1. [快速开始](#快速开始)
2. [理解不同类型的资源](#理解不同类型的资源)
3. [在 VSCode 中使用资源的方法](#在-vscode-中使用资源的方法)
4. [针对特定项目的最佳实践](#针对特定项目的最佳实践)
5. [常见场景示例](#常见场景示例)

## 快速开始

### 前置要求

1. **安装 GitHub Copilot**：确保您的 VSCode 中已安装 GitHub Copilot 扩展
2. **激活订阅**：确保您有有效的 GitHub Copilot 订阅
3. **克隆仓库**（可选）：克隆 Awesome Copilot 仓库到本地以便查阅
   ```bash
   git clone https://github.com/github/awesome-copilot.git
   ```

### 快速使用方法

1. **使用 MCP Server（推荐）**
   - 在 VSCode 中点击安装按钮：[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/mcp/vscode)
   - 这将自动配置 MCP Server，让您可以直接搜索和安装资源

2. **手动复制方法**
   - 浏览资源文件，复制您需要的内容到项目中

## 理解不同类型的资源

### 1. Prompts（提示词）
- **用途**：用于生成特定代码、文档或解决特定问题的任务提示
- **文件格式**：`.prompt.md`
- **使用方式**：通过 `/` 命令在 Copilot Chat 中调用
- **示例**：`/awesome-copilot create-readme` 生成项目 README

### 2. Instructions（指令）
- **用途**：提供编码规范和最佳实践，自动应用于特定文件类型
- **文件格式**：`.instructions.md`
- **使用方式**：基于文件模式自动激活（如 `*.py` 文件）
- **示例**：Python 文件自动应用 PEP 8 规范

### 3. Chat Modes（聊天模式）
- **用途**：专业 AI 角色，提供特定领域的专家级帮助
- **文件格式**：`.chatmode.md`
- **使用方式**：激活特定模式获得专业指导
- **示例**：DBA 模式、架构师模式、安全专家模式

### 4. Collections（集合）
- **用途**：相关资源的精选集合，围绕特定主题组织
- **文件格式**：`.collection.yml`
- **使用方式**：一次性导入整个主题相关的所有资源
- **示例**：Azure 开发集合、前端开发集合、测试自动化集合

## 在 VSCode 中使用资源的方法

### 方法 1：项目级配置（推荐用于团队项目）

1. **创建项目配置目录**
   ```bash
   mkdir -p .github/copilot
   ```

2. **复制所需资源**
   将需要的文件从 awesome-copilot 仓库复制到您的项目：
   ```bash
   # 复制特定 instruction
   cp /path/to/awesome-copilot/instructions/python.instructions.md .github/copilot/

   # 复制特定 prompt
   cp /path/to/awesome-copilot/prompts/create-readme.prompt.md .github/copilot/

   # 复制特定 chat mode
   cp /path/to/awesome-copilot/chatmodes/principal-software-engineer.chatmode.md .github/copilot/
   ```

3. **自定义配置**
   根据项目需求修改复制的文件内容

### 方法 2：全局配置（推荐用于个人使用）

1. **找到 VSCode 配置目录**
   - Windows: `%APPDATA%\Code\User\globalStorage\GitHub.copilot-chat`
   - macOS: `~/Library/Application Support/Code/User/globalStorage/GitHub.copilot-chat`
   - Linux: `~/.config/Code/User/globalStorage/GitHub.copilot-chat`

2. **创建资源文件**
   在上述目录中创建您需要的 `.md` 文件

### 方法 3：使用 MCP Server 动态加载

1. **配置 MCP Server**
   ```json
   {
     "servers": {
       "awesome-copilot": {
         "type": "stdio",
         "command": "docker",
         "args": [
           "run", "-i", "--rm",
           "ghcr.io/microsoft/mcp-dotnet-samples/awesome-copilot:latest"
         ]
       }
     }
   }
   ```

2. **搜索并安装资源**
   使用命令搜索所需资源并动态加载

## 针对特定项目的最佳实践

### Web 前端项目

**推荐使用的集合**：
- `frontend-web-dev.collection.yml` - 前端开发集合

**关键资源**：
```yaml
# 必备 Instructions
- reactjs.instructions.md      # React 最佳实践
- nextjs.instructions.md        # Next.js 规范
- tailwind.instructions.md      # Tailwind CSS 指南

# 有用的 Prompts
- create-component.prompt.md    # 生成组件
- optimize-performance.prompt.md # 性能优化

# Chat Modes
- expert-react-frontend-engineer.chatmode.md  # React 专家模式
```

### Python 后端项目

**推荐使用的集合**：
- `database-data-management.collection.yml` - 数据库管理

**关键资源**：
```yaml
# Instructions
- python.instructions.md         # Python 规范
- fastapi.instructions.md        # FastAPI 最佳实践

# Prompts
- create-api-endpoint.prompt.md  # 创建 API 端点
- write-tests.prompt.md          # 生成测试

# Chat Modes
- principal-software-engineer.chatmode.md  # 架构设计指导
```

### Azure 云项目

**推荐使用的集合**：
- `azure-cloud-development.collection.yml` - Azure 开发集合

**关键资源**：
```yaml
# Instructions
- bicep-code-best-practices.instructions.md
- terraform-azure.instructions.md

# Prompts
- az-cost-optimize.prompt.md

# Chat Modes
- azure-principal-architect.chatmode.md
```

## 常见场景示例

### 场景 1：新建 React + TypeScript 项目

```bash
# 1. 创建项目配置目录
mkdir -p .github/copilot

# 2. 创建项目专用的 instruction 文件
cat > .github/copilot/project.instructions.md << EOF
---
description: '项目特定的编码规范'
applyTo: '**/*.{ts,tsx,js,jsx}'
---

# 项目编码规范

- 使用 React Hooks 而非 Class 组件
- 所有组件使用 TypeScript 强类型
- 使用 React Query 进行数据获取
- 遵循 Atomic Design 原则组织组件
- 每个组件必须有对应的测试文件
EOF

# 3. 复制需要的 prompts
cp /path/to/awesome-copilot/prompts/create-component.prompt.md .github/copilot/
```

### 场景 2：优化现有项目代码质量

1. **导入代码质量相关资源**：
   ```bash
   # 复制安全和质量相关的 instructions
   cp awesome-copilot/collections/security-best-practices.collection.yml .github/copilot/
   ```

2. **激活代码审查模式**：
   在 Copilot Chat 中使用：
   - Chat Mode: `code-reviewer`
   - 命令：`审查当前文件的代码质量`

### 场景 3：快速原型开发

1. **使用快速开发 prompts**：
   ```
   /awesome-copilot scaffold-crud-api
   /awesome-copilot create-docker-compose
   ```

2. **激活快速开发模式**：
   使用 `rapid-prototyper` chat mode

## 进阶技巧

### 1. 创建项目专用的 Collection

创建 `.github/copilot/my-project.collection.yml`：

```yaml
id: my-project-collection
name: 我的项目专用集合
description: 针对当前项目优化的资源集合
tags: [custom, project-specific]
items:
  - path: instructions/python.instructions.md
    kind: instruction
  - path: prompts/create-api.prompt.md
    kind: prompt
  - path: chatmodes/dba.chatmode.md
    kind: chat-mode
```

### 2. 条件激活 Instructions

使用 `applyTo` 字段精确控制应用范围：

```yaml
---
applyTo: 'src/api/**/*.py'  # 仅应用于 API 目录的 Python 文件
---
```

### 3. 组合使用多个 Chat Modes

在复杂任务中，可以切换不同的专家模式：
1. 使用 `architect` 模式设计架构
2. 切换到 `implementation` 模式编码
3. 使用 `test-expert` 模式编写测试

## 维护和更新

### 定期更新资源

```bash
# 更新 awesome-copilot 仓库
cd awesome-copilot && git pull

# 检查并更新项目中使用的资源
diff -u .github/copilot/python.instructions.md awesome-copilot/instructions/python.instructions.md
```

### 贡献自定义资源

如果您创建了有用的自定义资源，考虑贡献回 awesome-copilot 仓库：

1. Fork 仓库
2. 添加您的资源文件
3. 提交 Pull Request

## 故障排除

### 常见问题

1. **资源未生效**
   - 检查文件名格式是否正确（`.instructions.md`, `.prompt.md` 等）
   - 确认文件位置正确
   - 重启 VSCode

2. **Prompt 无法使用**
   - 确认使用正确的命令格式：`/awesome-copilot <prompt-name>`
   - 检查 prompt 文件的 frontmatter 配置

3. **Instructions 未自动应用**
   - 验证 `applyTo` 模式匹配当前文件
   - 检查 YAML frontmatter 格式

## 总结

Awesome Copilot 资源库提供了丰富的工具来增强您的开发体验。关键是：

1. **选择合适的资源**：根据项目类型选择相关的 collections
2. **自定义配置**：根据团队规范调整 instructions
3. **持续优化**：随着项目发展，不断优化和添加新的资源
4. **团队协作**：将配置提交到版本控制，确保团队一致性

通过合理使用这些资源，您可以显著提高开发效率和代码质量。