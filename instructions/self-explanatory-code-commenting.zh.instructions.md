---
description: 'GitHub Copilot 编写注释以实现自解释代码并减少注释的指导原则。示例使用 JavaScript，但应适用于任何支持注释的语言。'
applyTo: '**'
---

# 自解释代码注释指导

## 核心原则
**编写能够自我说明的代码。只在必要时添加注释来解释为什么（WHY），而不是做什么（WHAT）。**
大多数时候我们不需要注释。

## 注释指导原则

### ❌ 避免这些注释类型

**显而易见的注释**
```javascript
// 不好：说明显而易见的事情
let counter = 0;  // 将计数器初始化为零
counter++;  // 计数器增加一
```

**冗余注释**
```javascript
// 不好：注释重复了代码
function getUserName() {
    return user.name;  // 返回用户的名字
}
```

**过时的注释**
```javascript
// 不好：注释与代码不匹配
// 按5%税率计算税费
const tax = price * 0.08;  // 实际上是8%
```

### ✅ 编写这些注释类型

**复杂业务逻辑**
```javascript
// 好的：解释为什么使用这种特定计算
// 应用累进税率：10万以下10%，超过部分20%
const tax = calculateProgressiveTax(income, [0.10, 0.20], [10000]);
```

**非显而易见的算法**
```javascript
// 好的：解释算法选择
// 使用Floyd-Warshall算法计算所有点对的最短路径
// 因为我们需要所有节点之间的距离
for (let k = 0; k < vertices; k++) {
    for (let i = 0; i < vertices; i++) {
        for (let j = 0; j < vertices; j++) {
            // ... 实现
        }
    }
}
```

**正则表达式模式**
```javascript
// 好的：解释正则表达式匹配什么
// 匹配邮箱格式：用户名@域名.扩展名
const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
```

**API 限制或陷阱**
```javascript
// 好的：解释外部约束
// GitHub API 速率限制：认证用户每小时5000次请求
await rateLimiter.wait();
const response = await fetch(githubApiUrl);
```

## 决策框架

在编写注释之前，问问自己：
1. **代码是否自解释？** → 不需要注释
2. **更好的变量/函数名能否消除注释需要？** → 重构而不是注释
3. **这是否解释了为什么（WHY），而不是做什么（WHAT）？** → 好注释
4. **这是否会帮助未来的维护者？** → 好注释

## 注释的特殊情况

### 公共 API
```javascript
/**
 * 使用标准公式计算复利。
 *
 * @param {number} principal - 初始投资金额
 * @param {number} rate - 年利率（小数形式，如5%写成0.05）
 * @param {number} time - 时间期限（年）
 * @param {number} compoundFrequency - 每年复利次数（默认：1）
 * @returns {number} 复利后的最终金额
 */
function calculateCompoundInterest(principal, rate, time, compoundFrequency = 1) {
    // ... 实现
}
```

### 配置和常量
```javascript
// 好的：解释来源或原因
const MAX_RETRIES = 3;  // 基于网络可靠性研究
const API_TIMEOUT = 5000;  // AWS Lambda超时为15秒，留有缓冲
```

### 注解
```javascript
// TODO: 在安全审查后替换为适当的用户身份验证
// FIXME: 生产环境内存泄漏 - 调查连接池问题
// HACK: 库v2.1.0错误的临时解决方案 - 升级后删除
// NOTE: 此实现假设所有计算都使用UTC时区
// WARNING: 此函数修改原始数组而不是创建副本
// PERF: 如果在热路径中频繁调用，考虑缓存此结果
// SECURITY: 在查询中使用前验证输入以防止SQL注入
// BUG: 数组为空时的边缘情况失败 - 需要调查
// REFACTOR: 将此逻辑提取到单独的工具函数中以便重用
// DEPRECATED: 使用newApiFunction()替代 - 这将在v3.0中删除
```

## 要避免的反模式

### 死代码注释
```javascript
// 不好：不要注释掉代码
// const oldFunction = () => { ... };
const newFunction = () => { ... };
```

### 变更日志注释
```javascript
// 不好：不要在注释中维护历史记录
// 2023-01-15由John修改
// 2023-02-03修复Sarah报告的错误
function processData() {
    // ... 实现
}
```

### 分隔符注释
```javascript
// 不好：不要使用装饰性注释
//=====================================
// 工具函数
//=====================================
```

## 质量检查清单

提交前，确保您的注释：
- [ ] 解释为什么（WHY），而不是做什么（WHAT）
- [ ] 语法正确且清晰
- [ ] 随着代码演进保持准确
- [ ] 为代码理解增加真正价值
- [ ] 放置在适当位置（在它们描述的代码上方）
- [ ] 使用正确拼写和专业语言

## 总结

记住：**最好的注释是您不需要编写的注释，因为代码是自文档化的。**