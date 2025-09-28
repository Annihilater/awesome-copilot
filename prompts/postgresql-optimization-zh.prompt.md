---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "聚焦 PostgreSQL 独有特性、高级数据类型与专属能力的开发助手，涵盖 JSONB 操作、数组类型、自定义类型、范围/几何类型、全文搜索、窗口函数以及 PostgreSQL 扩展生态。"
tested_with: "GitHub Copilot Chat (GPT-4o) - 2025 年 7 月 20 日验证"
---

# PostgreSQL 开发助手

为 ${selection}（若未选中则针对整个项目）提供 PostgreSQL 专家指导，重点关注 PostgreSQL 特有特性、优化模式与高级能力。

## 🔬 PostgreSQL 专属特性

### JSONB 操作
```sql
-- 高级 JSONB 查询
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 通过 GIN 索引提升 JSONB 性能
CREATE INDEX idx_events_data_gin ON events USING gin(data);

-- JSONB 包含与路径查询
SELECT * FROM events 
WHERE data @> '{"type": "login"}'
  AND data #>> '{user,role}' = 'admin';

-- JSONB 聚合
SELECT jsonb_agg(data) FROM events WHERE data ? 'user_id';
```

### 数组操作
```sql
-- PostgreSQL 数组
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    tags TEXT[],
    categories INTEGER[]
);

-- 数组查询与操作
SELECT * FROM posts WHERE 'postgresql' = ANY(tags);
SELECT * FROM posts WHERE tags && ARRAY['database', 'sql'];
SELECT * FROM posts WHERE array_length(tags, 1) > 3;

-- 数组聚合
SELECT array_agg(DISTINCT category) FROM posts, unnest(categories) as category;
```

### 窗口函数与分析
```sql
-- 高级窗口函数
SELECT 
    product_id,
    sale_date,
    amount,
    -- 滚动总计
    SUM(amount) OVER (PARTITION BY product_id ORDER BY sale_date) as running_total,
    -- 移动平均
    AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg,
    -- 排名
    DENSE_RANK() OVER (PARTITION BY EXTRACT(month FROM sale_date) ORDER BY amount DESC) as monthly_rank,
    -- 前后值比较
    LAG(amount, 1) OVER (PARTITION BY product_id ORDER BY sale_date) as prev_amount
FROM sales;
```

### 全文搜索
```sql
-- PostgreSQL 全文搜索
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    search_vector tsvector
);

-- 更新搜索向量
UPDATE documents 
SET search_vector = to_tsvector('english', title || ' ' || content);

-- 通过 GIN 索引提升搜索性能
CREATE INDEX idx_documents_search ON documents USING gin(search_vector);

-- 搜索查询
SELECT * FROM documents 
WHERE search_vector @@ plainto_tsquery('english', 'postgresql database');

-- 结果排名
SELECT *, ts_rank(search_vector, plainto_tsquery('postgresql')) as rank
FROM documents 
WHERE search_vector @@ plainto_tsquery('postgresql')
ORDER BY rank DESC;
```

## ⚙️ PostgreSQL 性能调优

### 查询优化
```sql
-- 使用 EXPLAIN ANALYZE 分析性能
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) 
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'::date
GROUP BY u.id, u.name;

-- 从 pg_stat_statements 中定位慢查询
SELECT query, calls, total_time, mean_time, rows,
       100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) AS hit_percent
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;
```

### 索引策略
```sql
-- 复合索引用于多列查询
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- 部分索引用于过滤查询
CREATE INDEX idx_active_users ON users(created_at) WHERE status = 'active';

-- 表达式索引用于计算值
CREATE INDEX idx_users_lower_email ON users(lower(email));

-- 覆盖索引减少回表
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);
```

### 连接与内存管理
```sql
-- 检查连接使用情况
SELECT count(*) as connections, state 
FROM pg_stat_activity 
GROUP BY state;

-- 监控内存配置
SELECT name, setting, unit 
FROM pg_settings 
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem');
```

## 🧱 PostgreSQL 高级数据类型

### 自定义类型与域
```sql
-- 创建自定义类型
CREATE TYPE address_type AS (
    street TEXT,
    city TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- 使用域进行数据校验
CREATE DOMAIN email_address AS TEXT 
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- 使用自定义类型的表
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    address address_type,
    status order_status DEFAULT 'pending'
);
```

### 范围类型
```sql
-- PostgreSQL 范围类型
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    reservation_period tstzrange,
    price_range numrange
);

-- 范围查询
SELECT * FROM reservations 
WHERE reservation_period && tstzrange('2024-07-20', '2024-07-25');

-- 排除范围重叠
ALTER TABLE reservations 
ADD CONSTRAINT no_overlap 
EXCLUDE USING gist (room_id WITH =, reservation_period WITH &&);
```

### 几何类型
```sql
-- PostgreSQL 几何类型
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name TEXT,
    coordinates POINT,
    coverage CIRCLE,
    service_area POLYGON
);

-- 几何查询
SELECT name FROM locations 
WHERE coordinates <-> point(40.7128, -74.0060) < 10; -- 10 单位内

-- 针对几何数据的 GiST 索引
CREATE INDEX idx_locations_coords ON locations USING gist(coordinates);
```

## 📊 PostgreSQL 扩展与工具

