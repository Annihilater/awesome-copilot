---
applyTo: '**/*.Tests.ps1'
description: '基于 Pester v5 约定的 PowerShell Pester 测试最佳实践'
---

# PowerShell Pester v5 测试指导原则

本指南提供使用 PowerShell Pester v5 模块创建自动化测试的 PowerShell 特定指导。有关一般 PowerShell 脚本最佳实践，请遵循 [powershell.instructions.md](./powershell.instructions.md) 中的 PowerShell cmdlet 开发指导原则。

## 文件命名和结构

- **文件约定：** 使用 `*.Tests.ps1` 命名模式
- **放置位置：** 将测试文件放在被测试代码旁边或专用测试目录中
- **导入模式：** 使用 `BeforeAll { . $PSScriptRoot/FunctionName.ps1 }` 导入被测试函数
- **无直接代码：** 将所有代码放在 Pester 块内（`BeforeAll`、`Describe`、`Context`、`It` 等）

## 测试结构层次

```powershell
BeforeAll { # Import tested functions }
Describe 'FunctionName' {
    Context 'When condition' {
        BeforeAll { # Setup for context }
        It 'Should behavior' { # Individual test }
        AfterAll { # Cleanup for context }
    }
}
```

## 核心关键字

- **`Describe`**：顶级分组，通常以被测试函数命名
- **`Context`**：Describe 内的子分组，用于特定场景
- **`It`**：个别测试用例，使用描述性名称
- **`Should`**：用于测试验证的断言关键字
- **`BeforeAll/AfterAll`**：每个块一次性设置/清理
- **`BeforeEach/AfterEach`**：每次测试前后的设置/清理

## 设置和清理

- **`BeforeAll`**：在包含块开始时运行一次，用于昂贵操作
- **`BeforeEach`**：在块中每个 `It` 之前运行，用于测试特定设置
- **`AfterEach`**：在每个 `It` 之后运行，即使测试失败也保证运行
- **`AfterAll`**：在块结束时运行一次，用于清理
- **变量作用域**：`BeforeAll` 变量可用于子块（只读），`BeforeEach/It/AfterEach` 共享相同作用域

## 断言（Should）

- **基本比较**：`-Be`、`-BeExactly`、`-Not -Be`
- **集合**：`-Contain`、`-BeIn`、`-HaveCount`
- **数值**：`-BeGreaterThan`、`-BeLessThan`、`-BeGreaterOrEqual`
- **字符串**：`-Match`、`-Like`、`-BeNullOrEmpty`
- **类型**：`-BeOfType`、`-BeTrue`、`-BeFalse`
- **文件**：`-Exist`、`-FileContentMatch`
- **异常**：`-Throw`、`-Not -Throw`

## 模拟

- **`Mock CommandName { ScriptBlock }`**：替换命令行为
- **`-ParameterFilter`**：仅在参数匹配条件时模拟
- **`-Verifiable`**：将模拟标记为需要验证
- **`Should -Invoke`**：验证模拟被调用特定次数
- **`Should -InvokeVerifiable`**：验证所有可验证模拟都被调用
- **作用域**：模拟默认为包含块作用域

```powershell
Mock Get-Service { @{ Status = 'Running' } } -ParameterFilter { $Name -eq 'TestService' }
Should -Invoke Get-Service -Exactly 1 -ParameterFilter { $Name -eq 'TestService' }
```

## 测试用例（数据驱动测试）

使用 `-TestCases` 或 `-ForEach` 进行参数化测试：

```powershell
It 'Should return <Expected> for <Input>' -TestCases @(
    @{ Input = 'value1'; Expected = 'result1' }
    @{ Input = 'value2'; Expected = 'result2' }
) {
    Get-Function $Input | Should -Be $Expected
}
```

## 数据驱动测试

- **`-ForEach`**：在 `Describe`、`Context` 和 `It` 上可用，用于从数据生成多个测试
- **`-TestCases`**：在 `It` 块上 `-ForEach` 的别名（向后兼容性）
- **哈希表数据**：每个项目定义测试中可用的变量（例如，`@{ Name = 'value'; Expected = 'result' }`）
- **数组数据**：使用 `$_` 变量表示当前项目
- **模板**：在测试名称中使用 `<variablename>` 进行动态扩展

