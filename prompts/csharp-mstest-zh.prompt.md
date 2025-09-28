---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取 MSTest 单元测试的最佳实践，包括数据驱动测试"
---

# MSTest 最佳实践

你的目标是帮助我使用 MSTest 编写有效的单元测试，涵盖标准和数据驱动的测试方法。

## 项目设置

- 使用单独的测试项目，命名约定为 `[ProjectName].Tests`
- 引用 MSTest 包
- 创建与被测类匹配的测试类（例如，`Calculator` 对应 `CalculatorTests`）
- 使用 .NET SDK 测试命令：`dotnet test` 运行测试

## 测试结构

- 对测试类使用 `[TestClass]` 属性
- 对测试方法使用 `[TestMethod]` 属性
- 遵循 Arrange-Act-Assert (AAA) 模式
- 使用 `MethodName_Scenario_ExpectedBehavior` 模式命名测试
- 使用 `[TestInitialize]` 和 `[TestCleanup]` 进行每个测试的设置和拆卸
- 使用 `[ClassInitialize]` 和 `[ClassCleanup]` 进行每个类的设置和拆卸
- 使用 `[AssemblyInitialize]` 和 `[AssemblyCleanup]` 进行程序集级别的设置和拆卸

## 标准测试

- 保持测试专注于单一行为
- 避免在一个测试方法中测试多个行为
- 使用清晰的断言来表达意图
- 仅包含验证测试用例所需的断言
- 使测试独立且幂等（可以按任何顺序运行）
- 避免测试相互依赖

## 数据驱动测试

- 将 `[TestMethod]` 与数据源属性结合使用
- 对内联测试数据使用 `[DataRow]`
- 对以编程方式生成的测试数据使用 `[DynamicData]`
- 使用 `[TestProperty]` 向测试添加元数据
- 在数据驱动测试中使用有意义的参数名称

## 断言

- 对值相等性使用 `Assert.AreEqual`
- 对引用相等性使用 `Assert.AreSame`
- 对布尔条件使用 `Assert.IsTrue`/`Assert.IsFalse`
- 对集合比较使用 `CollectionAssert`
- 对特定于字符串的断言使用 `StringAssert`
- 使用 `Assert.Throws<T>` 测试异常
- 确保断言本质上是简单的，并提供消息以便在失败时清晰明了

## 模拟和隔离

- 考虑将 Moq 或 NSubstitute 与 MSTest 一起使用
- 模拟依赖项以隔离被测单元
- 使用接口以方便模拟
- 考虑对复杂的测试设置使用 DI 容器

## 测试组织

- 按功能或组件对测试进行分组
- 使用 `[TestCategory("Category")]` 的测试类别
- 对关键测试使用 `[Priority(1)]` 的测试优先级
- 使用 `[Owner("DeveloperName")]` 指示所有权
