---
description: '将 Spring Boot JPA 应用程序转换为使用 Azure Cosmos DB 与 Spring Data Cosmos 的分步指南'
applyTo: '**/*.java,**/pom.xml,**/build.gradle,**/application*.properties'
---

# 将 Spring JPA 项目转换为 Spring Data Cosmos

此通用指南适用于任何 JPA 到 Spring Data Cosmos DB 转换项目。

## 高级计划

1. 交换构建依赖项（移除 JPA，添加 Cosmos + Identity）。
2. 添加 `cosmos` 配置文件和属性。
3. 添加具有适当 Azure 身份认证的 Cosmos 配置。
4. 转换实体（ids → `String`，添加 `@Container` 和 `@PartitionKey`，移除 JPA 映射，调整关系）。
5. 转换存储库（`JpaRepository` → `CosmosRepository`）。
6. **创建服务层**用于关系管理和模板兼容性。
7. **关键**：更新所有测试文件以使用 String ID 和 Cosmos 存储库。
8. 通过 `CommandLineRunner` 播种数据。
9. **关键**：测试运行时功能并修复模板兼容性问题。

## 分步指南

### 步骤 1 — 构建依赖项

- **Maven**（`pom.xml`）：
  - 移除依赖项 `spring-boot-starter-data-jpa`
  - 移除数据库特定依赖项（H2、MySQL、PostgreSQL），除非在其他地方需要
  - 添加 `com.azure:azure-spring-data-cosmos:5.17.0`（或最新兼容版本）
  - 添加 `com.azure:azure-identity:1.15.4`（DefaultAzureCredential 所需）
- **Gradle**：为 Gradle 语法应用相同的依赖项更改
- 移除 testcontainers 和 JPA 特定的测试依赖项

### 步骤 2 — 属性和配置

- 创建 `src/main/resources/application-cosmos.properties`：
  ```properties
  azure.cosmos.uri=${COSMOS_URI:https://localhost:8081}
  azure.cosmos.database=${COSMOS_DATABASE:petclinic}
  azure.cosmos.populate-query-metrics=false
  azure.cosmos.enable-multiple-write-locations=false
  ```
- 更新 `src/main/resources/application.properties`：
  ```properties
  spring.profiles.active=cosmos
  ```

### 步骤 3 — 使用 Azure Identity 的配置类

- 创建 `src/main/java/<rootpkg>/config/CosmosConfiguration.java`：
  ```java
  @Configuration
  @EnableCosmosRepositories(basePackages = "<rootpkg>")
  public class CosmosConfiguration extends AbstractCosmosConfiguration {

    @Value("${azure.cosmos.uri}")
    private String uri;

    @Value("${azure.cosmos.database}")
    private String dbName;

    @Bean
    public CosmosClientBuilder getCosmosClientBuilder() {
      return new CosmosClientBuilder().endpoint(uri).credential(new DefaultAzureCredentialBuilder().build());
    }

    @Override
    protected String getDatabaseName() {
      return dbName;
    }

    @Bean
    public CosmosConfig cosmosConfig() {
      return CosmosConfig.builder().enableQueryMetrics(false).build();
    }
  }

  ```
- **重要**：为生产安全使用 `DefaultAzureCredentialBuilder().build()` 而不是基于密钥的认证

### 步骤 4 — 实体转换

- 针对所有带有 JPA 注解的类（`@Entity`、`@MappedSuperclass`、`@Embeddable`）
- **基础实体更改**：
  - 将 `id` 字段类型从 `Integer` 更改为 `String`
  - 添加 `@Id` 和 `@GeneratedValue` 注解
  - 添加 `@PartitionKey` 字段（通常是 `String partitionKey`）
  - 移除所有 `jakarta.persistence` 导入
- **关键 - Cosmos DB 序列化要求**：
  - **移除所有需要持久化到 Cosmos DB 的字段上的 `@JsonIgnore` 注解**
  - **认证实体（User、Authority）必须完全可序列化** - 密码、权限或其他持久化字段上不能有 `@JsonIgnore`
  - **当需要控制 JSON 字段名但仍要持久化数据时，使用 `@JsonProperty` 而不是 `@JsonIgnore`**
  - **常见认证序列化错误**：`Cannot pass null or empty values to constructor` 通常意味着 `@JsonIgnore` 阻止了必需字段的序列化