```powershell
# 哈希表方法
It 'Returns <Expected> for <Name>' -ForEach @(
    @{ Name = 'test1'; Expected = 'result1' }
    @{ Name = 'test2'; Expected = 'result2' }
) { Get-Function $Name | Should -Be $Expected }

# 数组方法
It 'Contains <_>' -ForEach 'item1', 'item2' { Get-Collection | Should -Contain $_ }
```

## 标签

- **可用于**：`Describe`、`Context` 和 `It` 块
- **过滤**：使用 `-TagFilter` 和 `-ExcludeTagFilter` 与 `Invoke-Pester` 一起使用
- **通配符**：标签支持 `-like` 通配符进行灵活过滤

```powershell
Describe 'Function' -Tag 'Unit' {
    It 'Should work' -Tag 'Fast', 'Stable' { }
    It 'Should be slow' -Tag 'Slow', 'Integration' { }
}

# Run only fast unit tests
Invoke-Pester -TagFilter 'Unit' -ExcludeTagFilter 'Slow'
```

## 跳过

- **`-Skip`**：在 `Describe`、`Context` 和 `It` 上可用，用于跳过测试
- **条件性**：使用 `-Skip:$condition` 进行动态跳过
- **运行时跳过**：在测试执行期间使用 `Set-ItResult -Skipped`（设置/清理仍会运行）

```powershell
It 'Should work on Windows' -Skip:(-not $IsWindows) { }
Context 'Integration tests' -Skip { }
```

## 错误处理

- **失败时继续**：使用 `Should.ErrorAction = 'Continue'` 收集多个失败
- **关键时停止**：对前置条件使用 `-ErrorAction Stop`
- **测试异常**：使用 `{ Code } | Should -Throw` 进行异常测试

## 最佳实践

- **描述性名称**：使用清晰的测试描述来解释行为
- **AAA 模式**：安排（设置）、行动（执行）、断言（验证）
- **隔离测试**：每个测试都应该是独立的
- **避免别名**：使用完整的 cmdlet 名称（`Where-Object` 而不是 `?`）
- **单一职责**：尽可能每个测试一个断言
- **测试文件组织**：在 Context 块中分组相关测试。Context 块可以嵌套。

## 示例测试模式

```powershell
BeforeAll {
    . $PSScriptRoot/Get-UserInfo.ps1
}

Describe 'Get-UserInfo' {
    Context 'When user exists' {
        BeforeAll {
            Mock Get-ADUser { @{ Name = 'TestUser'; Enabled = $true } }
        }

        It 'Should return user object' {
            $result = Get-UserInfo -Username 'TestUser'
            $result | Should -Not -BeNullOrEmpty
            $result.Name | Should -Be 'TestUser'
        }

        It 'Should call Get-ADUser once' {
            Get-UserInfo -Username 'TestUser'
            Should -Invoke Get-ADUser -Exactly 1
        }
    }

    Context 'When user does not exist' {
        BeforeAll {
            Mock Get-ADUser { throw "User not found" }
        }

        It 'Should throw exception' {
            { Get-UserInfo -Username 'NonExistent' } | Should -Throw "*not found*"
        }
    }
}
```

## 配置

配置在测试文件**外部**定义，当调用 `Invoke-Pester` 时控制执行行为。

```powershell
# Create configuration (Pester 5.2+)
$config = New-PesterConfiguration
$config.Run.Path = './Tests'
$config.Output.Verbosity = 'Detailed'
$config.TestResult.Enabled = $true
$config.TestResult.OutputFormat = 'NUnitXml'
$config.Should.ErrorAction = 'Continue'
Invoke-Pester -Configuration $config
```

**关键部分**：Run（Path、Exit）、Filter（Tag、ExcludeTag）、Output（Verbosity）、TestResult（Enabled、OutputFormat）、CodeCoverage（Enabled、Path）、Should（ErrorAction）、Debug