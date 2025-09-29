---
description: '使用Azure验证的模块（AVM）在Terraform中创建，更新或查看Azure IAC。'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'microsoft.docs.mcp', 'azure_get_deployment_best_practices', 'azure_get_schema_for_Bicep']
---

# Azure AVM Terraform模式

使用Azure验证的模块进行Terraform，通过预构建的模块执行Azure最佳实践。

## 发现模块

- Terraform注册表：搜索“ AVM” +资源，按合作伙伴标签过滤。
-AVM索引：`https：// azure.github.io/azure-verified-modules/indexes/terraform/tf-reasource-modules/``

## 用法

- **示例**：复制示例，将 `source = "../../"` 替换为 `source = "Azure/avm-res-{service}-{resource}/azurerm"`，添加 `version` 并设置 `enable_telemetry`。
- **自定义**：复制配置说明，设置输入，并固定 `version`。

## 版本化

- 端点：`https：//registry.terraform.io/v1/modules/azure/ {module}/azurerm/versions`

## 来源

- 注册表：`https：//registry.terraform.io/modules/azure/ {module}/azurerm/最新
-github：`https：//gitureubub./azure/terreform-eaver-azurerm-avimerm-tores- {service}  -  {resource}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

## 命名约定

- 资源：azure/avm-res- {service}  -  {resource}/azurerm
- 模式：azure/avm-ptn- {模式}/azurerm
- 实用程序：azure/avm-utl- {utility}/azurerm

## 最佳实践

- 针模块和提供商版本
- 从官方示例开始
- 审查输入和输出
- 启用遥测
- 使用AVM实用程序模块
- 遵循Azurerm提供商的要求
- 更改后务必运行 `terraform fmt` 和 `terraform validate`。
- 使用`azure_get_deployment_best_practices`工具进行部署指导
- 使用`microsoft.docs.mcp`工具查找特定于Azure服务的指导

## Github副代理的自定义说明

**重要**：当Github副代理或GitHub副副代理正在处理此存储库时，必须执行以下本地单元测试以遵守PR检查。未能运行这些测试将导致PR验证失败：

```bash
./avm pre-commit
./avm tflint
./avm pr-check
```

这些命令必须在创建或更新任何拉动请求之前运行，以确保符合Azure验证的模块标准并防止CI/CD管道故障。
有关AVM过程的更多详细信息，请参见[Azure验证的模块贡献文档]（https://azure.github.io/azure-azure-verified-modules/contributing/contributing/terraform/testing/）。
