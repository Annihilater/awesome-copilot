```markdown
---
description: 'GitHub Copilot 的迁移和代码演进指令生成器。分析两个项目版本（分支、提交或发布）之间的差异，以创建精确的指令，使 Copilot 能够在技术迁移、重大重构或框架版本升级期间保持一致性。'
mode: 'agent'
---

# 迁移和代码演进指令生成器

## 配置变量

```
${MIGRATION_TYPE="框架版本|架构重构|技术迁移|依赖更新|模式变更"}
<!-- 迁移或演进的类型 -->

${SOURCE_REFERENCE="分支|提交|标签"}
<!-- 源参考点（之前的状态） -->

${TARGET_REFERENCE="分支|提交|标签"}  
<!-- 目标参考点（之后的状态） -->

${ANALYSIS_SCOPE="整个项目|特定文件夹|仅修改的文件"}
<!-- 分析范围 -->

${CHANGE_FOCUS="重大变更|新约定|过时模式|API 变更|配置"}
<!-- 变更的主要方面 -->

${AUTOMATION_LEVEL="保守|平衡|激进"}
<!-- Copilot 建议的自动化级别 -->

${GENERATE_EXAMPLES="true|false"}
<!-- 包括转换示例 -->

${VALIDATION_REQUIRED="true|false"}
<!-- 应用前需要验证 -->
```

## 生成的提示

```
"分析两个项目状态之间的代码演进，为 GitHub Copilot 生成精确的迁移指令。这些指令将指导 Copilot 在未来的修改中自动应用相同的转换模式。请遵循以下方法：

### 阶段 1：比较状态分析

#### 结构变更检测
- 比较 ${SOURCE_REFERENCE} 和 ${TARGET_REFERENCE} 之间的文件夹结构
- 识别移动、重命名或删除的文件
- 分析配置文件的变更
- 记录新的依赖项和已删除的依赖项

