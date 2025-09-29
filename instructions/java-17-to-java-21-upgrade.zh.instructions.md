---
applyTo: ['*']
description: "自 Java 17 发布以来采用新的 Java 21 功能的综合最佳实践。"
---

# Java 17 到 Java 21 升级指南

这些指导帮助 GitHub Copilot 协助开发人员将 Java 项目从 JDK 17 升级到 JDK 21，重点关注新的语言特性、API 变更和最佳实践。

## JDK 18-21 中的主要语言特性

### Pattern Matching for switch (JEP 441 - 在 21 中标准化)

**增强的 switch 表达式和语句**

在使用 switch 构造时：
- 建议在适当的地方将传统 switch 转换为模式匹配
- 使用模式匹配进行类型检查和解构
- 示例升级模式：
```java
// 旧方法 (Java 17)
public String processObject(Object obj) {
    if (obj instanceof String) {
        String s = (String) obj;
        return s.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer i = (Integer) obj;
        return i.toString();
    }
    return "unknown";
}

// 新方法 (Java 21)
public String processObject(Object obj) {
    return switch (obj) {
        case String s -> s.toUpperCase();
        case Integer i -> i.toString();
        case null -> "null";
        default -> "unknown";
    };
}
```

- 支持保护模式：
```java
switch (obj) {
    case String s when s.length() > 10 -> "Long string: " + s;
    case String s -> "Short string: " + s;
    case Integer i when i > 100 -> "Large number: " + i;
    case Integer i -> "Small number: " + i;
    default -> "Other";
}
```

### Record Patterns (JEP 440 - 在 21 中标准化)

**在模式匹配中解构 Records**

在使用 records 时：
- 建议使用记录模式进行解构
- 与 switch 表达式结合以实现强大的数据处理
- 示例用法：
```java
public record Point(int x, int y) {}
public record ColoredPoint(Point point, Color color) {}

// 在 switch 中解构
public String describe(Object obj) {
    return switch (obj) {
        case Point(var x, var y) -> "Point at (" + x + ", " + y + ")";
        case ColoredPoint(Point(var x, var y), var color) ->
            "Colored point at (" + x + ", " + y + ") in " + color;
        default -> "Unknown shape";
    };
}
```

- 在复杂模式匹配中使用：
```java
// 嵌套记录模式
switch (shape) {
    case Rectangle(ColoredPoint(Point(var x1, var y1), var c1),
                   ColoredPoint(Point(var x2, var y2), var c2))
        when c1 == c2 -> "Monochrome rectangle";
    case Rectangle r -> "Multi-colored rectangle";
}
```

### Virtual Threads (JEP 444 - 在 21 中标准化)

**轻量级并发**

在处理并发时：
- 为高吞吐量、并发应用程序建议 Virtual Threads
- 使用 `Thread.ofVirtual()` 创建虚拟线程
- 示例迁移模式：
```java
// 旧的平台线程方法
ExecutorService executor = Executors.newFixedThreadPool(100);
executor.submit(() -> {
    // 阻塞 I/O 操作
    httpClient.send(request);
});

// 新的虚拟线程方法
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // 阻塞 I/O 操作 - 现在扩展到数百万
        httpClient.send(request);
    });
}
```

- 使用结构化并发模式：
```java
// 结构化并发 (预览)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser(userId));
    Future<String> order = scope.fork(() -> fetchOrder(orderId));

    scope.join();           // 加入所有子任务
    scope.throwIfFailed();  // 传播错误

    return processResults(user.resultNow(), order.resultNow());
}
```

### String Templates (JEP 430 - 在 21 中预览)

**安全字符串插值**

在处理字符串格式化时：
- 为安全字符串插值建议 String Templates (预览功能)
- 使用 `--enable-preview` 启用预览功能
- 示例用法：
```java
// 传统连接
String message = "Hello, " + name + "! You have " + count + " messages.";

// String Templates (预览)
String message = STR."Hello, \{name}! You have \{count} messages.";

// 安全 HTML 生成
String html = HTML."<p>User: \{username}</p>";

// 安全 SQL 查询
PreparedStatement stmt = SQL."SELECT * FROM users WHERE id = \{userId}";
```

### Sequenced Collections (JEP 431 - 在 21 中标准化)

**增强的集合接口**

