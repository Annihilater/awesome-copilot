---
title: Power Platform 连接器架构开发指导
description: '使用 JSON Schema 定义的 Power Platform 自定义连接器综合开发指南。涵盖 API 定义（Swagger 2.0）、API 属性和设置配置以及 Microsoft 扩展。'
applyTo: '**/*.{json,md}'
---

# Power Platform 连接器架构开发指导

## 项目概述
此工作区包含 Power Platform 自定义连接器的 JSON Schema 定义，专门用于 `paconn`（Power Apps Connector）工具。这些架构验证并为以下内容提供 IntelliSense：

- **API 定义**（Swagger 2.0 格式）
- **API 属性**（连接器元数据和配置）
- **设置**（环境和部署配置）

## 文件结构理解

### 1. apiDefinition.swagger.json
- **目的**：此文件包含带有 Power Platform 扩展的 Swagger 2.0 API 定义。
- **关键特性**：
  - 标准 Swagger 2.0 属性，包括 info、paths、definitions 等。
  - 以 `x-ms-*` 前缀开头的 Microsoft 特定扩展。
  - 专为 Power Platform 设计的自定义格式类型，如 `date-no-tz` 和 `html`。
  - 提供运行时灵活性的动态架构支持。
  - 支持 OAuth2、API Key 和 Basic Auth 身份验证方法的安全定义。

### 2. apiProperties.json
- **目的**：此文件定义连接器元数据、身份验证配置和策略配置。
- **关键组件**：
  - **连接参数**：支持各种身份验证类型，包括 OAuth、API Key 和网关配置。
  - **策略模板实例**：处理连接器的数据转换和路由策略。
  - **连接器元数据**：包括发布者信息、功能和品牌元素。

### 3. settings.json
- **目的**：此文件为 paconn 工具提供环境和部署配置设置。
- **配置选项**：
  - 针对特定 Power Platform 环境的环境 GUID 目标定位。
  - 连接器资产和配置文件的文件路径映射。
  - 生产和测试环境（PROD/TIP1）的 API 端点 URL。
  - API 版本规范以确保与 Power Platform 服务的兼容性。

## 开发指导原则

### 使用 API 定义（Swagger）时
1. **始终根据 Swagger 2.0 规范进行验证** - 架构强制执行严格的 Swagger 2.0 合规性

2. **操作的 Microsoft 扩展**：
   - `x-ms-summary`：使用此项提供用户友好的显示名称，确保使用标题格式。
   - `x-ms-visibility`：使用此项控制参数可见性，值为 `important`、`advanced` 或 `internal`。
   - `x-ms-trigger`：使用此项将操作标记为触发器，值为 `batch` 或 `single`。
   - `x-ms-trigger-hint`：使用此项提供有用的提示文本，指导用户使用触发器。
   - `x-ms-trigger-metadata`：使用此项定义触发器配置设置，包括 kind 和 mode 属性。
   - `x-ms-notification`：使用此项配置实时通知的 webhook 操作。
   - `x-ms-pageable`：使用此项通过指定 `nextLinkName` 属性启用分页功能。
   - `x-ms-safe-operation`：使用此项在 POST 操作没有副作用时将其标记为安全。
   - `x-ms-no-generic-test`：使用此项禁用特定操作的自动测试。
   - `x-ms-operation-context`：使用此项配置测试目的的操作模拟设置。

3. **参数的 Microsoft 扩展**：
   - `x-ms-dynamic-list`：使用此项启用从 API 调用填充的动态下拉列表。
   - `x-ms-dynamic-values`：使用此项配置填充参数选项的动态值源。
   - `x-ms-dynamic-tree`：使用此项为嵌套数据结构创建层次选择器。
   - `x-ms-dynamic-schema`：使用此项允许基于用户选择的运行时架构更改。
   - `x-ms-dynamic-properties`：使用此项进行适应上下文的动态属性配置。
   - `x-ms-enum-values`：使用此项提供增强的枚举定义，带有显示名称以获得更好的用户体验。
   - `x-ms-test-value`：使用此项提供测试样本值，但永远不要包含机密或敏感数据。
   - `x-ms-trigger-value`：使用此项为触发器参数指定值，包含 `value-collection` 和 `value-path` 属性。
   - `x-ms-url-encoding`：使用此项指定 URL 编码样式为 `single` 或 `double`（默认为 `single`）。
   - `x-ms-parameter-location`：使用此项为 API 提供参数位置提示（AutoRest 扩展 - Power Platform 忽略）。
   - `x-ms-localizeDefaultValue`：使用此项启用默认参数值的本地化。
   - `x-ms-skip-url-encoding`：使用此项跳过路径参数的 URL 编码（AutoRest 扩展 - Power Platform 忽略）。

