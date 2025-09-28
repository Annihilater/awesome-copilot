---
description: "智能 README.md 生成提示，通过分析 .github/copilot 目录与 copilot-instructions.md，提取项目信息、技术栈、架构、开发流程、编码规范与测试方案，生成结构清晰、格式正确、面向开发者的仓库文档。"
mode: "agent"
---

# README 生成器提示

通过分析 `.github/copilot` 目录中的文档以及 `.github/copilot-instructions.md` 文件，为当前仓库生成一份全面的 README.md。按以下步骤操作：

1. 扫描 `.github/copilot` 目录下的所有文件，例如：
   - Architecture
   - Code_Exemplars
   - Coding_Standards
   - Project_Folder_Structure
   - Technology_Stack
   - Unit_Tests
   - Workflow_Analysis

2. 同时查看 `.github` 目录中的 `copilot-instructions.md`

3. 基于上述资料生成一份包含以下章节的 README.md：

## 项目名称与简介
- 从文档中提取项目名称与核心目标
- 简明描述项目的用途

## 技术栈
- 列出主要使用的技术、语言与框架
- 如有版本信息请一并标注
- 首选从 Technology_Stack 文件获取数据

## 项目架构
- 提供架构的高层概览
- 如文档描述，可包含简易示意图
- 主要来源：Architecture 文件

## 快速开始
- 根据技术栈提供安装说明
- 加入环境配置步骤
- 列出前置依赖

## 项目结构
- 简要说明目录组织方式
- 来源：Project_Folder_Structure 文件

## 核心特性
- 列举项目的主要功能
- 综合多份文档提炼要点

## 开发流程
- 概述项目的开发流程
- 如有分支策略，也一并说明
- 主要来源：Workflow_Analysis 文件

## 编码规范
- 总结关键编码规范与约定
- 来源：Coding_Standards 文件

## 测试
- 说明测试方案与使用工具
- 来源：Unit_Tests 文件

## 贡献指南
- 提供贡献流程与注意事项
- 如有代码示例可用作参考
- 来源：Code_Exemplars 与 copilot-instructions

## 许可证
- 如有许可证信息，请在此记录

请以规范的 Markdown 编排 README：
- 使用清晰的标题与副标题
- 根据需要添加代码块
- 通过列表提升可读性
- 链接相关文档
- 若有可用信息，可添加构建状态、版本等徽章

保持 README 简洁而信息充分，重点突出新开发者或用户需要了解的内容。

