````markdown
---
mode: "agent"
description: "遵循行业最佳实践和架构文档标准，为面向对象的组件创建全面、标准化的文档。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---

# 生成标准 OO 组件文档

为位于以下位置的面向对象组件创建全面文档：`${input:ComponentPath}`。

通过检查所提供路径中的代码来分析组件。如果是文件夹，则分析所有源文件。如果是单个文件，则将其视为主组件并分析同一目录中的相关文件。

## 文档标准

- DOC-001：遵循 C4 模型文档级别（上下文、容器、组件、代码）
- DOC-002：与 Arc42 软件架构文档模板保持一致
- DOC-003：符合 IEEE 1016 软件设计描述标准
- DOC-004：使用敏捷文档原则（恰到好处且有价值的文档）
- DOC-005：以开发人员和维护人员为主要受众

## 分析说明

- ANA-001：确定路径类型（文件夹与单个文件）并识别主组件
- ANA-002：检查源文件以了解类结构和继承
- ANA-003：识别设计模式和架构决策
- ANA-004：记录公共 API、接口和依赖项
- ANA-005：识别创建型/结构型/行为型模式
- ANA-006：记录方法参数、返回值、异常
- ANA-007：评估性能、安全性、可靠性、可维护性
- ANA-008：推断集成模式和数据流

## 特定于语言的优化

- LNG-001：**C#/.NET** - async/await、依赖注入、配置、处置
- LNG-002：**Java** - Spring 框架、注解、异常处理、打包
- LNG-003：**TypeScript/JavaScript** - 模块、异步模式、类型、npm
- LNG-004：**Python** - 包、虚拟环境、类型提示、测试

## 错误处理

- ERR-001：路径不存在 - 提供正确的格式指导
- ERR-002：未找到源文件 - 建议备用位置
- ERR-003：结构不清晰 - 记录发现并请求澄清
- ERR-004：非标准模式 - 记录自定义方法
- ERR-005：代码不足 - 关注可用信息，突出差距

## 输出格式

生成结构良好的 Markdown，具有清晰的标题层次结构、代码块、表格、项目符号列表以及适当的格式，以提高可读性和可维护性。

## 文件位置

文档应保存在 `/docs/components/` 目录中，并根据约定命名：`[component-name]-documentation.md`。

## 所需文档结构

文档文件必须遵循以下模板，确保所有部分都已适当填写。Markdown 的前置内容应按照以下示例正确构建：

````md
---
title: [组件名称] - 技术文档
component_path: `${input:ComponentPath}`
version: [可选：例如，1.0，日期]
date_created: [YYYY-MM-DD]
last_updated: [可选：YYYY-MM-DD]
owner: [可选：负责此组件的团队/个人]
tags: [可选：相关标签或类别的列表，例如，`component`、`service`、`tool`、`infrastructure`、`documentation`、`architecture` 等]
---

# [组件名称] 文档

[对组件及其在系统中的用途的简短介绍。]

## 1. 组件概述

### 目的/职责

- OVR-001：说明组件的主要职责
- OVR-002：定义范围（包括/排除的功能）
- OVR-003：描述系统上下文和关系

## 2. 架构部分

- ARC-001：记录使用的设计模式（存储库、工厂、观察者等）
- ARC-002：列出内部和外部依赖项及其用途
- ARC-003：记录组件交互和关系
- ARC-004：包括可视化图表（UML 类图、序列图、组件图）
- ARC-005：创建显示组件结构、关系和依赖项的 mermaid 图

### 组件结构和依赖项图

包括一个全面的 mermaid 图，显示：

- **组件结构** - 主要类、接口及其关系
- **内部依赖项** - 组件如何在系统内部交互
- **外部依赖项** - 外部库、服务、数据库、API
- **数据流** - 依赖项和交互的方向
- **继承/组合** - 类层次结构和组合关系

```mermaid
graph TD
    subgraph "组件系统"
        A[主组件] --> B[内部服务]
```
````
````
