---
description: 'C# 应用程序开发代码编写规则 by @jgkim999'
applyTo: '**/*.cs'
---

# C# 代码编写规则

## 命名约定 (Naming Conventions)

一致的命名约定是代码可读性的核心。建议遵循 Microsoft 的指导原则。

| 元素 | 命名约定 | 示例 |
|------|-----------|------|
| 接口 | 前缀 'I' + PascalCase | `IAsyncRepository`, `ILogger` |
| 公共 (public) 成员 | Pascal 大小写 (PascalCase) | `public int MaxCount;`, `public void GetData()` |
| 参数、局部变量 | 驼峰大小写 (camelCase) | `int userCount`, `string customerName` |
| 私有/内部字段 | 下划线(_) + 驼峰大小写 | `private string _connectionString;` |
| 常量 (const) | Pascal 大小写 (PascalCase) | `public const int DefaultTimeout = 5000;` |
| 泛型类型参数 | 前缀 'T' + 描述性名称 | `TKey`, `TValue`, `TResult` |
| 异步方法 | 'Async' 后缀 | `GetUserAsync`, `DownloadFileAsync` |

## 代码格式和可读性 (Formatting & Readability)

一致的格式使代码在视觉上更容易解析。

| 项目 | 规则 | 说明 |
|------|------|------|
| 缩进 | 使用 4 个空格 | 使用 4 个空格而不是制表符。cs 文件必须使用 4 个空格。 |
| 括号 | 始终使用大括号 {} | 即使控制语句（if、for、while 等）只有一行，也要始终使用大括号。 |
| 空行 | 逻辑分离 | 在方法定义、属性定义、逻辑分离的代码块之间添加空行。 |
| 语句编写 | 一行一个语句 | 一行只写一个语句。 |
| var 关键字 | 仅在类型明确时使用 | 只有在右侧可以明确推断变量类型时才使用 var。 |
| 命名空间 | 使用文件作用域命名空间 | 在 C# 10 及以上版本中，使用文件作用域命名空间来减少不必要的缩进。 |
| 注释 | 编写 XML 格式注释 | 对编写的 class 或函数始终编写 xml 格式的注释。 |

## 语言特性使用 (Language Features)

利用最新的 C# 特性使代码更简洁高效。

| 特性 | 说明 | 示例/参考 |
|------|------|------|
| 异步编程 | 对 I/O 绑定操作使用 async/await | `async Task<string> GetDataAsync()` |
| ConfigureAwait | 在库代码中减少上下文切换开销 | `await SomeMethodAsync().ConfigureAwait(false)` |
| LINQ | 集合数据查询和操作 | `users.Where(u => u.IsActive).ToList()` |
| 表达式主体成员 | 简洁地表达简单方法/属性 | `public string Name => _name;` |
| Nullable Reference Types | 在编译时防止 NullReferenceException | `#nullable enable` |
| using 声明 | 简洁处理 IDisposable 对象 | `using var stream = new FileStream(...);` |

## 性能和异常处理 (Performance & Exception Handling)

构建健壮快速应用程序的指导原则。

### 异常处理

只捕获可以处理的具体异常。应避免像 catch (Exception) 这样捕获一般异常。

不要使用异常进行程序流程控制。异常应该只用于意外的错误情况。

### 性能

当重复连接字符串时，使用 StringBuilder 而不是 + 运算符。

使用 Entity Framework Core 时，对只读查询使用 .AsNoTracking() 来提高性能。

避免不必要的对象分配，特别是在循环中要注意。

## 安全性 (Security)

编写安全代码的基本原则。

| 安全领域 | 规则 | 说明 |
|------|------|------|
| 输入验证 | 验证所有外部数据 | 不要信任来自外部（用户、API 等）的所有数据，始终进行有效性验证。 |
| 防止 SQL 注入 | 使用参数化查询 | 始终使用参数化查询或像 Entity Framework 这样的 ORM 来防止 SQL 注入攻击。 |
| 保护敏感数据 | 使用配置管理工具 | 密码、连接字符串、API 密钥等不要硬编码在源代码中，使用 Secret Manager、Azure Key Vault 等。 |

这些规则应该集成到项目的 .editorconfig 文件和团队的代码审查流程中，以持续维护高质量的代码。