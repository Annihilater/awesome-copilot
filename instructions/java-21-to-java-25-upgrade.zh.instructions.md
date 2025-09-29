---
applyTo: ['*']
description: "自 Java 21 发布以来采用新的 Java 25 功能的综合最佳实践。"
---

# Java 21 到 Java 25 升级指南

这些指导帮助 GitHub Copilot 协助开发人员将 Java 项目从 JDK 21 升级到 JDK 25，重点关注新的语言特性、API 变更和最佳实践。

## JDK 22-25 中的语言特性和 API 变更

### Pattern Matching Enhancements (JEP 455/488 - 在 23 中预览)

**在模式、instanceof 和 switch 中的原始类型**

在处理模式匹配时：
- 建议在 switch 表达式和 instanceof 检查中使用原始类型模式
- 从传统 switch 升级的示例：
```java
// 旧方法 (Java 21)
switch (x.getStatus()) {
    case 0 -> "okay";
    case 1 -> "warning";
    case 2 -> "error";
    default -> "unknown status: " + x.getStatus();
}

// 新方法 (Java 25 预览)
switch (x.getStatus()) {
    case 0 -> "okay";
    case 1 -> "warning";
    case 2 -> "error";
    case int i -> "unknown status: " + i;
}
```

- 使用 `--enable-preview` 标志启用预览功能
- 为更复杂的条件建议保护模式：
```java
switch (x.getYearlyFlights()) {
    case 0 -> ...;
    case int i when i >= 100 -> issueGoldCard();
    case int i -> ... // 处理 1-99 范围
}
```

### Class-File API (JEP 466/484 - 在 23 中第二次预览，在 25 中标准化)

**用标准 API 替换 ASM**

在检测字节码操作或类文件处理时：
- 建议从 ASM 库迁移到标准的 Class-File API
- 使用 `java.lang.classfile` 包而不是 `org.objectweb.asm`
- 示例迁移模式：
```java
// 旧的 ASM 方法
ClassReader reader = new ClassReader(classBytes);
ClassWriter writer = new ClassWriter(reader, 0);
// ... ASM 操作

// 新的 Class-File API 方法
ClassModel classModel = ClassFile.of().parse(classBytes);
byte[] newBytes = ClassFile.of().transform(classModel,
    ClassTransform.transformingMethods(methodTransform));
```

### Markdown Documentation Comments (JEP 467 - 在 23 中标准化)

**JavaDoc 现代化**

在处理 JavaDoc 注释时：
- 建议将富含 HTML 的 JavaDoc 转换为 Markdown 语法
- 使用 `///` 进行 Markdown 文档注释
- 示例转换：
```java
// 旧的 HTML JavaDoc
/**
 * Returns the <b>absolute</b> value of an {@code int} value.
 * <p>
 * If the argument is not negative, return the argument.
 * If the argument is negative, return the negation of the argument.
 *
 * @param a the argument whose absolute value is to be determined
 * @return the absolute value of the argument
 */

// 新的 Markdown JavaDoc
/// Returns the **absolute** value of an `int` value.
///
/// If the argument is not negative, return the argument.
/// If the argument is negative, return the negation of the argument.
///
/// @param a the argument whose absolute value is to be determined
/// @return the absolute value of the argument
```

### Derived Record Creation (JEP 468 - 在 23 中预览)

**Record 增强**

在处理 records 时：
- 建议使用 `with` 表达式创建派生记录
- 为派生记录创建启用预览功能
- 示例模式：
```java
// 而不是手动记录复制
public record Person(String name, int age, String email) {
    public Person withAge(int newAge) {
        return new Person(name, newAge, email);
    }
}

// 使用派生记录创建 (预览)
Person updated = person with { age = 30; };
```

### Stream Gatherers (JEP 473/485 - 在 23 中第二次预览，在 25 中标准化)

**增强的流处理**

在处理复杂流操作时：
- 为自定义中间操作建议使用 `Stream.gather()`
- 导入 `java.util.stream.Gatherers` 获取内置收集器
- 示例用法：
```java
// 自定义窗口操作
List<List<String>> windows = stream
    .gather(Gatherers.windowSliding(3))
    .toList();

// 带状态的自定义过滤
List<Integer> filtered = numbers.stream()
    .gather(Gatherers.fold(0, (state, element) -> {
        // 自定义有状态逻辑
        return state + element > threshold ? element : null;
    }))
    .filter(Objects::nonNull)
    .toList();
```

## 迁移警告和弃用

### sun.misc.Unsafe Memory Access Methods (JEP 471 - 在 23 中弃用)

