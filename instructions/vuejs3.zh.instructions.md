---
description: 'Vue.js 3 开发标准和最佳实践，包含 Composition API 和 TypeScript'
applyTo: '**/*.vue, **/*.ts, **/*.js, **/*.scss'
---

# Vue.js 3 开发指导原则

构建高质量 Vue.js 3 应用程序的指导原则，使用 Composition API、TypeScript 和现代最佳实践。

## 项目背景
- Vue 3.x 以 Composition API 为默认
- TypeScript 用于类型安全
- 单文件组件（`.vue`）使用 `<script setup>` 语法
- 现代构建工具（推荐 Vite）
- Pinia 用于应用状态管理
- 官方 Vue 风格指南和最佳实践

## 开发标准

### 架构
- 偏好 Composition API（`setup` 函数和组合式函数）而非 Options API
- 按功能或领域组织组件和组合式函数以实现可扩展性
- 分离专注于 UI 的组件（展示型）和专注于逻辑的组件（容器型）
- 将可重用逻辑提取到 `composables/` 目录中的组合式函数
- 按领域构建 store 模块（Pinia），明确定义 actions、state 和 getters

### TypeScript 集成
- 在 `tsconfig.json` 中启用 `strict` 模式以获得最大类型安全性
- 使用 `defineComponent` 或 `<script setup lang="ts">` 配合 `defineProps` 和 `defineEmits`
- 利用 `PropType<T>` 处理类型化的 props 和默认值
- 为复杂的 prop 和状态形状使用接口或类型别名
- 为事件处理器、refs 和 `useRoute`/`useRouter` 钩子定义类型
- 在适用的地方实现通用组件和组合式函数

### 组件设计
- 遵循组件的单一职责原则
- 组件名使用 PascalCase，文件名使用 kebab-case
- 保持组件小巧并专注于一个关注点
- 使用 `<script setup>` 语法以获得简洁性和性能
- 使用 TypeScript 验证 props；仅在必要时使用运行时检查
- 偏好插槽和作用域插槽以实现灵活的组合

### 状态管理
- 使用 Pinia 管理全局状态：用 `defineStore` 定义 store
- 对于简单的本地状态，在 `setup` 内使用 `ref` 和 `reactive`
- 使用 `computed` 处理派生状态
- 对复杂结构保持状态规范化
- 在 Pinia store 中使用 actions 处理异步逻辑
- 利用 store 插件进行持久化或调试

### Composition API 模式
- 为共享逻辑创建可重用的组合式函数，例如 `useFetch`、`useAuth`
- 使用 `watch` 和 `watchEffect` 时采用精确的依赖列表
- 在 `onUnmounted` 或 `watch` 清理回调中清理副作用
- 谨慎使用 `provide`/`inject` 进行深度依赖注入
- 使用 `useAsyncData` 或第三方数据工具（Vue Query）

### 样式
- 使用 `<style scoped>` 实现组件级样式或 CSS Modules
- 考虑使用实用优先框架（Tailwind CSS）进行快速样式设计
- 遵循 BEM 或函数式 CSS 约定进行类命名
- 利用 CSS 自定义属性进行主题设计和设计令牌
- 使用 CSS Grid 和 Flexbox 实现移动优先的响应式设计
- 确保样式具有可访问性（对比度、焦点状态）

### 性能优化
- 使用动态导入和 `defineAsyncComponent` 延迟加载组件
- 使用 `<Suspense>` 处理异步组件加载回退
- 对静态或不经常变化的元素应用 `v-once` 和 `v-memo`
- 使用 Vue DevTools 性能选项卡进行分析
- 避免不必要的监听器；尽可能偏好 `computed`
- 摇树优化未使用的代码并利用 Vite 的优化功能

### 数据获取
- 使用组合式函数如 `useFetch`（Nuxt）或 Vue Query 等库
- 明确处理加载、错误和成功状态
- 在组件卸载或参数更改时取消过时的请求
- 实现乐观更新，失败时回滚
- 缓存响应并使用后台重新验证

### 错误处理
- 使用全局错误处理器（`app.config.errorHandler`）处理未捕获的错误
- 在 `try/catch` 中包装有风险的逻辑；提供用户友好的消息
- 在组件中使用 `errorCaptured` 钩子建立本地边界
- 优雅地显示回退 UI 或错误警报
- 将错误记录到外部服务（Sentry、LogRocket）

### 表单和验证
- 使用 VeeValidate 或 @vueuse/form 等库进行声明式验证
- 使用受控的 `v-model` 绑定构建表单
- 在失焦或输入时进行验证，使用防抖以提高性能
- 在组合式函数中处理文件上传和复杂的多步骤表单
- 确保可访问的标签、错误声明和焦点管理

### 路由
- 使用 Vue Router 4 配合 `createRouter` 和 `createWebHistory`
- 实现嵌套路由和路由级代码分割
- 使用导航守卫（`beforeEnter`、`beforeEach`）保护路由
- 在 `setup` 中使用 `useRoute` 和 `useRouter` 进行程序化导航
- 正确管理查询参数和动态段
- 通过路由元字段实现面包屑数据

### 测试
- 使用 Vue Test Utils 和 Jest 编写单元测试
- 专注于行为而非实现细节
- 使用 `mount` 和 `shallowMount` 进行组件隔离
- 根据需要模拟全局插件（router、Pinia）
- 使用 Cypress 或 Playwright 添加端到端测试
- 使用 axe-core 集成测试可访问性

### 安全性
- 避免使用 `v-html`；严格清理任何 HTML 输入
- 使用 CSP 头来缓解 XSS 和注入攻击
- 在模板和指令中验证和转义数据
- 对所有 API 请求使用 HTTPS
- 将敏感令牌存储在仅限 HTTP 的 cookie 中，而不是 `localStorage`

### 可访问性
- 使用语义 HTML 元素和 ARIA 属性
- 为模态框和动态内容管理焦点
- 为交互式组件提供键盘导航
- 为图像和图标添加有意义的 `alt` 文本
- 确保颜色对比度符合 WCAG AA 标准

## 实施流程
1. 规划组件和组合式函数架构
2. 初始化 Vite 项目，配备 Vue 3 和 TypeScript
3. 定义 Pinia store 和组合式函数
4. 创建核心 UI 组件和布局
5. 集成路由和导航
6. 实现数据获取和状态逻辑
7. 构建带验证和错误状态的表单
8. 添加全局错误处理和回退 UI
9. 添加单元测试和端到端测试
10. 优化性能和包大小
11. 确保可访问性合规
12. 记录组件、组合式函数和 store

## 其他指导原则
- 遵循 Vue 官方风格指南（vuejs.org/style-guide）
- 使用 ESLint（配合 `plugin:vue/vue3-recommended`）和 Prettier 保持代码一致性
- 编写有意义的提交消息并维护干净的 git 历史
- 保持依赖项最新并审计漏洞
- 使用 JSDoc/TSDoc 记录复杂逻辑
- 使用 Vue DevTools 进行调试和分析

## 常见模式
- 无渲染组件和作用域插槽以实现灵活的 UI
- 使用 provide/inject 的复合组件
- 针对横切关注点的自定义指令
- 用于模态框和覆盖层的 Teleport
- 全局工具的插件系统（i18n、分析）
- 用于参数化逻辑的组合式函数工厂