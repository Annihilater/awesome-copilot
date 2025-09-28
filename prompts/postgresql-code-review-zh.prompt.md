---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems"]
description: "专注 PostgreSQL 最佳实践、反面模式与独特质量标准的代码审查助手，涵盖 JSONB 操作、数组使用、自定义类型、架构设计、函数优化，以及行级安全 (RLS) 等 PostgreSQL 专属安全特性。"
tested_with: "GitHub Copilot Chat (GPT-4o) - 2025 年 7 月 20 日验证"
---

# PostgreSQL 代码审查助手

针对 ${selection}（若未选中，则审查整个项目）提供 PostgreSQL 专家级代码审查，聚焦 PostgreSQL 特有的最佳实践、反模式与质量标准。

## 🎯 PostgreSQL 专属审查领域

### JSONB 最佳实践
```sql
-- ❌ 不佳：低效的 JSONB 查询（无索引支持）
SELECT * FROM orders WHERE data->>'status' = 'shipped';

-- ✅ 优秀：可建立索引的 JSONB 查询
CREATE INDEX idx_orders_status ON orders USING gin((data->'status'));
SELECT * FROM orders WHERE data @> '{"status": "shipped"}';

-- ❌ 不佳：未经过权衡的深度嵌套
UPDATE orders SET data = data || '{"shipping":{"tracking":{"number":"123"}}}';

-- ✅ 优秀：结构化 JSONB 并配合校验
ALTER TABLE orders ADD CONSTRAINT valid_status 
CHECK (data->>'status' IN ('pending', 'shipped', 'delivered'));
```

### 数组操作审查
```sql
-- ❌ 不佳：低效的数组查询（无法利用索引）
SELECT * FROM products WHERE 'electronics' = ANY(categories);

-- ✅ 优秀：使用 GIN 索引的数组查询
CREATE INDEX idx_products_categories ON products USING gin(categories);
SELECT * FROM products WHERE categories @> ARRAY['electronics'];

-- ❌ 不佳：在循环中进行数组拼接（触发器/函数内低效）

-- ✅ 优秀：批量数组操作
UPDATE products SET categories = categories || ARRAY['new_category']
WHERE id IN (SELECT id FROM products WHERE condition);
```

### PostgreSQL 架构设计审查
```sql
-- ❌ 不佳：未充分利用 PostgreSQL 特性
CREATE TABLE users (
    id INTEGER,
    email VARCHAR(255),
    created_at TIMESTAMP
);

-- ✅ 优秀：面向 PostgreSQL 优化的架构
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email CITEXT UNIQUE NOT NULL,  -- 不区分大小写的邮箱
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}',
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- 为 metadata 查询添加 JSONB GIN 索引
CREATE INDEX idx_users_metadata ON users USING gin(metadata);
```

### 自定义类型与域
```sql
-- ❌ 不佳：对特定数据仍使用通用类型
CREATE TABLE transactions (
    amount DECIMAL(10,2),
    currency VARCHAR(3),
    status VARCHAR(20)
);

-- ✅ 优秀：利用 PostgreSQL 自定义类型
CREATE TYPE currency_code AS ENUM ('USD', 'EUR', 'GBP', 'JPY');
CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
CREATE DOMAIN positive_amount AS DECIMAL(10,2) CHECK (VALUE > 0);

CREATE TABLE transactions (
    amount positive_amount NOT NULL,
    currency currency_code NOT NULL,
    status transaction_status DEFAULT 'pending'
);
```

## 🔍 PostgreSQL 反面模式

### 性能反面模式
- **忽视 PostgreSQL 特有索引**：未针对数据类型使用 GIN/GiST 等索引
- **误用 JSONB**：将 JSONB 当作普通字符串字段处理
- **忽略数组运算符**：使用低效数组操作
- **分区键选择不当**：未有效利用 PostgreSQL 分区能力

### 架构设计问题
- **不使用 ENUM**：对有限值集合仍采用 VARCHAR
- **缺少约束**：未设置 CHECK 约束进行数据校验
- **数据类型选择错误**：本应使用 TEXT 或 CITEXT 却使用 VARCHAR
- **JSONB 结构缺失**：缺乏受约束的 JSONB 结构

### 函数与触发器问题
```sql
-- ❌ 不佳：低效触发器函数
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();  -- 应使用 TIMESTAMPTZ
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ✅ 优秀：优化后的触发器函数
CREATE OR REPLACE FUNCTION update_modified_time()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 仅在必要时触发
CREATE TRIGGER update_modified_time_trigger
    BEFORE UPDATE ON table_name
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
    EXECUTE FUNCTION update_modified_time();
```

## 📊 PostgreSQL 扩展使用审查

### 扩展最佳实践
```sql
-- ✅ 创建前先检查扩展是否存在
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ✅ 合理使用扩展
-- 生成 UUID
SELECT uuid_generate_v4();

-- 密码哈希
SELECT crypt('password', gen_salt('bf'));

-- 模糊文本匹配
SELECT word_similarity('postgres', 'postgre');
```

## 🛡️ PostgreSQL 安全审查

### 行级安全 (RLS)
```sql
-- ✅ 实施 RLS
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_data_policy ON sensitive_data
    FOR ALL TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### 权限管理
```sql
-- ❌ 不佳：授予过度权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;

-- ✅ 优秀：粒度合理的权限
GRANT SELECT, INSERT, UPDATE ON specific_table TO app_user;
GRANT USAGE ON SEQUENCE specific_table_id_seq TO app_user;
```

## 🎯 PostgreSQL 代码质量检查清单

### 架构设计
- [ ] 使用合适的 PostgreSQL 数据类型（CITEXT、JSONB、数组等）
- [ ] 通过 ENUM 类型限制可选值
- [ ] 设置适当的 CHECK 约束
- [ ] 使用 TIMESTAMPTZ 而非 TIMESTAMP
- [ ] 定义可复用约束的自定义域 (DOMAIN)

### 性能考量
- [ ] 选择恰当的索引类型（JSONB/数组用 GIN，范围用 GiST）
- [ ] JSONB 查询使用包含运算符（@>、? 等）
- [ ] 数组操作使用 PostgreSQL 专属运算符
- [ ] 恰当使用窗口函数与 CTE
- [ ] 高效利用 PostgreSQL 特有函数

### PostgreSQL 特性利用
- [ ] 合理使用扩展
- [ ] 在适当场景使用 PL/pgSQL 存储过程
- [ ] 发挥 PostgreSQL 高级 SQL 能力
- [ ] 应用 PostgreSQL 特有的优化技术
- [ ] 在函数中实现完善的错误处理

### 安全与合规
- [ ] 在需要时启用行级安全 (RLS)
- [ ] 正确配置角色与权限
- [ ] 使用 PostgreSQL 内置加密函数
- [ ] 借助 PostgreSQL 功能实现审计记录

## 📝 PostgreSQL 专属审查指南

1. **数据类型优化**：确保恰当使用 PostgreSQL 专属类型
2. **索引策略**：审查索引类型并确认充分利用 PostgreSQL 索引
3. **JSONB 结构**：校验 JSONB 架构设计与查询模式
4. **函数质量**：审视 PL/pgSQL 函数的效率与最佳实践
5. **扩展使用**：验证 PostgreSQL 扩展是否合理应用
6. **性能特性**：检查 PostgreSQL 高级性能特性的利用情况
7. **安全实现**：审查 PostgreSQL 专属安全机制的落实

重点关注 PostgreSQL 独有的能力，确保代码充分发挥其特性，而不是将其当作普通 SQL 数据库来使用。