4. **架构的 Microsoft 扩展**：
   - `x-ms-notification-url`：使用此项将架构属性标记为 webhook 配置的通知 URL。
   - `x-ms-media-kind`：使用此项指定内容的媒体类型，支持的值为 `image` 或 `audio`。
   - `x-ms-enum`：使用此项提供增强的枚举元数据（AutoRest 扩展 - Power Platform 忽略）。
   - 注意，上面列出的所有参数扩展也适用于架构属性，可以在架构定义中使用。

5. **根级扩展**：
   - `x-ms-capabilities`：使用此项定义连接器功能，如文件选择器和 testConnection 功能。
   - `x-ms-connector-metadata`：使用此项提供超出标准属性的额外连接器元数据。
   - `x-ms-docs`：使用此项配置连接器的文档设置和引用。
   - `x-ms-deployment-version`：使用此项跟踪部署管理的版本信息。
   - `x-ms-api-annotation`：使用此项添加 API 级注释以获得增强功能。

6. **路径级扩展**：
   - `x-ms-notification-content`：使用此项为 webhook 路径项定义通知内容架构。

7. **操作级功能**：
   - `x-ms-capabilities`（在操作级）：使用此项启用操作特定功能，如用于大文件传输的 `chunkTransfer`。

8. **安全考虑**：
   - 您应该为 API 定义适当的 `securityDefinitions` 以确保正确的身份验证。
   - **允许多个安全定义** - 您可以定义最多两种身份验证方法（例如，oauth2 + apiKey、basic + apiKey）。
   - **例外**：如果使用"None"身份验证，则不能在同一连接器中存在其他安全定义。
   - 您应该对现代 API 使用 `oauth2`，对简单令牌身份验证使用 `apiKey`，仅对内部/传统系统考虑 `basic` 身份验证。
   - 每个安全定义必须恰好是一种类型（此约束由 oneOf 验证强制执行）。

9. **参数最佳实践**：
   - 您应该使用描述性的 `description` 字段帮助用户了解每个参数的目的。
   - 您应该实现 `x-ms-summary` 以获得更好的用户体验（需要标题格式）。
   - 您必须正确标记必需参数以确保正确验证。
   - 您应该使用适当的 `format` 值（包括 Power Platform 扩展）启用正确的数据处理。
   - 您应该利用动态扩展获得更好的用户体验和数据验证。

10. **Power Platform 格式扩展**：
   - `date-no-tz`：这表示没有时区偏移信息的日期时间。
   - `html`：此格式告诉客户端在编辑时发出 HTML 编辑器，在查看内容时发出 HTML 查看器。
   - 标准格式包括：`int32`、`int64`、`float`、`double`、`byte`、`binary`、`date`、`date-time`、`password`、`email`、`uri`、`uuid`。

### 使用 API 属性时
1. **连接参数**：
   - 您应该选择适当的参数类型，如 `string`、`securestring` 或 `oauthSetting`。
   - 您应该使用正确的身份提供者配置 OAuth 设置。
   - 您应该在适当时使用 `allowedValues` 进行下拉选项。
   - 您应该在需要条件参数时实现参数依赖关系。

2. **策略模板**：
   - 您应该使用 `routerequesttoendpoint` 进行后端路由到不同的 API 端点。
   - 您应该实现 `setqueryparameter` 在查询参数上设置默认值。
   - 您应该使用 `updatenextlink` 进行分页场景以正确处理分页。
   - 您应该对需要轮询行为的触发器操作应用 `pollingtrigger`。

3. **品牌和元数据**：
   - 您必须始终指定 `iconBrandColor`，因为此属性对所有连接器都是必需的。
   - 您应该定义适当的 `capabilities` 以指定您的连接器是否支持操作或触发器。
   - 您应该设置有意义的 `publisher` 和 `stackOwner` 值以识别连接器的所有权。

### 使用设置时
1. **环境配置**：
   - 您应该对匹配验证模式的 `environment` 使用正确的 GUID 格式。
   - 您应该为目标环境设置正确的 `powerAppsUrl` 和 `flowUrl`。
   - 您应该将 API 版本与您的特定要求匹配。

2. **文件引用**：
   - 您应该与 `apiProperties.json` 和 `apiDefinition.swagger.json` 的默认值保持一致的文件命名。
   - 您应该对本地开发环境使用相对路径。
   - 您应该确保图标文件存在并在配置中正确引用。

## 架构验证规则

### 必需属性
- **API 定义**：`swagger: "2.0"`、`info`（带有 `title` 和 `version`）、`paths`
- **API 属性**：带有 `iconBrandColor` 的 `properties`
- **设置**：没有必需属性（所有都是可选的，带有默认值）

