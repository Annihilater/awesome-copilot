---
description: '构建 TanStack Start 应用程序的指导原则'
applyTo: '**/*.ts, **/*.tsx, **/*.js, **/*.jsx, **/*.css, **/*.scss, **/*.json'
---

# TanStack Start 与 Shadcn/ui 开发指南

你是专门从事具有现代 React 模式的 TanStack Start 应用程序的专业 TypeScript 开发人员。

## 技术栈
- TypeScript（严格模式）
- TanStack Start（路由和 SSR）
- Shadcn/ui（UI 组件）
- Tailwind CSS（样式）
- Zod（验证）
- TanStack Query（客户端状态）

## 代码样式规则

- 绝不使用 `any` 类型 - 始终使用适当的 TypeScript 类型
- 优先使用函数组件而非类组件
- 始终使用 Zod schemas 验证外部数据
- 为所有路由包含错误和待处理边界
- 遵循无障碍最佳实践，使用 ARIA 属性

## 组件模式

使用具有适当 TypeScript 接口的函数组件：

```typescript
interface ButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export default function Button({ children, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button onClick={onClick} className={cn(buttonVariants({ variant }))}>
      {children}
    </button>
  );
}
```

## 数据获取

使用 Route Loaders 用于：
- 渲染所需的初始页面数据
- SSR 要求
- SEO 关键数据

使用 React Query 用于：
- 频繁更新的数据
- 可选/次要数据
- 具有乐观更新的客户端突变

```typescript
// Route Loader
export const Route = createFileRoute('/users')({
  loader: async () => {
    const users = await fetchUsers()
    return { users: userListSchema.parse(users) }
  },
  component: UserList,
})

// React Query
const { data: stats } = useQuery({
  queryKey: ['user-stats', userId],
  queryFn: () => fetchUserStats(userId),
  refetchInterval: 30000,
});
```

## Zod 验证

始终验证外部数据。在 `src/lib/schemas.ts` 中定义 schemas：

```typescript
export const userSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(100),
  email: z.string().email().optional(),
  role: z.enum(['admin', 'user']).default('user'),
})

export type User = z.infer<typeof userSchema>

// 安全解析
const result = userSchema.safeParse(data)
if (!result.success) {
  console.error('Validation failed:', result.error.format())
  return null
}
```

## 路由

在 `src/routes/` 中使用基于文件的路由构建路由。始终包含错误和待处理边界：

```typescript
export const Route = createFileRoute('/users/$id')({
  loader: async ({ params }) => {
    const user = await fetchUser(params.id);
    return { user: userSchema.parse(user) };
  },
  component: UserDetail,
  errorBoundary: ({ error }) => (
    <div className="text-red-600 p-4">Error: {error.message}</div>
  ),
  pendingBoundary: () => (
    <div className="flex items-center justify-center p-4">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
    </div>
  ),
});
```

## UI 组件

始终优先使用 Shadcn/ui 组件而非自定义组件：

```typescript
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

<Card>
  <CardHeader>
    <CardTitle>User Details</CardTitle>
  </CardHeader>
  <CardContent>
    <Button onClick={handleSave}>Save</Button>
  </CardContent>
</Card>
```

使用 Tailwind 进行响应式设计的样式：

```typescript
<div className="flex flex-col gap-4 p-6 md:flex-row md:gap-6">
  <Button className="w-full md:w-auto">Action</Button>
</div>
```

## 无障碍性

首先使用语义 HTML。只有在没有语义等价物存在时才添加 ARIA：

```typescript
// ✅ 好：具有最少 ARIA 的语义 HTML
<button onClick={toggleMenu}>
  <MenuIcon aria-hidden="true" />
  <span className="sr-only">Toggle Menu</span>
</button>

// ✅ 好：仅在需要时使用 ARIA（用于动态状态）
<button
  aria-expanded={isOpen}
  aria-controls="menu"
  onClick={toggleMenu}
>
  Menu
</button>

// ✅ 好：语义表单元素
<label htmlFor="email">Email Address</label>
<input id="email" type="email" />
{errors.email && (
  <p role="alert">{errors.email}</p>
)}
```

## 文件组织

```
src/
├── components/ui/    # Shadcn/ui 组件
├── lib/schemas.ts    # Zod schemas
├── routes/          # 基于文件的路由
└── routes/api/      # 服务器路由（.ts）
```

## 导入标准

对所有内部导入使用 `@/` 别名：

```typescript
// ✅ 好
import { Button } from '@/components/ui/button'
import { userSchema } from '@/lib/schemas'

// ❌ 坏
import { Button } from '../components/ui/button'
```

## 添加组件

需要时安装 Shadcn 组件：

```bash
npx shadcn@latest add button card input dialog
```

## 常见模式

- 始终使用 Zod 验证外部数据
- 对初始数据使用路由加载器，对更新使用 React Query
- 在所有路由上包含错误/待处理边界
- 优先使用 Shadcn 组件而非自定义 UI
- 一致使用 `@/` 导入
- 遵循无障碍最佳实践