- **实体特定更改**：
  - 将 `@Entity` 替换为 `@Container(containerName = "<plural-entity-name>")`
  - 移除 `@Table`、`@Column`、`@JoinColumn` 等
  - 移除关系注解（`@OneToMany`、`@ManyToOne`、`@ManyToMany`）
  - 对于关系：
    - 为一对多嵌入集合（例如，Owner 中的 `List<Pet> pets`）
    - 为多对一使用引用 ID（例如，Pet 中的 `String ownerId`）
    - **对于复杂关系**：存储 ID 但为模板添加瞬态属性
  - 添加构造函数设置分区键：`setPartitionKey("entityType")`
- **关键 - 认证实体模式**：
  - **对于使用 Spring Security 的 User 实体**：将权限存储为 `Set<String>` 而不是 `Set<Authority>` 对象
  - **示例 User 实体转换**：
    ```java
    @Container(containerName = "users")
    public class User {

      @Id
      private String id;

      @PartitionKey
      private String partitionKey = "user";

      private String login;
      private String password; // NO @JsonIgnore - must be serializable

      @JsonProperty("authorities") // Use @JsonProperty, not @JsonIgnore
      private Set<String> authorities = new HashSet<>(); // Store as strings

      // Add transient property for Spring Security compatibility if needed
      // @JsonIgnore - ONLY for transient properties not persisted to Cosmos
      private Set<Authority> authorityObjects = new HashSet<>();

      // Conversion methods between string authorities and Authority objects
      public void setAuthorityObjects(Set<Authority> authorities) {
        this.authorityObjects = authorities;
        this.authorities = authorities.stream().map(Authority::getName).collect(Collectors.toSet());
      }
    }

    ```
- **关键 - 关系更改的模板兼容性**：
  - **将关系转换为 ID 引用时，保留模板访问**
  - **示例**：如果实体有 `List<Specialty> specialties` → 转换为：
    - 存储：`List<String> specialtyIds`（持久化到 Cosmos）
    - 模板：`@JsonIgnore private List<Specialty> specialties = new ArrayList<>()`（瞬态）
    - 为两个属性添加 getter/setter
  - **更新实体方法逻辑**：`getNrOfSpecialties()` 应该使用瞬态列表
- **关键 - Thymeleaf/JSP 应用程序的模板兼容性**：
  - **识别模板属性访问**：在 `.html` 文件中搜索 `${entity.relationshipProperty}`
  - **对于模板中访问的每个关系属性**：
    - **存储**：保持基于 ID 的存储（例如，`List<String> specialtyIds`）
    - **模板访问**：添加带有 `@JsonIgnore` 的瞬态属性（例如，`private List<Specialty> specialties = new ArrayList<>()`）
    - **示例**：

      ```java
      // Stored in Cosmos (persisted)
      private List<String> specialtyIds = new ArrayList<>();

      // For template access (transient)
      @JsonIgnore
      private List<Specialty> specialties = new ArrayList<>();

      // Getters/setters for both properties
      public List<String> getSpecialtyIds() {
        return specialtyIds;
      }

      public List<Specialty> getSpecialties() {
        return specialties;
      }

      ```

    - **更新计数方法**：`getNrOfSpecialties()` 应该使用瞬态列表，而不是 ID 列表
- **关键 - 方法签名冲突**：
  - **将 ID 类型从 Integer 转换为 String 时，检查方法签名冲突**
  - **常见冲突**：`getPet(String name)` vs `getPet(String id)` - 两者都有相同的签名
  - **解决方案**：重命名方法使其特定：
    - `getPet(String id)` 用于基于 ID 的查找
    - `getPetByName(String name)` 用于基于名称的查找
    - `getPetByName(String name, boolean ignoreNew)` 用于条件基于名称的查找
  - **更新所有重命名方法的调用者**在控制器和测试中
- **实体的方法更新**：
  - 将 `addVisit(Integer petId, Visit visit)` 更新为 `addVisit(String petId, Visit visit)`
  - 确保所有 ID 比较逻辑使用 `.equals()` 而不是 `==`

### 步骤 5 — 存储库转换

- 更改所有存储库接口：
  - 从：`extends JpaRepository<Entity, Integer>`
  - 到：`extends CosmosRepository<Entity, String>`
- **查询方法更新**：
  - 从自定义查询中移除分页参数
  - 将 `Page<Entity> findByX(String param, Pageable pageable)` 更改为 `List<Entity> findByX(String param)`
  - 更新 `@Query` 注解以使用 Cosmos SQL 语法
  - **替换自定义方法名**：`findPetTypes()` → `findAllOrderByName()`
  - **更新所有引用**到控制器和格式化程序中更改的方法名

### 步骤 6 — **创建服务层**用于关系管理和模板兼容性

