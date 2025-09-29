---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取 JUnit 5 单元测试的最佳实践，包括数据驱动测试"
---

# JUnit 5+ 最佳实践

您的目标是帮助我使用 JUnit 5 编写有效的单元测试，涵盖标准和数据驱动的测试方法。

## 项目设置

- 使用标准的 Maven 或 Gradle 项目结构。
- 将测试源代码放在 `src/test/java` 中。
- 为参数化测试添加 `junit-jupiter-api`、`junit-jupiter-engine` 和 `junit-jupiter-params` 的依赖项。
- 使用构建工具命令运行测试：`mvn test` 或 `gradle test`。

## 测试结构

- 测试类应具有 `Test` 后缀，例如 `Calculator` 类的 `CalculatorTest`。
- 对测试方法使用 `@Test`。
- 遵循 Arrange-Act-Assert (AAA) 模式。
- 使用描述性约定命名测试，例如 `methodName_should_expectedBehavior_when_scenario`。
- 使用 `@BeforeEach` 和 `@AfterEach` 进行每个测试的设置和拆卸。
- 使用 `@BeforeAll` 和 `@AfterAll` 进行每个类的设置和拆卸（必须是静态方法）。
- 使用 `@DisplayName` 为测试类和方法提供人类可读的名称。

## 标准测试

- 保持测试专注于单一行为。
- 避免在一个测试方法中测试多个条件。
- 使测试独立且幂等（可以按任何顺序运行）。
- 避免测试之间的相互依赖。

## 数据驱动（参数化）测试

- 使用 `@ParameterizedTest` 将方法标记为参数化测试。
- 对简单的文字值（字符串、整数等）使用 `@ValueSource`。
- 使用 `@MethodSource` 引用一个工厂方法，该方法以 `Stream`、`Collection` 等形式提供测试参数。
- 对内联逗号分隔值使用 `@CsvSource`。
- 使用 `@CsvFileSource` 从类路径中使用 CSV 文件。
- 使用 `@EnumSource` 使用枚举常量。

## 断言

- 使用 `org.junit.jupiter.api.Assertions` 中的静态方法（例如 `assertEquals`、`assertTrue`、`assertNotNull`）。
- 为了获得更流畅、更易读的断言，请考虑使用像 AssertJ (`assertThat(...).is...`) 这样的库。
- 使用 `assertThrows` 或 `assertDoesNotThrow` 来测试异常。
- 使用 `assertAll` 对相关断言进行分组，以确保在测试失败之前检查所有断言。
- 在断言中使用描述性消息以提供失败时的清晰度。

## 模拟和隔离

- 使用像 Mockito 这样的模拟框架为依赖项创建模拟对象。
- 使用 Mockito 中的 `@Mock` 和 `@InjectMocks` 注解来简化模拟创建和注入。
- 使用接口来方便模拟。

## 测试组织

- 使用包按功能或组件对测试进行分组。
- 使用 `@Tag` 对测试进行分类（例如 `@Tag("fast")`、`@Tag("integration")`）。
- 在严格必要时，使用 `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` 和 `@Order` 来控制测试执行顺序。
- 使用 `@Disabled` 暂时跳过测试方法或类，并提供原因。
- 使用 `@Nested` 将测试分组在嵌套的内部类中，以获得更好的组织和结构。

```

```
