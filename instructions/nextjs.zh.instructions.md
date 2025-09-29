---
applyTo: '**'
---

# Next.js 最佳实践指南 (2025)

_最后更新：2025 年 7 月_

本文档总结了构建、组织和维护 Next.js 应用程序的最新权威最佳实践。旨在供 LLM 和开发者使用，以确保代码质量、可维护性和可扩展性。

---

## 1. 项目结构和组织

- **使用 `app/` 目录**（App Router）处理所有新项目。优先选择它而不是旧版的 `pages/` 目录。
- **顶级文件夹：**
  - `app/` — 路由、布局、页面和路由处理器
  - `public/` — 静态资源（图像、字体等）
  - `lib/` — 共享工具、API 客户端和逻辑
  - `components/` — 可重用的 UI 组件
  - `contexts/` — React 上下文提供者
  - `styles/` — 全局和模块化样式表
  - `hooks/` — 自定义 React hooks
  - `types/` — TypeScript 类型定义
- **就近原则：** 将文件（组件、样式、测试）放在使用它们的地方附近，但避免过深的嵌套结构。
- **路由组：** 使用括号（例如 `(admin)`）来分组路由而不影响 URL 路径。
- **私有文件夹：** 使用 `_` 前缀（例如 `_internal`）来退出路由并标识实现细节。

- **功能文件夹：** 对于大型应用，按功能分组（例如 `app/dashboard/`、`app/auth/`）。
- **使用 `src/`**（可选）：将所有源代码放在 `src/` 中以与配置文件分离。

## 2.1. 服务器和客户端组件集成（App Router）

**永远不要在服务器组件内使用带有 `{ ssr: false }` 的 `next/dynamic`。** 这不受支持并会导致构建/运行时错误。

**正确方法：**
- 如果您需要在服务器组件内使用客户端组件（例如，使用 hooks、浏览器 API 或仅客户端库的组件），您必须：
  1. 将所有仅客户端逻辑/UI 移动到专用的客户端组件中（在顶部使用 `'use client'`）。
  2. 在服务器组件中直接导入并使用该客户端组件（无需 `next/dynamic`）。
  3. 如果您需要组合多个仅客户端元素（例如，带有配置文件下拉菜单的导航栏），创建一个包含所有这些元素的单个客户端组件。

**示例：**

```tsx
// 服务器组件
import DashboardNavbar from '@/components/DashboardNavbar';

export default async function DashboardPage() {
  // ...服务器逻辑...
  return (
    <>
      <DashboardNavbar /> {/* 这是一个客户端组件 */}
      {/* ...页面的其余服务器渲染部分... */}
    </>
  );
}
```

**原因：**
- 服务器组件不能使用仅客户端功能或禁用 SSR 的动态导入。
- 客户端组件可以在服务器组件内渲染，但反之则不行。

**总结：**
始终将仅客户端 UI 移动到客户端组件中，并在您的服务器组件中直接导入它。永远不要在服务器组件中使用带有 `{ ssr: false }` 的 `next/dynamic`。

---

## 2. 组件最佳实践

- **组件类型：**
  - **服务器组件**（默认）：用于数据获取、重逻辑和非交互式 UI。
  - **客户端组件：** 在顶部添加 `'use client'`。用于交互性、状态或浏览器 API。
- **何时创建组件：**
  - 如果 UI 模式被重复使用一次以上。
  - 如果页面的某个部分复杂或自包含。
  - 如果它提高了可读性或可测试性。
- **命名约定：**
  - 对组件文件和导出使用 `PascalCase`（例如 `UserCard.tsx`）。
  - 对 hooks 使用 `camelCase`（例如 `useUser.ts`）。
  - 对静态资源使用 `snake_case` 或 `kebab-case`（例如 `logo_dark.svg`）。
  - 将上下文提供者命名为 `XyzProvider`（例如 `ThemeProvider`）。
- **文件命名：**
  - 使组件名与文件名匹配。
  - 对于单导出文件，默认导出组件。
  - 对于多个相关组件，使用 `index.ts` 桶文件。
- **组件位置：**
  - 将共享组件放在 `components/` 中。
  - 将路由特定组件放在相关路由文件夹内。
- **Props：**
  - 为 props 使用 TypeScript 接口。
  - 偏好显式 prop 类型和默认值。
- **测试：**
  - 与组件放在一起测试（例如 `UserCard.test.tsx`）。

## 3. 命名约定（通用）

- **文件夹：** `kebab-case`（例如 `user-profile/`）
- **文件：** 组件用 `PascalCase`，工具/hooks 用 `camelCase`，静态资源用 `kebab-case`
- **变量/函数：** `camelCase`
- **类型/接口：** `PascalCase`
- **常量：** `UPPER_SNAKE_CASE`

## 4. API 路由（路由处理器）

- **优先选择 API 路由而非 Edge 函数**，除非您需要超低延迟或地理分布。
- **位置：** 将 API 路由放在 `app/api/` 中（例如 `app/api/users/route.ts`）。
- **HTTP 方法：** 导出以 HTTP 动词命名的异步函数（`GET`、`POST` 等）。
- **请求/响应：** 使用 Web `Request` 和 `Response` API。使用 `NextRequest`/`NextResponse` 获得高级功能。
- **动态段：** 对动态 API 路由使用 `[param]`（例如 `app/api/users/[id]/route.ts`）。
- **验证：** 始终验证和清理输入。使用 `zod` 或 `yup` 等库。
- **错误处理：** 返回适当的 HTTP 状态码和错误消息。
- **身份验证：** 使用中间件或服务器端会话检查保护敏感路由。

## 5. 通用最佳实践

- **TypeScript：** 对所有代码使用 TypeScript。在 `tsconfig.json` 中启用 `strict` 模式。
- **ESLint 和 Prettier：** 强制执行代码风格和代码检查。使用官方 Next.js ESLint 配置。
- **环境变量：** 将机密存储在 `.env.local` 中。永远不要将机密提交到版本控制。
- **测试：** 使用 Jest、React Testing Library 或 Playwright。为所有关键逻辑和组件编写测试。
- **可访问性：** 使用语义 HTML 和 ARIA 属性。使用屏幕阅读器测试。
- **性能：**
  - 使用内置的图像和字体优化。
  - 对异步数据使用 Suspense 和加载状态。
  - 避免大型客户端包；将大部分逻辑保留在服务器组件中。
- **安全性：**
  - 清理所有用户输入。
  - 在生产中使用 HTTPS。
  - 设置安全的 HTTP 头。
- **文档：**
  - 编写清晰的 README 和代码注释。
  - 记录公共 API 和组件。

# 避免不必要的示例文件

不要在主代码库中创建示例/演示文件（如 ModalExample.tsx），除非用户特别请求实时示例、Storybook 故事或显式文档组件。默认情况下保持仓库干净且专注于生产。

# 始终使用最新的文档和指南
- 对于每个 Next.js 相关请求，首先搜索最新的 Next.js 文档、指南和示例。
- 如果可用，使用以下工具获取和搜索文档：
  - `resolve_library_id` 来解析文档中的包/库名称。
  - `get_library_docs` 获取最新文档。