---
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "runCommands"]
description: "获取 Entity Framework Core 的最佳实践"
---

# Entity Framework Core 最佳实践

您的目标是帮助我在使用 Entity Framework Core 时遵循最佳实践。

## 数据上下文设计

- 保持 DbContext 类的专注和内聚
- 对配置选项使用构造函数注入
- 重写 OnModelCreating 以进行流畅的 API 配置
- 使用 IEntityTypeConfiguration 分离实体配置
- 考虑为控制台应用或测试使用 DbContextFactory 模式

## 实体设计

- 使用有意义的主键（考虑自然键与代理键）
- 实现适当的关系（一对一、一对多、多对多）
- 使用数据注释或流畅的 API 进行约束和验证
- 实现适当的导航属性
- 考虑为值对象使用拥有的实体类型

## 性能

- 对只读查询使用 AsNoTracking()
- 对大型结果集使用 Skip() 和 Take() 实现分页
- 在需要时使用 Include() 预先加载相关实体
- 考虑使用投影（Select）仅检索所需字段
- 对频繁执行的查询使用已编译的查询
- 通过正确包含相关数据来避免 N+1 查询问题

## 迁移

- 创建小而专注的迁移
- 描述性地命名迁移
- 在应用于生产之前验证迁移 SQL 脚本
- 考虑使用迁移包进行部署
- 在适当时通过迁移添加数据种子

## 查询

- 审慎使用 IQueryable 并了解查询何时执行
- 优先使用强类型的 LINQ 查询而不是原始 SQL
- 使用适当的查询运算符（Where、OrderBy、GroupBy）
- 考虑为复杂操作使用数据库函数
- 为可重用查询实现规范模式

## 更改跟踪和保存

- 使用适当的更改跟踪策略
- 批量调用 SaveChanges()
- 为多用户场景实现并发控制
- 考虑为多个操作使用事务
- 使用适当的 DbContext 生命周期（Web 应用的作用域）

## 安全

- 通过使用参数化查询来避免 SQL 注入
- 实现适当的数据访问权限
- 小心使用原始 SQL 查询
- 考虑对敏感信息进行数据加密
- 使用迁移来管理数据库用户权限

## 测试

- 为单元测试使用内存数据库提供程序
- 为集成测试使用 SQLite 创建单独的测试上下文
- 为纯单元测试模拟 DbContext 和 DbSet
- 在隔离环境中测试迁移
- 考虑对模型更改进行快照测试

在审查我的 EF Core 代码时，请识别问题并提出遵循这些最佳实践的改进建议。