- **关键**：创建服务类来桥接 Cosmos 文档存储与现有模板期望
- **目的**：处理关系填充并维护模板兼容性
- **每个有关系的实体的服务模式**：
  ```java
  @Service
  public class EntityService {

    private final EntityRepository entityRepository;
    private final RelatedRepository relatedRepository;

    public EntityService(EntityRepository entityRepository, RelatedRepository relatedRepository) {
      this.entityRepository = entityRepository;
      this.relatedRepository = relatedRepository;
    }

    public List<Entity> findAll() {
      List<Entity> entities = entityRepository.findAll();
      entities.forEach(this::populateRelationships);
      return entities;
    }

    public Optional<Entity> findById(String id) {
      Optional<Entity> entityOpt = entityRepository.findById(id);
      if (entityOpt.isPresent()) {
        Entity entity = entityOpt.get();
        populateRelationships(entity);
        return Optional.of(entity);
      }
      return Optional.empty();
    }

    private void populateRelationships(Entity entity) {
      if (entity.getRelatedIds() != null && !entity.getRelatedIds().isEmpty()) {
        List<Related> related = entity
          .getRelatedIds()
          .stream()
          .map(relatedRepository::findById)
          .filter(Optional::isPresent)
          .map(Optional::get)
          .collect(Collectors.toList());
        // Set transient property for template access
        entity.setRelated(related);
      }
    }
  }

  ```

### 步骤 6.5 — **Spring Security 集成**（认证关键）

- **UserDetailsService 集成模式**：
  ```java
  @Service
  @Transactional
  public class DomainUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;
    private final AuthorityRepository authorityRepository;

    @Override
    public UserDetails loadUserByUsername(String login) {
      log.debug("Authenticating user: {}", login);

      return userRepository
        .findOneByLogin(login)
        .map(user -> createSpringSecurityUser(login, user))
        .orElseThrow(() -> new UsernameNotFoundException("User " + login + " was not found"));
    }

    private org.springframework.security.core.userdetails.User createSpringSecurityUser(String lowercaseLogin, User user) {
      if (!user.isActivated()) {
        throw new UserNotActivatedException("User " + lowercaseLogin + " was not activated");
      }

      // Convert string authorities back to GrantedAuthority objects
      List<GrantedAuthority> grantedAuthorities = user
        .getAuthorities()
        .stream()
        .map(SimpleGrantedAuthority::new)
        .collect(Collectors.toList());

      return new org.springframework.security.core.userdetails.User(user.getLogin(), user.getPassword(), grantedAuthorities);
    }
  }

  ```
- **关键认证要求**：
  - User 实体必须完全可序列化（密码/权限上不能有 `@JsonIgnore`）
  - 为 Cosmos DB 兼容性将权限存储为 `Set<String>`
  - 在 UserDetailsService 中在字符串权限和 `GrantedAuthority` 对象之间转换
  - 添加全面的调试日志以跟踪认证流程
  - 适当处理激活/停用用户状态

#### **模板关系填充模式**

每个返回用于模板渲染的实体的服务方法必须填充瞬态属性：

```java
private void populateRelationships(Entity entity) {
  // For each relationship used in templates
  if (entity.getRelatedIds() != null && !entity.getRelatedIds().isEmpty()) {
    List<Related> relatedObjects = entity
      .getRelatedIds()
      .stream()
      .map(relatedRepository::findById)
      .filter(Optional::isPresent)
      .map(Optional::get)
      .collect(Collectors.toList());
    entity.setRelated(relatedObjects); // Set transient property
  }
}

```

#### **控制器中的关键服务使用**

- **将所有直接存储库调用**替换为控制器中的服务调用
- **永远不要将存储库的实体直接返回**到模板而不进行关系填充
- **更新控制器**使用服务层而不是直接使用存储库
- **控制器模式更改**：

  ```java
  // OLD: Direct repository usage
  @Autowired
  private EntityRepository entityRepository;

  // NEW: Service layer usage
  @Autowired
  private EntityService entityService;
  // Update method calls
  // OLD: entityRepository.findAll()
  // NEW: entityService.findAll()

  ```

### 步骤 7 — 数据播种

- 创建实现 `CommandLineRunner` 的 `@Component`：
  ```java
  @Component
  public class DataSeeder implements CommandLineRunner {

    @Override
    public void run(String... args) throws Exception {
      if (ownerRepository.count() > 0) {
        return; // Data already exists
      }
      // Seed comprehensive test data with String IDs
      // Use meaningful ID patterns: "owner-1", "pet-1", "pettype-1", etc.
    }
  }

  ```
