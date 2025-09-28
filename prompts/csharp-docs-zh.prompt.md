---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "确保 C# 类型使用 XML 注释进行文档记录，并遵循文档记录的最佳实践。"
---

# C# 文档最佳实践

- 公共成员应使用 XML 注释进行文档记录。
- 也鼓励记录内部成员，特别是如果它们很复杂或不言自明。
- 使用 `<summary>` 作为方法描述。这应该是对方法功能的简要概述。
- 使用 `<param>` 作为方法参数。
- 使用 `<paramref>` 在文档中引用参数。
- 使用 `<returns>` 作为方法返回值。
- 使用 `<remarks>` 提供附加信息，可以包括实现细节、使用说明或任何其他相关上下文。
- 使用 `<example>` 提供有关如何使用成员的用法示例。
- 使用 `<exception>` 记录方法抛出的异常。
- 使用 `<see langword>` 表示特定于语言的关键字，如 `null`、`true`、`false`、`int`、`bool` 等。
- 使用 `<see cref>` 在行内（句子中）引用其他类型或成员。
- 使用 `<seealso>` 在联机文档的“另请参阅”部分中独立（不在句子中）引用其他类型或成员。
- 使用 `<inheritdoc/>` 从基类或接口继承文档。
  - 除非有重大的行为更改，在这种情况下，您应该记录差异。
- 使用 `<typeparam>` 表示泛型类型或方法中的类型参数。
- 使用 `<typeparamref>` 在文档中引用类型参数。
- 使用 `<c>` 表示行内代码片段。
- 使用 `<code>` 表示代码块。`<code>` 标签应放在 `<example>` 标签内。使用 `language` 属性添加代码示例的语言，例如 `<code language="csharp">`。
