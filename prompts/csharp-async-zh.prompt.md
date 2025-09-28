---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "获取 C# 异步编程的最佳实践"
---

# C# 异步编程最佳实践

你的目标是帮助我遵循 C# 异步编程的最佳实践。

## 命名约定

- 对所有异步方法使用“Async”后缀
- 在适用时，将方法名与其同步对应项匹配（例如，`GetData()` 对应 `GetDataAsync()`）

## 返回类型

- 当方法返回值时，返回 `Task<T>`
- 当方法不返回值时，返回 `Task`
- 在高性能场景中考虑使用 `ValueTask<T>` 以减少分配
- 避免为异步方法返回 `void`，事件处理程序除外

## 异常处理

- 在 await 表达式周围使用 try/catch 块
- 避免在异步方法中吞噬异常
- 在适当时使用 `ConfigureAwait(false)` 以防止库代码中出现死锁
- 使用 `Task.FromException()` 传播异常，而不是在返回 Task 的异步方法中抛出异常

## 性能

- 使用 `Task.WhenAll()` 并行执行多个任务
- 使用 `Task.WhenAny()` 实现超时或获取第一个完成的任务
- 在仅传递任务结果时，避免不必要的 async/await
- 为长时间运行的操作考虑使用取消令牌

## 常见陷阱

- 切勿在异步代码中使用 `.Wait()`、`.Result` 或 `.GetAwaiter().GetResult()`
- 避免混合使用阻塞和异步代码
- 不要创建 async void 方法（事件处理程序除外）
- 始终等待返回 Task 的方法

## 实现模式

- 为长时间运行的操作实现异步命令模式
- 使用异步流 (IAsyncEnumerable<T>) 异步处理序列
- 为公共 API 考虑基于任务的异步模式 (TAP)

在审查我的 C# 代码时，请识别这些问题并提出遵循这些最佳实践的改进建议。