在处理集合时：
- 使用新的 `SequencedCollection`、`SequencedSet`、`SequencedMap` 接口
- 跨集合类型统一访问第一个/最后一个元素
- 示例用法：
```java
// 在 Lists、Deques、LinkedHashSet 等上可用的新方法
List<String> list = List.of("first", "middle", "last");
String first = list.getFirst();  // "first"
String last = list.getLast();    // "last"
List<String> reversed = list.reversed(); // ["last", "middle", "first"]

// 适用于任何 SequencedCollection
SequencedSet<String> set = new LinkedHashSet<>();
set.addFirst("start");
set.addLast("end");
String firstElement = set.getFirst();
```

### Unnamed Patterns and Variables (JEP 443 - 在 21 中预览)

**简化的模式匹配**

在处理模式匹配时：
- 为不需要的值使用未命名模式 `_`
- 简化 switch 表达式和记录模式
- 示例用法：
```java
// 忽略未使用的变量
switch (ball) {
    case RedBall(_) -> "Red ball";     // 不关心大小
    case BlueBall(var size) -> "Blue ball size " + size;
}

// 忽略记录的部分
switch (point) {
    case Point(var x, _) -> "X coordinate: " + x; // 忽略 Y
    case ColoredPoint(Point(_, var y), _) -> "Y coordinate: " + y;
}

// 使用未命名变量的异常处理
try {
    riskyOperation();
} catch (IOException | SQLException _) {
    // 不需要异常详情
    handleError();
}
```

### Scoped Values (JEP 446 - 在 21 中预览)

**改进的上下文传播**

在处理线程本地数据时：
- 考虑 Scoped Values 作为 ThreadLocal 的现代替代方案
- 为虚拟线程提供更好的性能和更清晰的语义
- 示例用法：
```java
// 定义作用域值
private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

// 设置和使用作用域值
ScopedValue.where(USER_ID, "user123")
    .run(() -> {
        processRequest(); // 可以在调用链中的任何地方访问 USER_ID.get()
    });

// 在嵌套方法中
public void processRequest() {
    String userId = USER_ID.get(); // "user123"
    // 使用用户上下文处理
}
```

## API 增强和新功能

### UTF-8 by Default (JEP 400 - 在 18 中标准化)

在处理文件 I/O 时：
- UTF-8 现在是所有平台上的默认字符集
- 在预期使用 UTF-8 的地方移除显式字符集规范
- 示例简化：
```java
// 旧的显式 UTF-8 规范
Files.readString(path, StandardCharsets.UTF_8);
Files.writeString(path, content, StandardCharsets.UTF_8);

// 新的默认行为 (Java 18+)
Files.readString(path);  // 默认使用 UTF-8
Files.writeString(path, content);  // 默认使用 UTF-8
```

### Simple Web Server (JEP 408 - 在 18 中标准化)

在需要基本 HTTP 服务器时：
- 使用内置的 `jwebserver` 命令或 `com.sun.net.httpserver` 增强功能
- 非常适合测试和开发
- 示例用法：
```java
// 命令行
$ jwebserver -p 8080 -d /path/to/files

// 编程用法
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/", new SimpleFileHandler(Path.of("/tmp")));
server.start();
```

### Internet-Address Resolution SPI (JEP 418 - 在 19 中标准化)

在处理自定义 DNS 解析时：
- 为自定义地址解析实现 `InetAddressResolverProvider`
- 对服务发现和测试场景有用

### Key Encapsulation Mechanism API (JEP 452 - 在 21 中标准化)

在处理后量子密码学时：
- 使用 KEM API 进行密钥封装机制
- 示例用法：
```java
KeyPairGenerator kpg = KeyPairGenerator.getInstance("ML-KEM");
KeyPair kp = kpg.generateKeyPair();

KEM kem = KEM.getInstance("ML-KEM");
KEM.Encapsulator encapsulator = kem.newEncapsulator(kp.getPublic());
KEM.Encapsulated encapsulated = encapsulator.encapsulate();
```

## 弃用和警告

### Finalization Deprecation (JEP 421 - 在 18 中弃用)

在遇到 `finalize()` 方法时：
- 移除 finalize 方法并使用替代方案
- 建议 Cleaner API 或 try-with-resources
- 示例迁移：
```java
// 弃用的 finalize 方法
@Override
protected void finalize() throws Throwable {
    cleanup();
}

// 使用 Cleaner 的现代方法
private static final Cleaner CLEANER = Cleaner.create();

public MyResource() {
    cleaner.register(this, new CleanupTask(nativeResource));
}

private static class CleanupTask implements Runnable {
    private final long nativeResource;

    CleanupTask(long nativeResource) {
        this.nativeResource = nativeResource;
    }

    public void run() {
        cleanup(nativeResource);
    }
}
```

