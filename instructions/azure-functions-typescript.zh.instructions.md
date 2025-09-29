---
description: 'Azure Functions 的 TypeScript 模式'
applyTo: '**/*.ts, **/*.js, **/*.json'
---

## 代码生成指导原则
- 为 Node.js 生成现代 TypeScript 代码
- 对异步代码使用 `async/await`
- 尽可能使用 Node.js v20 内置模块，而不是外部包
- 始终使用 Node.js 异步函数，如使用 `node:fs/promises` 而不是 `fs`，以避免阻塞事件循环
- 在向项目添加任何额外依赖项之前请先询问
- API 是使用 Azure Functions 和 `@azure/functions@4` 包构建的
- 每个端点都应该有自己的函数文件，并使用以下命名约定：`src/functions/<resource-name>-<http-verb>.ts`
- 在对 API 进行更改时，请确保相应地更新 OpenAPI schema（如果存在）和 `README.md` 文件