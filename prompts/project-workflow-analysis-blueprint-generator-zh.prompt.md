---
description: "与技术栈无关的端到端应用流程文档生成器。自动检测项目架构模式、技术栈与数据流模式，生成涵盖入口、服务层、数据访问、错误处理与测试方案的详细实施蓝图，适用于 .NET、Java/Spring、React 及微服务架构等多种技术。"
mode: "agent"
---
# 项目工作流文档生成器

## 配置变量

```
${PROJECT_TYPE="Auto-detect|.NET|Java|Spring|Node.js|Python|React|Angular|Microservices|Other"}
<!-- 主要技术栈 -->

${ENTRY_POINT="API|GraphQL|Frontend|CLI|Message Consumer|Scheduled Job|Custom"}
<!-- 流程起点 -->

${PERSISTENCE_TYPE="Auto-detect|SQL Database|NoSQL Database|File System|External API|Message Queue|Cache|None"}
<!-- 数据存储类型 -->

${ARCHITECTURE_PATTERN="Auto-detect|Layered|Clean|CQRS|Microservices|MVC|MVVM|Serverless|Event-Driven|Other"}
<!-- 主要架构模式 -->

${WORKFLOW_COUNT=1-5}
<!-- 需要记录的工作流数量 -->

${DETAIL_LEVEL="Standard|Implementation-Ready"}
<!-- 输出的实施细节级别 -->

${INCLUDE_SEQUENCE_DIAGRAM=true|false}
<!-- 是否生成时序图 -->

${INCLUDE_TEST_PATTERNS=true|false}
<!-- 是否包含测试方案 -->
```

## 生成的提示词

```
"Analyze the codebase and document ${WORKFLOW_COUNT} representative end-to-end workflows 
that can serve as implementation templates for similar features. Use the following approach:
```

### 初始检测阶段

```
${PROJECT_TYPE == "Auto-detect" ? 
  "Begin by examining the codebase structure to identify technologies:
   - Check for .NET solutions/projects, Spring configurations, Node.js/Express files, etc.
   - Identify the primary programming language(s) and frameworks in use
   - Determine the architectural patterns based on folder structure and key components" 
  : "Focus on ${PROJECT_TYPE} patterns and conventions"}
```

```
${ENTRY_POINT == "Auto-detect" ? 
  "Identify typical entry points by looking for:
   - API controllers or route definitions
   - GraphQL resolvers
   - UI components that initiate network requests
   - Message handlers or event subscribers
   - Scheduled job definitions" 
  : "Focus on ${ENTRY_POINT} entry points"}
```

```
${PERSISTENCE_TYPE == "Auto-detect" ? 
  "Determine persistence mechanisms by examining:
   - Database context/connection configurations
   - Repository implementations
   - ORM mappings
   - External API clients
   - File system interactions" 
  : "Focus on ${PERSISTENCE_TYPE} interactions"}
```

### 工作流文档编写指引

针对系统中最具代表性的 `${WORKFLOW_COUNT}` 个工作流，依次完成以下内容：

#### 1. 工作流概览
   - 提供工作流名称与简要描述
   - 说明业务目标
   - 标识触发动作或事件
   - 列出完整流程涉及的所有文件/类

#### 2. 入口实现

**API 入口：**
```
${ENTRY_POINT == "API" || ENTRY_POINT == "Auto-detect" ? 
  "- Document the API controller class and method that receives the request
   - Show the complete method signature including attributes/annotations
   - Include the full request DTO/model class definition
   - Document validation attributes and custom validators
   - Show authentication/authorization attributes and checks" : ""}
```

**GraphQL 入口：**
```
${ENTRY_POINT == "GraphQL" || ENTRY_POINT == "Auto-detect" ? 
  "- Document the GraphQL resolver class and method
   - Show the complete schema definition for the query/mutation
   - Include input type definitions
   - Show resolver method implementation with parameter handling" : ""}
```

**前端入口：**
```
${ENTRY_POINT == "Frontend" || ENTRY_POINT == "Auto-detect" ? 
  "- Document the component that initiates the API call
   - Show the event handler that triggers the request
   - Include the API client service method
   - Show state management code related to the request" : ""}
```

**消息消费入口：**
```
${ENTRY_POINT == "Message Consumer" || ENTRY_POINT == "Auto-detect" ? 
  "- Document the message handler class and method
   - Show message subscription configuration
   - Include the complete message model definition
   - Show deserialization and validation logic" : ""}
```

#### 3. 服务层实现
   - 记录涉及的每个服务类及其依赖
   - 展示完整方法签名（参数与返回类型）
   - 包含关键业务逻辑的实际实现
   - 在适用场景记录接口定义
   - 展示依赖注入注册模式

**CQRS 模式：**
```
${ARCHITECTURE_PATTERN == "CQRS" || ARCHITECTURE_PATTERN == "Auto-detect" ? 
  "- Include complete command/query handler implementations" : ""}
```

**整洁架构模式：**
```
${ARCHITECTURE_PATTERN == "Clean" || ARCHITECTURE_PATTERN == "Auto-detect" ? 
  "- Show use case/interactor implementations" : ""}
```

