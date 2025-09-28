---
mode: "agent"
description: "结合当前仓库上下文与聊天记录，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 提示词，并避免与本仓库现有提示重复。"
tools: ["edit", "search", "runCommands", "runTasks", "think", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos", "search"]
---
# 推荐 Awesome GitHub Copilot 提示词

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/README.prompts.md) 中推荐尚未在本仓库提供的 prompt 文件。

## 流程

1. **获取可用提示词**：使用 `#fetch` 工具，从 [README.prompts.md](https://github.com/github/awesome-copilot/blob/main/README.prompts.md) 抽取提示列表与描述。
2. **扫描本地提示词**：发现 `.github/prompts/` 目录中的现有 prompt 文件。
3. **提取描述**：读取本地 prompt 的 front matter，获取描述信息。
4. **分析上下文**：审阅聊天记录、仓库文件与当前项目需求。
5. **比较现状**：检查本仓库已有提示词。
6. **匹配相关性**：将可用提示词与识别出的需求模式对比。
7. **展示选项**：输出相关提示词、描述、推荐理由与可用性状态。
8. **验证价值**：确认推荐提示词能提供新增能力。
9. **输出结果**：提供包含推荐项、描述、链接与本地相似提示词的表格。
   **等待** 用户请求后再安装指定提示词。未获指示不得安装。
10. **下载资产**：用户请求后，将对应提示词下载到 `.github/prompts/`，不得修改文件内容。使用 `#todos` 跟踪进度，优先 `#fetch`，必要时以 `curl` 保障下载成功。

## 上下文分析标准

🔍 **仓库模式**：
- 使用语言（.cs、.js、.py 等）
- 框架线索（ASP.NET、React、Azure 等）
- 项目类型（Web 应用、API、库、工具）
- 文档需求（README、规格、ADR）

🗨️ **聊天记录语境**：
- 近期讨论与痛点
- 功能需求或实现请求
- 代码审查模式
- 开发流程需求

## 输出格式

以表格对比 awesome-copilot 提示词与本地提示词：

| Awesome-Copilot Prompt | Description | Already Installed | Similar Local Prompt | Suggestion Rationale |
|-------------------------|-------------|-------------------|---------------------|---------------------|
| [code-review.md](https://github.com/github/awesome-copilot/blob/main/prompts/code-review.md) | Automated code review prompts | ❌ No | None | Would enhance development workflow with standardized code review processes |
| [documentation.md](https://github.com/github/awesome-copilot/blob/main/prompts/documentation.md) | Generate project documentation | ✅ Yes | create_oo_component_documentation.prompt.md | Already covered by existing documentation prompts |
| [debugging.md](https://github.com/github/awesome-copilot/blob/main/prompts/debugging.md) | Debug assistance prompts | ❌ No | None | Could improve troubleshooting efficiency for development team |

## 本地提示词发现流程

1. 列出 `.github/prompts/` 目录下所有 `*.prompt.md`。
2. 读取 front matter 获取 `description`。
3. 构建现有提示词清单。
4. 推荐时参考该清单避免重复。

## 要求

- 使用 `githubRepo` 获取 awesome-copilot 仓库内容。
- 扫描本地 `.github/prompts/` 目录。
- 读取本地 prompt front matter，提取描述。
- 与本地提示词对比，避免重复推荐。
- 聚焦提示库的空白领域。
- 确认推荐提示符合仓库目标与标准。
- 为每个建议提供明确理由。
- 提供 awesome-copilot 提示与相似本地提示链接。
- 除表格与分析外，不输出额外内容。

## 图标参考

- ✅ 已安装
- ❌ 未安装