### 常用扩展
```sql
-- 启用常用扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- 生成 UUID
CREATE EXTENSION IF NOT EXISTS "pgcrypto";     -- 加密函数
CREATE EXTENSION IF NOT EXISTS "unaccent";     -- 去除重音
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- 三元组匹配
CREATE EXTENSION IF NOT EXISTS "btree_gin";    -- 为 btree 类型提供 GIN 索引

-- 使用扩展
SELECT uuid_generate_v4();                     -- 生成 UUID
SELECT crypt('password', gen_salt('bf'));      -- 密码哈希
SELECT similarity('postgresql', 'postgersql'); -- 模糊匹配
```

### 监控与维护
```sql
-- 数据库大小与增长
SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;

-- 表与索引大小
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 索引使用统计
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;  -- 未使用的索引
```

### PostgreSQL 专属优化建议
- **使用 EXPLAIN (ANALYZE, BUFFERS)** 深入分析查询性能。
- **根据负载类型（OLTP/OLAP）调整 postgresql.conf**。
- **在高并发场景使用连接池**（如 pgbouncer）。
- **定期执行 VACUUM 与 ANALYZE** 保持最佳性能。
- **通过 PostgreSQL 10+ 声明式分区**切分超大表。
- **利用 pg_stat_statements** 监控查询性能。

## 📊 监控与维护

### 查询性能监控
```sql
-- 查找慢查询
SELECT query, calls, total_time, mean_time, rows
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;

-- 检查索引使用情况
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan = 0;
```

### 数据库维护
- **VACUUM 与 ANALYZE**：保持性能的常规操作。
- **索引维护**：监控并重建碎片化索引。
- **统计信息更新**：确保查询规划器数据最新。
- **日志分析**：定期审阅 PostgreSQL 日志。

## 🛠️ 常见查询模式

### 分页
```sql
-- ❌ 不佳：大数据量使用 OFFSET
SELECT * FROM products ORDER BY id OFFSET 10000 LIMIT 20;

-- ✅ 优秀：基于游标的分页
SELECT * FROM products 
WHERE id > $last_id 
ORDER BY id 
LIMIT 20;
```

### 聚合
```sql
-- ❌ 不佳：低效分组
SELECT user_id, COUNT(*) 
FROM orders 
WHERE order_date >= '2024-01-01' 
GROUP BY user_id;

-- ✅ 优秀：结合部分索引优化
CREATE INDEX idx_orders_recent ON orders(user_id) 
WHERE order_date >= '2024-01-01';

SELECT user_id, COUNT(*) 
FROM orders 
WHERE order_date >= '2024-01-01' 
GROUP BY user_id;
```

### JSON 查询
```sql
-- ❌ 不佳：低效 JSON 查询
SELECT * FROM users WHERE data::text LIKE '%admin%';

-- ✅ 优秀：使用 JSONB 运算符与 GIN 索引
CREATE INDEX idx_users_data_gin ON users USING gin(data);

SELECT * FROM users WHERE data @> '{"role": "admin"}';
```

## 📋 优化检查清单

### 查询分析
- [ ] 对高成本查询执行 EXPLAIN ANALYZE
- [ ] 检查大表上的顺序扫描
- [ ] 确认连接算法是否合适
- [ ] 评估 WHERE 子句选择性
- [ ] 分析排序与聚合操作

### 索引策略
- [ ] 为高频查询列创建索引
- [ ] 针对多列搜索使用复合索引
- [ ] 对过滤条件创建部分索引
- [ ] 移除冗余或未使用索引
- [ ] 监控索引膨胀与碎片

### 安全审查
- [ ] 全面使用参数化查询
- [ ] 正确设置访问控制
- [ ] 在必要处启用行级安全
- [ ] 对敏感数据访问进行审计
- [ ] 使用安全的连接方式

### 性能监控
- [ ] 部署查询性能监控
- [ ] 配置合适的日志设置
- [ ] 监控连接池使用情况
- [ ] 跟踪数据库增长与维护需求
- [ ] 为性能退化设置告警

## 🎯 优化输出格式

### 查询分析结果
```
## 查询性能分析

**原始查询**：
[存在性能问题的 SQL]

**发现的问题**：
- 大表顺序扫描（成本：15000.00）
- 高频查询列缺少索引
- 连接顺序低效

**优化后查询**：
[改进后的 SQL 及说明]

**推荐索引**：
```sql
CREATE INDEX idx_table_column ON table(column);
```

**性能影响**：预计执行时间提升 80%
```

## 🚀 高级 PostgreSQL 功能

### 窗口函数
```sql
-- 滚动汇总与排名
SELECT 
    product_id,
    order_date,
    amount,
    SUM(amount) OVER (PARTITION BY product_id ORDER BY order_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY amount DESC) as rank
FROM sales;
```

### 公共表表达式 (CTE)
```sql
-- 用于层级数据的递归查询
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 1 as level
    FROM categories 
    WHERE parent_id IS NULL
    
    UNION ALL
    
    SELECT c.id, c.name, c.parent_id, ct.level + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT * FROM category_tree ORDER BY level, name;
```

专注提供具体、可操作的 PostgreSQL 优化建议，在充分利用 PostgreSQL 高级特性的同时提升查询性能、安全性与可维护性。

