---
applyTo: '**/*.ps1,**/*.psm1'
description: '基于 Microsoft 指导原则的 PowerShell cmdlet 和脚本最佳实践'
---

# PowerShell Cmdlet 开发指导原则

本指南提供特定于 PowerShell 的指导，帮助 GitHub Copilot 生成符合习惯、安全且可维护的脚本。它与 Microsoft 的 PowerShell cmdlet 开发指导原则保持一致。

## 命名约定

- **动词-名词格式：**
  - 使用已批准的 PowerShell 动词（Get-Verb）
  - 使用单数名词
  - 动词和名词都使用 PascalCase
  - 避免特殊字符和空格

- **参数名称：**
  - 使用 PascalCase
  - 选择清晰、描述性的名称
  - 使用单数形式，除非总是复数
  - 遵循 PowerShell 标准名称

- **变量名称：**
  - 公共变量使用 PascalCase
  - 私有变量使用 camelCase
  - 避免缩写
  - 使用有意义的名称

- **避免别名：**
  - 使用完整的 cmdlet 名称
  - 避免在脚本中使用别名（例如，使用 Get-ChildItem 而不是 gci）
  - 记录任何自定义别名
  - 使用完整的参数名称

### 示例

```powershell
function Get-UserProfile {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Username,

        [Parameter()]
        [ValidateSet('Basic', 'Detailed')]
        [string]$ProfileType = 'Basic'
    )

    process {
        # Logic here
    }
}
```

## 参数设计

- **标准参数：**
  - 使用常用参数名称（`Path`、`Name`、`Force`）
  - 遵循内置 cmdlet 约定
  - 为专业术语使用别名
  - 记录参数目的

- **参数名称：**
  - 使用单数形式，除非总是复数
  - 选择清晰、描述性的名称
  - 遵循 PowerShell 约定
  - 使用 PascalCase 格式

- **类型选择：**
  - 使用常见的 .NET 类型
  - 实现适当的验证
  - 对有限选项考虑 ValidateSet
  - 在可能的情况下启用 tab 补全

- **开关参数：**
  - 使用 [switch] 表示布尔标志
  - 避免 $true/$false 参数
  - 省略时默认为 $false
  - 使用清晰的操作名称

### 示例

```powershell
function Set-ResourceConfiguration {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [Parameter()]
        [ValidateSet('Dev', 'Test', 'Prod')]
        [string]$Environment = 'Dev',

        [Parameter()]
        [switch]$Force,

        [Parameter()]
        [ValidateNotNullOrEmpty()]
        [string[]]$Tags
    )

    process {
        # Logic here
    }
}
```

## 管道和输出

- **管道输入：**
  - 对直接对象输入使用 `ValueFromPipeline`
  - 对属性映射使用 `ValueFromPipelineByPropertyName`
  - 为管道处理实现 Begin/Process/End 块
  - 记录管道输入要求

- **输出对象：**
  - 返回丰富的对象，而不是格式化文本
  - 对结构化数据使用 PSCustomObject
  - 避免使用 Write-Host 进行数据输出
  - 启用下游 cmdlet 处理

- **管道流式处理：**
  - 一次输出一个对象
  - 使用 process 块进行流式处理
  - 避免收集大数组
  - 启用即时处理

- **PassThru 模式：**
  - 操作 cmdlet 默认无输出
  - 实现 `-PassThru` 开关用于对象返回
  - 使用 `-PassThru` 返回修改/创建的对象
  - 使用 verbose/warning 进行状态更新

### 示例

```powershell
function Update-ResourceStatus {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline, ValueFromPipelineByPropertyName)]
        [string]$Name,

        [Parameter(Mandatory)]
        [ValidateSet('Active', 'Inactive', 'Maintenance')]
        [string]$Status,

        [Parameter()]
        [switch]$PassThru
    )

    begin {
        Write-Verbose "Starting resource status update process"
        $timestamp = Get-Date
    }

    process {
        # Process each resource individually
        Write-Verbose "Processing resource: $Name"

        $resource = [PSCustomObject]@{
            Name = $Name
            Status = $Status
            LastUpdated = $timestamp
            UpdatedBy = $env:USERNAME
        }

        # Only output if PassThru is specified
        if ($PassThru) {
            Write-Output $resource
        }
    }

    end {
        Write-Verbose "Resource status update process completed"
    }
}
```

## 错误处理和安全性

