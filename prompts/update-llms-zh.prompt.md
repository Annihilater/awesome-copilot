---
mode: "agent"
description: "根据 https://llmstxt.org/ 规范更新仓库根目录的 llms.txt，使其反映文档或规范的最新变动。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "githubRepo", "openSimpleBrowser", "problems", "runTasks", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---
# 更新 LLMs.txt 文件

更新仓库根目录的 `llms.txt`，使其准确反映文档、规范或仓库结构的变化。该文件为大型语言模型提供高层指引，帮助理解仓库目的与重要资料位置。

## 主要指令

保持 `llms.txt` 与 llms.txt 规范一致，同时反映最新仓库结构与内容。文件需兼顾 LLM 最佳阅读体验与人类可读性。

## 分析与规划阶段

在更新前必须完成彻底分析：

### 步骤 1：审查现有文件与规范
- 阅读当前 `llms.txt`，掌握其结构
- 查阅 https://llmstxt.org/ 规范，确保持续合规
- 根据仓库变动识别需更新区域

### 步骤 2：仓库结构分析
- 使用适当工具检查最新目录结构
- 与现有 `llms.txt` 对照
- 识别需纳入的新目录、文件或文档
- 记录已删除或迁移的文件

### 步骤 3：内容发现与变更检测
- 查找新的 README 及位置
- 搜索新的文档文件（如 `/docs/`、`/spec/` 下的 `.md`）
- 定位新的规范文件及用途
- 发现新的配置文件及重要程度
- 查找新的示例与代码样本
- 识别既有文档结构的变更

### 步骤 4：制定更新计划
基于分析输出结构化计划，包括：
- 维持准确性所需的修改
- 需要加入 `llms.txt` 的新文件
- 需删除或更新的过时引用
- 保持清晰度的组织改进

## 实施要求

### 格式合规
更新后的 `llms.txt` 必须遵循规范结构：

1. **H1 标题**：仓库/项目名称（必需）
2. **引用摘要**：使用 blockquote 的简要描述（推荐）
3. **附加说明**：可选，无标题的补充上下文
4. **文件列表章节**：一个或多个 H2 标题，使用 Markdown 列表列出文件

### 内容要求

#### 必备元素
- **项目名称**：H1 标题清晰描述
- **摘要**：简洁引用描述仓库目的
- **关键文件**：按类别组织的重要文件（H2 章节）

#### 链接格式
每个文件链接需遵循 `[描述性名称](相对路径): 可选描述`

#### 章节组织
将文件按逻辑分组，如：
- **Documentation**：核心文档
- **Specifications**：技术规范与需求
- **Examples**：示例代码与用法
- **Configuration**：安装与配置文件
- **Optional**：次要文件（用于可选上下文）

### 内容准则

#### 语言与风格
- 语言简洁明确，无歧义
- 避免未经解释的专业术语
- 同时面向人类与 LLM
- 描述具体且具有信息量

#### 文件选择标准
应包含能：
- 阐述仓库目标与范围
- 提供关键技术文档
- 展示使用示例与模式
- 定义接口与规范
- 提供配置与安装指南

排除以下文件：
- 纯实现细节
- 重复信息
- 构建产物或生成内容
- 与理解项目无关的资料

## 执行步骤

### 步骤 1：现状分析
1. 彻底阅读 `llms.txt`
2. 审视完整仓库结构
3. 对比现有引用与实际内容
4. 找出过时、缺失或错误引用
5. 记录结构性问题

### 步骤 2：内容规划
1. 判断核心目的描述是否需更新
2. 视需要改写摘要 blockquote
3. 规划新增文件/目录
4. 规划移除或迁移内容
5. 若有必要重新组织章节

### 步骤 3：文件更新
1. 修改仓库根目录的 `llms.txt`
2. 保持完全符合规范
3. 为新增文件添加合适描述
4. 移除或更新过时引用
5. 确保链接为有效相对路径

### 步骤 4：验证
1. 再次核对 https://llmstxt.org/ 规范
2. 确认所有链接有效可访问
3. 确保文件仍是高效的 LLM 导航工具
4. 验证文件兼顾人类与机器可读性

## 质量保证

### 格式验证
- ✅ H1 含项目名称
- ✅ Blockquote 摘要（如适用）
- ✅ H2 章节列出文件
- ✅ 正确的 Markdown 链接格式
- ✅ 无损坏或无效链接
- ✅ 格式始终一致

### 内容验证
- ✅ 语言清晰无歧义
- ✅ 涵盖关键文件
- ✅ 结构合理
- ✅ 描述适切
- ✅ 仍能高效指引 LLM

### 规范合规
- ✅ 完全遵守 https://llmstxt.org/
- ✅ 使用要求的 Markdown 结构
- ✅ 合理使用可选章节
- ✅ 文件位于仓库根目录 (`/llms.txt`)

## 更新策略

### 新增流程
新增内容时：
1. 确定归属章节
2. 编写清晰的链接名称
3. 撰写简洁且信息丰富的描述
4. 按字母或逻辑顺序排列
5. 如有必要，为新内容类型创建新章节

### 移除流程
移除过时内容时：
1. 确认文件确实删除或迁移
2. 若仅迁移，更新路径而非删除
3. 若章节为空，可一并移除
4. 必要时更新交叉引用

### 重组流程
调整结构时：
1. 保持从概况到细节的逻辑
2. 主要文档放于核心章节
3. 次要内容可移至 “Optional”
4. 确保新结构提升 LLM 导航体验

`llms.txt` 示例结构：

```txt
# [Repository Name]

> [Concise description of the repository's purpose and scope]

[Optional additional context paragraphs without headings]

## Documentation

- [Main README](README.md): Primary project documentation and getting started guide
- [Contributing Guide](CONTRIBUTING.md): Guidelines for contributing to the project
- [Code of Conduct](CODE_OF_CONDUCT.md): Community guidelines and expectations

## Specifications

- [Technical Specification](spec/technical-spec.md): Detailed technical requirements and constraints
- [API Specification](spec/api-spec.md): Interface definitions and data contracts

## Examples

- [Basic Example](examples/basic-usage.md): Simple usage demonstration
- [Advanced Example](examples/advanced-usage.md): Complex implementation patterns

## Configuration

- [Setup Guide](docs/setup.md): Installation and configuration instructions
- [Deployment Guide](docs/deployment.md): Production deployment guidelines

## Optional

- [Architecture Documentation](docs/architecture.md): Detailed system architecture
- [Design Decisions](docs/decisions.md): Historical design decision records
```

## 成功标准

更新后的 `llms.txt` 应：
1. 准确反映最新仓库结构与内容
2. 持续符合 llms.txt 规范
3. 清晰指向关键文档
4. 移除过时或错误引用
5. 纳入新的重要文件
6. 保持逻辑组织，便于 LLM 消化
7. 全程使用明确、无歧义语言
8. 兼顾人机双重读者

