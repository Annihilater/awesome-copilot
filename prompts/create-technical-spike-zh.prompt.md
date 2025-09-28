---
mode: "agent"
description: "创建有时间限制的技术难题研究文档，以便在实施前研究和解决关键开发决策。"
tools: ["runCommands", "runTasks", "edit", "search", "extensions", "usages", "vscodeAPI", "think", "problems", "changes", "testFailure", "openSimpleBrowser", "fetch", "githubRepo", "todos", "Microsoft Docs", "search"]
---

# 创建技术难题研究文档

为研究必须在开发开始前回答的关键问题，创建有时间限制的技术难题研究文档。每个难题研究都侧重于一个具体的技术决策，并有明确的可交付成果和时间表。

## 文档结构

在 `${input:FolderPath|docs/spikes}` 目录中创建单独的文件。使用模式 `[category]-[short-description]-spike.md` 命名每个文件（例如，`api-copilot-integration-spike.md`，`performance-realtime-audio-spike.md`）。

```md
---
title: "${input:SpikeTitle}"
category: "${input:Category|Technical}"
status: "🔴 未开始"
priority: "${input:Priority|高}"
timebox: "${input:Timebox|1 周}"
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
owner: "${input:Owner}"
tags: ["technical-spike", "${input:Category|technical}", "research"]
---

# ${input:SpikeTitle}

## 摘要

**难题研究目标：** [需要解决的清晰、具体的问题或决策]

**重要性：** [对开发/架构决策的影响]

**时间限制：** [分配给此难题研究的时间]

**决策截止日期：** [为避免阻塞开发，必须在此日期前解决]

## 研究问题

**主要问题：** [需要回答的主要技术问题]

**次要问题：**

- [相关问题 1]
- [相关问题 2]
- [相关问题 3]

## 调查计划

### 研究任务

- [ ] [具体研究任务 1]
- [ ] [具体研究任务 2]
- [ ] [具体研究任务 3]
- [ ] [创建概念验证/原型]
- [ ] [记录发现和建议]

### 成功标准

**此难题研究在以下情况下完成：**

- [ ] [具体标准 1]
- [ ] [具体标准 2]
- [ ] [记录了明确的建议]
- [ ] [概念验证完成（如果适用）]

## 技术背景

**相关组件：** [列出受此决策影响的系统组件]

**依赖关系：** [解决此问题所依赖的其他难题研究或决策]

**约束：** [影响解决方案的已知限制或要求]

## 研究发现

### 调查结果

[记录研究发现、测试结果和收集的证据]

### 原型/测试说明

[来自任何原型、难题研究或技术实验的结果]

### 外部资源

- [相关文档链接]
- [API 参考链接]
- [社区讨论链接]
- [示例/教程链接]

## 决策

### 建议

[基于研究发现的明确建议]

### 原理

[支持建议的理由和权衡]

### 备选方案

[考虑过的其他方案及其被拒绝的原因]

## 后续步骤

- [ ] [行动项 1]
- [ ] [行动项 2]
- [ ] [更新相关文档]

## 审批

**决策者：** [负责最终决策的人员/团队]

**审批状态：** [待定/已批准/已拒绝]

**审批日期：** [YYYY-MM-DD]
```
