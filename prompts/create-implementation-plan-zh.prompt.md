````markdown
---
mode: "agent"
description: "为新功能、重构现有代码或升级包、设计、架构或基础设施创建新的实施计划文件。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---

# 创建实施计划

## 主要指令

你的目标是为 `${input:PlanPurpose}` 创建一个新的实施计划文件。你的输出必须是机器可读的、确定性的，并且结构化以便其他 AI 系统或人类自主执行。

## 执行上下文

此提示专为 AI-to-AI 通信和自动化处理而设计。所有指令必须按字面意思解释并系统地执行，无需人工解释或澄清。

## 核心要求

- 生成可由 AI 代理或人类完全执行的实施计划
- 使用确定性语言，零歧义
- 将所有内容结构化为可自动解析和执行
- 确保完全自包含，无需外部依赖即可理解

## 计划结构要求

计划必须由包含可执行任务的离散、原子阶段组成。每个阶段必须能够由 AI 代理或人类独立处理，除非明确声明，否则没有跨阶段依赖关系。

## 阶段架构

- 每个阶段必须有可衡量的完成标准
- 除非指定了依赖关系，否则阶段内的任务必须可以并行执行
- 所有任务描述必须包括特定的文件路径、函数名称和确切的实施细节
- 任何任务都不应需要人工解释或决策

## AI 优化的实施标准

- 使用明确、无歧义的语言，无需任何解释
- 将所有内容结构化为机器可解析的格式（表格、列表、结构化数据）
- 在适用的情况下包括特定的文件路径、行号和确切的代码引用
- 明确定义所有变量、常量和配置值
- 在每个任务描述中提供完整的上下文
- 对所有标识符使用标准化的前缀（REQ-、TASK- 等）
- 包括可以自动验证的验证标准

## 输出文件规范

- 将实施计划文件保存在 `/plan/` 目录中
- 使用命名约定：`[purpose]-[component]-[version].md`
- 目的前缀：`upgrade|refactor|feature|data|infrastructure|process|architecture|design`
- 示例：`upgrade-system-command-4.md`、`feature-auth-module-1.md`
- 文件必须是有效的 Markdown，并具有正确的前置内容结构

## 强制模板结构

所有实施计划必须严格遵守以下模板。每个部分都是必需的，并且必须填充具体、可操作的内容。AI 代理必须在执行前验证模板合规性。

## 模板验证规则

- 所有前置内容字段必须存在且格式正确
- 所有节标题必须完全匹配（区分大小写）
- 所有标识符前缀必须遵循指定的格式
- 表格必须包括所有必需的列
- 最终输出中不得保留任何占位符文本

## 状态

实施计划的状态必须在前置内容中明确定义，并且必须反映计划的当前状态。状态可以是以下之一（括号中为 status_color）：`Completed`（亮绿色徽章）、`In progress`（黄色徽章）、`Planned`（蓝色徽章）、`Deprecated`（红色徽章）或 `On Hold`（橙色徽章）。它也应在引言部分显示为徽章。

```md
---
goal: [描述包实施计划目标的简明标题]
version: [可选：例如，1.0，日期]
date_created: [YYYY-MM-DD]
last_updated: [可选：YYYY-MM-DD]
owner: [可选：负责此规范的团队/个人]
status: 'Completed'|'In progress'|'Planned'|'Deprecated'|'On Hold'
tags: [可选：相关标签或类别的列表，例如，`feature`、`upgrade`、`chore`、`architecture`、`migration`、`bug` 等]
---

# 引言

![状态：<status>](https://img.shields.io/badge/status-<status>-<status_color>)

[对计划及其旨在实现的目标的简短介绍。]

## 1. 需求和约束

[明确列出影响计划并约束其实施方式的所有需求和约束。使用项目符号或表格以求清晰。]

- **REQ-001**：需求 1
- **SEC-001**：安全需求 1
- **[3 个字母]-001**：其他需求 1
- **CON-001**：约束 1
- **GUD-001**：指南 1
- **PAT-001**：要遵循的模式 1

## 2. 实施步骤

### 实施阶段 1

- GOAL-001：[描述此阶段的目标，例如，“实施功能 X”、“重构模块 Y”等]
```
````
