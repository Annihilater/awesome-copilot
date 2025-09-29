---
description: 'Next.js + Tailwind 开发标准和指令'
applyTo: '**/*.tsx, **/*.ts, **/*.jsx, **/*.js, **/*.css'
---

# Next.js + Tailwind 开发指令

使用 Tailwind CSS 样式和 TypeScript 构建高质量 Next.js 应用程序的指令。

## 项目上下文

- 最新版本的 Next.js（App Router）
- TypeScript 用于类型安全
- Tailwind CSS 用于样式设计

## 开发标准

### 架构
- App Router 与服务器和客户端组件
- 按功能/域分组路由
- 实现适当的错误边界
- 默认使用 React Server Components
- 在可能的情况下利用静态优化

### TypeScript
- 启用严格模式
- 清晰的类型定义
- 使用类型守卫进行适当的错误处理
- 使用 Zod 进行运行时类型验证

### 样式设计
- 使用一致色彩面板的 Tailwind CSS
- 响应式设计模式
- 深色模式支持
- 遵循容器查询最佳实践
- 维护语义化的 HTML 结构

### 状态管理
- 使用 React Server Components 管理服务器状态
- 使用 React hooks 管理客户端状态
- 适当的加载和错误状态
- 在适当的地方使用乐观更新

### 数据获取
- 在 Server Components 中直接进行数据库查询
- 使用 React Suspense 处理加载状态
- 适当的错误处理和重试逻辑
- 缓存失效策略

### 安全
- 输入验证和清理
- 适当的身份验证检查
- CSRF 保护
- 速率限制实现
- 安全的 API 路由处理

### 性能
- 使用 next/image 进行图像优化
- 使用 next/font 进行字体优化
- 路由预取
- 适当的代码分割
- 包体积优化

## 实现流程
1. 规划组件层次结构
2. 定义类型和接口
3. 实现服务器端逻辑
4. 构建客户端组件
5. 添加适当的错误处理
6. 实现响应式样式
7. 添加加载状态
8. 编写测试