---
mode: "agent"
description: "基于当前仓库上下文与聊天记录，从 awesome-copilot 仓库中推荐相关的自定义 Chat Mode 文件，并避免与本仓库已有模式重复。"
tools: ["edit", "search", "runCommands", "runTasks", "think", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos", "search"]
---

# 推荐 Awesome GitHub Copilot 自定义 Chat Mode

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/README.chatmodes.md) 中推荐尚未在本仓库提供的自定义 Chat Mode。目标文件位于 awesome-copilot 仓库的 [chatmodes](https://github.com/github/awesome-copilot/tree/main/chatmodes) 目录。

## 流程

1. **获取可用 Chat Mode 列表**：从 [README.chatmodes.md](https://github.com/github/awesome-copilot/blob/main/README.chatmodes.md) 抽取 Chat Mode 列表与描述。必须使用 `#fetch` 工具。
2. **扫描本地 Chat Mode**：发现 `.github/chatmodes/` 目录下的已有文件。
3. **提取描述**：读取本地 Chat Mode 文件的 front matter，获得描述信息。
4. **分析上下文**：审阅聊天记录、仓库文件与当前项目需求。
5. **比较现状**：确认本仓库已拥有的 Chat Mode，避免重复推荐。
6. **匹配相关性**：将可用 Chat Mode 与已识别的模式/需求进行比对。
7. **呈现选项**：输出相关 Chat Mode、描述、推荐理由与可用性状态。
8. **校验**：确保推荐的 Chat Mode 能带来新增价值。
9. **输出**：提供结构化表格，包含推荐项、描述、链接、与本地 Chat Mode 的对应关系及推荐理由。
   **等待** 用户请求后再执行安装操作。未获指示时不得安装。
10. **下载资源**：若用户指定安装，自动将对应文件下载至 `.github/chatmodes/`。禁止修改文件内容。使用 `#todos` 跟踪进度；优先使用 `#fetch` 下载，必要时可借助 `#runInTerminal` 的 `curl` 确保成功获取。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的编程语言（.cs、.js、.py 等）
- 框架特征（ASP.NET、React、Azure 等）
- 项目类型（Web 应用、API、库、工具等）
- 文档需求（README、规格说明、ADR 等）

🗨️ **聊天记录语境**：
- 近期讨论与痛点
- 功能请求或实现需求
- 代码审查模式
- 开发流程要求

## 输出格式

以结构化表格呈现 awesome-copilot Chat Mode 与本地 Chat Mode：

| Awesome-Copilot Custom Chat Mode | Description | Already Installed | Similar Local Custom Chat Mode | Suggestion Rationale |
|---------------------------|-------------|-------------------|-------------------------|---------------------|
| [code-reviewer.chatmode.md](https://github.com/github/awesome-copilot/blob/main/chatmodes/code-reviewer.chatmode.md) | Specialized code review custom chat mode | ❌ No | None | Would enhance development workflow with dedicated code review assistance |
| [architect.chatmode.md](https://github.com/github/awesome-copilot/blob/main/chatmodes/architect.chatmode.md) | Software architecture guidance | ✅ Yes | azure_principal_architect.chatmode.md | Already covered by existing architecture custom chat modes |
| [debugging-expert.chatmode.md](https://github.com/github/awesome-copilot/blob/main/chatmodes/debugging-expert.chatmode.md) | Debug assistance custom chat mode | ❌ No | None | Could improve troubleshooting efficiency for development team |

## 本地 Chat Mode 发现流程

1. 列出 `.github/chatmodes/` 目录下所有 `*.chatmode.md` 文件。
2. 读取每个文件的 front matter，提取 `description`。
3. 构建本地 Chat Mode 清单。
4. 在推荐时使用该清单避免重复。

## 要求

- 使用 `githubRepo` 工具访问 awesome-copilot 仓库的 chatmodes 目录。
- 扫描本地文件系统，了解现有 Chat Mode。
- 提取本地 Chat Mode 的 front matter 描述。
- 与本仓库现状对比，避免重复推荐。
- 聚焦于当前 Chat Mode 库的空白领域。
- 推荐项需与仓库目标与规范相契合。
- 为每个建议提供清晰理由。
- 同时提供 awesome-copilot Chat Mode 链接与相似本地 Chat Mode。
- 除表格与分析内容外，不要输出额外信息。

## 图标参考

- ✅ 已在仓库安装
- ❌ 尚未安装

