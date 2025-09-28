---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "创建带有正确 OpenAPI 文档的 ASP.NET Minimal API 端点"
---

# 带有 OpenAPI 的 ASP.NET Minimal API

您的目标是帮助我创建结构良好的 ASP.NET Minimal API 端点，并提供正确的类型和全面的 OpenAPI/Swagger 文档。

## API 组织

- 使用 `MapGroup()` 扩展对相关端点进行分组
- 对横切关注点使用端点过滤器
- 使用单独的端点类构建更大的 API
- 考虑对复杂的 API 使用基于功能的文件夹结构

## 请求和响应类型

- 定义显式的请求和响应 DTO/模型
- 创建具有正确验证属性的清晰模型类
- 对不可变的请求/响应对象使用记录类型
- 使用与 API 设计标准一致的有意义的属性名称
- 应用 `[Required]` 和其他验证属性来强制执行约束
- 使用 ProblemDetailsService 和 StatusCodePages 获取标准错误响应

## 类型处理

- 使用具有显式类型绑定的强类型路由参数
- 使用 `Results<T1, T2>` 表示多种响应类型
- 返回 `TypedResults` 而不是 `Results` 以获得强类型响应
- 利用 C# 10+ 的功能，如可空注释和仅 init 属性

## OpenAPI 文档

- 使用 .NET 9 中添加的内置 OpenAPI 文档支持
- 定义操作摘要和描述
- 使用 `WithName` 扩展方法添加 operationId
- 使用 `[Description()]` 为属性和参数添加描述
- 为请求和响应设置正确的内容类型
- 使用文档转换器添加服务器、标签和安全方案等元素
- 使用模式转换器将自定义应用于 OpenAPI 模式
