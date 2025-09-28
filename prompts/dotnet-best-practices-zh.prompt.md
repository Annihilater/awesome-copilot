```markdown
---
mode: 'agent'
description: '确保 .NET/C# 代码符合解决方案/项目的最佳实践。'
---
# .NET/C# 最佳实践

您的任务是确保 ${selection} 中的 .NET/C# 代码符合此解决方案/项目的特定最佳实践。这包括：

## 文档与结构

- 为所有公共类、接口、方法和属性创建全面的 XML 文档注释
- 在 XML 注释中包括参数描述和返回值描述
- 遵循既定的命名空间结构：{Core|Console|App|Service}.{Feature}

## 设计模式与架构

- 使用主构造函数语法进行依赖注入（例如，`public class MyClass(IDependency dependency)`）
- 使用通用基类实现命令处理程序模式（例如，`CommandHandler<TOptions>`）
- 使用清晰命名约定的接口隔离（接口前缀为“I”）
- 遵循工厂模式进行复杂对象创建。

## 依赖注入与服务

- 使用构造函数依赖注入，并通过 ArgumentNullException 进行空值检查
- 使用适当的生命周期（Singleton、Scoped、Transient）注册服务
- 使用 Microsoft.Extensions.DependencyInjection 模式
- 实现用于可测试性的服务接口

## 资源管理与本地化

- 使用 ResourceManager 获取本地化的消息和错误字符串
- 分离 LogMessages 和 ErrorMessages 资源文件
- 通过 `_resourceManager.GetString("MessageKey")` 访问资源

## 异步/等待模式

- 对所有 I/O 操作和长时间运行的任务使用异步/等待
- 从异步方法返回 Task 或 Task<T>
- 在适当的地方使用 ConfigureAwait(false)
- 正确处理异步异常

## 测试标准

- 使用 MSTest 框架和 FluentAssertions 进行断言
- 遵循 AAA 模式（Arrange、Act、Assert）
- 使用 Moq 模拟依赖项
- 测试成功和失败两种场景
- 包括空参数验证测试

## 配置与设置

- 使用带有数据注释的强类型配置类
- 实现验证属性（Required、NotEmptyOrWhitespace）
- 使用 IConfiguration 绑定进行设置
- 支持 appsettings.json 配置文件

## Semantic Kernel 与 AI 集成

- 使用 Microsoft.SemanticKernel 进行 AI 操作
- 实现正确的内核配置和服务注册
- 处理 AI 模型设置（ChatCompletion、Embedding 等）
- 使用结构化输出模式以获得可靠的 AI 响应

## 错误处理与日志记录

- 使用 Microsoft.Extensions.Logging 进行结构化日志记录
- 包括具有有意义上下文的作用域日志记录
- 抛出具有描述性消息的特定异常
- 对预期的失败场景使用 try-catch 块

## 性能与安全

- 在适用的情况下使用 C# 12+ 功能和 .NET 8 优化
- 实现正确的输入验证和清理
- 对数据库操作使用参数化查询
- 遵循 AI/ML 操作的安全编码实践

## 代码质量

- 确保符合 SOLID 原则
- 通过基类和实用程序避免代码重复
- 使用反映领域概念的有意义的名称
- 保持方法专注和内聚
- 为资源实现正确的处置模式

```