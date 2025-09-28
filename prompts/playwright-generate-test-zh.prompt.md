---
mode: agent
description: "根据场景使用 Playwright MCP 生成测试"
tools: ["changes", "codebase", "editFiles", "fetch", "findTestFiles", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "playwright"]
model: "Claude Sonnet 4"
---

# 使用 Playwright MCP 生成测试

你的目标是在完成所有预定步骤后，根据给定场景生成 Playwright 测试。

## 具体指令

- 用户会提供一个场景，你需要据此生成 Playwright 测试；若用户未提供场景，请先进行询问。
- **不要**在未完成所有规定步骤之前，过早生成测试代码，或仅根据场景直接输出代码。
- **必须**借助 Playwright MCP 提供的工具按步骤逐一执行。
- 只有在所有步骤完成后，才根据消息历史输出使用 `@playwright/test` 的 Playwright TypeScript 测试。
- 将生成的测试文件保存到 `tests` 目录。
- 执行该测试文件，并迭代修正直至测试通过。

