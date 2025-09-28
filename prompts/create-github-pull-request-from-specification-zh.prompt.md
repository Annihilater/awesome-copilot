```markdown
---
mode: "agent"
description: "使用 pull_request_template.md 模板从规范文件创建功能请求的 GitHub 拉取请求。"
tools: ["codebase", "search", "github", "create_pull_request", "update_pull_request", "get_pull_request_diff"]
---

# 从规范创建 GitHub 拉取请求

为 `${workspaceFolder}/.github/pull_request_template.md` 处的规范创建 GitHub 拉取请求。

## 流程

1. 使用“search”工具分析“${workspaceFolder}/.github/pull_request_template.md”中的规范文件模板以提取需求。
2. 使用“create_pull_request”工具在 `${input:targetBranch}` 上创建拉取请求草稿模板，并确保当前分支没有任何拉取请求存在 `get_pull_request`。如果有，则继续执行第 4 步，并跳过第 3 步。
3. 使用“get_pull_request_diff”工具获取拉取请求中的更改，以分析拉取请求中已更改的信息。
4. 使用“update_pull_request”工具更新上一步中创建的拉取请求正文和标题。合并从第一步中获取的模板信息，以根据需要更新正文和标题。
5. 使用“update_pull_request”工具从草稿切换到准备审查。以更新拉取请求的状态。
6. 使用“get_me”获取创建拉取请求的人员的用户名，并分配给 `update_issue` 工具。以分配拉取请求
7. 将创建的拉取请求的 URL 响应给用户。

## 要求

- 完整规范的单个拉取请求
- 识别规范的清晰标题/pull_request_template.md
- 在 pull_request_template.md 中填写足够的信息
- 创建前与现有拉取请求进行验证
```
