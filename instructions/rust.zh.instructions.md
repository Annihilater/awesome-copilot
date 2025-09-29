---
description: 'Rust 编程语言编码约定和最佳实践'
applyTo: '**/*.rs'
---

# Rust 编码约定和最佳实践

编写 Rust 代码时遵循惯用的 Rust 实践和社区标准。

这些指令基于 [The Rust Book](https://doc.rust-lang.org/book/)、[Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)、[RFC 430 命名约定](https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md) 和更广泛的 Rust 社区 [users.rust-lang.org](https://users.rust-lang.org)。

## 通用指令

- 始终优先考虑可读性、安全性和可维护性。
- 使用强类型并利用 Rust 的所有权系统实现内存安全。
- 将复杂函数分解为更小、更易管理的函数。
- 对于算法相关的代码，包括对所使用方法的解释。
- 编写具有良好可维护性实践的代码，包括对某些设计决策原因的注释。
- 使用 `Result<T, E>` 优雅地处理错误并提供有意义的错误消息。
- 对于外部依赖项，在文档中提及其用法和目的。
- 使用遵循 [RFC 430](https://github.com/rust-lang/rfcs/blob/master/text/0430-finalizing-naming-conventions.md) 的一致命名约定。
- 编写惯用、安全且高效的 Rust 代码，遵循借用检查器的规则。
- 确保代码编译时没有警告。

## 要遵循的模式

- 使用模块（`mod`）和公共接口（`pub`）来封装逻辑。
- 使用 `?`、`match` 或 `if let` 正确处理错误。
- 使用 `serde` 进行序列化，使用 `thiserror` 或 `anyhow` 处理自定义错误。
- 实现 trait 来抽象服务或外部依赖项。
- 使用 `async/await` 和 `tokio` 或 `async-std` 构建异步代码。
- 为了类型安全，偏好枚举而非标志和状态。
- 使用构建器模式创建复杂对象。
- 为了可测试性和重用性，分离二进制和库代码（`main.rs` vs `lib.rs`）。
- 使用 `rayon` 进行数据并行和 CPU 密集型任务。
- 使用迭代器而不是基于索引的循环，因为它们通常更快更安全。
- 当不需要所有权时，在函数参数中使用 `&str` 而不是 `String`。
- 偏好借用和零拷贝操作以避免不必要的分配。

### 所有权、借用和生命周期

- 除非需要所有权转移，否则偏好借用（`&T`）而不是克隆。
- 当需要修改借用数据时使用 `&mut T`。
- 当编译器无法推断生命周期时，显式注释生命周期。
- 对单线程引用计数使用 `Rc<T>`，对线程安全引用计数使用 `Arc<T>`。
- 在单线程上下文中使用 `RefCell<T>` 进行内部可变性，在多线程上下文中使用 `Mutex<T>` 或 `RwLock<T>`。

## 要避免的模式

- 除非绝对必要，否则不要使用 `unwrap()` 或 `expect()` — 偏好适当的错误处理。
- 避免在库代码中使用 panic — 返回 `Result` 代替。
- 不要依赖全局可变状态 — 使用依赖注入或线程安全容器。
- 避免深度嵌套的逻辑 — 使用函数或组合器重构。
- 不要忽略警告 — 在 CI 期间将它们视为错误。
- 除非必需且完全记录，否则避免使用 `unsafe`。
- 不要过度使用 `clone()`，除非需要所有权转移，否则使用借用而不是克隆。
- 避免过早的 `collect()`，保持迭代器的惰性直到实际需要集合。
- 避免不必要的分配 — 偏好借用和零拷贝操作。

## 代码风格和格式化

- 遵循 Rust 样式指南并使用 `rustfmt` 进行自动格式化。
- 尽可能保持行长度在 100 个字符以内。
- 使用 `///` 在项目前立即放置函数和结构体文档。
- 使用 `cargo clippy` 捕获常见错误并执行最佳实践。

## 错误处理

- 对可恢复错误使用 `Result<T, E>`，仅对不可恢复错误使用 `panic!`。
- 对于错误传播，偏好使用 `?` 操作符而不是 `unwrap()` 或 `expect()`。
- 使用 `thiserror` 创建自定义错误类型或实现 `std::error::Error`。
- 对可能存在或不存在的值使用 `Option<T>`。
- 提供有意义的错误消息和上下文。
- 错误类型应该是有意义且行为良好的（实现标准 trait）。
- 验证函数参数并为无效输入返回适当的错误。

## API 设计指导原则

### 通用 Trait 实现
在适当的地方积极实现通用 trait：
- `Copy`、`Clone`、`Eq`、`PartialEq`、`Ord`、`PartialOrd`、`Hash`、`Debug`、`Display`、`Default`
- 使用标准转换 trait：`From`、`AsRef`、`AsMut`
- 集合应该实现 `FromIterator` 和 `Extend`
- 注意：`Send` 和 `Sync` 在安全时由编译器自动实现；除非使用 `unsafe` 代码，否则避免手动实现

### 类型安全和可预测性
- 使用 newtype 提供静态区别
- 参数应该通过类型传达意义；偏好特定类型而不是通用的 `bool` 参数
- 为真正可选的值适当使用 `Option<T>`
- 具有明确接收者的函数应该是方法
- 只有智能指针应该实现 `Deref` 和 `DerefMut`

### 面向未来
- 使用密封 trait 防止下游实现
- 结构体应该有私有字段
- 函数应该验证其参数
- 所有公共类型必须实现 `Debug`

## 测试和文档

- 使用 `#[cfg(test)]` 模块和 `#[test]` 注解编写全面的单元测试。
- 在它们测试的代码旁边使用测试模块（`mod tests { ... }`）。
- 在 `tests/` 目录中使用描述性文件名编写集成测试。
- 为每个函数、结构体、枚举和复杂逻辑编写清晰简洁的注释。
- 确保函数具有描述性名称并包含全面的文档。
- 遵循 [API Guidelines](https://rust-lang.github.io/api-guidelines/) 使用 rustdoc（`///` 注释）记录所有公共 API。
- 使用 `#[doc(hidden)]` 从公共文档中隐藏实现细节。
- 记录错误条件、panic 场景和安全考虑。
- 示例应该使用 `?` 操作符，而不是 `unwrap()` 或已弃用的 `try!` 宏。

## 项目组织

- 在 `Cargo.toml` 中使用语义版本控制。
- 包含全面的元数据：`description`、`license`、`repository`、`keywords`、`categories`。
- 对可选功能使用特性标志。
- 使用 `mod.rs` 或命名文件将代码组织到模块中。
- 保持 `main.rs` 或 `lib.rs` 最小化 - 将逻辑移动到模块中。

## 质量检查清单

在发布或审查 Rust 代码之前，确保：

### 核心要求
- [ ] **命名**：遵循 RFC 430 命名约定
- [ ] **Trait**：在适当的地方实现 `Debug`、`Clone`、`PartialEq`
- [ ] **错误处理**：使用 `Result<T, E>` 并提供有意义的错误类型
- [ ] **文档**：所有公共项目都有带示例的 rustdoc 注释
- [ ] **测试**：包括边缘情况的全面测试覆盖

### 安全性和质量
- [ ] **安全性**：没有不必要的 `unsafe` 代码，适当的错误处理
- [ ] **性能**：高效使用迭代器，最小化分配
- [ ] **API 设计**：函数是可预测的、灵活的和类型安全的
- [ ] **面向未来**：结构体中的私有字段，适当的密封 trait
- [ ] **工具**：代码通过 `cargo fmt`、`cargo clippy` 和 `cargo test`