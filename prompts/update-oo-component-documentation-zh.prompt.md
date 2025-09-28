---
mode: "agent"
description: "按照行业最佳实践与架构文档标准，更新现有面向对象组件文档。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---
# 更新标准 OO 组件文档

通过分析组件代码，更新 `${file}` 对应的现有文档。

从文档 front matter (`component_path`) 中提取组件路径，或在内容中推断。审查组件当前实现并同步更新文档。

**文档标准：**

- DOC-001：遵循 C4 模型文档层级（Context、Containers、Components、Code）
- DOC-002：对齐 Arc42 软件架构文档模板
- DOC-003：符合 IEEE 1016 软件设计说明标准
- DOC-004：践行敏捷文档原则（只保留有价值的信息）
- DOC-005：将开发者与维护者作为主要受众

**分析指引：**

- ANA-001：阅读现有文档，理解组件上下文与结构
- ANA-002：从 front matter 或正文定位组件路径
- ANA-003：审查源代码中的类结构与继承关系
- ANA-004：比较文档与实现差异
- ANA-005：识别设计模式与架构变化
- ANA-006：更新公开 API、接口与依赖
- ANA-007：识别新增/变更的创建型、结构型、行为型模式
- ANA-008：更新方法参数、返回值、异常信息
- ANA-009：重新评估性能、安全性、可靠性、可维护性
- ANA-010：更新集成模式与数据流

**语言特定优化：**

- LNG-001：**C#/.NET** —— async/await、依赖注入、配置、资源释放
- LNG-002：**Java** —— Spring、注解、异常处理、包结构
- LNG-003：**TypeScript/JavaScript** —— 模块、异步模式、类型、npm
- LNG-004：**Python** —— 包、虚拟环境、类型注解、测试

**更新策略：**

- UPD-001：保留文档现有结构与格式
- UPD-002：将 `last_updated` 更新为当前日期
- UPD-003：如存在版本历史在 front matter 中保持
- UPD-004：组件功能显著扩展时可新增章节
- UPD-005：标记已弃用功能或破坏性变更
- UPD-006：更新示例以匹配当前 API
- UPD-007：刷新依赖列表与版本
- UPD-008：更新 mermaid 图表以反映当前架构

**错误处理：**

- ERR-001：文档不存在——提供定位建议
- ERR-002：文档无组件路径——请求澄清
- ERR-003：源码已迁移——建议新路径
- ERR-004：架构重大变更——突出破坏性调整
- ERR-005：缺乏源码访问——记录限制

**输出格式：**

在保持现有 Markdown 结构的前提下，更新内容以匹配当前实现，保留格式、标题层级与组织方式。

**要求的文档结构：**

```md
---
title: [Component Name] - Technical Documentation
component_path: [Current component path]
version: [Updated version if applicable]
date_created: [Original creation date - preserve]
last_updated: [YYYY-MM-DD - update to current date]
owner: [Preserve existing or update if changed]
tags: [Update tags as needed based on current functionality]
---

# [Component Name] Documentation

[Update introduction to reflect current component purpose and capabilities]

## 1. Component Overview

### Purpose/Responsibility
- OVR-001: Update component's primary responsibility
- OVR-002: Refresh scope (included/excluded functionality)
- OVR-003: Update system context and relationships

## 2. Architecture Section

- ARC-001: Update design patterns used (Repository, Factory, Observer, etc.)
- ARC-002: Refresh internal and external dependencies with current purposes
- ARC-003: Update component interactions and relationships
- ARC-004: Update visual diagrams (UML class, sequence, component)
- ARC-005: Refresh mermaid diagram showing current component structure, relationships, and dependencies

### Component Structure and Dependencies Diagram

Update the mermaid diagram to show current:
- **Component structure** - Current classes, interfaces, and their relationships
- **Internal dependencies** - How components currently interact within the system
- **External dependencies** - Current external libraries, services, databases, APIs
- **Data flow** - Current direction of dependencies and interactions
- **Inheritance/composition** - Current class hierarchies and composition relationships

```mermaid
[Update diagram to reflect current architecture]
```

## 3. Interface Documentation

- INT-001: Update all public interfaces and current usage patterns
- INT-002: Refresh method/property reference table with current API
- INT-003: Update events/callbacks/notification mechanisms

| Method/Property | Purpose | Parameters | Return Type | Usage Notes |
|-----------------|---------|------------|-------------|-------------|
| [Update table with current API] | | | | |

## 4. Implementation Details

- IMP-001: Update main implementation classes and current responsibilities
- IMP-002: Refresh configuration requirements and initialization patterns
- IMP-003: Update key algorithms and business logic
- IMP-004: Update performance characteristics and bottlenecks

## 5. Usage Examples

### Basic Usage

```csharp
// Update basic usage example to current API
```

### Advanced Usage

```csharp
// Update advanced configuration patterns to current implementation
```

- USE-001: Update basic usage examples
- USE-002: Refresh advanced configuration patterns
- USE-003: Update best practices and recommended patterns

## 6. Quality Attributes

- QUA-001: Update security (authentication, authorization, data protection)
- QUA-002: Refresh performance (characteristics, scalability, resource usage)
- QUA-003: Update reliability (error handling, fault tolerance, recovery)
- QUA-004: Refresh maintainability (standards, testing, documentation)
- QUA-005: Update extensibility (extension points, customization options)

## 7. Reference Information

- REF-001: Update dependencies with current versions and purposes
- REF-002: Refresh configuration options reference
- REF-003: Update testing guidelines and mock setup
- REF-004: Refresh troubleshooting (common issues, error messages)
- REF-005: Update related documentation links
- REF-006: Add change history and migration notes for this update

```

