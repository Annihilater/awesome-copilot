---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取 XUnit 单元测试的最佳实践，包括数据驱动测试"
---

# XUnit 最佳实践

你的目标是帮助我使用 XUnit 编写有效的单元测试，涵盖标准和数据驱动的测试方法。

## 项目设置

- 使用单独的测试项目，命名约定为 `[ProjectName].Tests`
- 引用 Microsoft.NET.Test.Sdk、xunit 和 xunit.runner.visualstudio 包
- 创建与被测类匹配的测试类（例如，`Calculator` 对应 `CalculatorTests`）
- 使用 .NET SDK 测试命令：`dotnet test` 运行测试

## 测试结构

- 无需测试类属性（与 MSTest/NUnit 不同）
- 对简单测试使用基于事实的测试，并使用 `[Fact]` 属性
- 遵循 Arrange-Act-Assert (AAA) 模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用构造函数进行设置，使用 `IDisposable.Dispose()` 进行拆卸
- 使用 `IClassFixture<T>` 在一个类中的测试之间共享上下文
- 使用 `ICollectionFixture<T>` 在多个测试类之间共享上下文

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言来表达意图
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可以按任何顺序运行）
- 避免测试相互依赖

## 数据驱动测试

- 将 `[Theory]` 与数据源属性结合使用
- 对内联测试数据使用 `[InlineData]`
- 对基于方法的测试数据使用 `[MemberData]`
- 对基于类的测试数据使用 `[ClassData]`
- 通过实现 `DataAttribute` 创建自定义数据属性
- 在数据驱动测试中使用有意义的参数名称

## 断言

- 对值相等性使用 `Assert.Equal`
- 对引用相等性使用 `Assert.Same`
- 对布尔条件使用 `Assert.True`/`Assert.False`
- 对集合使用 `Assert.Contains`/`Assert.DoesNotContain`
- 对正则表达式模式匹配使用 `Assert.Matches`/`Assert.DoesNotMatch`
- 使用 `Assert.Throws<T>` 或 `await Assert.ThrowsAsync<T>` 测试异常
- 使用流式断言库以获得更具可读性的断言

## mock 和隔离

- 考虑将 Moq 或 NSubstitute 与 XUnit 一起使用
- 模拟依赖项以隔离被测单元
- 使用接口以方便模拟
- 考虑对复杂的测试设置使用 DI 容器

## 测试组织

- 按功能或组件对测试进行分组
- 使用 `[Trait("Category", "CategoryName")]` 进行分类
- 使用集合装置对具有共享依赖项的测试进行分组
- 考虑使用输出帮助程序 (`ITestOutputHelper`) 进行测试诊断
- 使用 `Skip = "reason"` 在事实/理论属性中有条件地跳过测试
