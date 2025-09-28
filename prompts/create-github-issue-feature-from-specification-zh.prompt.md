```markdown
---
mode: "agent"
description: "使用 feature_request.yml 模板从规范文件创建功能请求的 GitHub Issue。"
tools: ["codebase", "search", "github", "create_issue", "search_issues", "update_issue"]
---

# 从规范创建 GitHub Issue

为 `${file}` 处的规范创建 GitHub Issue。

## 流程

1. 分析规范文件以提取需求
2. 使用 `search_issues` 检查现有问题
3. 使用 `create_issue` 创建新问题或使用 `update_issue` 更新现有问题
4. 使用 `feature_request.yml` 模板（回退到默认值）

## 要求

- 完整规范的单个问题
- 识别规范的清晰标题
- 仅包括规范要求的更改
- 创建前与现有问题进行验证

## 问题内容

- 标题：规范中的功能名称
- 描述：问题陈述、建议的解决方案和上下文
- 标签：feature、enhancement（视情况而定）
```
