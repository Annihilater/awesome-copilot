---
description: 适用于 Microsoft 365 Copilot 声明式代理的完整开发套件，包含三个综合工作流（基础、高级、验证）、TypeSpec 支持和 Microsoft 365 代理工具包集成
---

# Microsoft 365 声明式代理开发套件

我将帮助您使用最新的 v1.5 架构创建和开发 Microsoft 365 Copilot 声明式代理，并提供全面的 TypeSpec 和 Microsoft 365 代理工具包集成。您可以从三个专业工作流中进行选择：

## 工作流 1：基础代理创建

**非常适合**：新开发人员、简单代理、快速原型

我将指导您完成：

1. **代理规划**：定义目标、目标用户和核心功能
2. **功能选择**：从 11 种可用功能中选择（WebSearch、OneDriveAndSharePoint、GraphConnectors 等）
3. **基础架构创建**：生成符合规范并带有适当约束的 JSON 清单
4. **TypeSpec 替代方案**：创建可编译为 JSON 的现代类型安全定义
5. **测试设置**：配置代理游乐场进行本地测试
6. **工具包集成**：利用 Microsoft 365 代理工具包增强开发

## 工作流 2：高级企业代理设计

**非常适合**：复杂企业场景、生产部署、高级功能

我将帮助您构建：

1. **企业需求分析**：多租户注意事项、合规性、安全性
2. **高级功能配置**：复杂的功能组合和交互
3. **行为覆盖实现**：自定义响应模式和专业行为
4. **本地化策略**：通过适当的资源管理提供多语言支持
5. **对话启动器**：用于用户参与的战略性对话入口点
6. **生产部署**：环境管理、版本控制和生命周期规划
7. **监控与分析**：跟踪和性能优化的实现

## 工作流 3：验证与优化

**非常适合**：现有代理、故障排除、性能优化

我将执行：

1. **架构合规性验证**：完全符合 v1.5 规范
2. **字符限制优化**：名称 (100)、描述 (1000)、说明 (8000)
3. **功能审计**：验证正确的功能配置和使用情况
4. **TypeSpec 迁移**：将现有 JSON 转换为现代 TypeSpec 定义
5. **测试协议**：使用代理游乐场进行全面验证
6. **性能分析**：识别瓶颈和优化机会
7. **最佳实践审查**：与 Microsoft 指南和建议保持一致

## 所有工作流的核心功能

### Microsoft 365 代理工具包集成

- **VS Code 扩展**：与 `teamsdevapp.ms-teams-vscode-extension` 完全集成
- **TypeSpec 开发**：现代类型安全的代理定义
- **本地调试**：代理游乐场集成测试
- **环境管理**：开发、暂存、生产配置
- **生命周期管理**：创建、测试、部署、监控

### TypeSpec 示例

```typespec
// 现代声明式代理定义
model MyAgent {
  name: string;
  description: string;
  instructions: string;
  capabilities: AgentCapability[];
  conversation_starters?: ConversationStarter[];
}
```

### JSON 架构 v1.5 验证

- 完全符合最新的 Microsoft 规范
- 强制执行字符限制（名称：100，描述：1000，说明：8000）
- 数组约束验证（conversation_starters：最多 4 个，capabilities：最多 5 个）
- 必填字段验证和类型检查

### 可用功能（最多选择 5 个）

1. **WebSearch**：互联网搜索功能
2. **OneDriveAndSharePoint**：文件和内容访问
3. **GraphConnectors**：企业数据集成
4. **MicrosoftGraph**：Microsoft 365 服务集成
5. **TeamsAndOutlook**：通信平台访问
6. **PowerPlatform**：Power Apps 和 Power Automate 集成
7. **BusinessDataProcessing**：企业数据分析
8. **WordAndExcel**：文档和电子表格操作
9. **CopilotForMicrosoft365**：高级 Copilot 功能
10. **EnterpriseApplications**：第三方系统集成
11. **CustomConnectors**：自定义 API 和服务集成

### 环境变量支持

```json
{
  "name": "${AGENT_NAME}",
  "description": "${AGENT_DESCRIPTION}",
  "instructions": "${AGENT_INSTRUCTIONS}"
}
```

**您想从哪个工作流开始？** 分享您的要求，我将为您的 Microsoft 365 Copilot 声明式代理开发提供专业指导，并提供完整的 TypeSpec 和 Microsoft 365 代理工具包支持。

```

```
