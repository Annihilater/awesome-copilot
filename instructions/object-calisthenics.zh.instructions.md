---
applyTo: '**/*.{cs,ts,java}'
description: 针对业务域代码强制执行对象健身操原则，以确保代码清洁、可维护和健壮
---
# 对象健身操规则

> ⚠️ **警告：** 此文件包含 9 条原始对象健身操规则。不得添加额外规则，也不应替换或删除这些规则。
> 如有需要，以后可能会添加示例。

## 目标
此规则强制执行对象健身操原则，以确保后端代码的清洁性、可维护性和健壮性，**主要针对业务域代码**。

## 范围和应用
- **主要关注**：业务域类（聚合、实体、值对象、域服务）
- **次要关注**：应用层服务和用例处理器
- **豁免**：
  - DTOs（数据传输对象）
  - API 模型/契约
  - 配置类
  - 不含业务逻辑的简单数据容器
  - 需要灵活性的基础设施代码

## 核心原则


1. **每个方法只有一级缩进**：
   - 确保方法简单，缩进不超过一级。

   ```csharp
   // 错误示例 - 此方法有多级缩进
   public void SendNewsletter() {
         foreach (var user in users) {
            if (user.IsActive) {
               // Do something
               mailer.Send(user.Email);
            }
         }
   }
   // 正确示例 - 提取方法以减少缩进
   public void SendNewsletter() {
       foreach (var user in users) {
           SendEmail(user);
       }
   }
   private void SendEmail(User user) {
       if (user.IsActive) {
           mailer.Send(user.Email);
       }
   }

   // 正确示例 - 在发送邮件前过滤用户
   public void SendNewsletter() {
       var activeUsers = users.Where(user => user.IsActive);

       foreach (var user in activeUsers) {
           mailer.Send(user.Email);
       }
   }
   ```
2. **不要使用 ELSE 关键字**：

   - 避免使用 `else` 关键字以降低复杂性并提高可读性。
   - 使用早期返回来处理条件。
   - 使用快速失败原则
   - 使用守卫子句在方法开始时验证输入和条件。

   ```csharp
   // 错误示例 - 使用 else
   public void ProcessOrder(Order order) {
       if (order.IsValid) {
           // Process order
       } else {
           // Handle invalid order
       }
   }
   // 正确示例 - 避免 else
   public void ProcessOrder(Order order) {
       if (!order.IsValid) return;
       // Process order
   }
   ```

   快速失败原则示例：
   ```csharp
   public void ProcessOrder(Order order) {
       if (order == null) throw new ArgumentNullException(nameof(order));
       if (!order.IsValid) throw new InvalidOperationException("Invalid order");
       // Process order
   }
   ```

3. **包装所有基本类型和字符串**：
   - 避免在代码中直接使用基本类型。
   - 将它们包装在类中以提供有意义的上下文和行为。

   ```csharp
   // 错误示例 - 直接使用基本类型
   public class User {
       public string Name { get; set; }
       public int Age { get; set; }
   }
   // 正确示例 - 包装基本类型
   public class User {
       private string name;
       private Age age;
       public User(string name, Age age) {
           this.name = name;
           this.age = age;
       }
   }
   public class Age {
       private int value;
       public Age(int value) {
           if (value < 0) throw new ArgumentOutOfRangeException(nameof(value), "Age cannot be negative");
           this.value = value;
       }
   }
   ```

4. **一等公民集合**：
   - 使用集合封装数据和行为，而不是暴露原始数据结构。
一等公民集合：包含数组作为属性的类不应包含任何其他属性

```csharp
   // 错误示例 - 暴露原始集合
   public class Group {
      public int Id { get; private set; }
      public string Name { get; private set; }
      public List<User> Users { get; private set; }

      public int GetNumberOfUsersIsActive() {
         return Users
            .Where(user => user.IsActive)
            .Count();
      }
   }

   // 正确示例 - 封装集合行为
   public class Group {
      public int Id { get; private set; }
      public string Name { get; private set; }

      public GroupUserCollection userCollection { get; private set; } // 用户列表被封装在一个类中

      public int GetNumberOfUsersIsActive() {
         return userCollection
            .GetActiveUsers()
            .Count();
      }
   }
   ```

5. **每行一个点**：
   - 限制单行中方法调用的数量，以提高可读性和可维护性。

   ```csharp
   // 错误示例 - 单行中多个点
   public void ProcessOrder(Order order) {
       var userEmail = order.User.GetEmail().ToUpper().Trim();
       // Do something with userEmail
   }
   // 正确示例 - 每行一个点
   public void ProcessOrder(Order order) {
       var user = order.User;
       var email = user.GetEmail();
       var userEmail = email.ToUpper().Trim();
       // Do something with userEmail
   }
   ```