- **ShouldProcess 实现：**
  - 使用 `[CmdletBinding(SupportsShouldProcess = $true)]`
  - 设置适当的 `ConfirmImpact` 级别
  - 对系统更改调用 `$PSCmdlet.ShouldProcess()`
  - 使用 `ShouldContinue()` 进行额外确认

- **消息流：**
  - `Write-Verbose` 用于带 `-Verbose` 的操作详情
  - `Write-Warning` 用于警告条件
  - `Write-Error` 用于非终止错误
  - `throw` 用于终止错误
  - 除用户界面文本外避免使用 `Write-Host`

- **错误处理模式：**
  - 使用 try/catch 块进行错误管理
  - 设置适当的 ErrorAction 首选项
  - 返回有意义的错误消息
  - 需要时使用 ErrorVariable
  - 包括适当的终止与非终止错误处理

- **非交互式设计：**
  - 通过参数接受输入
  - 在脚本中避免 `Read-Host`
  - 支持自动化场景
  - 记录所有必需输入

### 示例

```powershell
function Remove-UserAccount {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [ValidateNotNullOrEmpty()]
        [string]$Username,

        [Parameter()]
        [switch]$Force
    )

    begin {
        Write-Verbose "Starting user account removal process"
        $ErrorActionPreference = 'Stop'
    }

    process {
        try {
            # Validation
            if (-not (Test-UserExists -Username $Username)) {
                Write-Error "User account '$Username' not found"
                return
            }

            # Confirmation
            $shouldProcessMessage = "Remove user account '$Username'"
            if ($Force -or $PSCmdlet.ShouldProcess($Username, $shouldProcessMessage)) {
                Write-Verbose "Removing user account: $Username"

                # Main operation
                Remove-ADUser -Identity $Username -ErrorAction Stop
                Write-Warning "User account '$Username' has been removed"
            }
        }
        catch [Microsoft.ActiveDirectory.Management.ADException] {
            Write-Error "Active Directory error: $_"
            throw
        }
        catch {
            Write-Error "Unexpected error removing user account: $_"
            throw
        }
    }

    end {
        Write-Verbose "User account removal process completed"
    }
}
```

## 文档和样式

- **基于注释的帮助：** 为任何面向公众的函数或 cmdlet 包含基于注释的帮助。在函数内部，添加一个 `<# ... #>` 帮助注释，至少包含：
  - `.SYNOPSIS` 简要描述
  - `.DESCRIPTION` 详细说明
  - `.EXAMPLE` 部分，包含实际用法
  - `.PARAMETER` 描述
  - `.OUTPUTS` 返回的输出类型
  - `.NOTES` 附加信息

- **一致的格式：**
  - 遵循一致的 PowerShell 样式
  - 使用适当的缩进（推荐 4 个空格）
  - 开放大括号与语句在同一行
  - 关闭大括号在新行
  - 在管道操作符后使用换行符
  - 函数和参数名称使用 PascalCase
  - 避免不必要的空白

- **管道支持：**
  - 为管道函数实现 Begin/Process/End 块
  - 在适当的地方使用 ValueFromPipeline
  - 支持按属性名称的管道输入
  - 返回适当的对象，而不是格式化文本

- **避免别名：** 使用完整的 cmdlet 名称和参数
  - 避免在脚本中使用别名（例如，使用 Get-ChildItem 而不是 gci）；别名在交互式 shell 使用中是可以接受的。
  - 使用 `Where-Object` 而不是 `?` 或 `where`
  - 使用 `ForEach-Object` 而不是 `%`
  - 使用 `Get-ChildItem` 而不是 `ls` 或 `dir`

## 完整示例：端到端 Cmdlet 模式

```powershell
function New-Resource {
    [CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
    param(
        [Parameter(Mandatory = $true,
                   ValueFromPipeline = $true,
                   ValueFromPipelineByPropertyName = $true)]
        [ValidateNotNullOrEmpty()]
        [string]$Name,

        [Parameter()]
        [ValidateSet('Development', 'Production')]
        [string]$Environment = 'Development'
    )

    begin {
        Write-Verbose "Starting resource creation process"
    }

    process {
        try {
            if ($PSCmdlet.ShouldProcess($Name, "Create new resource")) {
                # Resource creation logic here
                Write-Output ([PSCustomObject]@{
                    Name = $Name
                    Environment = $Environment
                    Created = Get-Date
                })
            }
        }
        catch {
            Write-Error "Failed to create resource: $_"
        }
    }

    end {
        Write-Verbose "Completed resource creation process"
    }
}
```