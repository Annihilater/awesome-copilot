---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取 NUnit 单元测试的最佳实践，包括数据驱动测试"
---

# NUnit 最佳实践

你的目标是帮助我使用 NUnit 编写有效的单元测试，涵盖标准和数据驱动的测试方法。

## 项目设置

- 使用单独的测试项目，命名约定为 `[ProjectName].Tests`
- 引用 Microsoft.NET.Test.Sdk、NUnit 和 NUnit3TestAdapter 包
- 创建与被测类匹配的测试类（例如，`Calculator` 对应 `CalculatorTests`）
- 使用 .NET SDK 测试命令：`dotnet test` 运行测试

## 测试结构

- 将 `[TestFixture]` 属性应用于测试类
- 对测试方法使用 `[Test]` 属性
- 遵循 Arrange-Act-Assert (AAA) 模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用 `[SetUp]` 和 `[TearDown]` 进行每个测试的设置和拆卸
- 使用 `[OneTimeSetUp]` 和 `[OneTimeTearDown]` 进行每个类的设置和拆卸
- 使用 `[SetUpFixture]` 进行程序集级别的设置和拆卸

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言来表达意图
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可以按任何顺序运行）
- 避免测试相互依赖

## 数据驱动测试

- 对内联测试数据使用 `[TestCase]`
- 对以编程方式生成的测试数据使用 `[TestCaseSource]`
- 对简单的参数组合使用 `[Values]`
- 对基于属性或方法的数据源使用 `[ValueSource]`
- 对随机数值测试值使用 `[Random]`
- 对顺序数值测试值使用 `[Range]`
- 对组合多个参数使用 `[Combinatorial]` 或 `[Pairwise]`

## 断言

- 将 `Assert.That` 与约束模型一起使用（首选的 NUnit 样式）
- 使用 `Is.EqualTo`、`Is.SameAs`、`Contains.Item` 等约束
- 对简单的值相等性使用 `Assert.AreEqual`（经典样式）
- 对集合比较使用 `CollectionAssert`
- 对特定于字符串的断言使用 `StringAssert`
- 使用 `Assert.Throws<T>` 或 `Assert.ThrowsAsync<T>` 测试异常
- 在断言中使用描述性消息以便在失败时清晰明了

## 模拟和隔离

- 考虑将 Moq 或 NSubstitute 与 NUnit 一起使用
- 模拟依赖项以隔离被测单元
- 使用接口以方便模拟
- 考虑对复杂的测试设置使用 DI 容器

## 测试组织

- 按功能或组件对测试进行分组
- 使用 `[Category("CategoryName")]` 的类别
- 在必要时使用 `[Order]` 控制测试执行顺序
- 使用 `[Author("DeveloperName")]` 指示所有权
- 使用 `[Description]` 提供其他测试信息
- 考虑对不应自动运行的测试使用 `[Explicit]`
- 使用 `[Ignore("Reason")]` 临时跳过测试