6. **不要缩写**：
   - 为类、方法和变量使用有意义的名称。
   - 避免可能导致混淆的缩写。

   ```csharp
   // 错误示例 - 缩写名称
   public class U {
       public string N { get; set; }
   }
   // 正确示例 - 有意义的名称
   public class User {
       public string Name { get; set; }
   }
   ```

7. **保持实体小巧（类、方法、命名空间或包）**：
   - 限制类和方法的大小以提高代码可读性和可维护性。
   - 每个类应该有单一职责并尽可能小。

   约束：
   - 每个类最多 10 个方法
   - 每个类最多 50 行
   - 每个包或命名空间最多 10 个类

   ```csharp
   // 错误示例 - 有多个职责的大类
   public class UserManager {
       public void CreateUser(string name) { /*...*/ }
       public void DeleteUser(int id) { /*...*/ }
       public void SendEmail(string email) { /*...*/ }
   }

   // 正确示例 - 有单一职责的小类
   public class UserCreator {
       public void CreateUser(string name) { /*...*/ }
   }
   public class UserDeleter {
       public void DeleteUser(int id) { /*...*/ }
   }

   public class UserUpdater {
       public void UpdateUser(int id, string name) { /*...*/ }
   }
   ```


8. **类的实例变量不超过两个**：
   - 通过限制实例变量的数量来鼓励类具有单一职责。
   - 将实例变量的数量限制为两个以保持简单性。
   - 不要将 ILogger 或任何其他日志记录器计算为实例变量。

   ```csharp
   // 错误示例 - 有多个实例变量的类
   public class UserCreateCommandHandler {
      // 错误：实例变量太多
      private readonly IUserRepository userRepository;
      private readonly IEmailService emailService;
      private readonly ILogger logger;
      private readonly ISmsService smsService;

      public UserCreateCommandHandler(IUserRepository userRepository, IEmailService emailService, ILogger logger, ISmsService smsService) {
         this.userRepository = userRepository;
         this.emailService = emailService;
         this.logger = logger;
         this.smsService = smsService;
      }
   }

   // 正确：有两个实例变量的类
   public class UserCreateCommandHandler {
      private readonly IUserRepository userRepository;
      private readonly INotificationService notificationService;
      private readonly ILogger logger; // 这不被计算为实例变量

      public UserCreateCommandHandler(IUserRepository userRepository, INotificationService notificationService, ILogger logger) {
         this.userRepository = userRepository;
         this.notificationService = notificationService;
         this.logger = logger;
      }
   }
   ```

9. **域类中不要有 Getters/Setters**：
   - 避免在域类中暴露属性的 setters。
   - 使用私有构造函数和静态工厂方法创建对象。
   - **注意**：此规则主要适用于域类，不适用于 DTOs 或数据传输对象。

   ```csharp
   // 错误示例 - 有公共 setters 的域类
   public class User {  // 域类
       public string Name { get; set; } // 在域类中避免这样做
   }

   // 正确示例 - 有封装的域类
   public class User {  // 域类
       private string name;
       private User(string name) { this.name = name; }
       public static User Create(string name) => new User(name);
   }

   // 可接受示例 - 有公共 setters 的 DTO
   public class UserDto {  // DTO - 豁免适用
       public string Name { get; set; } // 对于 DTOs 可接受
   }
   ```

## 实现指南
- **域类**：
  - 使用私有构造函数和静态工厂方法创建实例。
  - 避免暴露属性的 setters。
  - 对业务域代码严格应用所有 9 条规则。

- **应用层**：
  - 将这些规则应用于用例处理器和应用服务。
  - 专注于维护单一职责和清洁抽象。

- **DTOs 和数据对象**：
  - 对于 DTOs，可以放宽规则 3（包装基本类型）、8（两个实例变量）和 9（无 getters/setters）。
  - 对于数据传输对象，具有 getters/setters 的公共属性是可接受的。

- **测试**：
  - 确保测试验证对象的行为而不是其状态。
  - 测试类的规则可以为了可读性和可维护性而放宽。

- **代码审查**：
  - 在域和应用代码的代码审查中强制执行这些规则。
  - 对基础设施和 DTO 代码要务实。

## 参考资料
- [Object Calisthenics - Jeff Bay 的原始 9 条规则](https://www.cs.helsinki.fi/u/luontola/tdd-2009/ext/ObjectCalisthenics.pdf)
- [ThoughtWorks - Object Calisthenics](https://www.thoughtworks.com/insights/blog/object-calisthenics)
- [Clean Code: A Handbook of Agile Software Craftsmanship - Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)