### Dynamic Agent Loading (JEP 451 - 在 21 中警告)

在处理代理或工具时：
- 如果需要，添加 `-XX:+EnableDynamicAgentLoading` 来抑制警告
- 考虑在启动时加载代理而不是动态加载
- 更新工具以使用启动代理加载

## 构建配置更新

### 预览功能

对于使用预览功能的项目：
- 向编译器和运行时添加 `--enable-preview`
- Maven 配置：
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>21</release>
        <compilerArgs>
            <arg>--enable-preview</arg>
        </compilerArgs>
    </configuration>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <argLine>--enable-preview</argLine>
    </configuration>
</plugin>
```

- Gradle 配置：
```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}

tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}
```

### Virtual Threads 配置

对于使用 Virtual Threads 的应用程序：
- 不需要特殊的 JVM 标志 (在 21 中是标准功能)
- 考虑这些系统属性进行调试：
```bash
-Djdk.virtualThreadScheduler.parallelism=N  # 设置载体线程数
-Djdk.virtualThreadScheduler.maxPoolSize=N  # 设置最大池大小
```

## 运行时和 GC 改进

### Generational ZGC (JEP 439 - 在 21 中可用)

在配置垃圾收集时：
- 尝试 Generational ZGC 以获得更好的性能
- 使用以下命令启用：`-XX:+UseZGC -XX:+ZGenerational`
- 监控分配模式和 GC 行为

## 迁移策略

### 分步升级过程

1. **更新构建工具**：确保 Maven/Gradle 支持 JDK 21
2. **语言功能采用**：
   - 从 switch 的模式匹配开始 (标准)
   - 在有益的地方添加记录模式
   - 为 I/O 密集型应用程序考虑 Virtual Threads
3. **预览功能**：仅在特定用例需要时启用
4. **测试**：全面测试，特别是并发更改
5. **性能**：使用新的 GC 选项进行基准测试

### 代码审查检查清单

在审查 Java 21 升级代码时：
- [ ] 将适当的 instanceof 链转换为 switch 表达式
- [ ] 为数据解构使用记录模式
- [ ] 在适当的地方用 ScopedValues 替换 ThreadLocal
- [ ] 为高并发场景考虑 Virtual Threads
- [ ] 移除显式 UTF-8 字符集规范
- [ ] 用 Cleaner 或 try-with-resources 替换 finalize() 方法
- [ ] 为第一个/最后一个访问模式使用 SequencedCollection 方法
- [ ] 仅为使用中的预览功能添加预览标志

### 常见迁移模式

1. **Switch 增强**：
   ```java
   // 从 instanceof 链到 switch 表达式
   if (obj instanceof String s) return processString(s);
   else if (obj instanceof Integer i) return processInt(i);
   // 变成：
   return switch (obj) {
       case String s -> processString(s);
       case Integer i -> processInt(i);
       default -> processDefault(obj);
   };
   ```

2. **Virtual Thread 采用**：
   ```java
   // 从平台线程到虚拟线程
   Executors.newFixedThreadPool(200)
   // 变成：
   Executors.newVirtualThreadPerTaskExecutor()
   ```

3. **Record Pattern 使用**：
   ```java
   // 从手动解构到记录模式
   if (point instanceof Point p) {
       int x = p.x();
       int y = p.y();
   }
   // 变成：
   if (point instanceof Point(var x, var y)) {
       // 直接使用 x 和 y
   }
   ```

## 性能考虑

- Virtual Threads 在阻塞 I/O 中表现出色，但可能不会使 CPU 密集型任务受益
- Generational ZGC 可以减少大多数应用程序的 GC 开销
- switch 中的模式匹配通常比 instanceof 链更高效
- SequencedCollection 方法提供对第一个/最后一个元素的 O(1) 访问
- Scoped Values 对虚拟线程的开销比 ThreadLocal 更低

## 测试建议

- 在高并发下测试 Virtual Thread 应用程序
- 验证模式匹配涵盖所有预期情况
- 使用 Generational ZGC 与其他收集器进行性能测试
- 验证跨不同平台的 UTF-8 默认行为
- 在生产使用之前彻底测试预览功能

记住只在特别需要时启用预览功能，并在部署到生产环境之前在暂存环境中彻底测试。