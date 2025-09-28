---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "findTestFiles", "search", "writeTest"]
description: "为 Next.js + next-intl 应用添加新语言。"
---

本指南用于在使用 next-intl 的 Next.js 项目中添加新语言。

- 项目通过 next-intl 实现国际化。
- 所有翻译位于 `./messages` 目录。
- UI 语言切换组件是 `src/components/language-toggle.tsx`。
- 路由和中间件配置位于：
  - `src/i18n/routing.ts`
  - `src/middleware.ts`

添加新语言时：

- 将 `en.json` 中的所有内容翻译成新语言，确保 JSON 项全部完成翻译。
- 在 `routing.ts` 与 `middleware.ts` 中加入对应的路径配置。
- 在 `language-toggle.tsx` 中新增该语言选项。

