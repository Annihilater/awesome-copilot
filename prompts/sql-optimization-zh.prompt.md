---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "通用 SQL 性能优化助手，为 MySQL、PostgreSQL、SQL Server、Oracle 等提供查询调优、索引策略与数据库性能分析，包含执行计划解析、分页优化、批处理与性能监控指导。"
tested_with: "GitHub Copilot Chat (GPT-4o) - 2025 年 7 月 20 日验证"
---

# SQL 性能优化助手

为 ${selection}（若未选中则针对整个项目）提供专家级 SQL 性能优化建议，聚焦于适用于各类 SQL 数据库的通用优化技术。

## 🎯 核心优化领域

### 查询性能分析
```sql
-- ❌ 不佳：低效查询模式
SELECT * FROM orders o
WHERE YEAR(o.created_at) = 2024
  AND o.customer_id IN (
      SELECT c.id FROM customers c WHERE c.status = 'active'
  );

-- ✅ 良好：结合索引的优化查询
SELECT o.id, o.customer_id, o.total_amount, o.created_at
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
WHERE o.created_at >= '2024-01-01' 
  AND o.created_at < '2025-01-01'
  AND c.status = 'active';

-- 推荐索引：
-- CREATE INDEX idx_orders_created_at ON orders(created_at);
-- CREATE INDEX idx_customers_status ON customers(status);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```

### 索引策略优化
```sql
-- ❌ 不佳：索引设计过度宽泛
CREATE INDEX idx_user_data ON users(email, first_name, last_name, created_at);

-- ✅ 良好：针对查询模式优化复合索引
-- 先按 email 过滤，再按 created_at 排序
CREATE INDEX idx_users_email_created ON users(email, created_at);

-- 全文名搜索
CREATE INDEX idx_users_name ON users(last_name, first_name);

-- 用户状态查询
CREATE INDEX idx_users_status_created ON users(status, created_at)
WHERE status IS NOT NULL;
```

### 子查询优化
```sql
-- ❌ 不佳：关联子查询
SELECT p.product_name, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(price) 
    FROM products p2 
    WHERE p2.category_id = p.category_id
);

-- ✅ 良好：窗口函数方案
SELECT product_name, price
FROM (
    SELECT product_name, price,
           AVG(price) OVER (PARTITION BY category_id) as avg_category_price
    FROM products
) ranked
WHERE price > avg_category_price;
```

## 📊 性能调优技巧

### JOIN 优化
```sql
-- ❌ 不佳：连接顺序与过滤条件低效
SELECT o.*, c.name, p.product_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01'
  AND c.status = 'active';

-- ✅ 良好：带过滤条件的 INNER JOIN
SELECT o.id, o.total_amount, c.name, p.product_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id AND c.status = 'active'
INNER JOIN order_items oi ON o.id = oi.order_id
INNER JOIN products p ON oi.product_id = p.id
WHERE o.created_at > '2024-01-01';
```

### 分页优化
```sql
-- ❌ 不佳：OFFSET 分页在大偏移量下性能差
SELECT * FROM products 
ORDER BY created_at DESC 
LIMIT 20 OFFSET 10000;

-- ✅ 良好：基于游标的分页
SELECT * FROM products 
WHERE created_at < '2024-06-15 10:30:00'
ORDER BY created_at DESC 
LIMIT 20;

-- 或使用 ID 游标
SELECT * FROM products 
WHERE id > 1000
ORDER BY id 
LIMIT 20;
```

### 聚合优化
```sql
-- ❌ 不佳：多次重复聚合
SELECT COUNT(*) FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders WHERE status = 'shipped';
SELECT COUNT(*) FROM orders WHERE status = 'delivered';

-- ✅ 良好：单次条件聚合
SELECT 
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_count,
    COUNT(CASE WHEN status = 'shipped' THEN 1 END) as shipped_count,
    COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
FROM orders;
```

## 🔍 查询反面模式

### SELECT 性能问题
```sql
-- ❌ 不佳：SELECT * 反模式
SELECT * FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;

-- ✅ 良好：明确选择所需列
SELECT lt.id, lt.name, at.value
FROM large_table lt
JOIN another_table at ON lt.id = at.ref_id;
```

### WHERE 子句优化
```sql
-- ❌ 不佳：WHERE 中使用函数
SELECT * FROM orders 
WHERE UPPER(customer_email) = 'JOHN@EXAMPLE.COM';

-- ✅ 良好：索引友好
SELECT * FROM orders 
WHERE customer_email = 'john@example.com';
-- 可考虑：CREATE INDEX idx_orders_email ON orders(LOWER(customer_email));
```

