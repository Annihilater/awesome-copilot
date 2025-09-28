---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取使用 Kotlin 构建 Spring Boot 应用程序的最佳实践。"
---

# Spring Boot 与 Kotlin 最佳实践

你的目标是帮助我编写高质量、地道的 Kotlin Spring Boot 应用程序。

## 项目初始化与结构

- **构建工具：** 使用 Maven（`pom.xml`）或 Gradle（`build.gradle`），并启用 Kotlin 插件（`kotlin-maven-plugin` 或 `org.jetbrains.kotlin.jvm`）。
- **Kotlin 插件：** 针对 JPA，启用 `kotlin-jpa` 插件，以便无需样板代码即可自动将实体类设为 `open`。
- **Starters：** 常规使用 Spring Boot Starters（例如 `spring-boot-starter-web`、`spring-boot-starter-data-jpa`）。
- **包结构：** 以领域/功能划分代码（如 `com.example.app.order`、`com.example.app.user`），而非按分层划分。

## 依赖注入与组件

- **主构造函数：** 必要的依赖注入始终使用主构造函数，这是最符合 Kotlin 习惯的方式。
- **不可变性：** 在主构造函数中将依赖声明为 `private val`。优先使用 `val` 而非 `var`，以强化不可变性。
- **组件立场：** 与 Java 一样使用 `@Service`、`@Repository`、`@RestController` 等注解。

## 配置管理

- **外部化配置：** 使用 `application.yml`，可读性更好且结构层级清晰。
- **类型安全属性：** 使用 `@ConfigurationProperties` 搭配 `data class` 创建不可变、类型安全的配置对象。
- **环境配置：** 通过 Spring Profiles（如 `application-dev.yml`、`application-prod.yml`）管理不同环境的配置。
- **密钥管理：** 切勿硬编码密钥。使用环境变量或 HashiCorp Vault、AWS Secrets Manager 等密钥管理工具。

## Web 层（控制器）

- **RESTful API：** 设计清晰、一致的 RESTful 端点。
- **DTO 使用数据类：** 对所有 DTO 使用 Kotlin `data class`。这样可自动获得 `equals()`、`hashCode()`、`toString()` 和 `copy()`，并保持不可变性。
- **校验：** 在 DTO 数据类上使用 Java Bean Validation（JSR 380）注解（`@Valid`、`@NotNull`、`@Size` 等）。
- **错误处理：** 使用 `@ControllerAdvice` 与 `@ExceptionHandler` 实现全局异常处理，保持统一的错误响应。

## 服务层

- **业务逻辑：** 将业务逻辑封装在 `@Service` 类中。
- **无状态：** 服务应保持无状态。
- **事务管理：** 在服务方法上使用 `@Transactional`。在 Kotlin 中可以作用于类或函数级别。

## 数据层（仓储）

- **JPA 实体：** 使用类定义实体，并确保为 `open`。强烈建议使用 `kotlin-jpa` 编译器插件自动处理。
- **空值安全：** 利用 Kotlin 的空安全（`?`）在类型层面清晰标注可选字段。
- **Spring Data JPA：** 通过继承 `JpaRepository` 或 `CrudRepository` 使用 Spring Data JPA。
- **协程：** 对于响应式应用，可在数据层结合 Spring Boot 的 Kotlin 协程支持。

## 日志

- **伴生对象日志器：** 以伴生对象声明日志器是惯用写法。
  ```kotlin
  companion object {
      private val logger = LoggerFactory.getLogger(MyClass::class.java)
  }
  ```
- **参数化日志：** 使用参数化消息（`logger.info("Processing user {}...", userId)`）兼顾性能与可读性。

## 测试

- **JUnit 5：** 默认使用 JUnit 5，与 Kotlin 集成顺畅。
- **惯用测试库：** 为更流畅的语法，考虑使用 **Kotest** 断言与 **MockK** 模拟库，它们专为 Kotlin 设计。
- **测试切片：** 使用 `@WebMvcTest`、`@DataJpaTest` 等测试切片注解聚焦特定层级。
- **Testcontainers：** 通过 Testcontainers 在真实数据库、消息队列等环境下进行可靠的集成测试。

## 协程与异步编程

- **`suspend` 函数：** 在控制器和服务中使用 `suspend` 函数实现非阻塞异步代码。Spring Boot 对协程提供出色支持。
- **结构化并发：** 使用 `coroutineScope` 或 `supervisorScope` 管理协程生命周期。

