---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取 TUnit 单元测试的最佳实践，包括数据驱动测试"
---

# TUnit 最佳实践

你的目标是帮助我使用 TUnit 编写有效的单元测试，涵盖标准和数据驱动的测试方法。

## 项目设置

- 使用单独的测试项目，命名约定为 `[ProjectName].Tests`
- 引用 TUnit 包和 TUnit.Assertions 以进行流式断言
- 创建与被测类匹配的测试类（例如，`Calculator` 对应 `CalculatorTests`）
- 使用 .NET SDK 测试命令：`dotnet test` 运行测试
- TUnit 需要 .NET 8.0 或更高版本

## 测试结构

- 无需测试类属性（如 xUnit/NUnit）
- 对测试方法使用 `[Test]` 属性（不像 xUnit 那样使用 `[Fact]`）
- 遵循 Arrange-Act-Assert (AAA) 模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用生命周期挂钩：`[Before(Test)]` 用于设置，`[After(Test)]` 用于拆卸
- 使用 `[Before(Class)]` 和 `[After(Class)]` 在一个类中的测试之间共享上下文
- 使用 `[Before(Assembly)]` 和 `[After(Assembly)]` 在测试类之间共享上下文
- TUnit 支持高级生命周期挂钩，如 `[Before(TestSession)]` 和 `[After(TestSession)]`

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用 TUnit 的流式断言语法 `await Assert.That()`
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可以按任何顺序运行）
- 避免测试相互依赖（如果需要，使用 `[DependsOn]` 属性）

## 数据驱动测试

- 对内联测试数据使用 `[Arguments]` 属性（等效于 xUnit 的 `[InlineData]`）
- 对基于方法的测试数据使用 `[MethodData]` 属性（等效于 xUnit 的 `[MemberData]`）
- 对基于类的测试数据使用 `[ClassData]`
- 通过实现 `ITestDataSource` 创建自定义数据源
- 在数据驱动测试中使用有意义的参数名称
- 可以将多个 `[Arguments]` 属性应用于同一个测试方法

## 断言

- 对值相等性使用 `await Assert.That(value).IsEqualTo(expected)`
- 对引用相等性使用 `await Assert.That(value).IsSameReferenceAs(expected)`
- 对布尔条件使用 `await Assert.That(value).IsTrue()` 或 `await Assert.That(value).IsFalse()`
- 对集合使用 `await Assert.That(collection).Contains(item)` 或 `await Assert.That(collection).DoesNotContain(item)`
- 对正则表达式模式匹配使用 `await Assert.That(value).Matches(pattern)`
- 使用 `await Assert.That(action).Throws<TException>()` 或 `await Assert.That(asyncAction).ThrowsAsync<TException>()` 测试异常
- 使用 `.And` 运算符链接断言：`await Assert.That(value).IsNotNull().And.IsEqualTo(expected)`
- 使用 `.Or` 运算符表示替代条件：`await Assert.That(value).IsEqualTo(1).Or.IsEqualTo(2)`
- 对具有容差的 DateTime 和数值比较使用 `.Within(tolerance)`
- 所有断言都是异步的，必须等待

## 高级功能

- 使用 `[Repeat(n)]` 多次重复测试
- 对失败时自动重试使用 `[Retry(n)]`
- 使用 `[ParallelLimit<T>]` 控制并行执行限制
- 使用 `[Skip("reason")]` 有条件地跳过测试
- 使用 `[DependsOn(nameof(OtherTest))]` 创建测试依赖项
- 使用 `[Timeout(milliseconds)]` 设置测试超时
- 通过扩展 TUnit 的基属性创建自定义属性

## 测试组织

- 按功能或组件对测试进行分组
- 对测试分类使用 `[Category("CategoryName")]`
- 对自定义测试名称使用 `[DisplayName("Custom Test Name")]`
- 考虑使用 `TestContext` 进行测试诊断和信息
- 对特定于平台的测试使用自定义的 `[WindowsOnly]` 等条件属性

## 性能和并行执行

- TUnit 默认并行运行测试（不像 xUnit 需要显式配置）
- 使用 `[NotInParallel]` 禁用特定测试的并行执行
- 使用 `[ParallelLimit<T>]` 和自定义限制类来控制并发
- 同一个类中的测试默认按顺序运行
- 将 `[Repeat(n)]` 与 `[ParallelLimit<T>]` 一起用于负载测试场景

## 从 xUnit 迁移

- 将 `[Fact]` 替换为 `[Test]`
- 将 `[Theory]` 替换为 `[Test]` 并使用 `[Arguments]` 获取数据
- 将 `[InlineData]` 替换为 `[Arguments]`
- 将 `[MemberData]` 替换为 `[MethodData]`
- 将 `Assert.Equal` 替换为 `await Assert.That(actual).IsEqualTo(expected)`
- 将 `Assert.True` 替换为 `await Assert.That(condition).IsTrue()`
- 将 `Assert.Throws<T>` 替换为 `await Assert.That(action).Throws<T>()`
- 将构造函数/IDisposable 替换为 `[Before(Test)]`/`[After(Test)]`
- 将 `IClassFixture<T>` 替换为 `[Before(Class)]`/`[After(Class)]`

**为什么选择 TUnit 而不是 xUnit？**

- TUnit 默认并行运行测试，而 xUnit 需要显式配置。
- TUnit 具有更丰富的生命周期挂钩，包括 `[Before(TestSession)]` 和 `[After(TestSession)]`。
- TUnit 具有更丰富的断言，包括 `And` 和 `Or` 运算符。
- TUnit 具有更丰富的属性，包括 `[Repeat]`、`[Retry]` 和 `[DependsOn]`。
- TUnit 具有更丰富的条件属性，包括自定义的 `[WindowsOnly]`。
- TUnit 具有更丰富的并行执行控制，包括 `[ParallelLimit<T>]`。
- TUnit 具有更丰富的测试组织，包括 `[DisplayName]`。
- TUnit 具有更丰富的测试上下文，包括 `TestContext`。
- TUnit 具有更丰富的迁移指南，包括从 xUnit 迁移。
