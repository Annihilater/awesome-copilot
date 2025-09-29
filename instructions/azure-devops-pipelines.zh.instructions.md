---
description: 'Azure DevOps Pipeline YAML 文件的最佳实践'
applyTo: '**/azure-pipelines.yml, **/azure-pipelines*.yml, **/*.pipeline.yml'
---

# Azure DevOps Pipeline YAML 最佳实践

## 通用指南

- 使用适当的缩进（2个空格）一致地应用 YAML 语法
- 始终为管道、阶段、作业和步骤包含有意义的名称和显示名称
- 实施适当的错误处理和条件执行
- 使用变量和参数使管道可重用且可维护
- 对服务连接和权限遵循最小权限原则
- 包含用于故障排除的全面日志记录和诊断

## 管道结构

- 使用阶段组织复杂管道以获得更好的可视化和控制
- 使用作业对相关步骤进行分组，并在可能时启用并行执行
- 在阶段和作业之间实施适当的依赖关系
- 使用模板构建可重用的管道组件
- 保持管道文件专注和模块化 - 将大型管道拆分为多个文件

## 构建最佳实践

- 使用特定的代理池版本和虚拟机镜像以确保一致性
- 缓存依赖项（npm、NuGet、Maven 等）以提高构建性能
- 实施具有有意义名称和保留策略的适当构件管理
- 使用构建变量管理版本号和构建元数据
- 包含代码质量关卡（代码检查、测试、安全扫描）
- 确保构建具有可重现性且与环境无关

## 测试集成

- 将单元测试作为构建过程的一部分运行
- 以标准格式（JUnit、VSTest 等）发布测试结果
- 包含代码覆盖率报告和质量关卡
- 在适当的阶段实施集成测试和端到端测试
- 在可用时使用测试影响分析来优化测试执行
- 在测试失败时快速失败以提供及时反馈

## 安全考虑

- 使用 Azure Key Vault 管理敏感配置和机密
- 通过变量组实施适当的机密管理
- 使用具有最少所需权限的服务连接
- 启用安全扫描（依赖项漏洞、静态分析）
- 为生产部署实施审批关卡
- 在可能时使用托管标识而非服务主体

## 部署策略

- 实施适当的环境提升流程（开发 → 预发布 → 生产）
- 使用针对适当环境的部署作业
- 在合适时实施蓝绿部署或金丝雀部署策略
- 包含回滚机制和健康检查
- 使用基础设施即代码（ARM、Bicep、Terraform）进行一致的部署
- 为每个环境实施适当的配置管理

## 变量和参数管理

- 使用变量组在管道间共享配置
- 实施运行时参数以实现灵活的管道执行
- 根据分支或环境使用条件变量
- 保护敏感变量并将其标记为机密
- 记录变量的目的和预期值
- 使用变量模板处理复杂的变量逻辑

## 性能优化

- 在适当时使用并行作业和矩阵策略
- 为依赖项和构建输出实施适当的缓存策略
- 在不需要完整历史记录时对 Git 操作使用浅克隆
- 使用多阶段构建和层缓存优化 Docker 镜像构建
- 监控管道性能并优化瓶颈
- 高效使用管道资源触发器

## 监控和可观测性

- 在整个管道中包含全面的日志记录
- 使用 Azure Monitor 和 Application Insights 进行部署跟踪
- 实施适当的失败和成功通知策略
- 包含部署健康检查和自动回滚触发器
- 使用管道分析识别改进机会
- 记录管道行为和故障排除步骤

## 模板和可重用性

- 为常见模式创建管道模板
- 使用扩展模板进行完整的管道继承
- 为可重用的任务序列实施步骤模板
- 使用变量模板处理复杂的变量逻辑
- 适当地对模板进行版本控制以确保稳定性
- 记录模板参数和使用示例

## 分支和触发器策略

- 为不同的分支类型实施适当的触发器
- 使用路径过滤器仅在相关文件更改时触发构建
- 为 main/master 分支配置适当的 CI/CD 触发器
- 使用拉取请求触发器进行代码验证
- 为维护任务实施定时触发器
- 为多仓库场景考虑资源触发器

## 示例结构

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    exclude:
      - docs/*
      - README.md

variables:
  - group: shared-variables
  - name: buildConfiguration
    value: 'Release'

stages:
  - stage: Build
    displayName: 'Build and Test'
    jobs:
      - job: Build
        displayName: 'Build Application'
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: UseDotNet@2
            displayName: 'Use .NET SDK'
            inputs:
              version: '8.x'

          - task: DotNetCoreCLI@2
            displayName: 'Restore dependencies'
            inputs:
              command: 'restore'
              projects: '**/*.csproj'

          - task: DotNetCoreCLI@2
            displayName: 'Build application'
            inputs:
              command: 'build'
              projects: '**/*.csproj'
              arguments: '--configuration $(buildConfiguration) --no-restore'

  - stage: Deploy
    displayName: 'Deploy to Staging'
    dependsOn: Build
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployToStaging
        displayName: 'Deploy to Staging Environment'
        environment: 'staging'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  displayName: 'Download drop artifact'
                  artifact: drop
                - task: AzureWebApp@1
                  displayName: 'Deploy to Azure Web App'
                  inputs:
                    azureSubscription: 'staging-service-connection'
                    appType: 'webApp'
                    appName: 'myapp-staging'
                    package: '$(Pipeline.Workspace)/drop/**/*.zip'
```

## 要避免的常见反模式

- 在 YAML 文件中硬编码敏感值
- 使用过于宽泛的触发器导致不必要的构建
- 在单个阶段中混合构建和部署逻辑
- 不实施适当的错误处理和清理
- 使用已弃用的任务版本而没有升级计划
- 创建难以维护的单体管道
- 不使用适当的命名约定以确保清晰性
- 忽略管道安全最佳实践
