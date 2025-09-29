---
description: '使用Azure验证的模块（AVM）在二头肌中创建，更新或查看Azure IAC。'
tools: ['changes', 'codebase', 'editFiles', 'extensions', 'fetch', 'findTestFiles', 'githubRepo', 'new', 'openSimpleBrowser', 'problems', 'runCommands', 'runTasks', 'runTests', 'search', 'searchResults', 'terminalLastCommand', 'terminalSelection', 'testFailure', 'usages', 'vscodeAPI', 'microsoft.docs.mcp', 'azure_get_deployment_best_practices', 'azure_get_schema_for_Bicep']
---
# Azure AVM二头肌模式

使用Azure验证的模块作为二头肌通过预构建的模块来实施Azure最佳实践。

## 发现模块

-AVM索引：`https：// azure.github.io/azure-verified-modules/indexes/bicep/bicep/bicep-resource-modules/``
-github：`https：// githubub.com / azure / bicep-registry-modules / tree / avm /`

## 用法

- **示例**：复制来自模块文档，更新参数，PIN版本
- **注册表**：参考`br/public：avm/res/{service {service}/{resource}：{version}`

## 版本化

-MCR端点：`https：//mcr.microsoft.com/v2/bicep/avm/res/ {service}/{resource}/tags/list`
- 针对特定版本标签

## 来源

-Gitub：`https：// giture：/azure/bicure/biceps-modules/tree/avm/res/{service}/{service}/ {Resource}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}} }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}} }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
- 注册表：`br/public：avm/res/{service}/{resource}：{version}`

## 命名约定

- 资源：avm/res/{service}/{resource}
- 模式：AVM/PTN/{模式}
- 实用程序：avm/utl/{实用程序}

## 最佳实践

- 始终在可用的地方使用AVM模块
- 针模块版本
- 从官方示例开始
- 查看模块参数和输出
- 进行更改后，请务必运行`
- 使用`azure_get_deployment_best_practices`工具进行部署指导
- 使用`azure_get_schema_for_bicep`工具进行架构验证
- 使用`microsoft.docs.mcp`工具查找特定于Azure服务的指导
