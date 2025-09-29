---
description: '构建 Spring Boot 基础应用程序的指导原则'
applyTo: '**/*.java, **/*.kt'
---

# Spring Boot 开发

## 通用指导原则

- 在审查代码变更时只提供高可信度的建议。
- 编写具有良好可维护性实践的代码，包括对特定设计决策的注释说明。
- 处理边界情况并编写清晰的异常处理。
- 对于第三方库或外部依赖，在注释中说明其用途和目的。

## Spring Boot 指导原则

### 依赖注入

- 对所有必需的依赖使用构造器注入。
- 将依赖字段声明为 `private final`。

### 配置

- 使用 YAML 文件（`application.yml`）进行外部化配置。
- 环境配置文件：使用 Spring profiles 为不同环境（dev、test、prod）配置
- 配置属性：使用 @ConfigurationProperties 进行类型安全的配置绑定
- 密钥管理：使用环境变量或密钥管理系统外部化密钥

### 代码组织

- 包结构：按功能/领域而非层次组织
- 关注点分离：保持 controllers 精简，services 专注，repositories 简单
- 工具类：使工具类为 final 并使用私有构造器

### Service 层

- 将业务逻辑放在 `@Service` 注解的类中。
- Services 应该是无状态且可测试的。
- 通过构造器注入 repositories。
- Service 方法签名应使用领域 ID 或 DTO，除非必要，否则不要直接暴露 repository 实体。

### 日志记录

- 对所有日志使用 SLF4J（`private static final Logger logger = LoggerFactory.getLogger(MyClass.class);`）。
- 不要直接使用具体实现（Logback、Log4j2）或 `System.out.println()`。
- 使用参数化日志：`logger.info("User {} logged in", userId);`。

### 安全性和输入处理

- 使用参数化查询 | 始终使用 Spring Data JPA 或 `NamedParameterJdbcTemplate` 防止 SQL 注入。
- 使用 JSR-380（`@NotNull`、`@Size` 等）注解和 `BindingResult` 验证请求体和参数

## 构建和验证

- 添加或修改代码后，验证项目是否继续成功构建。
- 如果项目使用 Maven，运行 `mvn clean install`。
- 如果项目使用 Gradle，运行 `./gradlew build`（或在 Windows 上运行 `gradlew.bat build`）。
- 确保所有测试作为构建的一部分通过。