#### 4. 数据映射模式
   - 记录 DTO 与领域模型的映射代码
   - 展示对象映射配置或手动映射方法
   - 包含映射过程中的校验逻辑
   - 记录映射过程中产生的领域事件

#### 5. 数据访问实现
   - 记录仓储接口及其实现
   - 展示完整方法签名（参数与返回类型）
   - 包含实际查询实现
   - 记录实体/模型类定义与全部属性
   - 展示事务处理模式

**SQL 数据库模式：**
```
${PERSISTENCE_TYPE == "SQL Database" || PERSISTENCE_TYPE == "Auto-detect" ? 
  "- Include ORM configurations, annotations, or Fluent API usage
   - Show actual SQL queries or ORM statements" : ""}
```

**NoSQL 数据库模式：**
```
${PERSISTENCE_TYPE == "NoSQL Database" || PERSISTENCE_TYPE == "Auto-detect" ? 
  "- Show document structure definitions
   - Include document query/update operations" : ""}
```

#### 6. 响应构建
   - 记录响应 DTO/模型类定义
   - 展示领域/实体模型到响应模型的映射
   - 包含状态码选择逻辑
   - 记录错误响应结构与生成方式

#### 7. 错误处理模式
   - 记录工作流中使用的异常类型
   - 展示各层的 try/catch 模式
   - 包含全局异常处理配置
   - 记录错误日志实现
   - 展示重试策略或断路器模式
   - 记录失败场景下的补偿措施

#### 8. 异步处理模式
   - 记录后台任务调度代码
   - 展示事件发布实现
   - 包含消息队列发送模式
   - 记录回调或 Webhook 实现
   - 展示异步操作的跟踪与监控方式

**测试方案（可选）：**
```
${INCLUDE_TEST_PATTERNS ? 
  "9. **Testing Approach**
     - Document unit test implementations for each layer
     - Show mocking patterns and test fixture setup
     - Include integration test implementations
     - Document test data generation approaches
     - Show API/controller test implementations" : ""}
```

**时序图（可选）：**
```
${INCLUDE_SEQUENCE_DIAGRAM ? 
  "10. **Sequence Diagram**
      - Generate a detailed sequence diagram showing all components
      - Include method calls with parameter types
      - Show return values between components
      - Document conditional flows and error paths" : ""}
```

#### 11. 命名约定
记录以下内容的统一模式：
- 控制器命名（如 `EntityNameController`）
- 服务命名（如 `EntityNameService`）
- 仓储命名（如 `IEntityNameRepository`）
- DTO 命名（如 `EntityNameRequest`、`EntityNameResponse`）
- CRUD 方法的命名规范
- 变量命名约定
- 文件组织模式

#### 12. 实施模板
提供可复用的代码模板，用于：
- 按既定模式创建新 API 端点
- 实现新的服务方法
- 添加新的仓储方法
- 创建新的领域模型类
- 实现完整的错误处理

### 按技术栈定制的实施模式

**.NET 实施模式（如检测到）：**
```
${PROJECT_TYPE == ".NET" || PROJECT_TYPE == "Auto-detect" ? 
  "- Complete controller class with attributes, filters, and dependency injection
   - Service registration in Startup.cs or Program.cs
   - Entity Framework DbContext configuration
   - Repository implementation with EF Core or Dapper
   - AutoMapper profile configurations
   - Middleware implementations for cross-cutting concerns
   - Extension method patterns
   - Options pattern implementation for configuration
   - Logging implementation with ILogger
   - Authentication/authorization filter or policy implementations" : ""}
```

**Spring 实施模式（如检测到）：**
```
${PROJECT_TYPE == "Java" || PROJECT_TYPE == "Spring" || PROJECT_TYPE == "Auto-detect" ? 
  "- Complete controller class with annotations and dependency injection
   - Service implementation with transaction boundaries
   - Repository interface and implementation
   - JPA entity definitions with relationships
   - DTO class implementations
   - Bean configuration and component scanning
   - Exception handler implementations
   - Custom validator implementations" : ""}
```

**React 实施模式（如检测到）：**
```
${PROJECT_TYPE == "React" || PROJECT_TYPE == "Auto-detect" ? 
  "- Component structure with props and state
   - Hook implementation patterns (useState, useEffect, custom hooks)
   - API service implementation
   - State management patterns (Context, Redux)
   - Form handling implementations
   - Route configuration" : ""}
```

### 实施指南

基于已记录的工作流，为新功能的开发提供具体指导：

#### 1. 步骤化实施流程
- 新增类似功能时的起点
- 实施顺序（如 模型 → 仓储 → 服务 → 控制器）
- 如何整合现有的横切关注点

#### 2. 需要避免的常见陷阱
- 指出现有实现中容易出错的环节
- 提醒性能方面的注意事项
- 列出常见缺陷或问题

#### 3. 扩展机制
- 说明如何接入现有扩展点
- 展示如何在不修改原有代码的情况下添加新行为
- 解释基于配置驱动的功能模式

**结论：**
以总结结束，概述在实现新功能时应遵循的关键模式，以保持与现有代码库的一致性。"

