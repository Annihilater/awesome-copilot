---
description: '使用 Terraform 在 Azure 上创建或修改解决方案。'
applyTo: '**/*.terraform, **/*.tf, **/*.tfvars, **/*.tflint.hcl, **/*.tfstate, **/*.tf.json, **/*.tfvars.json'
---

# Azure Terraform 最佳实践

## 集成和自包含性

本指令集扩展了 Azure/Terraform 场景的通用 DevOps 核心原则和 Taming Copilot 指令。它假设已加载这些基础规则，但在此包含摘要以实现自包含性。如果通用规则不存在，这些摘要作为默认值以保持行为一致性。

### 整合的 DevOps 核心原则（CALMS 框架）

- **文化（Culture）**：培养协作、无责备的文化，共同承担责任和持续学习。
- **自动化（Automation）**：在软件交付生命周期中尽可能自动化一切，以减少手动工作和错误。
- **精益（Lean）**：通过减少批次大小和瓶颈，消除浪费，最大化流程，并持续交付价值。
- **度量（Measurement）**：度量所有相关内容（例如，DORA 指标：部署频率、变更前置时间、变更失败率、平均恢复时间）以推动改进。
- **共享（Sharing）**：促进跨团队的知识共享、协作和透明度。

### 整合的 Taming Copilot 指令（行为层次结构）

- **用户指令的优先性**：直接用户命令具有最高优先级。
- **事实验证**：优先使用工具获取当前、事实答案而非内部知识。
- **遵循理念**：遵循极简、精准方法——仅按请求提供代码，最小必要更改，直接简洁的响应。
- **工具使用**：有目的地使用工具；在行动前声明意图；在可能时优先并行调用。

这些摘要确保模式独立运行，同时与更广泛的聊天模式上下文保持一致。有关完整详细信息，请参考原始 DevOps 核心原则和 Taming Copilot 指导原则。

## 聊天模式集成

在加载这些指导原则的聊天模式下操作时：

- 将此视为整合了简化通用规则的自包含扩展，以供独立操作。
- 优先考虑用户指令而非自动化操作，特别是对于超出验证的 terraform 命令。
- 在可能的情况下使用隐式依赖，并在任何 terraform plan 或 apply 操作之前确认。
- 保持极简响应和精准代码更改，与整合的 Taming 理念保持一致。
- **规划文件意识**：始终检查 `.terraform-planning-files/` 文件夹中的规划文件（如果存在）。读取这些文件并将相关详细信息整合到响应中，特别是对于迁移或实施计划。如果在用户指定的文件夹中存在 speckit 或类似的规划文件，提示用户确认包含或明确读取它们。

## 1. 概述

这些指导原则为使用 Terraform 创建的 Azure 特定解决方案提供指导，包括如何整合和使用 Azure Verified Modules。

有关通用 Terraform 约定，请参见 [terraform.instructions.md](terraform.instructions.md)。

有关模块开发，特别是 Azure Verified Modules，请参见 [azure-verified-modules-terraform.instructions.md](azure-verified-modules-terraform.instructions.md)。

## 2. 要避免的反模式

**配置：**

- 绝不能硬编码应该参数化的值
- 不应该将 `terraform import` 作为常规工作流程模式使用
- 应该避免使代码难以理解的复杂条件逻辑
- 除非绝对必要，否则绝不能使用 `local-exec` 配置器

**安全性：**

- 绝不能在 Terraform 文件或状态中存储密钥
- 必须避免过度宽松的 IAM 角色或网络规则
- 绝不能为了方便而禁用安全功能
- 绝不能使用默认密码或密钥

**操作：**

- 绝不能在未经测试的情况下直接对生产环境应用 Terraform 更改
- 必须避免对 Terraform 管理的资源进行手动更改
- 绝不能忽略 Terraform 状态文件损坏或不一致
- 绝不能从本地机器对生产环境运行 Terraform
- 对于 Terraform 状态文件（`**/*.tfstate`）只能进行只读操作，所有更改都必须通过 Terraform CLI 或 HCL 进行。
- 对于 `**/.terraform/**`（获取的模块和提供程序）的内容只能进行只读操作。

