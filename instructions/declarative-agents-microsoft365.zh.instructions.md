---
description: 针对 Microsoft 365 Copilot 声明式 agent 的综合开发指导方针，使用 schema v1.5、TypeSpec 集成和 Microsoft 365 Agents Toolkit 工作流程
applyTo: "**.json, **.ts, **.tsp, **manifest.json, **agent.json, **declarative-agent.json"
---

# Microsoft 365 声明式 Agent 开发指导方针

## 概述

Microsoft 365 Copilot 声明式 agent 是强大的自定义 AI 助手，它们扩展了 Microsoft 365 Copilot 的专业化功能、企业数据访问和自定义行为。这些指导方针提供了使用最新 v1.5 JSON schema 规范和完整 Microsoft 365 Agents Toolkit 集成创建生产就绪 agent 的综合开发实践。

## Schema 规范 v1.5

### 核心属性

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json",
  "version": "v1.5",
  "name": "string (max 100 characters)",
  "description": "string (max 1000 characters)",
  "instructions": "string (max 8000 characters)",
  "capabilities": ["array (max 5 items)"],
  "conversation_starters": ["array (max 4 items, optional)"]
}
```

### 字符限制与约束
- **Name**: 最大 100 个字符，必需
- **Description**: 最大 1000 个字符，必需
- **Instructions**: 最大 8000 个字符，必需
- **Capabilities**: 最大 5 项，最少 1 项
- **Conversation Starters**: 最大 4 项，可选

## 可用功能

### 核心功能
1. **WebSearch**: 互联网搜索和实时信息访问
2. **OneDriveAndSharePoint**: 文件访问、文档搜索、内容管理
3. **GraphConnectors**: 来自第三方系统的企业数据集成
4. **MicrosoftGraph**: 访问 Microsoft 365 服务和数据

### 通信与协作
5. **TeamsAndOutlook**: Teams 聊天、会议、邮件集成
6. **CopilotForMicrosoft365**: 高级 Copilot 功能和工作流程

### 业务应用
7. **PowerPlatform**: Power Apps、Power Automate、Power BI 集成
8. **BusinessDataProcessing**: 高级数据分析和处理
9. **WordAndExcel**: 文档创建、编辑、分析
10. **EnterpriseApplications**: 第三方业务系统集成
11. **CustomConnectors**: 自定义 API 和服务集成

## Microsoft 365 Agents Toolkit 集成

### VS Code 扩展设置
```bash
# 安装 Microsoft 365 Agents Toolkit
# Extension ID: teamsdevapp.ms-teams-vscode-extension
```

### TypeSpec 开发工作流程

#### 1. 现代 Agent 定义
```typespec
import "@typespec/json-schema";

using TypeSpec.JsonSchema;

@jsonSchema("/schemas/declarative-agent/v1.5/schema.json")
namespace DeclarativeAgent;

/** Microsoft 365 Declarative Agent */
model Agent {
  /** Schema version */
  @minLength(1)
  $schema: "https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json";

  /** Agent version */
  version: "v1.5";

  /** Agent name (max 100 characters) */
  @maxLength(100)
  @minLength(1)
  name: string;

  /** Agent description (max 1000 characters) */
  @maxLength(1000)
  @minLength(1)
  description: string;

  /** Agent instructions (max 8000 characters) */
  @maxLength(8000)
  @minLength(1)
  instructions: string;

  /** Agent capabilities (1-5 items) */
  @minItems(1)
  @maxItems(5)
  capabilities: AgentCapability[];

  /** Conversation starters (max 4 items) */
  @maxItems(4)
  conversation_starters?: ConversationStarter[];
}

/** Available agent capabilities */
union AgentCapability {
  "WebSearch",
  "OneDriveAndSharePoint",
  "GraphConnectors",
  "MicrosoftGraph",
  "TeamsAndOutlook",
  "PowerPlatform",
  "BusinessDataProcessing",
  "WordAndExcel",
  "CopilotForMicrosoft365",
  "EnterpriseApplications",
  "CustomConnectors"
}