### OR vs UNION 优化
```sql
-- ❌ 不佳：复杂 OR 条件
SELECT * FROM products 
WHERE (category = 'electronics' AND price < 1000)
   OR (category = 'books' AND price < 50);

-- ✅ 良好：使用 UNION 提升优化机会
SELECT * FROM products WHERE category = 'electronics' AND price < 1000
UNION ALL
SELECT * FROM products WHERE category = 'books' AND price < 50;
```

## 📈 与数据库无关的优化

### 批量操作
```sql
-- ❌ 不佳：逐行插入
INSERT INTO products (name, price) VALUES ('Product 1', 10.00);
INSERT INTO products (name, price) VALUES ('Product 2', 15.00);
INSERT INTO products (name, price) VALUES ('Product 3', 20.00);

-- ✅ 良好：批量插入
INSERT INTO products (name, price) VALUES 
('Product 1', 10.00),
('Product 2', 15.00),
('Product 3', 20.00);
```

### 临时表使用
```sql
-- ✅ 良好：利用临时表处理复杂逻辑
CREATE TEMPORARY TABLE temp_calculations AS
SELECT customer_id, 
       SUM(total_amount) as total_spent,
       COUNT(*) as order_count
FROM orders 
WHERE created_at >= '2024-01-01'
GROUP BY customer_id;

-- 使用临时表进行后续计算
SELECT c.name, tc.total_spent, tc.order_count
FROM temp_calculations tc
JOIN customers c ON tc.customer_id = c.id
WHERE tc.total_spent > 1000;
```

## 🛠️ 索引管理

### 索引设计原则
```sql
-- ✅ 良好：覆盖索引设计
CREATE INDEX idx_orders_covering 
ON orders(customer_id, created_at) 
INCLUDE (total_amount, status);  -- SQL Server 语法
-- 或：CREATE INDEX idx_orders_covering ON orders(customer_id, created_at, total_amount, status); -- 其他数据库
```

### 部分索引策略
```sql
-- ✅ 良好：针对特定条件的部分索引
CREATE INDEX idx_orders_active 
ON orders(created_at) 
WHERE status IN ('pending', 'processing');
```

## 📊 性能监控查询

### 查询性能分析
```sql
-- 用于识别慢查询的通用方法（语法因数据库而异）

-- MySQL：
SELECT query_time, lock_time, rows_sent, rows_examined, sql_text
FROM mysql.slow_log
ORDER BY query_time DESC;

-- PostgreSQL：
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY total_time DESC;

-- SQL Server：
SELECT 
    qs.total_elapsed_time/qs.execution_count as avg_elapsed_time,
    qs.execution_count,
    SUBSTRING(qt.text, (qs.statement_start_offset/2)+1,
        ((CASE qs.statement_end_offset WHEN -1 THEN DATALENGTH(qt.text)
        ELSE qs.statement_end_offset END - qs.statement_start_offset)/2)+1) as query_text
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.sql_handle) qt
ORDER BY avg_elapsed_time DESC;
```

## 🎯 通用优化检查清单

### 查询结构
- [ ] 生产查询避免使用 SELECT *
- [ ] 正确选择 JOIN 类型（INNER、LEFT/RIGHT）
- [ ] 在 WHERE 中尽早过滤
- [ ] 子查询适当使用 EXISTS 替代 IN
- [ ] 避免阻止索引使用的函数

### 索引策略
- [ ] 高频查询列均建立索引
- [ ] 复合索引列顺序正确
- [ ] 避免过度索引（影响写操作）
- [ ] 适时使用覆盖索引
- [ ] 针对特定查询模式使用部分索引

### 数据类型与架构
- [ ] 数据类型选择兼顾存储效率
- [ ] 合理范式化（OLTP 建议 3NF，OLAP 适当反范式化）
- [ ] 通过约束辅助优化器
- [ ] 大表适时分区

### 查询模式
- [ ] 使用 LIMIT/TOP 控制返回行数
- [ ] 实现高效分页策略
- [ ] 批量处理大规模数据变更
- [ ] 避免 N+1 查询问题
- [ ] 重复查询使用预编译语句

### 性能测试
- [ ] 使用真实数据量进行测试
- [ ] 分析查询执行计划
- [ ] 持续监控查询性能
- [ ] 为慢查询设置告警
- [ ] 定期检查索引使用情况

## 📝 优化方法论

1. **识别**：使用数据库工具定位慢查询
2. **分析**：检视执行计划，找出瓶颈
3. **优化**：应用适当的优化策略
4. **验证**：确认性能提升
5. **监控**：持续跟踪性能指标
6. **迭代**：定期回顾与优化

专注于可衡量的性能提升，并始终使用真实数据与查询模式验证优化效果。

