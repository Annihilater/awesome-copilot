---
applyTo: ["*"]
description: "自 Java 11 发布以来采用新的 Java 17 功能的综合最佳实践。"
---

# Java 11 到 Java 17 升级指南

## 项目背景

本指南为升级 Java 项目从 JDK 11 到 JDK 17 提供全面的 GitHub Copilot 指导，涵盖基于这两个版本之间集成的 47 个 JEP 的主要语言特性、API 变更和迁移模式。

## 语言特性和 API 变更

### JEP 395: Records (Java 16)

**迁移模式**：将数据类转换为 records

```java
// 旧：传统数据类
public class Person {
    private final String name;
    private final int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String name() { return name; }
    public int age() { return age; }

    @Override
    public boolean equals(Object obj) { /* boilerplate */ }
    @Override
    public int hashCode() { /* boilerplate */ }
    @Override
    public String toString() { /* boilerplate */ }
}

// 新：Record (Java 16+)
public record Person(String name, int age) {
    // 紧凑构造器用于验证
    public Person {
        if (age < 0) throw new IllegalArgumentException("Age cannot be negative");
    }

    // 可以添加自定义方法
    public boolean isAdult() {
        return age >= 18;
    }
}
```

### JEP 409: Sealed Classes (Java 17)

**迁移模式**：使用 sealed classes 限制继承

```java
// 新：Sealed class 层次结构
public sealed class Shape
    permits Circle, Rectangle, Triangle {

    public abstract double area();
}

public final class Circle extends Shape {
    private final double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public final class Rectangle extends Shape {
    private final double width, height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public double area() {
        return width * height;
    }
}

public non-sealed class Triangle extends Shape {
    // Non-sealed 允许进一步继承
    private final double base, height;

    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }

    @Override
    public double area() {
        return 0.5 * base * height;
    }
}
```

### JEP 394: Pattern Matching for instanceof (Java 16)

**迁移模式**：简化 instanceof 检查

```java
// 旧：传统的 instanceof 与强制转换
public String processObject(Object obj) {
    if (obj instanceof String) {
        String str = (String) obj;
        return str.toUpperCase();
    } else if (obj instanceof Integer) {
        Integer num = (Integer) obj;
        return "Number: " + num;
    } else if (obj instanceof List<?>) {
        List<?> list = (List<?>) obj;
        return "List with " + list.size() + " elements";
    }
    return "Unknown type";
}

// 新：instanceof 的模式匹配 (Java 16+)
public String processObject(Object obj) {
    if (obj instanceof String str) {
        return str.toUpperCase();
    } else if (obj instanceof Integer num) {
        return "Number: " + num;
    } else if (obj instanceof List<?> list) {
        return "List with " + list.size() + " elements";
    }
    return "Unknown type";
}

// 与 sealed classes 配合使用效果很好
public String describeShape(Shape shape) {
    if (shape instanceof Circle circle) {
        return "Circle with radius " + circle.radius();
    } else if (shape instanceof Rectangle rect) {
        return "Rectangle " + rect.width() + "x" + rect.height();
    } else if (shape instanceof Triangle triangle) {
        return "Triangle with base " + triangle.base();
    }
    return "Unknown shape";
}
```

### JEP 361: Switch Expressions (Java 14)

**迁移模式**：将 switch 语句转换为表达式

```java
// 旧：传统 switch 语句
public String getDayType(DayOfWeek day) {
    String result;
    switch (day) {
        case MONDAY:
        case TUESDAY:
        case WEDNESDAY:
        case THURSDAY:
        case FRIDAY:
            result = "Workday";
            break;
        case SATURDAY:
        case SUNDAY:
            result = "Weekend";
            break;
        default:
            throw new IllegalArgumentException("Unknown day: " + day);
    }
    return result;
}

// 新：Switch 表达式 (Java 14+)
public String getDayType(DayOfWeek day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Workday";
        case SATURDAY, SUNDAY -> "Weekend";
    };
}

// 使用 yield 处理复杂逻辑
public int calculateScore(Grade grade) {
    return switch (grade) {
        case A -> 100;
        case B -> 85;
        case C -> 70;
        case D -> {
            System.out.println("Consider improvement");
            yield 55;
        }
        case F -> {
            System.out.println("Needs retake");
            yield 0;
        }
    };
}
```