在检测 `sun.misc.Unsafe` 使用时：
- 警告关于弃用的内存访问方法
- 建议迁移到标准替代方案：
```java
// 弃用：sun.misc.Unsafe 内存访问
Unsafe unsafe = Unsafe.getUnsafe();
unsafe.getInt(object, offset);

// 首选：VarHandle API
VarHandle vh = MethodHandles.lookup()
    .findVarHandle(MyClass.class, "fieldName", int.class);
int value = (int) vh.get(object);

// 或者对于堆外：Foreign Function & Memory API
MemorySegment segment = MemorySegment.ofArray(new int[10]);
int value = segment.get(ValueLayout.JAVA_INT, offset);
```

### JNI Usage Warnings (JEP 472 - 在 24 中警告)

在检测 JNI 使用时：
- 警告即将对 JNI 使用的限制
- 为使用 JNI 的应用程序建议添加 `--enable-native-access` 标志
- 在可能的地方推荐迁移到 Foreign Function & Memory API
- 在 module-info.java 中添加本地访问条目：
```java
module com.example.app {
    requires jdk.unsupported; // 用于剩余的 JNI 使用
}
```

## 垃圾收集更新

### ZGC Generational Mode (JEP 474 - 在 23 中默认)

在配置垃圾收集时：
- 默认 ZGC 现在使用分代模式
- 如果显式使用非分代 ZGC，更新 JVM 标志：
```bash
# 显式非分代模式 (将显示弃用警告)
-XX:+UseZGC -XX:-ZGenerational

# 默认分代模式
-XX:+UseZGC
```

### G1 Improvements (JEP 475 - 在 24 中实现)

在使用 G1GC 时：
- 不需要代码更改 - 内部 JVM 优化
- 可能会看到 C2 编译器的编译性能改进

## Vector API (JEP 469 - 在 25 中第八次孵化)

在处理数值计算时：
- 为 SIMD 操作建议 Vector API (仍在孵化中)
- 添加 `--add-modules jdk.incubator.vector`
- 示例用法：
```java
import jdk.incubator.vector.*;

// 传统标量计算
for (int i = 0; i < a.length; i++) {
    c[i] = a[i] + b[i];
}

// 向量化计算
var species = IntVector.SPECIES_PREFERRED;
for (int i = 0; i < a.length; i += species.length()) {
    var va = IntVector.fromArray(species, a, i);
    var vb = IntVector.fromArray(species, b, i);
    var vc = va.add(vb);
    vc.intoArray(c, i);
}
```

## 编译和构建配置

### 预览功能

对于使用预览功能的项目：
- 向编译器参数添加 `--enable-preview`
- 向运行时参数添加 `--enable-preview`
- Maven 配置：
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <release>25</release>
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
        languageVersion = JavaLanguageVersion.of(25)
    }
}

tasks.withType<JavaCompile> {
    options.compilerArgs.add("--enable-preview")
}

tasks.withType<Test> {
    jvmArgs("--enable-preview")
}
```

## 迁移策略

### 分步升级过程

1. **更新构建工具**：确保 Maven/Gradle 支持 JDK 25
2. **更新依赖项**：检查 JDK 25 兼容性
3. **处理警告**：解决来自 JEP 471/472 的弃用警告
4. **启用预览功能**：如果使用模式匹配或其他预览功能
5. **彻底测试**：特别是使用 JNI 或 sun.misc.Unsafe 的应用程序
6. **性能测试**：验证新 ZGC 默认设置的 GC 行为

### 代码审查检查清单

在审查 Java 25 升级代码时：
- [ ] 用 Class-File API 替换 ASM 使用
- [ ] 将复杂的 HTML JavaDoc 转换为 Markdown
- [ ] 在适用的地方在 switch 表达式中使用原始模式
- [ ] 用 VarHandle 或 FFM API 替换 sun.misc.Unsafe
- [ ] 为 JNI 使用添加本地访问权限
- [ ] 为复杂流操作使用 Stream gatherers
- [ ] 为预览功能更新构建配置

### 测试考虑

- 使用 `--enable-preview` 标志测试预览功能
- 验证 JNI 应用程序在本地访问警告下工作
- 使用新的 ZGC 分代模式进行性能测试
- 验证使用 Markdown 注释的 JavaDoc 生成

## 常见陷阱

1. **预览功能依赖**：不要在库代码中使用预览功能，除非有明确文档
2. **本地访问**：直接或间接使用 JNI 的应用程序可能需要 `--enable-native-access` 配置
3. **Unsafe 迁移**：不要延迟从 sun.misc.Unsafe 迁移 - 弃用警告表明未来会移除
4. **模式匹配范围**：原始模式适用于所有原始类型，不仅仅是 int
5. **Record 增强**：派生记录创建在 Java 23 中需要预览标志

## 性能考虑

- ZGC 分代模式可能改善大多数工作负载的性能
- Class-File API 减少 ASM 相关开销
- Stream gatherers 为复杂流操作提供更好的性能
- G1GC 改进减少 JIT 编译开销

记住在将 Java 25 升级部署到生产系统之前，在暂存环境中彻底测试。