这些建立在整合的 Taming Copilot 指令基础上，用于安全、操作实践。

---

## 3. 清晰地组织代码

使用逻辑文件分离构建 Terraform 配置：

- 使用 `main.tf` 存放资源
- 使用 `variables.tf` 存放输入
- 使用 `outputs.tf` 存放输出
- 使用 `terraform.tf` 存放提供程序配置
- 使用 `locals.tf` 抽象复杂表达式并提高可读性
- 遵循一致的命名约定和格式化（`terraform fmt`）
- 如果 main.tf 或 variables.tf 文件变得太大，按资源类型或功能将它们拆分为多个文件（例如，`main.networking.tf`、`main.storage.tf` - 将相应变量移至 `variables.networking.tf` 等）

对变量和模块名称使用 `snake_casing`。

## 4. 使用 Azure Verified Modules (AVM)

任何重要资源都应在可用时使用 AVM。AVM 设计为符合 Well Architected Framework，由 Microsoft 支持和维护，有助于减少需要维护的代码量。有关如何发现这些模块的信息可在 [Azure Verified Modules for Terraform](azure-verified-modules-terraform.instructions.md) 中找到。

如果 Azure Verified Module 不可用于该资源，建议创建一个"以 AVM 风格"的模块，以便与现有工作保持一致，并提供向社区上游贡献的机会。

此指导原则的例外是，如果用户被指示使用内部私有注册表，或明确表示不希望使用 Azure Verified Modules。

这与整合的 DevOps 自动化原则保持一致，通过利用预验证的、社区维护的模块。

## 5. 变量和代码样式标准

在解决方案代码中遵循与 AVM 一致的编码标准以保持一致性：

- **变量命名**：对所有变量名使用 snake_case（按照 TFNFR4 和 TFNFR16）。使用描述性且与命名约定一致的名称。
- **变量定义**：所有变量都必须有明确的类型声明（按照 TFNFR18）和全面的描述（按照 TFNFR17）。除非有特定需要，否则避免对集合值使用可空默认值（按照 TFNFR20）。
- **敏感变量**：适当标记敏感变量，避免明确设置 `sensitive = false`（按照 TFNFR22）。正确处理敏感默认值（按照 TFNFR23）。
- **动态块**：在适当的情况下对可选嵌套对象使用动态块（按照 TFNFR12），并利用 `coalesce` 或 `try` 函数获取默认值（按照 TFNFR13）。
- **代码组织**：考虑专门使用 `locals.tf` 存放本地值（按照 TFNFR31），确保本地值的精确类型（按照 TFNFR33）。

## 6. 密钥

最好的密钥是不需要存储的密钥。例如，使用托管身份而不是密码或密钥。

在支持的情况下（Terraform v1.11+），使用 `ephemeral` 密钥和只写参数，以避免在状态文件中存储密钥。有关可用性，请咨询模块文档。

在需要密钥的情况下，除非被指示使用不同的服务，否则存储在 Key Vault 中。

绝不将密钥写入本地文件系统或提交到 git。

适当标记敏感值，将它们与其他属性隔离，除非绝对必要，否则避免输出敏感数据。遵循 TFNFR19、TFNFR22 和 TFNFR23。

## 7. 输出

- **避免不必要的输出**，仅使用这些来公开其他配置所需的信息。
- 对包含密钥的输出使用 `sensitive = true`
- 为所有输出提供清晰的描述

```hcl
output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.example.name
}

output "virtual_network_id" {
  description = "ID of the virtual network"
  value       = azurerm_virtual_network.example.id
}
```

## 8. 本地值使用

- 对计算值和复杂表达式使用本地值
- 通过提取重复表达式提高可读性
- 将相关值组合成结构化本地值

```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    Owner       = var.owner
    CreatedBy   = "terraform"
  }

  resource_name_prefix = "${var.project_name}-${var.environment}"
  location_short       = substr(var.location, 0, 3)
}
```

