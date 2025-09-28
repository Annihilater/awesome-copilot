---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "通用 SQL 代码审查助手，为 MySQL、PostgreSQL、SQL Server、Oracle 等数据库提供全面的安全性、可维护性与代码质量检查，重点关注 SQL 注入防护、访问控制、代码规范与反面模式检测，可与 SQL 优化提示配合使用。"
tested_with: "GitHub Copilot Chat (GPT-4o) - 2025 年 7 月 20 日验证"
---

# SQL 代码审查

对 ${selection}（若未选中则审查整个项目）执行全面的 SQL 代码审查，重点覆盖安全性、性能、可维护性与数据库最佳实践。

## 🔒 安全分析

### 防止 SQL 注入
```sql
-- ❌ 严重：存在 SQL 注入风险
query = "SELECT * FROM users WHERE id = " + userInput;
query = f"DELETE FROM orders WHERE user_id = {user_id}";

-- ✅ 安全：参数化查询
-- PostgreSQL/MySQL
PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?';
EXECUTE stmt USING @user_id;

-- SQL Server
EXEC sp_executesql N'SELECT * FROM users WHERE id = @id', N'@id INT', @id = @user_id;
```

### 访问控制与权限
- **最小权限原则**：只授予必要权限
- **基于角色的访问**：使用数据库角色而非直接授予用户权限
- **架构安全**：正确设置模式拥有者与访问控制
- **函数/存储过程安全**：审查 DEFINER 与 INVOKER 权限

### 数据保护
- **敏感数据暴露**：避免在含敏感字段的表上使用 SELECT *
- **审计日志**：确保敏感操作有日志记录
- **数据脱敏**：使用视图或函数隐藏敏感数据
- **加密**：验证敏感数据的加密存储

## ⚡ 性能优化

### 查询结构分析
```sql
-- ❌ 不佳：低效查询模式
SELECT DISTINCT u.* 
FROM users u, orders o, products p
WHERE u.id = o.user_id 
AND o.product_id = p.id
AND YEAR(o.order_date) = 2024;

-- ✅ 良好：优化后的结构
SELECT u.id, u.name, u.email
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2024-01-01' 
AND o.order_date < '2025-01-01';
```

### 索引策略审查
- **缺失索引**：识别需要建立索引的列
- **索引过多**：查找未使用或冗余索引
- **复合索引**：针对复杂查询建立多列索引
- **索引维护**：检查索引碎片或过时情况

### 连接优化
- **连接类型**：确认使用正确的连接（INNER/LEFT/EXISTS 等）
- **连接顺序**：优先处理结果集较小的表
- **笛卡尔积**：识别并修复缺失连接条件
- **子查询 vs JOIN**：选择更高效的方案

### 聚合与窗口函数
```sql
-- ❌ 不佳：低效聚合
SELECT user_id, 
       (SELECT COUNT(*) FROM orders o2 WHERE o2.user_id = o1.user_id) as order_count
FROM orders o1
GROUP BY user_id;

-- ✅ 良好：高效聚合
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id;
```

## 🛠️ 代码质量与可维护性

### SQL 风格与格式
```sql
-- ❌ 不佳：格式混乱
select u.id,u.name,o.total from users u left join orders o on u.id=o.user_id where u.status='active' and o.order_date>='2024-01-01';

-- ✅ 良好：清晰可读
SELECT u.id,
       u.name,
       o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.order_date >= '2024-01-01';
```

### 命名规范
- **命名一致**：表、列、约束保持统一风格
- **语义清晰**：数据库对象名称应清晰易懂
- **避免保留字**：不使用数据库保留字作为标识符
- **大小写一致**：模式内大小写使用一致

### 架构设计审查
- **范式化程度**：避免过度或不足范式化
- **数据类型**：为性能与存储选择合适类型
- **约束**：正确使用 PRIMARY KEY、FOREIGN KEY、CHECK、NOT NULL
- **默认值**：设置合理的列默认值

## 🗄️ 数据库特定最佳实践

### PostgreSQL
```sql
-- JSON 数据使用 JSONB
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- JSONB 查询使用 GIN 索引
CREATE INDEX idx_events_data ON events USING gin(data);

-- 多值列使用数组类型
CREATE TABLE tags (
    post_id INT,
    tag_names TEXT[]
);
```

