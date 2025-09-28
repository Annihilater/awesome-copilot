---
mode: agent
description: "使用 Playwright MCP 探索网站以开展测试"
tools: ["changes", "codebase", "editFiles", "fetch", "findTestFiles", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "playwright"]
model: "Claude Sonnet 4"
---

# 网站测试探索

你的目标是探索目标网站并识别关键功能。

## 具体指令

1. 使用 Playwright MCP Server 访问提供的 URL。如果没有提供 URL，请先向用户索取。
2. 识别并交互 3-5 个核心功能或用户流程。
3. 记录用户交互、相关的 UI 元素（及其定位器）与预期结果。
4. 完成后关闭浏览器上下文。
5. 提供一份精简总结，概述探索发现。
6. 基于探索结果提出并生成测试用例。

