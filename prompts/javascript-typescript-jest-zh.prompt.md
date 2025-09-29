---
description: "使用 Jest 编写 JavaScript/TypeScript 测试的最佳实践，包括模拟策略、测试结构和常见模式。"
mode: "agent"
---

### 测试结构

- 测试文件以 `.test.ts` 或 `.test.js` 为后缀命名
- 将测试文件放在其测试的代码旁边或专用的 `__tests__` 目录中
- 使用描述性的测试名称来解释预期的行为
- 使用嵌套的 describe 块来组织相关的测试
- 遵循模式：`describe('组件/函数/类', () => { it('应该做某事', () => {}) })`

### 有效的模拟

- 模拟外部依赖项（API、数据库等）以隔离您的测试
- 对模块级模拟使用 `jest.mock()`
- 对特定函数模拟使用 `jest.spyOn()`
- 使用 `mockImplementation()` 或 `mockReturnValue()` 定义模拟行为
- 在 `afterEach` 中使用 `jest.resetAllMocks()` 在测试之间重置模拟

### 测试异步代码

- 始终返回 promise 或在测试中使用 async/await 语法
- 对 promise 使用 `resolves`/`rejects` 匹配器
- 使用 `jest.setTimeout()` 为慢速测试设置适当的超时

### 快照测试

- 对不经常更改的 UI 组件或复杂对象使用快照测试
- 保持快照小而集中
- 在提交之前仔细审查快照更改

### 测试 React 组件

- 使用 React Testing Library 而不是 Enzyme 来测试组件
- 测试用户行为和组件可访问性
- 按可访问性角色、标签或文本内容查询元素
- 使用 `userEvent` 而不是 `fireEvent` 以获得更真实的用户交互

## 常见的 Jest 匹配器

- 基本：`expect(value).toBe(expected)`、`expect(value).toEqual(expected)`
- 真值：`expect(value).toBeTruthy()`、`expect(value).toBeFalsy()`
- 数字：`expect(value).toBeGreaterThan(3)`、`expect(value).toBeLessThanOrEqual(3)`
- 字符串：`expect(value).toMatch(/pattern/)`、`expect(value).toContain('substring')`
- 数组：`expect(array).toContain(item)`、`expect(array).toHaveLength(3)`
- 对象：`expect(object).toHaveProperty('key', value)`
- 异常：`expect(fn).toThrow()`、`expect(fn).toThrow(Error)`
- 模拟函数：`expect(mockFn).toHaveBeenCalled()`、`expect(mockFn).toHaveBeenCalledWith(arg1, arg2)`

```

```
