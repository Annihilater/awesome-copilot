```markdown
---
mode: "agent"
description: "使用 feature_request.yml 模板从规范文件为未实现的需求创建 GitHub Issues。"
tools: ["codebase", "search", "github", "create_issue", "search_issues", "update_issue"]
---

# 为未满足的规范需求创建 GitHub Issues

为 `${file}` 处规范中未实现的需求创建 GitHub Issues。

## 流程

1. 分析规范文件以提取所有需求
2. 检查每个需求的代码库实现状态
3. 使用 `search_issues` 搜索现有问题以避免重复
4. 每个未实现的需求使用 `create_issue` 创建新问题
5. 使用 `feature_request.yml` 模板（回退到默认值）

## 要求

- 每个未实现的规范需求一个问题
- 清晰的需求 ID 和描述映射
- 包括实现指南和验收标准
- 创建前与现有问题进行验证

## 问题内容

- 标题：需求 ID 和简要描述
- 描述：详细需求、实现方法和上下文
- 标签：feature、enhancement（视情况而定）

## 实现检查

- 在代码库中搜索相关的代码模式
- 检查 `/spec/` 目录中的相关规范文件
- 验证需求是否未部分实现
```