### JEP 406: Pattern Matching for switch (Preview in Java 17)

**迁移模式**：增强的 switch 与模式 (预览功能)

```java
// 需要 --enable-preview 标志
public String formatValue(Object obj) {
    return switch (obj) {
        case String s -> "String: " + s;
        case Integer i -> "Integer: " + i;
        case null -> "null value";
        case default -> "Unknown: " + obj.getClass().getSimpleName();
    };
}

// 使用保护模式
public String categorizeNumber(Object obj) {
    return switch (obj) {
        case Integer i when i < 0 -> "Negative integer";
        case Integer i when i == 0 -> "Zero";
        case Integer i when i > 0 -> "Positive integer";
        case Double d when d.isNaN() -> "Not a number";
        case Number n -> "Other number: " + n;
        case null -> "null";
        case default -> "Not a number";
    };
}
```

### JEP 378: Text Blocks (Java 15)

**迁移模式**：对多行字符串使用文本块

```java
// 旧：连接的字符串
String html = "<html>\n" +
              "  <body>\n" +
              "    <h1>Hello World</h1>\n" +
              "    <p>Welcome to Java 17!</p>\n" +
              "  </body>\n" +
              "</html>";

String sql = "SELECT p.id, p.name, p.email, " +
             "       a.street, a.city, a.state " +
             "FROM person p " +
             "JOIN address a ON p.address_id = a.id " +
             "WHERE p.active = true " +
             "ORDER BY p.name";

// 新：文本块 (Java 15+)
String html = """
              <html>
                <body>
                  <h1>Hello World</h1>
                  <p>Welcome to Java 17!</p>
                </body>
              </html>
              """;

String sql = """
             SELECT p.id, p.name, p.email,
                    a.street, a.city, a.state
             FROM person p
             JOIN address a ON p.address_id = a.id
             WHERE p.active = true
             ORDER BY p.name
             """;

// 与字符串插值方法结合使用
String json = """
              {
                "name": "%s",
                "age": %d,
                "city": "%s"
              }
              """.formatted(name, age, city);
```

### JEP 358: Helpful NullPointerExceptions (Java 14)

**迁移指导**：更好的 NPE 调试 (在 Java 17 中默认启用)

```java
// 旧的 NPE 消息："Exception in thread 'main' java.lang.NullPointerException"
// 新的 NPE 消息准确显示什么是 null：
// "Cannot invoke 'String.length()' because the return value of 'Person.getName()' is null"

public class PersonProcessor {
    public void processPersons(List<Person> persons) {
        // 这将准确显示哪个 person.getName() 返回了 null
        persons.stream()
            .mapToInt(person -> person.getName().length())  // 如果 getName() 返回 null，会有清晰的 NPE
            .sum();
    }

    // 更好的错误消息有助于处理复杂表达式
    public void complexExample(Map<String, List<Person>> groups) {
        // NPE 将准确显示链中哪一部分是 null
        int totalNameLength = groups.get("admins")
                                  .get(0)
                                  .getName()
                                  .length();
    }
}
```

### JEP 371: Hidden Classes (Java 15)

**迁移模式**：用于框架和代理生成

```java
// 用于创建动态代理的框架
public class DynamicProxyExample {
    public static <T> T createProxy(Class<T> interfaceClass, InvocationHandler handler) {
        // Hidden classes 为动态生成的类提供更好的封装
        MethodHandles.Lookup lookup = MethodHandles.lookup();

        // 框架代码会使用 hidden classes 来获得更好的隔离
        // 这通常由框架处理，而不是应用程序代码
        return interfaceClass.cast(
            Proxy.newProxyInstance(
                interfaceClass.getClassLoader(),
                new Class<?>[]{interfaceClass},
                handler
            )
        );
    }
}
```