- **关键 - JDK 17+ 的 BigDecimal 反射问题**：
  - **如果使用 BigDecimal 字段**，在播种期间可能遇到反射错误
  - **错误模式**：`Unable to make field private final java.math.BigInteger java.math.BigDecimal.intVal accessible`
  - **解决方案**：
    1. 对货币值使用 `Double` 或 `String` 而不是 `BigDecimal`
    2. 添加 JVM 参数：`--add-opens java.base/java.math=ALL-UNNAMED`
    3. 在 try-catch 中包装 BigDecimal 操作并优雅处理
  - **即使播种失败，应用程序也会成功启动** - 检查日志中的播种错误

### 步骤 8 — 测试文件转换（关键部分）

**此步骤经常被忽略但对成功转换至关重要**

#### A. **编译检查策略**

- **每次重大更改后，运行 `mvn test-compile` 以尽早发现问题**
- **在继续之前系统性地修复编译错误**
- **不要依赖 IDE - Maven 编译会揭示所有问题**

#### B. **系统性搜索和更新所有测试文件**

**使用搜索工具查找和更新每个出现：**

- 搜索：`int.*TEST.*ID` → 替换为：`String.*TEST.*ID = "test-xyz-1"`
- 搜索：`setId\(\d+\)` → 替换为：`setId("test-id-X")`
- 搜索：`findById\(\d+\)` → 替换为：`findById("test-id-X")`
- 搜索：`\.findPetTypes\(\)` → 替换为：`.findAllOrderByName()`
- 搜索：`\.findByLastNameStartingWith\(.*,.*Pageable` → 移除分页参数

#### C. 更新测试注解和导入

- 将 `@DataJpaTest` 替换为 `@SpringBootTest` 或适当的切片测试
- 移除 `@AutoConfigureTestDatabase` 注解
- 从测试中移除 `@Transactional`（除非单分区操作）
- 移除来自 `org.springframework.orm` 包的导入

#### D. 修复所有测试文件中的实体 ID 使用

**必须更新的关键文件（搜索整个测试目录）：**

- `*ControllerTests.java` - 路径变量、实体创建、模拟设置
- `*ServiceTests.java` - 存储库交互、实体 ID
- `EntityUtils.java` - ID 处理的实用方法
- `*FormatterTests.java` - 存储库方法调用
- `*ValidatorTests.java` - 使用 String ID 创建实体
- 集成测试类 - 测试数据设置

#### E. **修复受存储库更改影响的控制器和服务类**

- **更新调用签名已更改的存储库方法的控制器**
- **更新使用存储库方法的格式化程序/转换器**
- **要检查的常见文件**：
  - `PetTypeFormatter.java` - 经常调用 `findPetTypes()` 方法
  - `*Controller.java` - 可能有要移除的分页逻辑
  - 使用存储库方法的服务类

#### F. 更新测试中的存储库模拟

- 从存储库模拟中移除分页：
  - `given(repository.findByX(param, pageable)).willReturn(pageResult)`
  - → `given(repository.findByX(param)).willReturn(listResult)`
- 更新模拟中的方法名：
  - `given(petTypeRepository.findPetTypes()).willReturn(types)`
  - → `given(petTypeRepository.findAllOrderByName()).willReturn(types)`

#### G. 修复测试使用的实用类

- 更新 `EntityUtils.java` 或类似文件：
  - 移除 JPA 特定异常导入（`ObjectRetrievalFailureException`）
  - 将方法签名从 `int id` 更改为 `String id`
  - 更新 ID 比较逻辑：`entity.getId() == entityId` → `entity.getId().equals(entityId)`
  - 用标准异常（`IllegalArgumentException`）替换 JPA 异常

#### H. 更新 String ID 的断言

- 更改 ID 断言：
  - `assertThat(entity.getId()).isNotZero()` → `assertThat(entity.getId()).isNotEmpty()`
  - `assertThat(entity.getId()).isEqualTo(1)` → `assertThat(entity.getId()).isEqualTo("test-id-1")`
  - JSON 路径断言：`jsonPath("$.id").value(1)` → `jsonPath("$.id").value("test-id-1")`

### 步骤 9 — **运行时测试和模板兼容性**

#### **关键**：编译成功后测试运行中的应用程序

- **启动应用程序**：`mvn spring-boot:run`
- **浏览所有页面**在 Web 界面中识别运行时错误
- **转换后的常见运行时问题**：
  - 模板尝试访问不再存在的属性（例如，`vet.specialties`）
  - 服务层不填充瞬态关系属性
  - 控制器不使用服务层进行关系加载

#### **模板兼容性修复**：

- **如果模板访问关系属性**（例如，`entity.relatedObjects`）：
  - 确保实体上存在具有适当 getter/setter 的瞬态属性
  - 验证服务层填充这些瞬态属性
  - 更新 `getNrOfXXX()` 方法以使用瞬态列表而不是 ID 列表
