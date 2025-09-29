---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
description: "获取使用 Spring Boot 开发应用程序的最佳实践。"
---

# Spring Boot 最佳实践

您的目标是通过遵循既定的最佳实践，帮助我编写高质量的 Spring Boot 应用程序。

## 项目设置和结构

- **构建工具：** 使用 Maven (`pom.xml`) 或 Gradle (`build.gradle`) 进行依赖管理。
- **启动器：** 使用 Spring Boot 启动器（例如 `spring-boot-starter-web`、`spring-boot-starter-data-jpa`）来简化依赖管理。
- **包结构：** 按功能/领域组织代码（例如 `com.example.app.order`、`com.example.app.user`），而不是按层（例如 `com.example.app.controller`、`com.example.app.service`）。

## 依赖注入和组件

- **构造函数注入：** 始终对必需的依赖项使用基于构造函数的注入。这使得组件更易于测试，并且依赖项是明确的。
- **不可变性：** 将依赖项字段声明为 `private final`。
- **组件构造型：** 适当地使用 `@Component`、`@Service`、`@Repository` 和 `@Controller`/`@RestController` 注解来定义 bean。

## 配置

- **外部化配置：** 使用 `application.yml`（或 `application.properties`）进行配置。YAML 因其可读性和层次结构而通常更受青睐。
- **类型安全的属性：** 使用 `@ConfigurationProperties` 将配置绑定到强类型的 Java 对象。
- **配置文件：** 使用 Spring 配置文件（`application-dev.yml`、`application-prod.yml`）来管理特定于环境的配置。
- **机密管理：** 不要硬编码机密。使用环境变量或专用的机密管理工具，如 HashiCorp Vault 或 AWS Secrets Manager。

## Web 层（控制器）

- **RESTful API：** 设计清晰一致的 RESTful 端点。
- **DTO（数据传输对象）：** 使用 DTO 在 API 层中公开和使用数据。不要将 JPA 实体直接公开给客户端。
- **验证：** 在 DTO 上使用 Java Bean 验证 (JSR 380) 和注解（`@Valid`、`@NotNull`、`@Size`）来验证请求负载。
- **错误处理：** 使用 `@ControllerAdvice` 和 `@ExceptionHandler` 实现全局异常处理程序，以提供一致的错误响应。

## 服务层

- **业务逻辑：** 将所有业务逻辑封装在 `@Service` 类中。
- **无状态：** 服务应该是无状态的。
- **事务管理：** 在服务方法上使用 `@Transactional` 以声明方式管理数据库事务。在最必要的粒度级别上应用它。

## 数据层（存储库）

- **Spring Data JPA：** 通过扩展 `JpaRepository` 或 `CrudRepository` 来使用 Spring Data JPA 存储库进行标准数据库操作。
- **自定义查询：** 对于复杂的查询，请使用 `@Query` 或 JPA Criteria API。
- **投影：** 使用 DTO 投影仅从数据库中获取必要的数据。

## 日志记录

- **SLF4J：** 使用 SLF4J API 进行日志记录。
- **记录器声明：** `private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`
- **参数化日志记录：** 使用参数化消息（`logger.info("Processing user {}...", userId);`）而不是字符串连接来提高性能。

## 测试

- **单元测试：** 使用 JUnit 5 和像 Mockito 这样的模拟框架为服务和组件编写单元测试。
- **集成测试：** 使用 `@SpringBootTest` 进行加载 Spring 应用程序上下文的集成测试。
- **测试切片：** 使用 `@WebMvcTest`（用于控制器）或 `@DataJpaTest`（用于存储库）等测试切片注解来隔离测试应用程序的特定部分。
- **Testcontainers：** 考虑使用 Testcontainers 进行与真实数据库、消息代理等的可靠集成测试。

## 安全

- **Spring Security：** 使用 Spring Security 进行身份验证和授权。
- **密码编码：** 始终使用像 BCrypt 这样的强哈希算法对密码进行编码。
- **输入清理：** 通过使用 Spring Data JPA 或参数化查询来防止 SQL 注入。通过正确编码输出来防止跨站脚本 (XSS)。

```

```