### JEP 334: JVM Constants API (Java 12)

**迁移模式**：用于编译时常量

```java
import java.lang.constant.*;

// 用于高级元编程和工具
public class ConstantExample {
    // 为计算值使用动态常量
    public static final DynamicConstantDesc<String> COMPUTED_CONSTANT =
        DynamicConstantDesc.of(
            ConstantDescs.BSM_INVOKE,
            "computeValue",
            ConstantDescs.CD_String
        );

    // 主要由编译器和框架开发人员使用
    public static String computeValue() {
        return "Computed at runtime, cached as constant";
    }
}
```

### JEP 415: Context-Specific Deserialization Filters (Java 17)

**迁移模式**：增强对象反序列化的安全性

```java
import java.io.*;

public class SecureDeserialization {
    // 为安全性设置反序列化过滤器
    public static void setupSerializationFilters() {
        // 全局过滤器
        ObjectInputFilter globalFilter = ObjectInputFilter.Config.createFilter(
            "java.base/*;java.util.*;!*"
        );
        ObjectInputFilter.Config.setSerialFilter(globalFilter);
    }

    public <T> T deserializeSecurely(byte[] data, Class<T> expectedType) throws IOException, ClassNotFoundException {
        try (ByteArrayInputStream bis = new ByteArrayInputStream(data);
             ObjectInputStream ois = new ObjectInputStream(bis)) {

            // 上下文特定过滤器
            ObjectInputFilter contextFilter = ObjectInputFilter.Config.createFilter(
                expectedType.getName() + ";java.lang.*;!*"
            );
            ois.setObjectInputFilter(contextFilter);

            return expectedType.cast(ois.readObject());
        }
    }
}
```

### JEP 356: Enhanced Pseudo-Random Number Generators (Java 17)

**迁移模式**：使用新的随机生成器接口

```java
import java.util.random.*;

// 旧：受限的 Random 类
Random oldRandom = new Random();
int oldValue = oldRandom.nextInt(100);

// 新：增强的随机生成器 (Java 17+)
RandomGenerator generator = RandomGeneratorFactory
    .of("Xoshiro256PlusPlus")
    .create(System.nanoTime());

RandomGenerator.SplittableGenerator splittableGenerator =
    RandomGeneratorFactory.of("L64X128MixRandom").create();

// 更适合并行处理
splittableGenerator.splits(4)
    .parallel()
    .mapToInt(rng -> rng.nextInt(1000))
    .forEach(System.out::println);

// 可流式传输的随机值
generator.ints(10, 1, 101)
    .forEach(System.out::println);
```

## I/O 和网络改进

### JEP 380: Unix-Domain Socket Channels (Java 16)

**迁移模式**：使用 Unix domain socket 进行本地 IPC

```java
import java.net.UnixDomainSocketAddress;
import java.nio.channels.*;

// 旧：用于本地通信的 TCP socket
// ServerSocketChannel server = ServerSocketChannel.open();
// server.bind(new InetSocketAddress("localhost", 8080));

// 新：Unix domain sockets (Java 16+)
public class UnixSocketExample {
    public void createUnixDomainServer() throws IOException {
        Path socketPath = Path.of("/tmp/my-app.socket");
        UnixDomainSocketAddress address = UnixDomainSocketAddress.of(socketPath);

        try (ServerSocketChannel server = ServerSocketChannel.open(StandardProtocolFamily.UNIX)) {
            server.bind(address);

            while (true) {
                try (SocketChannel client = server.accept()) {
                    // 处理客户端连接
                    handleClient(client);
                }
            }
        }
    }

    public void connectToUnixSocket() throws IOException {
        Path socketPath = Path.of("/tmp/my-app.socket");
        UnixDomainSocketAddress address = UnixDomainSocketAddress.of(socketPath);

        try (SocketChannel client = SocketChannel.open(address)) {
            // 与服务器通信
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            client.read(buffer);
        }
    }

    private void handleClient(SocketChannel client) throws IOException {
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        int bytesRead = client.read(buffer);
        // 处理客户端数据
    }
}
```