- **检查日志中的 SpEL（Spring Expression Language）错误**：
  - `Property or field 'xxx' cannot be found` → 添加缺失的瞬态属性
  - `EL1008E` 错误 → 服务层不填充关系

#### **服务层验证**：

- **确保所有控制器使用服务层**而不是直接存储库访问
- **验证服务方法在返回实体之前填充关系**
- **通过 Web 界面测试所有 CRUD 操作**

### 步骤 9.5 — **模板运行时验证**（关键）

#### **系统性模板测试过程**

成功编译和应用程序启动后：

1. **系统性地导航到应用程序中的每个页面**
2. **测试显示实体数据的每个模板**：
   - 列表页面（例如，`/vets`、`/owners`）
   - 详细页面（例如，`/owners/{id}`、`/vets/{id}`）
   - 表单和编辑页面
3. **寻找特定的模板错误**：
   - `Property or field 'relationshipName' cannot be found on object of type 'EntityName'`
   - `EL1008E` Spring Expression Language 错误
   - 关系应该出现的地方出现空或缺失数据

#### **模板错误解决检查清单**

遇到模板错误时：

- [ ] **从错误消息中识别缺失属性**
- [ ] **检查属性是否作为瞬态字段存在**在实体中
- [ ] **验证服务层在返回实体之前填充属性**
- [ ] **确保控制器使用服务层**，而不是直接存储库访问
- [ ] **修复后再次测试特定页面**

#### **常见模板错误模式**

- `Property or field 'specialties' cannot be found` → 在 Vet 实体中添加 `@JsonIgnore private List<Specialty> specialties`
- `Property or field 'pets' cannot be found` → 在 Owner 实体中添加 `@JsonIgnore private List<Pet> pets`
- 显示空关系数据 → 服务不填充瞬态属性

### 步骤 10 — **系统性错误解决过程**

#### 编译失败时：

1. **首先运行 `mvn compile`** - 在测试之前修复主源问题
2. **运行 `mvn test-compile`** - 系统性地修复每个测试编译错误
3. **专注于最频繁的错误模式**：
   - `int cannot be converted to String` → 更改测试常量和实体 setter
   - `method X cannot be applied to given types` → 移除分页参数
   - `cannot find symbol: method Y()` → 更新为新存储库方法名
   - 方法签名冲突 → 重命名冲突方法

#### 运行时失败时：

1. **检查应用程序日志**中的特定错误消息
2. **寻找模板/SpEL 错误**：
   - `Property or field 'xxx' cannot be found` → 向实体添加瞬态属性
   - 缺失关系数据 → 服务层不填充关系
3. **验证控制器中的服务层使用**
4. **通过所有应用程序页面测试导航**

#### 常见错误模式和解决方案：

- **`method findByLastNameStartingWith cannot be applied`** → 移除 `Pageable` 参数
- **`cannot find symbol: method findPetTypes()`** → 更改为 `findAllOrderByName()`
- **`incompatible types: int cannot be converted to String`** → 更新测试 ID 常量
- **`method getPet(String) is already defined`** → 重命名一个方法（例如，`getPetByName`）
- **`cannot find symbol: method isNotZero()`** → 对 String ID 更改为 `isNotEmpty()`
- **`Property or field 'specialties' cannot be found`** → 添加瞬态属性并在服务中填充
- **`ClassCastException: reactor.core.publisher.BlockingIterable cannot be cast to java.util.List`** → 修复存储库 `findAllWithEagerRelationships()` 方法以使用 StreamSupport
- **`Unable to make field...BigDecimal.intVal accessible`** → 在整个应用程序中用 Double 替换 BigDecimal
- **健康检查数据库失败** → 从健康检查就绪配置中移除 'db'

#### **模板特定运行时错误**

- **`Property or field 'XXX' cannot be found on object of type 'YYY'`**：

  - 根本原因：模板访问已转换为 ID 存储的关系属性
  - 解决方案：向实体添加瞬态属性 + 在服务层填充
  - 预防：在转换关系之前始终检查模板使用

- **`EL1008E` Spring Expression Language 错误**：

  - 根本原因：服务层不填充瞬态属性
  - 解决方案：验证 `populateRelationships()` 方法被调用并工作
  - 预防：服务层实现后测试所有模板导航

- **模板中空/null 关系数据**：
  - 根本原因：控制器绕过服务层或服务不填充关系
  - 解决方案：确保所有控制器方法使用服务层进行实体检索
  - 预防：永远不要将存储库结果直接返回到模板

### 步骤 11 — 验证检查清单

转换后，验证：

