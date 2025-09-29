---
description: '创建和管理 awesome-copilot 集合的指南'
applyTo: 'collections/*.collection.yml'
---

# 集合开发

## 集合说明

在 awesome-copilot 仓库中使用集合时：

- 在提交前始终使用 `node validate-collections.js` 验证集合
- 遵循已建立的集合清单 YAML 模式
- 仅引用仓库中的现有文件
- 使用具有小写字母、数字和连字符的描述性集合 ID
- 保持集合专注于特定的工作流程或主题
- 测试所有引用的项目能够良好地协同工作

## 集合结构

- **必需字段**：id、name、description、items
- **可选字段**：tags、display
- **项目要求**：path 必须存在，kind 必须匹配文件扩展名
- **显示选项**：ordering（alpha/manual）、show_badge（true/false）

## 验证规则

- 集合 ID 在所有集合中必须唯一
- 文件路径必须存在并匹配项目类型
- 标签只能使用小写字母、数字和连字符
- 集合必须包含 1-50 个项目
- 描述必须为 1-500 个字符

## 最佳实践

- 将 3-10 个相关项目分组以获得最佳可用性
- 使用清晰、描述性的名称和描述
- 添加相关标签以提高可发现性
- 测试集合启用的完整工作流程
- 确保项目有效地相互补充

## 文件组织

- 集合不需要文件重新组织
- 项目可以位于仓库中的任何地方
- 使用相对于仓库根目录的路径
- 维护现有的目录结构（prompts/、instructions/、chatmodes/）

## 生成过程

- 集合通过 `update-readme.js` 自动生成 README 文件
- 在 collections/ 目录中创建单独的集合页面
- 主集合概览生成为 README.collections.md
- 为每个项目自动创建 VS Code 安装徽章