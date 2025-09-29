---
applyTo: '*'
description: 'Quarkus 开发标准和指令'
---

- 使用 Java 17 或更高版本构建高质量 Quarkus 应用程序的指令。

## 项目背景

- 最新 Quarkus 版本：3.x
- Java 版本：17 或更高版本
- 使用 Maven 或 Gradle 进行构建管理。
- 专注于清洁架构、可维护性和性能。

## 开发标准

  - 为每个类、方法和复杂逻辑编写清晰简洁的注释。
  - 对公共 API 和方法使用 Javadoc 以确保消费者的清晰理解。
  - 在整个项目中保持一致的编码风格，遵循 Java 约定。
  - 遵循 Quarkus 编码标准和最佳实践，以获得最佳性能和可维护性。
  - 遵循 Jarkarta EE 和 MicroProfile 约定，确保包组织的清晰性。
  - 在适当的地方使用 Java 17 或更高版本的特性，如 record 和 sealed class。

## 命名约定
  - 类名使用 PascalCase（例如，`ProductService`，`ProductResource`）。
  - 方法和变量名使用 camelCase（例如，`findProductById`，`isProductAvailable`）。
  - 常量使用 ALL_CAPS（例如，`DEFAULT_PAGE_SIZE`）。

## Quarkus
  - 利用 Quarkus Dev Mode 实现更快的开发周期。
  - 使用 Quarkus 扩展和最佳实践实现构建时优化。
  - 使用 GraalVM 配置原生构建以获得最佳性能（例如，使用 quarkus-maven-plugin）。
  - 使用 quarkus 日志功能（JBoss、SL4J 或 JUL）实现一致的日志记录实践。

### Quarkus 特定模式
- 使用 `@ApplicationScoped` 而不是 `@Singleton` 来创建单例 bean
- 使用 `@Inject` 进行依赖注入
- 优先使用 Panache 存储库而不是传统的 JPA 存储库
- 在修改数据的服务方法上使用 `@Transactional`
- 应用带有描述性 REST 端点路径的 `@Path`
- 为 REST 资源使用 `@Consumes(MediaType.APPLICATION_JSON)` 和 `@Produces(MediaType.APPLICATION_JSON)`

### REST 资源
- 始终使用 JAX-RS 注解（`@Path`、`@GET`、`@POST` 等）
- 返回适当的 HTTP 状态码（200、201、400、404、500）
- 对复杂响应使用 `Response` 类
- 包含带有 try-catch 块的适当错误处理
- 使用 Bean Validation 注解验证输入参数
- 为公共端点实现速率限制

### 数据访问
- 优先使用 Panache 实体（扩展 `PanacheEntity`）而不是传统 JPA
- 对复杂查询使用 Panache 存储库（`PanacheRepository<T>`）
- 始终对数据修改使用 `@Transactional`
- 对复杂数据库操作使用命名查询
- 为列表端点实现适当的分页

### 配置
- 对简单配置使用 `application.properties` 或 `application.yaml`
- 对类型安全的配置类使用 `@ConfigProperty`
- 对敏感数据优先使用环境变量
- 对不同环境使用配置文件（dev、test、prod）

### 测试
- 对集成测试使用 `@QuarkusTest`
- 对单元测试使用 JUnit 5
- 对原生构建测试使用 `@QuarkusIntegrationTest`
- 使用 `@QuarkusTestResource` 模拟外部依赖项
- 对 REST 端点测试使用 RestAssured（`@QuarkusTestResource`）
- 对修改数据库的测试使用 `@Transactional`
- 对数据库集成测试使用 test-containers

### 不要使用这些模式：
- 不要在测试中使用字段注入（使用构造函数注入）
- 不要硬编码配置值
- 不要忽略异常

## 开发工作流程

### 创建新功能时：
1. 创建具有适当验证的实体
2. 创建具有自定义查询的存储库
3. 创建具有业务逻辑的服务
4. 创建具有适当端点的 REST 资源
5. 编写全面的测试
6. 添加适当的错误处理
7. 更新文档

## 安全考虑

### 实现安全性时：
- 使用 Quarkus Security 扩展（例如，`quarkus-smallrye-jwt`、`quarkus-oidc`）。
- 使用 MicroProfile JWT 或 OIDC 实现基于角色的访问控制（RBAC）。
- 验证所有输入参数