- [ ] **主应用程序编译**：`mvn compile` 成功
- [ ] **所有测试文件编译**：`mvn test-compile` 成功
- [ ] **无编译错误**：解决每一个编译错误
- [ ] **应用程序成功启动**：`mvn spring-boot:run` 无错误
- [ ] **所有网页加载**：无运行时错误地浏览所有应用程序页面
- [ ] **服务层填充关系**：瞬态属性正确设置
- [ ] **所有模板页面无错误渲染**：浏览整个应用程序
- [ ] **关系数据正确显示**：列表、计数和相关对象正确显示
- [ ] **日志中无 SpEL 模板错误**：导航期间检查应用程序日志
- [ ] **瞬态属性有 @JsonIgnore 注解**：防止 JSON 序列化问题
- [ ] **一致使用服务层**：控制器中无直接存储库访问用于模板渲染
- [ ] 无剩余 `jakarta.persistence` 导入
- [ ] 所有实体 ID 一致为 `String` 类型
- [ ] 所有存储库接口扩展 `CosmosRepository<Entity, String>`
- [ ] 配置使用 `DefaultAzureCredential` 进行认证
- [ ] 数据播种组件存在并工作
- [ ] 测试文件一致使用 String ID
- [ ] 存储库模拟更新为 Cosmos 方法
- [ ] **实体类中无方法签名冲突**
- [ ] **所有重命名方法在调用者中更新**（控制器、测试、格式化程序）

### 避免的常见陷阱

1. **不频繁检查编译** - 每次重大更改后运行 `mvn test-compile`
2. **方法签名冲突** - 转换 ID 类型时的方法重载问题
3. **忘记更新方法调用者** - 重命名方法时，更新所有调用者
4. **缺失存储库方法重命名** - 自定义存储库方法必须在调用的所有地方更新
5. **使用基于密钥的认证** - 使用 `DefaultAzureCredential` 代替
6. **混合 Integer 和 String ID** - 在所有地方保持 String ID 一致，特别是在测试中
7. **不更新控制器分页逻辑** - 存储库更改时从控制器中移除分页
8. **保留 JPA 特定测试注解** - 替换为 Cosmos 兼容的替代方案
9. **不完整的测试文件更新** - 搜索整个测试目录，不只是明显的文件
10. **跳过运行时测试** - 始终测试运行中的应用程序，不只是编译
11. **缺失服务层** - 不要从控制器直接访问存储库
12. **忘记瞬态属性** - 模板可能需要访问关系数据
13. **不测试模板导航** - 编译成功不意味着模板工作
14. **模板缺失瞬态属性** - 模板需要对象访问，不只是 ID
15. **服务层绕过** - 控制器必须使用服务，永远不要直接存储库访问
16. **不完整关系填充** - 服务方法必须填充模板使用的所有瞬态属性
17. **忘记瞬态属性上的 @JsonIgnore** - 防止序列化问题
18. **持久化字段上的 @JsonIgnore** - **关键**：永远不要在需要存储到 Cosmos DB 的字段上使用 `@JsonIgnore`
19. **认证序列化错误** - User/Authority 实体必须完全可序列化，不能有 `@JsonIgnore` 阻止必需字段
20. **BigDecimal 反射问题** - 为 JDK 17+ 兼容性使用替代数据类型或 JVM 参数
21. **存储库反应类型转换** - 不要将 `findAll()` 直接转换为 `List`，使用 `StreamSupport.stream().collect(Collectors.toList())`
22. **健康检查数据库引用** - JPA 移除后从 Spring Boot 健康检查中移除数据库依赖
23. **集合类型不匹配** - 一致地更新服务方法以处理 String vs 对象集合

### 系统性调试编译问题

如果转换后编译失败：

1. **从主编译开始**：`mvn compile` - 首先修复实体和控制器问题
2. **然后测试编译**：`mvn test-compile` - 系统性地修复每个错误
3. **检查整个代码库中剩余的 `jakarta.persistence` 导入**
4. **验证所有测试常量使用 String ID** - 搜索 `int.*TEST.*ID`
5. **确保存储库方法签名匹配**新的 Cosmos 接口
6. **检查实体关系和测试中的混合 Integer/String ID 使用**
7. **验证所有模拟使用正确方法名**（`findAllOrderByName()` 不是 `findPetTypes()`）
8. **寻找方法签名冲突** - 通过重命名冲突方法解决
9. **验证断言方法与 String ID 一起工作**（`isNotEmpty()` 不是 `isNotZero()`）

### 系统性调试运行时问题

如果成功编译后运行时失败：

1. **检查应用程序启动日志**中的初始化错误
2. **浏览所有页面**以识别模板/控制器问题
3. **在日志中寻找 SpEL 模板错误**：
   - `Property or field 'xxx' cannot be found` → 缺失瞬态属性
   - `EL1008E` → 服务层不填充关系
