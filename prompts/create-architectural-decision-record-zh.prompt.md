````markdown
---
mode: "agent"
description: "为 AI 优化的决策文档创建架构决策记录 (ADR) 文档。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---

# 创建架构决策记录

为 `${input:DecisionTitle}` 创建一个 ADR 文档，使用为 AI 使用和人类可读性优化的结构化格式。

## 输入

- **上下文**: `${input:Context}`
- **决策**: `${input:Decision}`
- **备选方案**: `${input:Alternatives}`
- **利益相关者**: `${input:Stakeholders}`

## 输入验证

如果任何必需的输入未提供或无法从对话历史中确定，请在继续生成 ADR 之前要求用户提供缺失的信息。

## 要求

- 使用精确、无歧义的语言
- 遵循带有前置内容的标准化 ADR 格式
- 包括正面和负面后果
- 记录备选方案及其拒绝理由
- 为机器解析和人类参考构建结构
- 对多项目部分使用编码项目符号（3-4 个字母的代码 + 3 位数字）

ADR 必须保存在 `/docs/adr/` 目录中，并使用命名约定：`adr-NNNN-[title-slug].md`，其中 NNNN 是下一个顺序的 4 位数字（例如，`adr-0001-database-selection.md`）。

## 所需文档结构

文档文件必须遵循以下模板，确保所有部分都已适当填写。Markdown 的前置内容应按照以下示例正确构建：

```md
---
title: "ADR-NNNN: [决策标题]"
status: "已提议"
date: "YYYY-MM-DD"
authors: "[利益相关者姓名/角色]"
tags: ["架构", "决策"]
supersedes: ""
superseded_by: ""
---

# ADR-NNNN: [决策标题]

## 状态

**已提议** | 已接受 | 已拒绝 | 已取代 | 已弃用

## 上下文

[需要此决策的问题陈述、技术约束、业务需求和环境因素。]

## 决策

[选择的解决方案，并附有明确的选择理由。]

## 后果

### 正面

- **POS-001**: [有益的结果和优势]
- **POS-002**: [性能、可维护性、可伸缩性改进]
- **POS-003**: [与架构原则的一致性]

### 负面

- **NEG-001**: [权衡、限制、缺点]
- **NEG-002**: [引入的技术债务或复杂性]
- **NEG-003**: [风险和未来挑战]

## 考虑的备选方案

### [备选方案 1 名称]

- **ALT-001**: **描述**: [简要技术描述]
- **ALT-002**: **拒绝理由**: [为什么未选择此选项]

### [备选方案 2 名称]

- **ALT-003**: **描述**: [简要技术描述]
- **ALT-004**: **拒绝理由**: [为什么未选择此选项]

## 实施说明

- **IMP-001**: [关键实施注意事项]
- **IMP-002**: [如果适用，迁移或推出策略]
- **IMP-003**: [监控和成功标准]

## 参考

- **REF-001**: [相关的 ADR]
- **REF-002**: [外部文档]
- **REF-003**: [引用的标准或框架]
```
````

```

```
