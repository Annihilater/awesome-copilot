---
description: 'Oqtane 模块模式'
applyTo: '**/*.razor, **/*.razor.cs, **/*.razor.css'
---

## Blazor 代码风格和结构

- 编写符合习惯且高效的 Blazor 和 C# 代码。
- 遵循 .NET 和 Blazor 约定。
- 适当使用 Razor Components 进行基于组件的 UI 开发。
- 适当使用 Blazor Components 进行基于组件的 UI 开发。
- 对于较小的组件优先使用内联函数，但将复杂逻辑分离到代码后置或服务类中。
- 在适用的地方应使用 Async/await 以确保非阻塞的 UI 操作。


## 命名约定

- 对组件名称、方法名称和公共成员使用 PascalCase。
- 对私有字段和局部变量使用 camelCase。
- 接口名称以 "I" 为前缀（例如，IUserService）。

## Blazor 和 .NET 特定指南

- 利用 Blazor 的内置功能进行组件生命周期管理（例如，OnInitializedAsync、OnParametersSetAsync）。
- 有效使用 @bind 进行数据绑定。
- 在 Blazor 中利用依赖注入进行服务管理。
- 遵循关注点分离原则构建 Blazor 组件和服务。
- 始终使用最新版本的 C#，目前是 C# 13 功能，如记录类型、模式匹配和全局 using。

## Oqtane 特定指南
- 查看 [主要 Oqtane 仓库](https://github.com/oqtane/oqtane.framework) 中的基类和模式
- 遵循客户端服务器模式进行模块开发。
- Client 项目在 modules 文件夹中有各种模块。
- 客户端模块中的每个操作都是一个单独的 razor 文件，继承自 ModuleBase，其中 index.razor 是默认操作。
- 对于复杂的客户端处理（如获取数据），创建一个继承自 ServiceBase 的服务类，位于 services 文件夹中。每个模块一个服务类。
- 客户端服务应使用 ServiceBase 方法调用服务器端点
- Server 项目包含 MVC Controllers，每个模块一个，与客户端服务调用匹配。每个控制器将调用由 DI 管理的服务器端服务或存储库
- 服务器项目对模块使用存储库模式，每个模块一个存储库类以匹配控制器。

## 错误处理和验证

- 对 Blazor 页面和 API 调用实现适当的错误处理。
- 使用基类的内置 Oqtane 日志记录方法。
- 在后端使用日志记录进行错误跟踪，考虑在 Blazor 中使用 ErrorBoundary 等工具捕获 UI 级错误。
- 在表单中使用 FluentValidation 或 DataAnnotations 实现验证。

## Blazor API 和性能优化

- 根据项目需求最优地利用 Blazor 服务器端或 WebAssembly。
- 对可能阻塞主线程的 API 调用或 UI 操作使用异步方法（async/await）。
- 通过减少不必要的渲染并有效使用 StateHasChanged() 来优化 Razor 组件。
- 通过避免不必要的重新渲染来最小化组件渲染树，在适当的地方使用 ShouldRender()。
- 使用 EventCallbacks 高效处理用户交互，在触发事件时只传递最少的数据。

## 缓存策略

- 对经常使用的数据实现内存缓存，特别是对于 Blazor Server 应用。使用 IMemoryCache 进行轻量级缓存解决方案。
- 对于 Blazor WebAssembly，利用 localStorage 或 sessionStorage 在用户会话之间缓存应用状态。
- 对于需要在多个用户或客户端之间共享状态的大型应用，考虑分布式缓存策略（如 Redis 或 SQL Server Cache）。
- 通过存储响应来缓存 API 调用，以避免在数据不太可能更改时进行冗余调用，从而改善用户体验。

## 状态管理库

- 使用 Blazor 的内置级联参数和 EventCallbacks 在组件之间进行基本状态共享。
- 在适当时使用基类中内置的 Oqtane 状态管理，如 PageState 和 SiteState。
- 当应用程序在复杂性上增长时，避免添加额外的依赖项，如 Fluxor 或 BlazorState。
- 对于 Blazor WebAssembly 中的客户端状态持久化，考虑使用 Blazored.LocalStorage 或 Blazored.SessionStorage 在页面重新加载之间维护状态。
- 对于服务器端 Blazor，使用 Scoped Services 和 StateContainer 模式在用户会话内管理状态，同时最小化重新渲染。

## API 设计和集成

- 使用服务基类方法与外部 APIs 或服务器项目后端通信。
- 为 API 调用实现错误处理，使用 try-catch 并在 UI 中提供适当的用户反馈。

## 在 Visual Studio 中的测试和调试

- 所有单元测试和集成测试应在 Visual Studio Enterprise 中完成。
- 使用 xUnit、NUnit 或 MSTest 测试 Blazor 组件和服务。
- 在测试期间使用 Moq 或 NSubstitute 模拟依赖项。
- 使用浏览器开发者工具调试 Blazor UI 问题，使用 Visual Studio 的调试工具处理后端和服务器端问题。
- 对于性能分析和优化，依赖 Visual Studio 的诊断工具。

## 安全和身份验证

- 使用内置的 Oqtane 基类成员（如 User.Roles）实现身份验证和授权。
- 对所有 Web 通信使用 HTTPS，并确保实现适当的 CORS 策略。