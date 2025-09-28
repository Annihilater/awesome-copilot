---
mode: "agent"
tools: ["githubRepo", "github", "get_issue", "get_issue_comments", "get_me", "list_issues"]
description: "列出当前仓库中分配给我的议题。"
---

搜索当前仓库（使用 #githubRepo 获取仓库信息），并利用 #list_issues 列出所有分配给我的 issue。

根据 issue 的创建时间、评论数量以及状态（开放/已关闭）提出我应该优先处理的议题建议。

