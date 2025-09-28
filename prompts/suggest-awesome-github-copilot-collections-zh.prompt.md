---
mode: "agent"
description: "结合当前仓库上下文与聊天记录，从 awesome-copilot 仓库中推荐合适的 GitHub Copilot 集合，并支持自动下载与安装集合资产。"
tools: ["edit", "search", "runCommands", "runTasks", "think", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos", "search"]
---
# 推荐 Awesome GitHub Copilot 集合

分析当前仓库上下文，推荐来自 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/README.collections.md) 的相关集合，以提升本仓库的开发效率。

## 流程

1. **获取集合列表**：使用 `#fetch` 工具，从 [README.collections.md](https://github.com/github/awesome-copilot/blob/main/README.collections.md) 抽取集合及描述。
2. **扫描本地资产**：识别 `prompts/`、`instructions/`、`chatmodes/` 目录中的现有文件。
3. **提取本地描述**：读取本地资产的 front matter，了解已有能力。
4. **分析仓库上下文**：审阅聊天记录、仓库文件、使用语言、框架与当前需求。
5. **匹配集合相关性**：将集合内容与已识别的模式和需求对比。
6. **检查资产重叠**：分析集合中的各项资产，避免与本地重复。
7. **展示集合选项**：输出推荐集合、描述、项目数量与推荐理由。
8. **提供使用指导**：说明集合如何提升开发流程。
   **等待** 用户明确请求后再执行安装。未获指示不得安装。
9. **下载资产**：若用户确认安装集合，自动下载并安装集合中的各类资产（prompts、instructions、chatmodes），保持文件内容原样。优先使用 `#fetch`，必要时配合 `#runInTerminal` 的 `curl` 获取内容。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs、.js、.py、.ts、.bicep、.tf 等）
- 框架线索（ASP.NET、React、Azure、Next.js、Angular 等）
- 项目类型（Web 应用、API、库、工具、基础设施）
- 文档需求（README、规格文档、ADR、架构决策）
- 开发流程信号（CI/CD、测试、部署）

🗨️ **聊天记录语境**：
- 近期讨论与痛点
- 功能需求或实现难点
- 代码审查模式与质量问题
- 开发流程需求与挑战
- 技术栈与架构决策

## 输出格式

以结构化表格呈现推荐集合及其价值：

### 集合推荐

| Collection Name | Description | Items | Asset Overlap | Suggestion Rationale |
|-----------------|-------------|-------|---------------|---------------------|
| [Azure & Cloud Development](https://github.com/github/awesome-copilot/blob/main/collections/azure-cloud-development.md) | Comprehensive Azure cloud development tools including Infrastructure as Code, serverless functions, architecture patterns, and cost optimization | 15 items | 3 similar | Would enhance Azure development workflow with Bicep, Terraform, and cost optimization tools |
| [C# .NET Development](https://github.com/github/awesome-copilot/blob/main/collections/csharp-dotnet-development.md) | Essential prompts, instructions, and chat modes for C# and .NET development including testing, documentation, and best practices | 7 items | 2 similar | Already covered by existing .NET-related assets but includes advanced testing patterns |
| [Testing & Test Automation](https://github.com/github/awesome-copilot/blob/main/collections/testing-automation.md) | Comprehensive collection for writing tests, test automation, and test-driven development | 11 items | 1 similar | Could significantly improve testing practices with TDD guidance and automation tools |

### 推荐集合资产分析

**Azure & Cloud Development 集合分析：**
- ✅ **新增资产 (12)**：Azure 成本优化、Bicep 计划模式、AVM 模块、Logic Apps 专家模式
- ⚠️ **类似资产 (3)**：Azure DevOps 流水线（类似现有 CI/CD）、Terraform（基础内容重叠）、容器化（已有 Docker 基础）
- 🎯 **高价值**：成本优化、基础设施即代码、Azure 专属架构指导

**安装预览：**
- 将安装至 `prompts/`：4 个 Azure 专属提示词
- 安装至 `instructions/`：6 个基础设施与 DevOps 最佳实践
- 安装至 `chatmodes/`：5 个 Azure 专家模式

## 本地资产发现流程

1. **扫描资产目录**：
   - 列出 `prompts/` 下所有 `*.prompt.md`
   - 列出 `instructions/` 下所有 `*.instructions.md`
   - 列出 `chatmodes/` 下所有 `*.chatmode.md`

2. **提取资产元数据**：读取每个文件的 front matter，包括：
   - `description`：核心用途
   - `tools`：所需工具与能力
   - `mode`：运行模式（针对 prompts）
   - `model`：模型需求（针对 chatmodes）

3. **构建资产清单**：按以下维度整理现有能力：
   - **技术焦点**：语言、框架、平台
   - **工作流类型**：开发、测试、部署、文档、规划
   - **专业程度**：通用 vs 专家模式

4. **识别覆盖空白**：对比仓库技术栈、聊天记录体现的需求，以及项目类型对应的行业最佳实践，找出缺失领域（如安全、性能、架构等）。

## 集合资产下载流程

用户确认安装集合后：

1. **获取集合清单**：下载 awesome-copilot 仓库中的集合 YAML。
2. **下载单个资产**：对集合中的每个条目：
   - 从 GitHub 获取原始文件内容
   - 校验文件格式与 front matter
   - 检查命名是否符合约定
3. **安装至对应目录**：
   - `*.prompt.md` → `prompts/`
   - `*.instructions.md` → `instructions/`
   - `*.chatmode.md` → `chatmodes/`
4. **避免重复**：遇到与本地高度相似的文件应跳过。
5. **输出安装摘要**：提供安装结果与使用说明。

## 要求

- 使用 `fetch` 获取集合数据。
- 使用 `githubRepo` 获取单个资产内容。
- 扫描本地 `prompts/`、`instructions/`、`chatmodes/`。
- 读取本地资产 front matter，提取描述与能力。
- 将集合与仓库上下文对比，挑选相关集合。
- 重点填补能力空白，避免重复。
- 推荐集合需符合项目技术栈与开发需求。
- 为每个推荐提供明确收益说明。
- 支持自动下载并安装集合资产。
- 确保下载文件遵循命名与格式标准。
- 提供使用指导，说明集合如何增强工作流。
- 附上集合及其资产的链接。

## 集合安装流程

1. **用户确认集合**：用户选择要安装的集合。
2. **获取集合清单**：下载集合 YAML。
3. **资产下载循环**：对每个资产：
   - 下载原始内容
   - 校验格式
   - 检查是否与本地高度重叠
   - 安装至对应目录
4. **安装总结**：报告安装结果并附使用说明。
5. **工作流增强指南**：解释集合如何提升开发能力。

## 安装后指导

安装集合后需提供：
- **资产概览**：列出新安装的 prompts、instructions、chatmodes。
- **使用示例**：说明如何激活与使用。
- **流程整合**：最佳实践与流程建议。
- **定制建议**：如何针对项目需求进行调整。
- **相关集合**：推荐可配套的其他集合。

## 图标说明

- ✅ 推荐安装的集合
- ⚠️ 存在部分重叠但仍有价值
- ❌ 不建议安装（重叠严重或无关）
- 🎯 填补关键能力空白的集合
- 📁 集合部分安装（部分资产因重复被跳过）
- 🔄 需按仓库需求定制的集合