### JEP 352: Non-Volatile Mapped Byte Buffers (Java 14)

**迁移模式**：用于持久内存操作

```java
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.StandardOpenOption;

public class PersistentMemoryExample {
    public void usePersistentMemory() throws IOException {
        Path nvmFile = Path.of("/mnt/pmem/data.bin");

        try (FileChannel channel = FileChannel.open(nvmFile,
                StandardOpenOption.READ,
                StandardOpenOption.WRITE,
                StandardOpenOption.CREATE)) {

            // 映射为持久内存
            MappedByteBuffer buffer = channel.map(
                FileChannel.MapMode.READ_WRITE, 0, 1024,
                ExtendedMapMode.READ_WRITE_SYNC
            );

            // 写入跨崩溃持久化的数据
            buffer.putLong(0, System.currentTimeMillis());
            buffer.putInt(8, 12345);

            // 强制写入持久存储
            buffer.force();
        }
    }
}
```

## 构建系统配置

### Maven 配置

```xml
<properties>
    <maven.compiler.source>17</maven.compiler.source>
    <maven.compiler.target>17</maven.compiler.target>
    <maven.compiler.release>17</maven.compiler.release>
</properties>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <release>17</release>
                <!-- 如果使用 JEP 406，启用预览功能 -->
                <compilerArgs>
                    <arg>--enable-preview</arg>
                </compilerArgs>
            </configuration>
        </plugin>

        <!-- 用于使用预览功能运行测试 -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0</version>
            <configuration>
                <argLine>--enable-preview</argLine>
            </configuration>
        </plugin>
    </plugins>
</build>
```

### Gradle 配置

```kotlin
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks.withType<JavaCompile> {
    options.release.set(17)
    // 如有需要启用预览功能
    options.compilerArgs.addAll(listOf("--enable-preview"))
}

tasks.withType<Test> {
    useJUnitPlatform()
    // 为测试启用预览功能
    jvmArgs("--enable-preview")
}
```

## 弃用和移除

### JEP 411: Deprecate the Security Manager for Removal

**迁移模式**：移除 Security Manager 依赖

```java
// 旧：使用 Security Manager
SecurityManager sm = System.getSecurityManager();
if (sm != null) {
    sm.checkPermission(new RuntimePermission("shutdownHooks"));
}

// 新：替代安全方法
// 使用应用级安全、容器或进程隔离
// 大多数应用程序不需要 Security Manager 功能
```

### JEP 398: Deprecate the Applet API for Removal

**迁移模式**：从 Applets 迁移到现代 web 技术

```java
// 旧：Java Applet (已弃用)
public class MyApplet extends Applet {
    @Override
    public void start() {
        // Applet 代码
    }
}

// 新：现代替代方案
// 1. 转换为独立的 Java 应用程序
public class MyApplication extends JFrame {
    public MyApplication() {
        setTitle("My Application");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        // 应用程序代码
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new MyApplication().setVisible(true);
        });
    }
}

// 2. 使用 Java Web Start 替代方案 (jlink)
// 3. 使用现代框架转换为 web 应用程序
```

### JEP 372: Remove the Nashorn JavaScript Engine

**迁移模式**：使用替代的 JavaScript 引擎

```java
// 旧：Nashorn (在 Java 17 中已移除)
// ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");

// 新：替代方法
// 1. 使用 GraalVM JavaScript 引擎
ScriptEngine engine = new ScriptEngineManager().getEngineByName("graal.js");

// 2. 使用外部 JavaScript 执行
ProcessBuilder pb = new ProcessBuilder("node", "script.js");
Process process = pb.start();

// 3. 使用基于 web 的方法或嵌入式浏览器
```

## JVM 和性能改进

### JEP 377: ZGC - A Scalable Low-Latency Garbage Collector (Java 15)

