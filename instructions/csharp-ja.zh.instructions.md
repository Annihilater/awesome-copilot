---
description: 'C# 应用程序构建指导原则 by @tsubakimoto'
applyTo: '**/*.cs'
---

# C# 应用程序开发

## C# 指导原则
- 始终使用最新的 C#。目前是 C# 13 功能。
- 为每个函数编写清晰简洁的注释。

## 通用指导原则
- 在代码更改审查中，仅提出高可信度的建议。
- 编写具有良好可维护性实践的代码，包括对设计决策原因的注释。
- 处理边缘情况并编写清晰的异常处理。
- 对于库和外部依赖项，在注释中明确其用途和目的。

## 命名约定

- 组件名、方法名、公共成员使用 PascalCase。
- 私有字段和局部变量使用 camelCase。
- 接口名以"I"为前缀（例：IUserService）。

## 格式化

- 应用 `.editorconfig` 中定义的代码格式样式。
- 推荐使用文件作用域的 namespace 声明和单行 using 指令。
- 在任何代码块（if、for、while、foreach、using、try 等）的开始大括号前换行。
- 方法的最终 return 语句单独占一行。
- 尽可能使用模式匹配和 switch 表达式。
- 使用 `nameof` 而不是字符串字面量来引用成员名。
- 为所有公共 API 创建 XML 文档注释。如果可能的话，还包括 `<example>` 和 `<code>`。

## 项目设置和配置

- 指导如何使用适当的模板创建新的 .NET 项目。
- 解释生成的每个文件和文件夹的目的，帮助理解项目结构。
- 展示功能文件夹或领域驱动设计（DDD）的组织方法。
- 展示通过模型、服务、数据访问层的职责分离。
- 解释 ASP.NET Core 9 中的 Program.cs 和配置系统，以及环境特定设置。

## Nullable 引用类型

- 变量声明为非 null，在入口点检查 `null`。
- 始终使用 `is null` 或 `is not null`，而不是 `== null` 或 `!= null`。
- 信任 C# 的 null 注释，当类型系统保证值非 null 时，不要添加不必要的 null 检查。

## 数据访问模式

- 指导使用 Entity Framework Core 实现数据访问层。
- 解释开发和生产中的选择（SQL Server、SQLite、In-Memory）。
- 展示仓储模式的实现以及其有效应用场景。
- 展示数据库迁移和数据种子的实现方法。
- 解释避免常见性能问题的高效查询模式。

## 认证和授权

- 指导使用 JWT Bearer 令牌实现身份验证。
- 解释与 ASP.NET Core 相关的 OAuth 2.0 和 OpenID Connect 概念。
- 展示基于角色和基于策略的授权实现方法。
- 展示与 Microsoft Entra ID（原 Azure AD）的集成。
- 解释如何一致地保护基于控制器的 API 和 Minimal API。

## 验证和错误处理

- 指导使用数据注释和 FluentValidation 实现模型验证。
- 解释验证管道和自定义验证响应的方法。
- 展示使用中间件的全局异常处理策略。
- 展示如何在整个 API 中创建一致的错误响应。
- 解释为标准化错误响应实现 Problem Details（RFC 7807）。

## API 版本控制和文档

- 指导 API 版本控制策略的实现和解释。
- 展示带有适当文档的 Swagger / OpenAPI 实现。
- 展示如何记录端点、参数、响应和身份验证。
- 解释基于控制器的 API 和 Minimal API 的版本控制。
- 指导创建对用户有用的有意义的 API 文档。

## 日志记录和监控

- 指导使用 Serilog 等实现结构化日志记录。
- 解释日志级别以及各自应该使用的场景。
- 展示与 Application Insights 的集成以收集遥测数据。
- 展示如何实现自定义遥测和相关 ID 以进行请求跟踪。
- 解释如何监控 API 的性能、错误和使用模式。

## 测试

- 应用程序的关键路径必须包含测试用例。
- 指导单元测试的创建。
- 不写"Act"、"Arrange"、"Assert"注释。
- 匹配邻近文件的现有样式（测试方法名称和大小写）。
- 解释 API 端点的集成测试技术。
- 展示如何模拟依赖项以进行有效测试。
- 展示如何测试身份验证和授权逻辑。
- 解释适用于 API 开发的测试驱动开发（TDD）原则。

## 性能优化

- 指导缓存策略（内存中、分布式、响应缓存）的实现。
- 解释异步编程模式以及为什么它对 API 性能很重要。
- 展示针对大型数据集的分页、过滤和排序。
- 展示如何实现压缩等性能优化。
- 解释如何测量和基准测试 API 性能。

## 部署和 DevOps

- 指导使用 .NET 内置容器支持（`dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer`）对 API 进行容器化。
- 解释手动创建 Dockerfile 与 .NET 容器发布功能的区别。
- 解释针对 .NET 应用程序的 CI/CD 管道。
- 展示部署到 Azure App Service、Azure Container Apps 和其他托管选项。
- 展示如何实现健康检查和 Readiness Probe。
- 解释每个部署阶段的环境特定配置。