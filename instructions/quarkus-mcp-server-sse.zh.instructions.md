---
applyTo: '*'
description: 'Quarkus 和 MCP Server 使用 HTTP SSE 传输开发标准和指令'
---
# Quarkus MCP Server

使用 Java 21、Quarkus 和 HTTP SSE 传输构建 MCP 服务器。

## 技术栈

- Java 21 与 Quarkus 框架
- MCP Server 扩展：`mcp-server-sse`
- CDI 用于依赖注入
- MCP 端点：`http://localhost:8080/mcp/sse`

## 快速开始

```bash
quarkus create app --no-code -x rest-client-jackson,qute,mcp-server-sse your-domain-mcp-server
```

## 结构

- 使用标准 Java 命名约定（PascalCase 类，camelCase 方法）
- 按包组织：`model`、`repository`、`service`、`mcp`
- 对不可变数据模型使用 Record 类型
- 不可变数据的状态管理必须由存储库层管理
- 为公共方法添加 Javadoc

## MCP 工具

- 必须是 `@ApplicationScoped` CDI bean 中的公共方法
- 使用 `@Tool(name="tool_name", description="clear description")`
- 永远不要返回 `null` — 改为返回错误消息
- 始终验证参数并优雅地处理错误

## 架构

- 分离关注点：MCP 工具 → 服务层 → 存储库
- 使用 `@Inject` 进行依赖注入
- 使数据操作线程安全
- 使用 `Optional<T>` 避免空指针异常

## 常见问题

- 不要在 MCP 工具中放置业务逻辑（使用服务层）
- 不要从工具中抛出异常（返回错误字符串）
- 不要忘记验证输入参数
- 使用边缘情况进行测试（null、空输入）