### MySQL
```sql
-- 选择合适的存储引擎
CREATE TABLE sessions (
    id VARCHAR(128) PRIMARY KEY,
    data TEXT,
    expires TIMESTAMP
) ENGINE=InnoDB;

-- 针对 InnoDB 优化
ALTER TABLE large_table 
ADD INDEX idx_covering (status, created_at, id);
```

### SQL Server
```sql
-- 选择合适的数据类型
CREATE TABLE products (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_at DATETIME2 DEFAULT GETUTCDATE()
);

-- 分析型场景使用列存储索引
CREATE COLUMNSTORE INDEX idx_sales_cs ON sales;
```

### Oracle
```sql
-- 使用序列实现自增
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;

CREATE TABLE users (
    id NUMBER DEFAULT user_id_seq.NEXTVAL PRIMARY KEY,
    name VARCHAR2(255) NOT NULL
);
```

## 🧪 测试与验证

### 数据完整性检查
```sql
-- 验证引用完整性
SELECT o.user_id 
FROM orders o 
LEFT JOIN users u ON o.user_id = u.id 
WHERE u.id IS NULL;

-- 检查数据一致性
SELECT COUNT(*) as inconsistent_records
FROM products 
WHERE price < 0 OR stock_quantity < 0;
```

### 性能测试
- **执行计划**：审查查询执行计划
- **负载测试**：使用真实数据量验证性能
- **压力测试**：检查并发场景表现
- **回归测试**：确保优化不破坏功能

## 📊 常见反面模式

### N+1 查询问题
```sql
-- ❌ 不佳：应用层出现 N+1 查询
for user in users:
    orders = query("SELECT * FROM orders WHERE user_id = ?", user.id)

-- ✅ 良好：单条优化查询
SELECT u.*, o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### 过度使用 DISTINCT
```sql
-- ❌ 不佳：用 DISTINCT 掩盖连接问题
SELECT DISTINCT u.name 
FROM users u, orders o 
WHERE u.id = o.user_id;

-- ✅ 良好：使用正确连接替代 DISTINCT
SELECT u.name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.name;
```

### WHERE 子句中误用函数
```sql
-- ❌ 不佳：函数导致无法走索引
SELECT * FROM orders 
WHERE YEAR(order_date) = 2024;

-- ✅ 良好：使用范围条件利用索引
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' 
  AND order_date < '2025-01-01';
```

## 📋 SQL 审查清单

### 安全
- [ ] 所有用户输入均已参数化
- [ ] 无字符串拼接生成的动态 SQL
- [ ] 权限控制合理
- [ ] 敏感数据受到保护
- [ ] 已消除 SQL 注入风险

### 性能
- [ ] 高频查询列具备索引
- [ ] 无不必要的 SELECT *
- [ ] JOIN 经过优化且类型正确
- [ ] WHERE 条件具备选择性并可使用索引
- [ ] 子查询已优化或转换为 JOIN

### 代码质量
- [ ] 命名规范一致
- [ ] 格式与缩进规范
- [ ] 复杂逻辑附有说明
- [ ] 使用合适的数据类型
- [ ] 实施适当的错误处理

### 架构设计
- [ ] 表结构符合合理范式
- [ ] 约束保证数据完整性
- [ ] 索引支持主要查询模式
- [ ] 正确定义外键关系
- [ ] 默认值设置合理

## 🎯 输出格式

### 问题模板
```
## [PRIORITY] [CATEGORY]: [Brief Description]

**Location**: [Table/View/Procedure name and line number if applicable]
**Issue**: [Detailed explanation of the problem]
**Security Risk**: [If applicable - injection risk, data exposure, etc.]
**Performance Impact**: [Query cost, execution time impact]
**Recommendation**: [Specific fix with code example]

**Before**:
```sql
-- Problematic SQL
```

**After**:
```sql
-- Improved SQL
```

**Expected Improvement**: [Performance gain, security benefit]
```

### 总结评估
- **安全评分**： [1-10] —— SQL 注入防护、访问控制
- **性能评分**： [1-10] —— 查询效率、索引利用
- **可维护性评分**： [1-10] —— 代码质量、文档
- **架构质量评分**： [1-10] —— 设计模式、范式

### 三大优先事项
1. **[关键安全修复]**：消除 SQL 注入漏洞
2. **[性能优化]**：补充缺失索引或优化查询
3. **[代码质量]**：改进命名规范与文档

请提供可执行的数据库无关建议，并突出平台特有的优化与最佳实践。