/** Conversation starter definition */
model ConversationStarter {
  /** Starter text (max 100 characters) */
  @maxLength(100)
  @minLength(1)
  text: string;
}
```

#### 2. 编译为 JSON
```bash
# 将 TypeSpec 编译为 JSON manifest
tsp compile agent.tsp --emit=@typespec/json-schema
```

### 环境配置

#### 开发环境
```json
{
  "name": "${DEV_AGENT_NAME}",
  "description": "Development version: ${AGENT_DESCRIPTION}",
  "instructions": "${AGENT_INSTRUCTIONS}",
  "capabilities": ["${REQUIRED_CAPABILITIES}"]
}
```

#### 生产环境
```json
{
  "name": "${PROD_AGENT_NAME}",
  "description": "${AGENT_DESCRIPTION}",
  "instructions": "${AGENT_INSTRUCTIONS}",
  "capabilities": ["${PRODUCTION_CAPABILITIES}"]
}
```

## 开发最佳实践

### 1. Schema 验证
```typescript
// 对 v1.5 schema 进行验证
const schema = await fetch('https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.5/schema.json');
const validator = new JSONSchema(schema);
const isValid = validator.validate(agentManifest);
```

### 2. 字符限制管理
```typescript
// 验证辅助函数
function validateName(name: string): boolean {
  return name.length > 0 && name.length <= 100;
}

function validateDescription(description: string): boolean {
  return description.length > 0 && description.length <= 1000;
}

function validateInstructions(instructions: string): boolean {
  return instructions.length > 0 && instructions.length <= 8000;
}
```

### 3. 功能选择策略
- **从简单开始**: 从 1-2 个核心功能开始
- **渐进式添加**: 根据用户反馈添加功能
- **性能测试**: 彻底测试每个功能组合
- **企业就绪**: 考虑合规性和安全性影响

## Agents Playground 测试

### 本地测试设置
```bash
# 启动 Agents Playground
npm install -g @microsoft/agents-playground
agents-playground start --manifest=./agent.json
```

### 测试场景
1. **功能验证**: 测试每个声明的功能
2. **对话流程**: 验证对话启动器
3. **错误处理**: 测试无效输入和边缘情况
4. **性能**: 测量响应时间和可靠性

## 部署与生命周期管理

### 1. 开发生命周期
```mermaid
graph LR
    A[TypeSpec Definition] --> B[JSON Compilation]
    B --> C[Local Testing]
    C --> D[Validation]
    D --> E[Staging Deployment]
    E --> F[Production Release]
```

### 2. 版本管理
```json
{
  "name": "MyAgent v1.2.0",
  "description": "Production agent with enhanced capabilities",
  "version": "v1.5",
  "metadata": {
    "version": "1.2.0",
    "build": "20241208.1",
    "environment": "production"
  }
}
```

### 3. 环境提升
- **开发**: 完整调试、详细日志
- **测试**: 类生产测试、性能监控
- **生产**: 优化性能、最少日志

## 高级功能

### 行为覆盖
```json
{
  "instructions": "You are a specialized financial analyst agent. Always provide disclaimers for financial advice.",
  "behavior_overrides": {
    "response_tone": "professional",
    "max_response_length": 2000,
    "citation_requirements": true
  }
}
```

### 本地化支持
```json
{
  "name": {
    "en-US": "Financial Assistant",
    "es-ES": "Asistente Financiero",
    "fr-FR": "Assistant Financier"
  },
  "description": {
    "en-US": "Provides financial analysis and insights",
    "es-ES": "Proporciona análisis e insights financieros",
    "fr-FR": "Fournit des analyses et insights financiers"
  }
}
```

## 监控与分析

### 性能指标
- 每个功能的响应时间
- 用户与对话启动器的参与度
- 错误率和失败模式
- 功能利用率统计

### 日志策略
```typescript
// agent 交互的结构化日志
const log = {
  timestamp: new Date().toISOString(),
  agentName: "MyAgent",
  version: "1.2.0",
  userId: "user123",
  capability: "WebSearch",
  responseTime: 1250,
  success: true
};
```

## 安全与合规

### 数据隐私
- 为敏感信息实施适当的数据处理
- 确保符合 GDPR、CCPA 和组织政策
- 对企业功能使用适当的访问控制

### 安全考虑
- 验证所有输入和输出
- 实施速率限制和滥用防护
- 监控可疑活动模式
- 定期安全审计和更新

## 故障排除

### 常见问题
1. **Schema 验证错误**: 检查字符限制和必需字段
2. **功能冲突**: 验证功能组合是否受支持
3. **性能问题**: 监控响应时间并优化指令
4. **部署失败**: 验证环境配置和权限

### 调试工具
- TypeSpec 编译器诊断
- Agents Playground 调试
- Microsoft 365 Agents Toolkit 日志
- Schema 验证工具

这个综合指南确保了强大、可扩展且可维护的 Microsoft 365 Copilot 声明式 agent，具有完整的 TypeSpec 和 Microsoft 365 Agents Toolkit 集成。