#### 代码转换分析
${MIGRATION_TYPE == "框架版本" ? 
  "- 识别框架版本之间的 API 变更
   - 分析正在使用的新功能
   - 记录过时的方法/属性
   - 注意语法或约定变更" : ""}

${MIGRATION_TYPE == "架构重构" ? 
  "- 分析架构模式变更
   - 识别引入的新抽象
   - 记录职责重组
   - 注意数据流的变更" : ""}

${MIGRATION_TYPE == "技术迁移" ? 
  "- 分析一种技术被另一种技术替代的情况
   - 识别功能等效性
   - 记录 API 和语法变更
   - 注意新的依赖项和配置" : ""}

#### 转换模式提取
- 识别应用的重复转换
- 分析从旧格式到新格式的转换规则
- 记录异常和特殊情况
- 创建前后对应矩阵

### 阶段 2：迁移指令生成

创建一个 `.github/copilot-migration-instructions.md` 文件，结构如下：

\`\`\`markdown
# GitHub Copilot 迁移指令

## 迁移上下文
- **类型**：${MIGRATION_TYPE}
- **从**：${SOURCE_REFERENCE} 
- **到**：${TARGET_REFERENCE}
- **日期**：[GENERATION_DATE]
- **范围**：${ANALYSIS_SCOPE}

## 自动转换规则

### 1. 强制转换
${AUTOMATION_LEVEL != "保守" ? 
  "[AUTOMATIC_TRANSFORMATION_RULES]
   - **旧模式**：[OLD_CODE]
   - **新模式**：[NEW_CODE]
   - **触发器**：何时检测此模式
   - **操作**：自动应用的转换" : ""}

### 2. 带验证的转换
${VALIDATION_REQUIRED == "true" ? 
  "[TRANSFORMATIONS_WITH_VALIDATION]
   - **检测到的模式**：[DESCRIPTION]
   - **建议的转换**：[NEW_APPROACH]
   - **所需验证**：[VALIDATION_CRITERIA]
   - **替代方案**：[ALTERNATIVE_OPTIONS]" : ""}

### 3. API 对应关系
${CHANGE_FOCUS == "API 变更" || MIGRATION_TYPE == "框架版本" ? 
  "[API_CORRESPONDENCE_TABLE]
   | 旧 API   | 新 API   | 注意事项     | 示例        |
   | --------- | --------- | --------- | -------------- |
   | [OLD_API] | [NEW_API] | [CHANGES] | [CODE_EXAMPLE] | " : ""} |

### 4. 要采用的新模式
[DETECTED_EMERGING_PATTERNS]
- **模式**：[PATTERN_NAME]
- **用法**：[WHEN_TO_USE] 
- **实现**：[HOW_TO_IMPLEMENT]
- **优点**：[ADVANTAGES]

### 5. 要避免的过时模式
[DETECTED_OBSOLETE_PATTERNS]
- **过时模式**：[OLD_PATTERN]
- **为何避免**：[REASONS]
- **替代方案**：[NEW_PATTERN]
- **迁移**：[CONVERSION_STEPS]

## 特定文件类型的指令

${GENERATE_EXAMPLES == "true" ? 
  "### 配置文件
   [CONFIG_TRANSFORMATION_EXAMPLES]
   
   ### 主要源文件
   [SOURCE_TRANSFORMATION_EXAMPLES]
   
   ### 测试文件
   [TEST_TRANSFORMATION_EXAMPLES]" : ""}

## 验证与安全

### 自动控制点
- 每次转换后要执行的验证
- 要运行以验证变更的测试
- 要监控的性能指标
- 要执行的兼容性检查

### 手动升级
需要人工干预的情况：
- [COMPLEX_CASES_LIST]
- [ARCHITECTURAL_DECISIONS]
- [BUSINESS_IMPACTS]

## 迁移监控

### 跟踪指标
- 自动迁移的代码百分比
- 所需的手动验证次数
- 自动转换的错误率
- 每个文件的平均迁移时间

### 错误报告
如何向 Copilot 报告不正确的转换：
- 用于改进规则的反馈模式
- 要记录的异常
- 要对指令进行的调整

\`\`\`

### 阶段 3：上下文示例生成

${GENERATE_EXAMPLES == "true" ? 
  "#### 转换示例
   对于每个识别出的模式，生成：
   
   \`\`\`
   // 之前 (${SOURCE_REFERENCE})
   [OLD_CODE_EXAMPLE]
   
   // 之后 (${TARGET_REFERENCE}) 
   [NEW_CODE_EXAMPLE]
   
   // COPILOT 指令
   当您看到此模式 [TRIGGER] 时，请按照以下步骤将其转换为 [NEW_PATTERN]：[STEPS]
   \`\`\`" : ""}

### 阶段 4：验证与优化

#### 指令测试
- 在测试代码上应用指令
- 验证转换的一致性
- 根据结果调整规则
- 记录异常和边缘情况

#### 迭代优化  
${AUTOMATION_LEVEL == "激进" ? 
  "- 优化规则以最大化自动化
   - 减少检测中的误报
   - 提高转换准确性
   - 记录经验教训" : ""}

### 最终结果

使 GitHub Copilot 能够：
1. 在未来的修改中**自动应用**相同的转换
2. 与新采用的约定**保持一致性**  
3. 通过自动提出替代方案**避免过时的模式**
4. 通过利用获得的经验**加速未来的迁移**
5. 通过自动化重复转换**减少错误**

这些指令将 Copilot 转变为一个智能迁移助手，能够一致可靠地重现您的技术演进决策。
"
```

## 典型用例

### 框架版本迁移
非常适合记录从 Angular 14 到 Angular 17、React 类组件到 Hooks 或 .NET Framework 到 .NET Core 的过渡。自动识别重大变更并生成相应的转换规则。

### 技术栈演进  
在完全替换技术时至关重要：jQuery 到 React、REST 到 GraphQL、SQL 到 NoSQL。创建包含模式映射的综合迁移指南。

### 架构重构
非常适合大型重构，如单体到微服务、MVC 到清晰架构或组件到可组合架构。为未来类似的转换保留架构知识。

### 设计模式现代化
用于采用新模式：存储库模式、依赖注入、观察者到响应式编程。记录基本原理和实现差异。

## 独特优势

### 🧠 **人工智能增强**
与传统的迁移文档不同，这些指令“训练”GitHub Copilot 在未来的代码修改中自动重现您的技术演进决策。

### 🔄 **知识资本化**  
将特定的项目经验转化为可重用的规则，避免迁移专业知识的流失，并加速未来类似的转换。

### 🎯 **上下文感知精度**
生成针对您的特定代码库量身定制的指令，而不是通用建议，并提供来自您项目演进的真实前后示例。

### ⚡ **自动化一致性**
确保新的代码添加自动遵循新的约定，防止架构回归并保持代码演进的一致性。
````