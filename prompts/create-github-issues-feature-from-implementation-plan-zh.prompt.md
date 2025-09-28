```markdown
---
mode: "agent"
description: "使用 feature_request.yml 或 chore_request.yml 模板从实施计划阶段创建 GitHub Issues。"
tools: ["codebase", "search", "github", "create_issue", "search_issues", "update_issue"]
---

# 从实施计划创建 GitHub Issue

为 `${file}` 处的实施计划创建 GitHub Issues。

## 流程

1. 分析计划文件以识别阶段
2. 使用 `search_issues` 检查现有问题
3. 每个阶段使用 `create_issue` 创建新问题或使用 `update_issue` 更新现有问题
4. 使用 `feature_request.yml` 或 `chore_request.yml` 模板（回退到默认值）

## 要求

- 每个实施阶段一个问题
- 清晰、结构化的标题和描述
- 仅包括计划要求的更改
- 创建前与现有问题进行验证

## 问题内容

- 标题：实施计划中的阶段名称
- 描述：阶段详细信息、要求和上下文
- 标签：适合问题类型（功能/琐事）
```