4. **验证正在使用服务层**而不是直接存储库访问
5. **检查瞬态属性在服务方法中被填充**
6. **通过 Web 界面测试所有 CRUD 操作**
7. **验证数据播种正确工作**并维护关系
8. **认证特定调试**：
   - `Cannot pass null or empty values to constructor` → 检查必需字段上的 `@JsonIgnore`
   - `BadCredentialsException` → 验证 User 实体序列化和密码字段可访问性
   - 检查日志中的 "DomainUserDetailsService" 调试输出以跟踪认证流程

### **成功的专业提示**

- **尽早和频繁编译** - 不要让错误积累
- **使用全局搜索和替换** - 查找要更新的模式的所有出现
- **系统性** - 在移动到下一个之前修复所有文件中的一种错误类型
- **仔细测试方法重命名** - 确保所有调用者都已更新
- **使用有意义的 String ID** - "owner-1"、"pet-1" 而不是随机字符串
- **检查控制器类** - 它们经常调用更改签名的存储库方法
- **始终测试运行时** - 编译成功不保证功能模板
- **服务层至关重要** - 在文档存储和模板期望之间架桥

### **认证故障排除指南**（关键）

#### **常见认证序列化错误**：

1. **`Cannot pass null or empty values to constructor`**：

   - **根本原因**：`@JsonIgnore` 阻止必需字段序列化到 Cosmos DB
   - **解决方案**：从所有持久化字段移除 `@JsonIgnore`（密码、权限等）
   - **验证**：检查 User 实体在存储字段上没有 `@JsonIgnore`

2. **登录期间 `BadCredentialsException`**：

   - **根本原因**：认证期间密码字段不可访问
   - **解决方案**：确保密码字段可序列化且在 UserDetailsService 中可访问
   - **验证**：在 `loadUserByUsername` 方法中添加调试日志

3. **权限加载不正确**：

   - **根本原因**：权限对象存储为复杂实体而不是字符串
   - **解决方案**：将权限存储为 `Set<String>` 并在 UserDetailsService 中转换为 `GrantedAuthority`
   - **模式**：

     ```java
     // In User entity - stored in Cosmos
     @JsonProperty("authorities")
     private Set<String> authorities = new HashSet<>();

     // In UserDetailsService - convert for Spring Security
     List<GrantedAuthority> grantedAuthorities = user
       .getAuthorities()
       .stream()
       .map(SimpleGrantedAuthority::new)
       .collect(Collectors.toList());

     ```

4. **认证期间找不到用户实体**：
   - **根本原因**：存储库查询方法不与 String ID 一起工作
   - **解决方案**：更新存储库 `findOneByLogin` 方法以与 Cosmos DB 一起工作
   - **验证**：独立测试存储库方法

#### **认证调试检查清单**：

- [ ] User 实体完全可序列化（持久化字段上无 `@JsonIgnore`）
- [ ] 密码字段可访问且不为 null
- [ ] 权限存储为 `Set<String>`
- [ ] UserDetailsService 将字符串权限转换为 `GrantedAuthority`
- [ ] 存储库方法与 String ID 一起工作
- [ ] 认证服务中启用调试日志
- [ ] 用户激活状态适当检查
- [ ] 使用已知凭据测试登录（admin/admin）

### **常见运行时问题和解决方案**

#### **问题 1：存储库反应类型转换错误**

**错误**：`ClassCastException: reactor.core.publisher.BlockingIterable cannot be cast to java.util.List`

**根本原因**：Cosmos 存储库返回反应类型（`Iterable`）但传统 JPA 代码期望 `List`

**解决方案**：在存储库方法中正确转换反应类型：

```java
// WRONG - Direct casting fails
default List<Entity> customFindMethod() {
    return (List<Entity>) this.findAll(); // ClassCastException!
}

// CORRECT - Convert Iterable to List
default List<Entity> customFindMethod() {
    return StreamSupport.stream(this.findAll().spliterator(), false)
            .collect(Collectors.toList());
}
```

**要检查的文件**：

- 所有带有自定义默认方法的存储库接口
- 任何从 Cosmos 存储库调用返回 `List<Entity>` 的方法
- 导入 `java.util.stream.StreamSupport` 和 `java.util.stream.Collectors`

#### **问题 2：Java 17+ 中的 BigDecimal 反射问题**

**错误**：`Unable to make field private final java.math.BigInteger java.math.BigDecimal.intVal accessible`

**根本原因**：Java 17+ 模块系统在序列化期间限制对 BigDecimal 内部字段的反射访问

**解决方案**：

