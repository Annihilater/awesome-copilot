---
description: '使用 ASP.NET 构建 REST API 的指南'
applyTo: '**/*.cs, **/*.json'
---

# ASP.NET REST API 开发

## 指导说明
- 指导用户使用 ASP.NET Core 9 构建他们的第一个 REST API。
- 解释传统的 Web API 控制器和较新的 Minimal API 方法。
- 为每个实施决策提供教育背景，帮助用户理解底层概念。
- 强调 API 设计、测试、文档和部署的最佳实践。
- 专注于在代码示例的基础上提供解释，而不仅仅是实现功能。

## API 设计基础

- 解释 REST 架构原则及其如何应用于 ASP.NET Core API。
- 指导用户设计有意义的面向资源的 URL 和适当的 HTTP 动词使用。
- 演示传统基于控制器的 API 和 Minimal API 之间的差异。
- 在 REST 的背景下解释状态码、内容协商和响应格式。
- 帮助用户了解何时根据项目要求选择控制器 vs Minimal API。

## 项目设置和结构

- 指导用户使用适当的模板创建新的 ASP.NET Core 9 Web API 项目。
- 解释每个生成文件和文件夹的目的，建立对项目结构的理解。
- 演示如何使用功能文件夹或领域驱动设计原则组织代码。
- 展示模型、服务和数据访问层的正确关注点分离。
- 解释 ASP.NET Core 9 中的 Program.cs 和配置系统，包括环境特定设置。

## 构建基于控制器的 API

- 指导创建具有适当资源命名和 HTTP 动词实现的 RESTful 控制器。
- 解释属性路由及其相对于传统路由的优势。
- 演示模型绑定、验证和 [ApiController] 属性的作用。
- 展示依赖注入在控制器中的工作原理。
- 解释操作返回类型（IActionResult、ActionResult<T>、特定返回类型）以及何时使用每种类型。

## 实现 Minimal API

- 指导用户使用 Minimal API 语法实现相同的端点。
- 解释端点路由系统以及如何组织路由组。
- 演示 Minimal API 中的参数绑定、验证和依赖注入。
- 展示如何构建更大的 Minimal API 应用程序以保持可读性。
- 与基于控制器的方法进行比较和对比，帮助用户理解差异。

## 数据访问模式

- 指导使用 Entity Framework Core 实现数据访问层。
- 解释开发和生产的不同选项（SQL Server、SQLite、In-Memory）。
- 演示仓储模式实现以及何时有益。
- 展示如何实现数据库迁移和数据种子。
- 解释高效的查询模式以避免常见的性能问题。

## 身份验证和授权

- 指导用户使用 JWT Bearer 令牌实现身份验证。
- 解释与 ASP.NET Core 相关的 OAuth 2.0 和 OpenID Connect 概念。
- 展示如何实现基于角色和基于策略的授权。
- 演示与 Microsoft Entra ID（原 Azure AD）的集成。
- 解释如何一致地保护基于控制器和 Minimal API 的端点。

## 验证和错误处理

- 指导使用数据注解和 FluentValidation 实现模型验证。
- 解释验证管道以及如何自定义验证响应。
- 使用中间件演示全局异常处理策略。
- 展示如何创建跨 API 的一致错误响应。
- 解释问题详情（RFC 7807）实现标准化错误响应。

## API 版本控制和文档

- 指导用户实现和解释 API 版本控制策略。
- 演示具有适当文档的 Swagger/OpenAPI 实现。
- 展示如何记录端点、参数、响应和身份验证。
- 解释基于控制器和 Minimal API 中的版本控制。
- 指导用户创建有意义的 API 文档来帮助消费者。

## 日志记录和监控

- 指导使用 Serilog 或其他提供商实现结构化日志记录。
- 解释日志级别以及何时使用每个级别。
- 演示与 Application Insights 的集成以进行遥测收集。
- 展示如何实现自定义遥测和关联 ID 用于请求跟踪。
- 解释如何监控 API 性能、错误和使用模式。

## 测试 REST API

- 指导用户为控制器、Minimal API 端点和服务创建单元测试。
- 解释 API 端点的集成测试方法。
- 演示如何模拟依赖项以进行有效测试。
- 展示如何测试身份验证和授权逻辑。
- 解释应用于 API 开发的测试驱动开发原则。

## 性能优化

- 指导用户实现缓存策略（内存缓存、分布式缓存、响应缓存）。
- 解释异步编程模式以及它们对 API 性能的重要性。
- 为大数据集演示分页、过滤和排序。
- 展示如何实现压缩和其他性能优化。
- 解释如何测量和基准测试 API 性能。

## 部署和 DevOps

- 指导用户使用 .NET 的内置容器支持（`dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer`）容器化他们的 API。
- 解释手动 Dockerfile 创建与 .NET 的容器发布功能之间的差异。
- 解释 ASP.NET Core 应用程序的 CI/CD 管道。
- 演示部署到 Azure App Service、Azure Container Apps 或其他托管选项。
- 展示如何实现健康检查和就绪探针。
- 解释不同部署阶段的环境特定配置。
