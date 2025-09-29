---
description: '.NET MAUI组件和应用程序模式'
applyTo: '**/*.xaml, **/*.cs'
---

# .NET MAUI

## .NET MAUI代码风格和结构

- 编写惯用且高效的.NET MAUI和C#代码。
- 遵循.NET和.NET MAUI约定。
- 对较小的组件优先使用内联函数，但将复杂逻辑分离到代码后置或服务类中。
- 应在适用的地方使用Async/await来确保非阻塞UI操作。

## 命名约定

- 对组件名称、方法名称和公共成员遵循PascalCase。
- 对私有字段和局部变量使用camelCase。
- 接口名称以"I"为前缀（例如IUserService）。

## .NET MAUI和.NET特定指导原则

- 利用.NET MAUI的内置功能处理组件生命周期（例如OnAppearing、OnDisappearing）。
- 使用{Binding}有效地进行数据绑定。
- 遵循关注点分离原则构建.NET MAUI组件和服务。
- 始终使用最新版本的C#，目前是C# 13功能，如记录类型、模式匹配和全局using。

## 错误处理和验证

- 为.NET MAUI页面和API调用实现适当的错误处理。
- 在后端使用日志记录错误跟踪，并考虑使用MAUI Community Toolkit的Logger等工具在MAUI中捕获UI级别错误。
- 在表单中使用FluentValidation或DataAnnotations实现验证。

## MAUI API和性能优化

- 利用MAUI的内置功能处理组件生命周期（例如OnAppearing、OnDisappearing）。
- 对可能阻塞主线程的API调用或UI操作使用异步方法（async/await）。
- 通过减少不必要的渲染和高效使用OnPropertyChanged()来优化MAUI组件。
- 通过避免不必要的重新渲染来最小化组件渲染树，在适当的地方使用BatchBegin()和BatchCommit()。

## 缓存策略

- 对频繁使用的数据实现内存缓存，特别是对MAUI应用程序。对轻量级缓存解决方案使用IMemoryCache。
- 对需要跨多个用户或客户端共享状态的大型应用程序考虑分布式缓存策略（如Redis或SQL Server Cache）。
- 通过存储响应来缓存API调用，以避免在数据不太可能更改时进行冗余调用，从而改善用户体验。

## 状态管理库

- 使用依赖注入和.NET MAUI Community Toolkit在组件间共享状态。

## API设计和集成

- 使用HttpClient或其他适当的服务与外部API或您自己的后端通信。
- 对API调用使用try-catch实现错误处理，并在UI中提供适当的用户反馈。

## 测试和调试

- 使用xUnit、NUnit或MSTest测试组件和服务。
- 在测试期间使用Moq或NSubstitute模拟依赖项。

## 安全和认证

- 在必要时在MAUI应用程序中实现认证和授权，使用OAuth或JWT令牌进行API认证。
- 对所有网络通信使用HTTPS，确保实现适当的CORS策略。

## API文档和Swagger

- 对后端API服务使用Swagger/OpenAPI进行API文档。
- 确保为模型和API方法提供XML文档以增强Swagger文档。