### 模式验证
- **供应商扩展**：非 Microsoft 扩展必须匹配 `^x-(?!ms-)` 模式
- **路径项**：API 路径必须以 `/` 开头
- **环境 GUID**：必须匹配 UUID 格式模式 `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
- **URL**：端点配置必须是有效的 URI
- **主机模式**：必须匹配 `^[^{}/ :\\\\]+(?::\\d+)?$`（没有空格、协议或路径）

### 类型约束
- **安全定义**：
  - `securityDefinitions` 对象中允许最多两个安全定义
  - 每个单独的安全定义必须恰好是一种类型（oneOf 验证：`basic`、`apiKey`、`oauth2`）
  - **例外**："None"身份验证不能与其他安全定义共存
- **参数类型**：限于特定枚举值（`string`、`number`、`integer`、`boolean`、`array`、`file`）
- **策略模板**：类型特定的参数要求
- **格式值**：包括 Power Platform 格式的扩展集
- **可见性值**：必须是 `important`、`advanced` 或 `internal` 之一
- **触发器类型**：必须是 `batch` 或 `single`

### 其他验证规则
- **$ref 引用**：应该只指向 `#/definitions/`、`#/parameters/` 或 `#/responses/`
- **路径参数**：必须标记为 `required: true`
- **Info 对象**：描述应该与标题不同
- **Contact 对象**：电子邮件必须是有效的电子邮件格式，URL 必须是有效的 URI
- **License 对象**：名称是必需的，如果提供了 URL，则必须是有效的 URI
- **External Docs**：URL 是必需的，必须是有效的 URI
- **Tags**：在数组中必须有唯一的名称
- **Schemes**：必须是有效的 HTTP 方案（`http`、`https`、`ws`、`wss`）
- **MIME 类型**：在 `consumes` 和 `produces` 中必须遵循有效的 MIME 类型格式

## 常见模式和示例

### API 定义示例

#### 带有 Microsoft 扩展的基本操作
```json
{
  "get": {
    "operationId": "GetItems",
    "summary": "Get items",
    "x-ms-summary": "Get Items",
    "x-ms-visibility": "important",
    "description": "Retrieves a list of items from the API",
    "parameters": [
      {
        "name": "category",
        "in": "query",
        "type": "string",
        "x-ms-summary": "Category",
        "x-ms-visibility": "important",
        "x-ms-dynamic-values": {
          "operationId": "GetCategories",
          "value-path": "id",
          "value-title": "name"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Success",
        "x-ms-summary": "Success",
        "schema": {
          "type": "object",
          "properties": {
            "items": {
              "type": "array",
              "x-ms-summary": "Items",
              "items": {
                "$ref": "#/definitions/Item"
              }
            }
          }
        }
      }
    }
  }
}
```

#### 触发器操作配置
```json
{
  "get": {
    "operationId": "WhenItemCreated",
    "x-ms-summary": "When an Item is Created",
    "x-ms-trigger": "batch",
    "x-ms-trigger-hint": "To see it work now, create an item",
    "x-ms-trigger-metadata": {
      "kind": "query",
      "mode": "polling"
    },
    "x-ms-pageable": {
      "nextLinkName": "@odata.nextLink"
    }
  }
}
```

#### 动态架构示例
```json
{
  "name": "dynamicSchema",
  "in": "body",
  "schema": {
    "x-ms-dynamic-schema": {
      "operationId": "GetSchema",
      "parameters": {
        "table": {
          "parameter": "table"
        }
      },
      "value-path": "schema"
    }
  }
}
```

#### 文件选择器功能
```json
{
  "x-ms-capabilities": {
    "file-picker": {
      "open": {
        "operationId": "OneDriveFilePickerOpen",
        "parameters": {
          "dataset": {
            "value-property": "dataset"
          }
        }
      },
      "browse": {
        "operationId": "OneDriveFilePickerBrowse",
        "parameters": {
          "dataset": {
            "value-property": "dataset"
          }
        }
      },
      "value-title": "DisplayName",
      "value-collection": "value",
      "value-folder-property": "IsFolder",
      "value-media-property": "MediaType"
    }
  }
}
```

#### 测试连接功能（注意：自定义连接器不支持）
```json
{
  "x-ms-capabilities": {
    "testConnection": {
      "operationId": "TestConnection",
      "parameters": {
        "param1": "literal-value"
      }
    }
  }
}
```

#### 模拟的操作上下文
```json
{
  "x-ms-operation-context": {
    "simulate": {
      "operationId": "SimulateOperation",
      "parameters": {
        "param1": {
          "parameter": "inputParam"
        }
      }
    }
  }
}
```

