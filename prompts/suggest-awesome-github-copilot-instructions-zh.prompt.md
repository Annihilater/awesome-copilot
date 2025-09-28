---
mode: "agent"
description: "结合当前仓库上下文与聊天记录，从 awesome-copilot 仓库中推荐相关的 GitHub Copilot 指令文件，并避免与本仓库现有指令重复。"
tools: ["edit", "search", "runCommands", "runTasks", "think", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos", "search"]
---
# 推荐 Awesome GitHub Copilot 指令

分析当前仓库上下文，从 [GitHub awesome-copilot 仓库](https://github.com/github/awesome-copilot/blob/main/README.instructions.md) 中推荐尚未在本仓库提供的 copilot-instruction 文件。

## 流程

1. **获取可用指令**：使用 `#fetch` 工具，从 [README.instructions.md](https://github.com/github/awesome-copilot/blob/main/README.instructions.md) 抽取指令列表与描述。
2. **扫描本地指令**：发现 `.github/instructions/` 目录下的现有指令文件。
3. **提取描述**：读取本地指令的 front matter，获得描述与 `applyTo` 模式。
4. **分析上下文**：审阅聊天记录、仓库文件与当前项目需求。
5. **比较现状**：检查本仓库已具备的指令。
6. **匹配相关性**：将可用指令与识别出的需求模式对比。
7. **展示选项**：输出相关指令、描述、推荐理由与可用性状态。
8. **验证价值**：确认推荐指令能带来新增能力，而非重复。
9. **输出结果**：提供包含推荐项、描述、链接与本地相似指令的表格。
   **等待** 用户请求后再安装指定指令。未获指示不得安装。
10. **下载资产**：用户请求后，将对应指令下载到 `.github/instructions/`，不得修改文件内容。使用 `#todos` 跟踪进度，优先 `#fetch`，必要时以 `curl` 保障下载成功。

## 上下文分析标准

🔍 **仓库模式**：
- 使用的语言（.cs、.js、.py、.ts 等）
- 框架线索（ASP.NET、React、Azure、Next.js 等）
- 项目类型（Web 应用、API、库、工具）
- 开发流程需求（测试、CI/CD、部署）

🗨️ **聊天记录语境**：
- 近期讨论与痛点
- 技术相关问题
- 编码规范讨论
- 开发流程要求

## 输出格式

以表格对比 awesome-copilot 指令与本地指令：

| Awesome-Copilot Instruction | Description | Already Installed | Similar Local Instruction | Suggestion Rationale |
|------------------------------|-------------|-------------------|---------------------------|---------------------|
| [blazor.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/blazor.instructions.md) | Blazor development guidelines | ❌ No | blazor.instructions.md | Already covered by existing Blazor instructions |
| [reactjs.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/reactjs.instructions.md) | ReactJS development standards | ❌ No | None | Would enhance React development with established patterns |
| [java.instructions.md](https://github.com/github/awesome-copilot/blob/main/instructions/java.instructions.md) | Java development best practices | ❌ No | None | Could improve Java code quality and consistency |

## 本地指令发现流程

1. 列出 `instructions/` 目录下所有 `*.instructions.md`。
2. 读取 front matter 获取 `description` 与 `applyTo`。
3. 构建现有指令清单，记录适用范围。
4. 推荐时参考该清单避免重复。

## 文件结构要求

GitHub 文档建议：
- **仓库级指令**：`.github/copilot-instructions.md`（作用于整个仓库）
- **路径特定指令**：`.github/instructions/NAME.instructions.md`（通过 `applyTo` 控制范围）
- **公共指令**：`instructions/NAME.instructions.md`（用于分享分发）

## Front Matter 结构

awesome-copilot 指令使用以下 front matter：
```markdown
---
description: 'Brief description of what this instruction provides'
applyTo: '**/*.js,**/*.ts' # Optional: glob patterns for file matching
---
```

## 要求

- 使用 `githubRepo` 获取 awesome-copilot 仓库内容。
- 扫描本地 `instructions/` 目录。
- 读取本地指令 front matter，提取描述与 `applyTo`。
- 与本地指令对比，避免重复推荐。
- 聚焦现有指令库的空白。
- 确认推荐指令符合仓库目标与标准。
- 为每个建议提供明确理由。
- 提供 awesome-copilot 指令与相似本地指令的链接。
- 考量技术栈兼容性与项目需求。
- 除表格与分析外，不输出额外内容。

## 图标参考

- ✅ 已安装
- ❌ 未安装

