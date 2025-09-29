---
description: 'Angular 专用编码标准和最佳实践'
applyTo: '**/*.ts, **/*.html, **/*.scss, **/*.css'
---

# Angular 开发指南

适用于使用 TypeScript 生成高质量 Angular 应用程序的指南，使用 Angular Signals 进行状态管理，遵循 https://angular.dev 中概述的 Angular 最佳实践。

## 项目上下文
- 最新版本的 Angular（默认使用独立组件）
- TypeScript 用于类型安全
- Angular CLI 用于项目设置和脚手架
- 遵循 Angular 风格指南（https://angular.dev/style-guide）
- 使用 Angular Material 或其他现代 UI 库以实现一致的样式（如果指定）

## 开发标准

### 架构
- 除非明确需要模块，否则使用独立组件
- 按功能模块或领域组织代码以实现可扩展性
- 为功能模块实现懒加载以优化性能
- 有效使用 Angular 的内置依赖注入系统
- 使用明确的关注点分离来构建组件（智能组件 vs 展示组件）

### TypeScript
- 在 `tsconfig.json` 中启用严格模式以确保类型安全
- 为组件、服务和模型定义清晰的接口和类型
- 使用类型守卫和联合类型进行强健的类型检查
- 使用 RxJS 操作符（例如 `catchError`）实现适当的错误处理
- 为响应式表单使用类型化表单（例如 `FormGroup`、`FormControl`）

### 组件设计
- 遵循 Angular 组件生命周期钩子的最佳实践
- 当使用 Angular >= 19 时，使用 `input()`、`output()`、`viewChild()`、`viewChildren()`、`contentChild()` 和 `viewChildren()` 函数而不是装饰器；否则使用装饰器
- 利用 Angular 的变更检测策略（默认策略或 `OnPush` 用于性能优化）
- 保持模板简洁，将逻辑放在组件类或服务中
- 使用 Angular 指令和管道实现可重用功能

### 样式
- 使用 Angular 的组件级 CSS 封装（默认：ViewEncapsulation.Emulated）
- 优先使用 SCSS 进行样式设计，实现一致的主题
- 使用 CSS Grid、Flexbox 或 Angular CDK Layout 工具实现响应式设计
- 如果使用 Angular Material，遵循其主题指南
- 使用 ARIA 属性和语义 HTML 维护可访问性（a11y）

### 状态管理
- 使用 Angular Signals 在组件和服务中进行响应式状态管理
- 利用 `signal()`、`computed()` 和 `effect()` 进行响应式状态更新
- 对可变状态使用可写信号，对派生状态使用计算信号
- 使用信号处理加载和错误状态，并提供适当的 UI 反馈
- 在将信号与 RxJS 结合使用时，使用 Angular 的 `AsyncPipe` 处理模板中的 observables

### 数据获取
- 使用 Angular 的 `HttpClient` 进行 API 调用并使用适当的类型
- 实现 RxJS 操作符进行数据转换和错误处理
- 在独立组件中使用 Angular 的 `inject()` 函数进行依赖注入
- 实现缓存策略（例如，为 observables 使用 `shareReplay`）
- 将 API 响应数据存储在信号中以进行响应式更新
- 使用全局拦截器处理 API 错误以实现一致的错误处理

### 安全性
- 使用 Angular 的内置清理功能清理用户输入
- 实现路由守卫进行身份验证和授权
- 使用 Angular 的 `HttpInterceptor` 进行 CSRF 保护和 API 身份验证头
- 使用 Angular 的响应式表单和自定义验证器验证表单输入
- 遵循 Angular 的安全最佳实践（例如，避免直接 DOM 操作）

### 性能
- 使用 `ng build --prod` 启用生产构建以进行优化
- 为路由使用懒加载以减少初始包大小
- 使用 `OnPush` 策略和信号优化变更检测以实现细粒度响应性
- 在 `ngFor` 循环中使用 trackBy 以提高渲染性能
- 使用 Angular Universal 实现服务器端渲染（SSR）或静态站点生成（SSG）（如果指定）

### 测试
- 使用 Jasmine 和 Karma 为组件、服务和管道编写单元测试
- 使用 Angular 的 `TestBed` 进行组件测试，并使用模拟依赖项
- 使用 Angular 的测试工具测试基于信号的状态更新
- 使用 Cypress 或 Playwright 编写端到端测试（如果指定）
- 使用 `HttpClientTestingModule` 模拟 HTTP 请求
- 确保关键功能的高测试覆盖率

## 实施流程
1. 规划项目结构和功能模块
2. 定义 TypeScript 接口和模型
3. 使用 Angular CLI 构建组件、服务和管道
4. 使用基于信号的状态实现数据服务和 API 集成
5. 构建具有清晰输入和输出的可重用组件
6. 添加响应式表单和验证
7. 使用 SCSS 和响应式设计应用样式
8. 实现懒加载路由和守卫
9. 使用信号添加错误处理和加载状态
10. 编写单元测试和端到端测试
11. 优化性能和包大小

## 附加指南
- 遵循 Angular 的命名约定（例如，`feature.component.ts`、`feature.service.ts`）
- 使用 Angular CLI 命令生成样板代码
- 使用清晰的 JSDoc 注释记录组件和服务
- 在适用的情况下确保可访问性合规性（WCAG 2.1）
- 使用 Angular 的内置 i18n 进行国际化（如果指定）
- 通过创建可重用的工具和共享模块保持代码 DRY
- 一致地使用信号进行状态管理以确保响应式更新