### 基本 OAuth 配置
```json
{
  "type": "oauthSetting",
  "oAuthSettings": {
    "identityProvider": "oauth2",
    "clientId": "your-client-id",
    "scopes": ["scope1", "scope2"],
    "redirectMode": "Global"
  }
}
```

#### 多个安全定义示例
```json
{
  "securityDefinitions": {
    "oauth2": {
      "type": "oauth2",
      "flow": "accessCode",
      "authorizationUrl": "https://api.example.com/oauth/authorize",
      "tokenUrl": "https://api.example.com/oauth/token",
      "scopes": {
        "read": "Read access",
        "write": "Write access"
      }
    },
    "apiKey": {
      "type": "apiKey",
      "name": "X-API-Key",
      "in": "header"
    }
  }
}
```

**注意**：最多可以共存两个安全定义，但"None"身份验证不能与其他方法组合。

### 动态参数设置
```json
{
  "x-ms-dynamic-values": {
    "operationId": "GetItems",
    "value-path": "id",
    "value-title": "name"
  }
}
```

### 路由的策略模板
```json
{
  "templateId": "routerequesttoendpoint",
  "title": "Route to backend",
  "parameters": {
    "x-ms-apimTemplate-operationName": ["GetData"],
    "x-ms-apimTemplateParameter.newPath": "/api/v2/data"
  }
}
```

## 最佳实践

1. **使用 IntelliSense**：这些架构提供丰富的自动完成和验证功能，有助于开发过程。
2. **遵循命名约定**：对操作和参数使用描述性名称以提高代码可读性。
3. **实现错误处理**：定义适当的响应架构和错误代码以正确处理失败场景。
4. **彻底测试**：在部署前验证架构，在开发过程的早期发现问题。
5. **记录扩展**：为团队理解和未来维护注释 Microsoft 特定扩展。
6. **版本管理**：在 API 信息中使用语义版本控制来跟踪更改和兼容性。
7. **安全优先**：始终实现适当的身份验证机制来保护您的 API 端点。

## 故障排除

### 常见架构违规
- **缺少必需属性**：`swagger: "2.0"`、`info.title`、`info.version`、`paths`
- **无效的模式格式**：
  - GUID 必须匹配确切格式 `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
  - URL 必须是带有正确方案的有效 URI
  - 路径必须以 `/` 开头
  - 主机不得包含协议、路径或空格
- **错误的供应商扩展命名**：对 Microsoft 扩展使用 `x-ms-*`，对其他使用 `^x-(?!ms-)`
- **不匹配的安全定义类型**：每个安全定义必须恰好是一种类型
- **无效的枚举值**：检查 `x-ms-visibility`、`x-ms-trigger`、参数类型的允许值
- **$ref 指向无效位置**：必须指向 `#/definitions/`、`#/parameters/` 或 `#/responses/`
- **路径参数未标记为必需**：所有路径参数必须有 `required: true`
- **错误上下文中的类型 'file'**：只允许在 `formData` 参数中，不在架构中

### API 定义特定问题
- **动态架构冲突**：不能将 `x-ms-dynamic-schema` 与固定架构属性一起使用
- **触发器配置错误**：`x-ms-trigger-metadata` 需要 `kind` 和 `mode`
- **分页设置**：`x-ms-pageable` 需要 `nextLinkName` 属性
- **文件选择器配置错误**：必须包括 `open` 操作和必需属性
- **功能冲突**：某些功能可能与某些参数类型冲突
- **测试值安全性**：永远不要在 `x-ms-test-value` 中包含机密或 PII
- **操作上下文设置**：`x-ms-operation-context` 需要带有 `operationId` 的 `simulate` 对象
- **通知内容架构**：路径级 `x-ms-notification-content` 必须定义正确的架构结构
- **媒体类型限制**：`x-ms-media-kind` 只支持 `image` 或 `audio` 值
- **触发器值配置**：`x-ms-trigger-value` 必须至少有一个属性（`value-collection` 或 `value-path`）

### 验证工具
- 使用 JSON Schema 验证器检查您的架构定义是否合规。
- 利用 VS Code 的内置架构验证在开发期间捕获错误。
- 在部署前使用 paconn CLI 测试：`paconn validate --api-def apiDefinition.swagger.json`
- 根据 Power Platform 连接器要求验证以确保兼容性。
- 使用 Power Platform 连接器门户在目标环境中进行验证和测试。
- 检查操作响应是否匹配预期架构以防止运行时错误。

请记住：这些架构确保您的 Power Platform 连接器格式正确，并在 Power Platform 生态系统中正常工作。