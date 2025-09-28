---
mode: "agent"
description: "分析应用中使用的 Azure 资源（IaC 文件和/或目标资源组中的资源）并优化成本 - 为已识别的优化创建 GitHub 问题。"
---

# Azure 成本优化

此工作流分析基础架构即代码 (IaC) 文件和 Azure 资源，以生成成本优化建议。它为每个优化机会创建单独的 GitHub 问题，外加一个 EPIC 问题以协调实施，从而实现成本节约计划的高效跟踪和执行。

## 先决条件

- 已配置并验证 Azure MCP 服务器
- 已配置并验证 GitHub MCP 服务器
- 已识别目标 GitHub 存储库
- 已部署 Azure 资源（IaC 文件可选但有帮助）
- 优先使用 Azure MCP 工具 (`azmcp-*`)，而不是直接使用 Azure CLI（如果可用）

## 工作流步骤

### 第 1 步：获取 Azure 最佳实践

**操作**：在分析前检索成本优化最佳实践
**工具**：Azure MCP 最佳实践工具
**过程**：

1. **加载最佳实践**：
   - 执行 `azmcp-bestpractices-get` 以获取一些最新的 Azure 优化指南。这可能无法涵盖所有场景，但提供了一个基础。
   - 尽可能使用这些实践来为后续分析和建议提供信息
   - 在优化建议中引用最佳实践，可以来自 MCP 工具输出或常规 Azure 文档

### 第 2 步：发现 Azure 基础架构

**操作**：动态发现和分析 Azure 资源和配置
**工具**：Azure MCP 工具 + Azure CLI 回退 + 本地文件系统访问
**过程**：

1. **资源发现**：

   - 执行 `azmcp-subscription-list` 以查找可用的订阅
   - 执行 `azmcp-group-list --subscription <subscription-id>` 以查找资源组
   - 获取相关组中所有资源的列表：
     - 使用 `az resource list --subscription <id> --resource-group <name>`
   - 对于每种资源类型，如果可能，首先使用 MCP 工具，然后使用 CLI 回退：
     - `azmcp-cosmos-account-list --subscription <id>` - Cosmos DB 帐户
     - `azmcp-storage-account-list --subscription <id>` - 存储帐户
     - `azmcp-monitor-workspace-list --subscription <id>` - Log Analytics 工作区
     - `azmcp-keyvault-key-list` - Key Vault
     - `az webapp list` - Web 应用（回退 - 没有可用的 MCP 工具）
     - `az appservice plan list` - 应用服务计划（回退）
     - `az functionapp list` - 函数应用（回退）
     - `az sql server list` - SQL 服务器（回退）
     - `az redis list` - Redis 缓存（回退）
     - ... 其他资源类型依此类推

2. **IaC 检测**：

   - 使用 `file_search` 扫描 IaC 文件："`**/*.bicep`", "`**/*.tf`", "**/main.json", "`**/_template_.json`"
   - 解析资源定义以了解预期的配置
   - 与发现的资源进行比较以识别差异
   - 注意 IaC 文件的存在，以便稍后提出实施建议
   - 不要使用存储库中的任何其他文件，只使用 IaC 文件。不允许使用其他文件，因为它不是事实来源。
   - 如果找不到 IaC 文件，则停止并向用户报告未找到 IaC 文件。

3. **配置分析**：
   - 提取每个资源的当前 SKU、层和设置
   - 识别资源关系和依赖关系
   - 映射可用的资源利用率模式

### 第 3 步：收集使用指标并验证当前成本

**操作**：收集利用率数据并验证实际资源成本
**工具**：Azure MCP 监视工具 + Azure CLI
**过程**：

1. **查找监视源**：

   - 使用 `azmcp-monitor-workspace-list --subscription <id>` 查找 Log Analytics 工作区
   - 使用 `azmcp-monitor-table-list --subscription <id> --workspace <name> --table-type "CustomLog"` 发现可用数据

2. **执行使用情况查询**：

   - 将 `azmcp-monitor-log-query` 与这些预定义查询一起使用：
     - 查询：“recent” 用于最近的活动模式
     - 查询：“errors” 用于指示问题的错误级别日志
   - 对于自定义分析，请使用 KQL 查询：

   ```kql
   // 应用服务的 CPU 利用率
   AppServiceAppLogs
   | where TimeGenerated > ago(7d)
   | summarize avg(CpuTime) by Resource, bin(TimeGenerated, 1h)

   // Cosmos DB RU 消耗
   AzureDiagnostics
   | where ResourceProvider == "MICROSOFT.DOCUMENTDB"
   | where TimeGenerated > ago(7d)
   | summarize avg(RequestCharge) by Resource

   // 存储帐户访问模式
   StorageBlobLogs
   | where TimeGenerated > ago(7d)
   | summarize RequestCount=count() by AccountName, bin(TimeGenerated, 1d)
   ```

3. **计算基线指标**：

   - CPU/内存利用率平均值
   - 数据库吞吐量模式
   - 存储访问频率
   - 函数执行率

4. **验证当前成本**：
   - 使用在第 2 步中发现的 SKU/层配置