**迁移模式**：为低延迟应用程序启用 ZGC

```bash
# 启用 ZGC
-XX:+UseZGC
-XX:+UnlockExperimentalVMOptions  # Java 17 中不需要

# 监控 ZGC 性能
-XX:+LogVMOutput
-XX:LogFile=gc.log
```

### JEP 379: Shenandoah - A Low-Pause-Time Garbage Collector (Java 15)

**迁移模式**：为一致延迟启用 Shenandoah

```bash
# 启用 Shenandoah
-XX:+UseShenandoahGC
-XX:+UnlockExperimentalVMOptions  # Java 17 中不需要

# Shenandoah 调优
-XX:ShenandoahGCHeuristics=adaptive
```

### JEP 341: Default CDS Archives (Java 12) & JEP 350: Dynamic CDS Archives (Java 13)

**迁移模式**：改进的启动性能

```bash
# CDS 默认启用，但您可以创建自定义存档
# 创建自定义 CDS 存档
java -XX:DumpLoadedClassList=classes.lst -cp myapp.jar com.example.Main
java -Xshare:dump -XX:SharedClassListFile=classes.lst -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar

# 使用自定义 CDS 存档
java -XX:SharedArchiveFile=myapp.jsa -cp myapp.jar com.example.Main
```

## 测试和迁移策略

### 第1阶段：基础 (第1-2周)

1. **更新构建系统**

   - 修改 Maven/Gradle 配置为 Java 17
   - 更新 CI/CD 管道
   - 验证依赖兼容性

2. **处理移除和弃用**
   - 移除 Nashorn JavaScript 引擎使用
   - 替换弃用的 Applet API
   - 更新 Security Manager 使用

### 第2阶段：语言特性 (第3-4周)

1. **实现 Records**

   - 将数据类转换为 records
   - 在紧凑构造器中添加验证
   - 测试序列化兼容性

2. **添加模式匹配**
   - 转换 instanceof 链
   - 实现类型安全的强制转换模式

### 第3阶段：高级特性 (第5-6周)

1. **Switch 表达式**

   - 将 switch 语句转换为表达式
   - 使用新的箭头语法
   - 实现复杂的 yield 逻辑

2. **文本块**
   - 替换连接的多行字符串
   - 更新 SQL 和 HTML 生成
   - 使用格式化方法

### 第4阶段：Sealed Classes (第7-8周)

1. **设计 sealed 层次结构**

   - 识别继承限制
   - 实现 sealed class 模式
   - 与模式匹配结合

2. **测试和验证**
   - 全面的测试覆盖
   - 性能基准测试
   - 兼容性验证

## 性能考虑

### Records vs 传统类

- Records 更节省内存
- 更快的创建和相等性检查
- 自动序列化支持
- 考虑用于数据传输对象

### 模式匹配性能

- 消除冗余类型检查
- 减少强制转换开销
- 更好的 JVM 优化机会
- 与 sealed classes 一起使用以获得详尽性

### Switch 表达式优化

- 更高效的字节码生成
- 更好的常量折叠
- 改进的分支预测
- 用于复杂条件逻辑

## 最佳实践

1. **对数据类使用 Records**

   - 不可变数据容器
   - API 数据传输对象
   - 配置对象

2. **战略性地应用模式匹配**

   - 替换 instanceof 链
   - 与 sealed classes 一起使用
   - 与 switch 表达式结合

3. **对多行内容采用文本块**

   - SQL 查询
   - JSON 模板
   - HTML 内容
   - 配置文件

4. **使用 Sealed Classes 设计**

   - 领域建模
   - 状态机
   - 代数数据类型
   - API 演化控制

5. **利用增强的随机生成器**
   - 并行处理场景
   - 高质量随机数
   - 统计应用
   - 游戏和模拟

这个综合指南使 GitHub Copilot 能够在将 Java 11 项目升级到 Java 17 时提供上下文相关的建议，重点关注语言增强、API 改进和现代 Java 开发实践。