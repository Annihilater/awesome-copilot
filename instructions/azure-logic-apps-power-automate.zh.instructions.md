---
description: '使用最佳实践开发 Azure Logic Apps 和 Power Automate 工作流的指南，涵盖工作流定义语言 (WDL)、集成模式和企业自动化'
applyTo: "**/*.json,**/*.logicapp.json,**/workflow.json,**/*-definition.json,**/*.flow.json"
---

# Azure Logic Apps 和 Power Automate 指南

## 概述

这些指南将帮助您使用基于 JSON 的工作流定义语言 (WDL) 编写高质量的 Azure Logic Apps 和 Microsoft Power Automate 工作流定义。Azure Logic Apps 是一个基于云的集成平台即服务 (iPaaS)，提供 1,400+ 连接器来简化跨服务和协议的集成。遵循这些指导原则来创建强健、高效和可维护的云工作流自动化解决方案。

## 工作流定义语言结构

使用 Logic Apps 或 Power Automate 流 JSON 文件时，确保您的工作流遵循以下标准结构：

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "actions": { },
    "contentVersion": "1.0.0.0",
    "outputs": { },
    "parameters": { },
    "staticResults": { },
    "triggers": { }
  },
  "parameters": { }
}
```

## Azure Logic Apps 和 Power Automate 开发最佳实践

### 1. 触发器

- **根据您的场景使用适当的触发器类型**：
  - **Request 触发器**：用于同步 API 式工作流
  - **Recurrence 触发器**：用于计划操作
  - **事件驱动触发器**：用于响应式模式（Service Bus、Event Grid 等）
- **配置适当的触发器设置**：
  - 设置合理的超时时间
  - 对高容量数据源使用分页设置
  - 实施适当的身份验证

```json
"triggers": {
  "manual": {
    "type": "Request",
    "kind": "Http",
    "inputs": {
      "schema": {
        "type": "object",
        "properties": {
          "requestParameter": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### 2. 操作

- **为操作命名描述性名称**以表明其目的
- **使用作用域组织复杂的工作流**进行逻辑分组
- **对不同操作使用适当的操作类型**：
  - 用于 API 调用的 HTTP 操作
  - 用于内置集成的连接器操作
  - 用于转换的数据操作

```json
"actions": {
  "Get_Customer_Data": {
    "type": "Http",
    "inputs": {
      "method": "GET",
      "uri": "https://api.example.com/customers/@{triggerBody()?['customerId']}",
      "headers": {
        "Content-Type": "application/json"
      }
    },
    "runAfter": {}
  }
}
```

### 3. 错误处理和可靠性

- **实施强健的错误处理**：
  - 使用 "runAfter" 配置处理失败
  - 为瞬态错误配置重试策略
  - 使用带有 "runAfter" 条件的作用域用于错误分支
- **为关键操作实施回退机制**
- **为外部服务调用添加超时**
- **对复杂错误处理场景使用 runAfter 条件**

```json
"actions": {
  "HTTP_Action": {
    "type": "Http",
    "inputs": { },
    "retryPolicy": {
      "type": "fixed",
      "count": 3,
      "interval": "PT20S",
      "minimumInterval": "PT5S",
      "maximumInterval": "PT1H"
    }
  },
  "Handle_Success": {
    "type": "Scope",
    "actions": { },
    "runAfter": {
      "HTTP_Action": ["Succeeded"]
    }
  },
  "Handle_Failure": {
    "type": "Scope",
    "actions": {
      "Log_Error": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['loganalytics']['connectionId']"
            }
          },
          "method": "post",
          "body": {
            "LogType": "WorkflowError",
            "ErrorDetails": "@{actions('HTTP_Action').outputs.body}",
            "StatusCode": "@{actions('HTTP_Action').outputs.statusCode}"
          }
        }
      },
      "Send_Notification": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['office365']['connectionId']"
            }
          },
          "method": "post",
          "path": "/v2/Mail",
          "body": {
            "To": "support@contoso.com",
            "Subject": "Workflow Error - HTTP Call Failed",
            "Body": "<p>The HTTP call failed with status code: @{actions('HTTP_Action').outputs.statusCode}</p>"
          }
        },
        "runAfter": {
          "Log_Error": ["Succeeded"]
        }
      }
    },
    "runAfter": {
      "HTTP_Action": ["Failed", "TimedOut"]
    }
  }
}
```

### 4. 表达式和函数

- **使用内置表达式函数**转换数据
- **保持表达式简洁易读**
- **为复杂表达式添加注释说明**

常见表达式模式：
- 字符串操作：`concat()`、`replace()`、`substring()`
- 集合操作：`filter()`、`map()`、`select()`
- 条件逻辑：`if()`、`and()`、`or()`、`equals()`
- 日期/时间操作：`formatDateTime()`、`addDays()`
- JSON 处理：`json()`、`array()`、`createArray()`

```json
"Set_Variable": {
  "type": "SetVariable",
  "inputs": {
    "name": "formattedData",
    "value": "@{map(body('Parse_JSON'), item => {
      return {
        id: item.id,
        name: toUpper(item.name),
        date: formatDateTime(item.timestamp, 'yyyy-MM-dd')
      }
    })}"
  }
}
```

#### 在 Power Automate 条件中使用表达式

Power Automate 在条件中支持高级表达式来检查多个值。使用复杂逻辑条件时，请使用以下模式：

- 比较单个值：使用基本条件设计器界面
- 多个条件：在高级模式中使用高级表达式

Power Automate 条件中的常见逻辑表达式函数：

| 表达式 | 描述 | 示例 |
|------------|-------------|---------|
| `and` | 当两个参数都为真时返回真 | `@and(equals(item()?['Status'], 'completed'), equals(item()?['Assigned'], 'John'))` |
| `or` | 当任一参数为真时返回真 | `@or(equals(item()?['Status'], 'completed'), equals(item()?['Status'], 'unnecessary'))` |
| `equals` | 检查值是否相等 | `@equals(item()?['Status'], 'blocked')` |
| `greater` | 检查第一个值是否大于第二个 | `@greater(item()?['Due'], item()?['Paid'])` |
| `less` | 检查第一个值是否小于第二个 | `@less(item()?['dueDate'], addDays(utcNow(),1))` |
| `empty` | 检查对象、数组或字符串是否为空 | `@empty(item()?['Status'])` |
| `not` | 返回布尔值的相反值 | `@not(contains(item()?['Status'], 'Failed'))` |

示例：检查状态是否为 "completed" 或 "unnecessary"：
```
@or(equals(item()?['Status'], 'completed'), equals(item()?['Status'], 'unnecessary'))
```

示例：检查状态是否为 "blocked" 且分配给特定人员：
```
@and(equals(item()?['Status'], 'blocked'), equals(item()?['Assigned'], 'John Wonder'))
```

示例：检查付款是否逾期且未完成：
```
@and(greater(item()?['Due'], item()?['Paid']), less(item()?['dueDate'], utcNow()))
```

**注意：** 在 Power Automate 中，在表达式中访问前面步骤的动态值时，使用语法 `item()?['PropertyName']` 来安全访问集合中的属性。

### 5. 参数和变量

- **将工作流参数化**以便在不同环境中重用
- **在工作流中使用变量存储临时值**
- **定义具有默认值和描述的清晰参数架构**

```json
"parameters": {
  "apiEndpoint": {
    "type": "string",
    "defaultValue": "https://api.dev.example.com",
    "metadata": {
      "description": "The base URL for the API endpoint"
    }
  }
},
"variables": {
  "requestId": "@{guid()}",
  "processedItems": []
}
```

### 6. 控制流

- **使用条件**进行分支逻辑
- **对独立操作实施并行分支**
- **对集合使用 foreach 循环**，设置合理的批次大小
- **应用 until 循环**，设置适当的退出条件

```json
"Process_Items": {
  "type": "Foreach",
  "foreach": "@body('Get_Items')",
  "actions": {
    "Process_Single_Item": {
      "type": "Scope",
      "actions": { }
    }
  },
  "runAfter": {
    "Get_Items": ["Succeeded"]
  },
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 10
    }
  }
}
```

### 7. 内容和消息处理

- **验证消息架构**以确保数据完整性
- **实施适当的内容类型处理**
- **使用 Parse JSON 操作**处理结构化数据

```json
"Parse_Response": {
  "type": "ParseJson",
  "inputs": {
    "content": "@body('HTTP_Request')",
    "schema": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string"
        },
        "data": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": { }
          }
        }
      }
    }
  }
}
```

### 8. 安全最佳实践

- **尽可能使用托管身份**
- **在 Key Vault 中存储密钥**
- **对连接实施最少权限访问**
- **使用身份验证保护 API 端点**
- **对 HTTP 触发器实施 IP 限制**
- **对参数和消息中的敏感数据应用数据加密**
- **使用 Azure RBAC** 控制对 Logic Apps 资源的访问
- **定期进行安全审查**工作流和连接

```json
"Get_Secret": {
  "type": "ApiConnection",
  "inputs": {
    "host": {
      "connection": {
        "name": "@parameters('$connections')['keyvault']['connectionId']"
      }
    },
    "method": "get",
    "path": "/secrets/@{encodeURIComponent('apiKey')}/value"
  }
},
"Call_Protected_API": {
  "type": "Http",
  "inputs": {
    "method": "POST",
    "uri": "https://api.example.com/protected",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer @{body('Get_Secret')?['value']}"
    },
    "body": {
      "data": "@variables('processedData')"
    }
  },
  "authentication": {
    "type": "ManagedServiceIdentity"
  },
  "runAfter": {
    "Get_Secret": ["Succeeded"]
  }
}
```

## 性能优化

- **最小化不必要的操作**
- **在可用时使用批处理操作**
- **优化表达式**以降低复杂性
- **配置适当的超时值**
- **对大数据集实施分页**
- **对可并行化操作实施并发控制**

```json
"Process_Items": {
  "type": "Foreach",
  "foreach": "@body('Get_Items')",
  "actions": {
    "Process_Single_Item": {
      "type": "Scope",
      "actions": { }
    }
  },
  "runAfter": {
    "Get_Items": ["Succeeded"]
  },
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 10
    }
  }
}
```

### 工作流设计最佳实践

- **将工作流限制在 50 个操作或更少**以获得最佳设计器性能
- **在必要时将复杂业务逻辑拆分**为多个较小的工作流
- **对需要零停机部署的关键逻辑应用使用部署槽**
- **避免在触发器和操作定义中硬编码属性**
- **添加描述性注释**提供触发器和操作定义的上下文
- **在可用时使用内置操作**而不是共享连接器以获得更好的性能
- **对 B2B 场景和 EDI 消息处理使用集成帐户**
- **在组织中重用工作流模板**用于标准模式
- **避免作用域和操作的深度嵌套**以保持可读性

### 监控和可观察性

- **配置诊断设置**来捕获工作流运行和指标
- **添加跟踪 ID** 以关联相关的工作流运行
- **实施具有适当详细级别的全面日志记录**
- **为工作流失败和性能下降设置警报**
- **使用 Application Insights** 进行端到端跟踪和监控

## 平台类型和注意事项

### Azure Logic Apps 与 Power Automate

虽然 Azure Logic Apps 和 Power Automate 共享相同的底层工作流引擎和语言，但它们有不同的目标受众和功能：

- **Power Automate**：
  - 面向业务用户的用户友好界面
  - Power Platform 生态系统的一部分
  - 与 Microsoft 365 和 Dynamics 365 集成
  - 用于 UI 自动化的桌面流功能

- **Azure Logic Apps**：
  - 企业级集成平台
  - 面向开发人员，具有高级功能
  - 更深入的 Azure 服务集成
  - 更广泛的监控和运维功能

### Logic App 类型

#### 消费型 Logic Apps
- 按执行付费的定价模式
- 无服务器架构
- 适用于可变或不可预测的工作负载

#### 标准 Logic Apps
- 基于 App Service 计划的固定定价
- 可预测的性能
- 本地开发支持
- 与虚拟网络集成

#### 集成服务环境 (ISE)
- 专用部署环境
- 更高的吞吐量和更长的执行持续时间
- 直接访问虚拟网络资源
- 隔离的运行时环境

### Power Automate 许可类型
- **Power Automate 按用户计划**：面向个人用户
- **Power Automate 按流计划**：用于特定工作流
- **Power Automate 流程计划**：用于 RPA 功能
- **Power Automate 包含在 Office 365 中**：Office 365 用户的有限功能

## 常见集成模式

### 架构模式
- **中介模式**：使用 Logic Apps/Power Automate 作为系统间的编排层
- **基于内容的路由**：根据内容将消息路由到不同目的地
- **消息转换**：在格式间转换消息（JSON、XML、EDI 等）
- **分散-聚集**：并行分发工作并聚合结果
- **协议桥接**：连接使用不同协议的系统（REST、SOAP、FTP 等）
- **索取检查**：在 blob 存储或数据库中外部存储大型负载
- **Saga 模式**：使用补偿操作管理分布式事务以处理失败
- **编排模式**：在没有中央编排器的情况下协调多个服务

### 操作模式
- **异步处理模式**：用于长时间运行的操作
  ```json
  "LongRunningAction": {
    "type": "Http",
    "inputs": {
      "method": "POST",
      "uri": "https://api.example.com/longrunning",
      "body": { "data": "@triggerBody()" }
    },
    "retryPolicy": {
      "type": "fixed",
      "count": 3,
      "interval": "PT30S"
    }
  }
  ```

- **Webhook 模式**：用于基于回调的处理
  ```json
  "WebhookAction": {
    "type": "ApiConnectionWebhook",
    "inputs": {
      "host": {
        "connection": {
          "name": "@parameters('$connections')['servicebus']['connectionId']"
        }
      },
      "body": {
        "content": "@triggerBody()"
      },
      "path": "/subscribe/topics/@{encodeURIComponent('mytopic')}/subscriptions/@{encodeURIComponent('mysubscription')}"
    }
  }
  ```

### 企业集成模式
- **B2B 消息交换**：在交易伙伴间交换 EDI 文档（AS2、X12、EDIFACT）
- **集成帐户**：用于存储和管理 B2B 工件（协议、架构、映射）
- **规则引擎**：使用 Azure Logic Apps 规则引擎实施复杂业务规则
- **消息验证**：根据架构验证消息以确保合规性和数据完整性
- **事务处理**：使用补偿事务处理业务事务以进行回滚

## Logic Apps 的 DevOps 和 CI/CD

### 源代码控制和版本管理

- **在源代码控制中存储 Logic App 定义**（Git、Azure DevOps、GitHub）
- **使用 ARM 模板**部署到多个环境
- **实施适合发布节奏的分支策略**
- **使用标签或版本属性对 Logic Apps 进行版本控制**

### 自动化部署

- **使用 Azure DevOps 管道**或 GitHub Actions 进行自动化部署
- **实施环境特定值的参数化**
- **使用部署槽**进行零停机部署
- **在 CI/CD 管道中包含部署后验证测试**

```yaml
# Logic App 部署的 Azure DevOps YAML 管道示例
trigger:
  branches:
    include:
    - main
    - release/*

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureResourceManagerTemplateDeployment@3
  inputs:
    deploymentScope: 'Resource Group'
    azureResourceManagerConnection: 'Your-Azure-Connection'
    subscriptionId: '$(subscriptionId)'
    action: 'Create Or Update Resource Group'
    resourceGroupName: '$(resourceGroupName)'
    location: '$(location)'
    templateLocation: 'Linked artifact'
    csmFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-template.json'
    csmParametersFile: '$(System.DefaultWorkingDirectory)/arm-templates/logicapp-parameters-$(Environment).json'
    deploymentMode: 'Incremental'
```

## 跨平台注意事项

在同时使用 Azure Logic Apps 和 Power Automate 时：

- **导出/导入兼容性**：流可以从 Power Automate 导出并导入到 Logic Apps，但可能需要一些修改
- **连接器差异**：某些连接器在一个平台中可用，但在另一个中不可用
- **环境隔离**：Power Automate 环境提供隔离，可能有不同的策略
- **ALM 实践**：考虑对 Logic Apps 使用 Azure DevOps，对 Power Automate 使用解决方案

### 迁移策略

- **评估**：评估复杂性和迁移的适用性
- **连接器映射**：在平台间映射连接器并识别差距
- **测试策略**：在切换前实施并行测试
- **文档**：记录所有配置更改以供参考

## 其他资源

- [Azure Logic Apps 文档](https://docs.microsoft.com/en-us/azure/logic-apps/)
- [Power Automate 文档](https://docs.microsoft.com/en-us/power-automate/)
- [工作流定义语言架构](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-workflow-definition-language)
- [Power Automate 与 Logic Apps 比较](https://docs.microsoft.com/en-us/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs)
- [企业集成模式](https://docs.microsoft.com/en-us/azure/logic-apps/enterprise-integration-overview)
- [Logic Apps B2B 文档](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-enterprise-integration-b2b)
- [Azure Logic Apps 限制和配置](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-limits-and-config)
- [Logic Apps 性能优化](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-performance-optimization)
- [Logic Apps 安全概述](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-securing-a-logic-app)
- [API Management 和 Logic Apps 集成](https://docs.microsoft.com/en-us/azure/api-management/api-management-create-api-logic-app)
- [Logic Apps 标准网络](https://docs.microsoft.com/en-us/azure/logic-apps/connect-virtual-network-vnet-isolated-environment)