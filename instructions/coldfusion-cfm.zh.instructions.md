---
description: 'ColdFusion CFM 文件和应用程序模式'
applyTo: "**/*.cfm"
---

# ColdFusion 编码标准

- 尽可能使用 CFScript 以获得更简洁的语法。
- 避免使用已弃用的标签和函数。
- 遵循变量和组件的一致命名约定。
- 使用 `cfqueryparam` 防止 SQL 注入。
- 在 <cfoutput> 块内使用 ## 转义 CSS 哈希符号
- 在 <cfoutput> 块内使用 HTMX 时，通过使用双哈希符号 (##) 转义哈希符号 (#) 以防止意外的变量插值。
- 如果你在 HTMX 目标文件中，请确保第一行是：<cfsetting showDebugOutput = "false">

# 其他最佳实践

- 使用 `Application.cfc` 进行应用程序设置和请求处理。
- 将代码组织成可重用的 CFC（组件）以便于维护。
- 验证和清理所有用户输入。
- 使用 `cftry`/`cfcatch` 进行错误处理和日志记录。
- 避免在源文件中硬编码凭据或敏感数据。
- 使用一致的缩进（按照全局标准，使用 2 个空格）。
- 为复杂逻辑添加注释，并为函数编写用途和参数的文档。
- 优先使用 `cfinclude` 引入共享模板，但避免循环引用。

- 尽可能使用三元运算符
- 确保一致的制表符对齐。