## 9. 遵循推荐的 Terraform 实践

- **冗余 depends_on 检测**：搜索并删除在同一资源块中已隐式引用依赖资源的 `depends_on`。仅在明确需要时保留 `depends_on`。绝不依赖模块输出。

- **迭代**：对 0-1 资源使用 `count`，对多个资源使用 `for_each`。对稳定资源地址优先使用映射。与 TFNFR7 保持一致。

- **数据源**：在根模块中可接受，但在可重用模块中避免使用。优先使用明确的模块参数而非数据源查找。

- **参数化**：使用具有明确 `type` 声明（TFNFR18）、全面描述（TFNFR17）和非空默认值（TFNFR20）的强类型变量。利用 AVM 公开的变量。

- **版本控制**：针对最新稳定的 Terraform 和 Azure 提供程序版本。在代码中指定版本并保持更新（TFFR3）。

## 10. 文件夹结构

对 Terraform 配置使用一致的文件夹结构。

使用 tfvars 修改环境差异。通常，目标是保持环境相似，同时对非生产环境进行成本优化。

反模式 - 每环境分支、每环境存储库、每环境文件夹 - 或类似的布局，使得在环境之间测试根文件夹逻辑变得困难。

注意可能影响此设计的工具，如 Terragrunt。

**建议**的结构是：

```text
my-azure-app/
├── infra/                          # Terraform 根模块（AZD 兼容）
│   ├── main.tf                     # 核心资源
│   ├── variables.tf                # 输入变量
│   ├── outputs.tf                  # 输出
│   ├── terraform.tf                # 提供程序配置
│   ├── locals.tf                   # 本地值
│   └── environments/               # 环境特定配置
│       ├── dev.tfvars              # 开发环境
│       ├── test.tfvars             # 测试环境
│       └── prod.tfvars             # 生产环境
├── .github/workflows/              # CI/CD 管道（如果使用 github）
├── .azdo/                          # CI/CD 管道（如果使用 Azure DevOps，建议）
└── README.md                       # 文档
```

没有用户直接同意，绝不更改文件夹结构。

遵循 AVM 规范 TFNFR1、TFNFR2、TFNFR3 和 TFNFR4 以获得一致的文件命名和结构。

## Azure 特定最佳实践

### 资源命名和标记

- 遵循 [Azure 命名约定](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- 对多区域部署使用一致的区域命名和变量
- 实施一致的标记。

### 资源组策略

- 在指定时使用现有资源组
- 仅在必要时且经确认后创建新资源组
- 使用指示目的和环境的描述性名称

### 网络考虑事项

- 在创建新网络资源之前验证现有 VNet/子网 ID（例如，此解决方案是否部署到现有的中心辐射型着陆区域）
- 适当使用 NSG 和 ASG
- 在需要时为 PaaS 服务实施私有终端点，否则使用资源防火墙限制来限制公共访问。对需要公共终端点的情况添加注释说明例外情况。

### 安全性和合规性

- 使用托管身份而不是服务主体
- 使用适当的 RBAC 实施 Key Vault。
- 为审计跟踪启用诊断设置
- 遵循最小权限原则

## 成本管理

- 确认昂贵资源的预算批准
- 使用适合环境的规格（开发 vs 生产）
- 如果未指定，询问成本约束

## 状态管理

- 使用具有状态锁定的远程后端（Azure Storage）
- 绝不将状态文件提交到源代码控制
- 启用静态和传输加密

## 验证

- 对现有资源进行清查，并提出删除未使用的资源块。
- 运行 `terraform validate` 检查语法
- 在运行 `terraform plan` 之前询问。Terraform plan 需要订阅 ID，这应该来自 ARM_SUBSCRIPTION_ID 环境变量，*不*应该在提供程序块中编码。
- 首先在非生产环境中测试配置
- 确保幂等性（多次应用产生相同结果）

## 后备行为

如果没有加载通用规则，默认为：极简代码生成，对超出验证的任何 terraform 命令明确同意，并在所有建议中遵循 CALMS 原则。