1. **对简单情况替换为 Double**：

   ```java
   // Before: BigDecimal fields
   private BigDecimal amount;

   // After: Double fields (if precision requirements allow)
   private Double amount;

   ```

2. **对高精度要求使用 String**：

   ```java
   // Store as String, convert as needed
   private String amount; // Store "1500.00"

   public BigDecimal getAmountAsBigDecimal() {
     return new BigDecimal(amount);
   }

   ```

3. **添加 JVM 参数**（如果必须保留 BigDecimal）：
   ```
   --add-opens java.base/java.math=ALL-UNNAMED
   ```

#### **问题 3：健康检查数据库依赖**

**错误**：应用程序健康检查失败，寻找已移除的数据库组件

**根本原因**：Spring Boot 健康检查在移除后仍引用 JPA/数据库依赖

**解决方案**：更新健康检查配置：

```yaml
# In application.yml - Remove database from health checks
management:
  health:
    readiness:
      include: 'ping,diskSpace' # Remove 'db' if present
```

**要检查的文件**：

- 所有 `application*.yml` 配置文件
- 移除任何数据库特定健康指标
- 检查执行器端点配置

#### **问题 4：服务中的集合类型不匹配**

**错误**：实体关系转换为基于字符串的存储后类型不匹配错误

**根本原因**：实体转换后服务方法期望不同的集合类型

**解决方案**：更新服务方法以处理新的实体结构：

```java
// Before: Entity relationships
public Set<RelatedEntity> getRelatedEntities() {
    return entity.getRelatedEntities(); // Direct entity references
}

// After: String-based relationships with conversion
public Set<RelatedEntity> getRelatedEntities() {
    return entity.getRelatedEntityIds()
        .stream()
        .map(relatedRepository::findById)
        .filter(Optional::isPresent)
        .map(Optional::get)
        .collect(Collectors.toSet());
}

### **增强错误解决过程**

#### **常见错误模式和解决方案**：

1. **反应类型转换错误**：
   - **模式**：`cannot be cast to java.util.List`
   - **修复**：使用 `StreamSupport.stream().collect(Collectors.toList())`
   - **文件**：带有自定义默认方法的存储库接口

2. **BigDecimal 序列化错误**：
   - **模式**：`Unable to make field...BigDecimal.intVal accessible`
   - **修复**：替换为 Double、String 或添加 JVM 模块打开
   - **文件**：实体类、DTO、数据初始化类

3. **健康检查数据库错误**：
   - **模式**：健康检查失败寻找数据库
   - **修复**：从健康检查配置中移除数据库引用
   - **文件**：application.yml 配置文件

4. **集合类型转换错误**：
   - **模式**：实体关系处理中的类型不匹配
   - **修复**：更新服务方法以处理基于字符串的实体引用
   - **文件**：服务类、DTO、实体关系方法

#### **增强验证检查清单**：
- [ ] **存储库反应转换处理**：集合返回上无 ClassCastException
- [ ] **BigDecimal 兼容性解决**：Java 17+ 序列化工作
- [ ] **健康检查更新**：健康配置中无数据库依赖
- [ ] **服务层集合处理**：基于字符串的实体引用正确工作
- [ ] **数据播种完成**：日志中出现 "Data seeding completed" 消息
- [ ] **应用程序完全启动**：前端和后端都可访问
- [ ] **认证工作**：可以登录而无序列化错误
- [ ] **CRUD 操作功能**：所有实体操作通过 UI 工作

## **快速参考：常见迁移后修复**

### **要检查的顶级运行时问题**

1. **存储库集合转换**：
   ```java
   // Fix any repository methods that return collections:
   default List<Entity> customFindMethod() {
       return StreamSupport.stream(this.findAll().spliterator(), false)
               .collect(Collectors.toList());
   }
   ```

2. **BigDecimal 兼容性（Java 17+）**：

   ```java
   // Replace BigDecimal fields with alternatives:
   private Double amount; // Or String for high precision

   ```

3. **健康检查配置**：
   ```yaml
   # Remove database dependencies from health checks:
   management:
     health:
       readiness:
         include: 'ping,diskSpace'
   ```

### **认证转换模式**

- **从需要 Cosmos DB 持久化的字段移除 `@JsonIgnore`**
- **将复杂对象存储为简单类型**（例如，权限作为 `Set<String>`）
- **在服务/存储库层中在简单和复杂类型之间转换**

### **模板/UI 兼容性模式**

- **为 UI 访问相关数据添加带有 `@JsonIgnore` 的瞬态属性**
- **使用服务层**在渲染前填充瞬态关系
- **永远不要将存储库结果直接返回**到模板而不进行关系填充