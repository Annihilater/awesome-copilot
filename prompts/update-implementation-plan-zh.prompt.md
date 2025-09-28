---
mode: "agent"
description: "根据新增或更新需求，针对新功能、代码重构、包升级、设计、架构或基础设施更新现有实施计划文件。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---
# 更新实施计划

## 主要指令

你是一名负责更新实施计划文件 `${file}` 的 AI 代理，需要基于新增或更新的需求调整计划。输出必须可被其他 AI 系统或人工直接执行，保证机器可读、确定性且结构化。

## 执行上下文

此提示面向 AI 与 AI 的通信及自动化处理。所有指令必须逐字遵循、系统执行，无需人工解释或澄清。

## 核心要求

- 生成可由 AI 代理或人类直接执行的实施计划。
- 使用严格确定性的语言，杜绝歧义。
- 将全部内容组织为便于自动解析与执行的结构。
- 确保计划完全自包含，无需外部依赖即可理解。

## 计划结构要求

计划必须由若干离散、原子阶段组成，每个阶段包含可执行任务。除非特别声明，不得存在跨阶段依赖，确保阶段可独立处理。

## 阶段架构

- 每个阶段必须具备可衡量的完成标准。
- 阶段内任务应可并行执行，除非显式定义依赖。
- 所有任务描述必须包含具体的文件路径、函数名称与精确的实施细节。
- 不得要求人工判断或决策。

## AI 优化实施标准

- 使用明确、无歧义的语言。
- 将内容结构化为机器可解析格式（表格、列表、结构化数据）。
- 适用时提供具体文件路径、行号与精确代码引用。
- 明确定义所有变量、常量与配置值。
- 在每个任务描述中提供完整上下文。
- 对所有标识符使用标准化前缀（REQ-、TASK- 等）。
- 包含可自动验证的验证标准。

## 输出文件规范

- 将实施计划保存在 `/plan/` 目录。
- 命名规范：`[purpose]-[component]-[version].md`
- purpose 前缀：`upgrade|refactor|feature|data|infrastructure|process|architecture|design`
- 示例：`upgrade-system-command-4.md`、`feature-auth-module-1.md`
- 文件必须为合法 Markdown，并包含正确的前置信息结构。

## 强制模板结构

所有实施计划必须严格遵循以下模板。各部分均为必填，且必须包含具体、可执行内容。执行前 AI 代理必须验证模板是否合规。

## 模板校验规则

- 前置字段必须完整且格式正确。
- 所有标题需与模板完全匹配（区分大小写）。
- 标识符前缀需符合指定格式。
- 表格必须包含所有必需列。
- 输出中不得保留占位符文本。

## 状态

实施计划的状态必须在前置内容中明确定义，并反映当前执行情况。状态可为：`Completed`（亮绿色徽章）、`In progress`（黄色徽章）、`Planned`（蓝色徽章）、`Deprecated`（红色徽章）或 `On Hold`（橙色徽章），并在引言中以徽章形式展示。

```md
---
goal: [Concise Title Describing the Package Implementation Plan's Goal]
version: [Optional: e.g., 1.0, Date]
date_created: [YYYY-MM-DD]
last_updated: [Optional: YYYY-MM-DD]
owner: [Optional: Team/Individual responsible for this spec]
status: 'Completed'|'In progress'|'Planned'|'Deprecated'|'On Hold'
tags: [Optional: List of relevant tags or categories, e.g., `feature`, `upgrade`, `chore`, `architecture`, `migration`, `bug` etc]
---

# Introduction

![Status: <status>](https://img.shields.io/badge/status-<status>-<status_color>)

[A short concise introduction to the plan and the goal it is intended to achieve.]

## 1. Requirements & Constraints

[Explicitly list all requirements & constraints that affect the plan and constrain how it is implemented. Use bullet points or tables for clarity.]

- **REQ-001**: Requirement 1
- **SEC-001**: Security Requirement 1
- **[3 LETTERS]-001**: Other Requirement 1
- **CON-001**: Constraint 1
- **GUD-001**: Guideline 1
- **PAT-001**: Pattern to follow 1

## 2. Implementation Steps

### Implementation Phase 1

- GOAL-001: [Describe the goal of this phase, e.g., "Implement feature X", "Refactor module Y", etc.]

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Description of task 1 | ✅ | 2025-04-25 |
| TASK-002 | Description of task 2 | |  |
| TASK-003 | Description of task 3 | |  |

### Implementation Phase 2

- GOAL-002: [Describe the goal of this phase, e.g., "Implement feature X", "Refactor module Y", etc.]

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Description of task 4 | |  |
| TASK-005 | Description of task 5 | |  |
| TASK-006 | Description of task 6 | |  |

## 3. Alternatives

[A bullet point list of any alternative approaches that were considered and why they were not chosen. This helps to provide context and rationale for the chosen approach.]

- **ALT-001**: Alternative approach 1
- **ALT-002**: Alternative approach 2

## 4. Dependencies

[List any dependencies that need to be addressed, such as libraries, frameworks, or other components that the plan relies on.]

- **DEP-001**: Dependency 1
- **DEP-002**: Dependency 2

## 5. Files

[List the files that will be affected by the feature or refactoring task.]

- **FILE-001**: Description of file 1
- **FILE-002**: Description of file 2

## 6. Testing

[List the tests that need to be implemented to verify the feature or refactoring task.]

- **TEST-001**: Description of test 1
- **TEST-002**: Description of test 2

## 7. Risks & Assumptions

[List any risks or assumptions related to the implementation of the plan.]

- **RISK-001**: Risk 1
- **ASSUMPTION-001**: Assumption 1

## 8. Related Specifications / Further Reading

[Link to related spec 1]
[Link to relevant external documentation]
```

