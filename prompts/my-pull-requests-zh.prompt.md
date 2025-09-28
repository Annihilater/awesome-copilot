---
mode: "agent"
tools: ["githubRepo", "github", "get_me", "get_pull_request", "get_pull_request_comments", "get_pull_request_diff", "get_pull_request_files", "get_pull_request_reviews", "get_pull_request_status", "list_pull_requests", "request_copilot_review"]
description: "列出当前仓库中属于我的拉取请求。"
---

搜索当前仓库（使用 #githubRepo 获取仓库信息），并利用 #list_pull_requests 列出所有分配给我的拉取请求。

描述每个 PR 的目的与详情。

如果某个 PR 正在等待他人审核，请在回答中突出提示。

如果 PR 中存在检查失败，说明失败原因并给出可能的修复建议。

如果该 PR 未使用 Copilot 进行过代码审查，请提供使用 #request_copilot_review 发起审查的选项。

