---
description: '基于 Microsoft Power Apps YAML 架构 v3.0 的 Power Apps Canvas 应用 YAML 结构综合指南。涵盖 Power Fx 公式、控件结构、数据类型和源代码管理最佳实践。'
applyTo: '**/*.{yaml,yml,md,pa.yaml}'
---

# Power Apps Canvas 应用 YAML 结构指南

## 概述
本文档基于官方 Microsoft Power Apps YAML 架构（v3.0）和 Power Fx 文档，提供使用 Power Apps canvas 应用的 YAML 代码的全面指导。

**官方架构来源**: https://raw.githubusercontent.com/microsoft/PowerApps-Tooling/refs/heads/master/schemas/pa-yaml/v3.0/pa.schema.yaml

## Power Fx 设计原则
Power Fx 是在整个 Power Apps canvas 应用中使用的公式语言。它遵循以下核心原则：

### 设计原则
- **简单性**: 使用来自 Excel 公式的熟悉概念
- **Excel 一致性**: 与 Excel 公式语法和行为保持一致
- **声明式**: 描述您想要什么，而不是如何实现它
- **函数式**: 避免副作用；大多数函数是纯函数
- **组合式**: 通过组合更简单的函数构建复杂逻辑
- **强类型**: 类型系统确保数据完整性
- **集成化**: 在 Power Platform 中无缝工作

### 语言哲学
Power Fx 提倡：
- 通过类似 Excel 的公式进行低代码开发
- 当依赖关系发生变化时自动重新计算
- 具有编译时检查的类型安全
- 函数式编程模式

## 根结构
每个 Power Apps YAML 文件遵循此顶级结构：

```yaml
App:
  Properties:
    # 应用级属性和公式
    StartScreen: =Screen1

Screens:
  # 屏幕定义

ComponentDefinitions:
  # 自定义组件定义

DataSources:
  # 数据源配置

EditorState:
  # 编辑器元数据（屏幕顺序等）
```

## 1. App 部分
`App` 部分定义应用程序级属性和配置。

```yaml
App:
  Properties:
    StartScreen: =Screen1
    BackEnabled: =false
    # 其他应用属性与 Power Fx 公式
```

### 要点：
- 包含应用程序范围的设置
- 属性使用 Power Fx 公式（以 `=` 为前缀）
- 通常指定 `StartScreen` 属性

## 2. Screens 部分
将应用程序中的所有屏幕定义为无序映射。

```yaml
Screens:
  Screen1:
    Properties:
      # 屏幕属性
    Children:
      - Label1:
          Control: Label
          Properties:
            Text: ="Hello World"
            X: =10
            Y: =10
      - Button1:
          Control: Button
          Properties:
            Text: ="Click Me"
            X: =10
            Y: =100
```

### 屏幕结构：
- **Properties**: 屏幕级属性和公式
- **Children**: 屏幕上的控件数组（按 z-index 排序）

### 控件定义格式：
```yaml
ControlName:
  Control: ControlType      # 必需: 控件类型标识符
  Properties:
    PropertyName: =PowerFxFormula
  # 可选属性:
  Group: GroupName          # 用于在 Studio 中组织控件
  Variant: VariantName      # 控件变体（影响默认属性）
  MetadataKey: Key          # 控件的元数据标识符
  Layout: LayoutName        # 布局配置
  IsLocked: true/false      # 控件在编辑器中是否锁定
  Children: []              # 用于容器控件（按 z-index 排序）
```

### 控件版本控制：
您可以使用 `@` 操作符指定控件版本：
```yaml
MyButton:
  Control: Button@2.1.0     # 特定版本
  Properties:
    Text: ="Click Me"

MyLabel:
  Control: Label            # 默认使用最新版本
  Properties:
    Text: ="Hello World"
```

## 3. 控件类型

### 标准控件
常见的第一方控件包括：
- **基础控件**: `Label`, `Button`, `TextInput`, `HTMLText`
- **输入控件**: `Slider`, `Toggle`, `Checkbox`, `Radio`, `Dropdown`, `Combobox`, `DatePicker`, `ListBox`
- **显示控件**: `Image`, `Icon`, `Video`, `Audio`, `PDF viewer`, `Barcode scanner`
- **布局控件**: `Container`, `Rectangle`, `Circle`, `Gallery`, `DataTable`, `Form`
- **图表控件**: `Column chart`, `Line chart`, `Pie chart`
- **高级控件**: `Timer`, `Camera`, `Microphone`, `Add picture`, `Import`, `Export`

### 容器和布局控件
容器控件及其子控件的特别注意事项：
```yaml
MyContainer:
  Control: Container
  Properties:
    Width: =300
    Height: =200
    Fill: =RGBA(240, 240, 240, 1)
  Children:
    - Label1:
        Control: Label
        Properties:
          Text: ="Inside Container"
          X: =10         # 相对于容器
          Y: =10         # 相对于容器
    - Button1:
        Control: Button
        Properties:
          Text: ="Container Button"
          X: =10
          Y: =50
```

### 自定义组件
```yaml
MyCustomControl:
  Control: Component
  ComponentName: MyComponent
  Properties:
    X: =10
    Y: =10
    # 自定义组件属性
```

### 代码组件（PCF）
```yaml
MyPCFControl:
  Control: CodeComponent
  ComponentName: publisherprefix_namespace.classname
  Properties:
    X: =10
    Y: =10
```

## 4. 组件定义
定义可重用的自定义组件：

```yaml
ComponentDefinitions:
  MyComponent:
    DefinitionType: CanvasComponent
    Description: "一个可重用的组件"
    AllowCustomization: true
    AccessAppScope: false
    CustomProperties:
      InputText:
        PropertyKind: Input
        DataType: Text
        Description: "输入文本属性"
        Default: ="Default Value"
      OutputValue:
        PropertyKind: Output
        DataType: Number
        Description: "输出数字值"
    Properties:
      Fill: =RGBA(255, 255, 255, 1)
      Height: =100
      Width: =200
    Children:
      - Label1:
          Control: Label
          Properties:
            Text: =Parent.InputText
```

### 自定义属性类型：
- **Input**: 从父级接收值
- **Output**: 向父级发送值
- **InputFunction**: 由父级调用的函数
- **OutputFunction**: 在组件中定义的函数
- **Event**: 向父级触发事件
- **Action**: 具有副作用的函数

### 数据类型：
- `Text`, `Number`, `Boolean`
- `DateAndTime`, `Color`, `Currency`
- `Record`, `Table`, `Image`
- `VideoOrAudio`, `Screen`

## 5. 数据源
配置数据连接：

```yaml
DataSources:
  MyTable:
    Type: Table
    Parameters:
      TableLogicalName: account

  MyActions:
    Type: Actions
    ConnectorId: shared_office365users
    Parameters:
      # 其他连接器参数
```

### 数据源类型：
- **Table**: Dataverse 表或其他表格数据
- **Actions**: 连接器操作和流

## 6. 编辑器状态
维护编辑器组织：

```yaml
EditorState:
  ScreensOrder:
    - Screen1
    - Screen2
    - Screen3
  ComponentDefinitionsOrder:
    - MyComponent
    - AnotherComponent
```

## Power Fx 公式指导原则

### 公式语法：
- 所有公式必须以 `=` 开头
- 使用 Power Fx 语法进行表达式
- Null 值可以表示为 `null`（不带引号）
- 示例：
  ```yaml
  Text: ="Hello World"
  X: =10
  Visible: =Toggle1.Value
  OnSelect: =Navigate(Screen2, ScreenTransition.Fade)
  OptionalProperty: null    # 表示无值
  ```

### 常见公式模式：
```yaml
# 静态值
Text: ="Static Text"
X: =50
Visible: =true

# 控件引用
Text: =TextInput1.Text
Visible: =Toggle1.Value

# 父级引用（用于容器/画廊中的控件）
Width: =Parent.Width - 20
Height: =Parent.TemplateHeight    # 在画廊模板中

# 函数
OnSelect: =Navigate(NextScreen, ScreenTransition.Slide)
Text: =Concatenate("Hello ", User().FullName)

# 条件逻辑
Visible: =If(Toggle1.Value, true, false)
Fill: =If(Button1.Pressed, RGBA(255,0,0,1), RGBA(0,255,0,1))

# 数据操作
Items: =Filter(DataSource, Status = "Active")
Text: =LookUp(Users, ID = 123).Name
```

### Z-Index 和控件排序：
- `Children` 数组中的控件按 z-index 排序
- 数组中的第一个控件 = 底层（z-index 1）
- 数组中的最后一个控件 = 顶层（最高 z-index）
- 所有控件使用从 1 开始的升序

## 命名约定

### 实体名称：
- 屏幕名称：描述性且唯一
- 控件名称：类型名称 + 数字（例如，`Button1`, `Label2`）
- 组件名称：PascalCase

### 属性名称：
- 标准属性：使用架构中的确切大小写
- 自定义属性：建议使用 PascalCase

## 最佳实践

### 1. 结构组织：
- 保持屏幕逻辑组织
- 使用 `Group` 属性对相关控件进行分组
- 为所有实体使用有意义的名称

### 2. 公式编写：
- 保持公式可读且格式良好
- 在可能的情况下在复杂公式中使用注释
- 避免过于复杂的嵌套表达式

### 3. 组件设计：
- 设计可重用的组件
- 为自定义属性提供清晰的描述
- 使用适当的属性类型（Input/Output）

### 4. 数据源管理：
- 为数据源使用描述性名称
- 记录连接要求
- 保持数据源配置最小化

## 验证规则

### 必需属性：
- 所有控件必须有 `Control` 属性
- 组件定义必须有 `DefinitionType`
- 数据源必须有 `Type`

### 命名模式：
- 实体名称：最少 1 个字符，字母数字
- 控件类型 ID：遵循模式 `^([A-Z][a-zA-Z0-9]*/)?[A-Z][a-zA-Z0-9]*(@\d+\.\d+\.\d+)?$`
- 代码组件名称：遵循模式 `^([a-z][a-z0-9]{1,7})_([a-zA-Z0-9]\.)+[a-zA-Z0-9]+$`

## 常见问题和解决方案

### 1. 无效的控件类型：
- 确保控件类型拼写正确
- 检查大小写是否正确
- 验证控件类型是否在架构中受支持

### 2. 公式错误：
- 所有公式必须以 `=` 开头
- 使用正确的 Power Fx 语法
- 检查正确的属性引用

### 3. 结构验证：
- 保持正确的 YAML 缩进
- 确保必需属性存在
- 严格遵循架构结构

### 4. 自定义组件问题：
- 验证 `ComponentName` 与定义匹配
- 确保自定义属性定义正确
- 检查属性类型是否合适
- 如果使用外部组件，验证组件库引用

### 5. 性能考虑：
- 避免在 YAML 中使用深度嵌套的公式
- 使用高效的数据源查询
- 为大型数据集考虑可委托的公式
- 最小化频繁更新属性中的复杂计算

## 高级主题

### 1. 组件库集成：
```yaml
ComponentDefinitions:
  MyLibraryComponent:
    DefinitionType: CanvasComponent
    AllowCustomization: true
    ComponentLibraryUniqueName: "pub_MyComponentLibrary"
    # 组件定义详情
```

### 2. 响应式设计考虑：
- 使用 `Parent.Width` 和 `Parent.Height` 进行响应式大小调整
- 为复杂 UI 考虑基于容器的布局
- 使用公式进行动态定位和大小调整

### 3. 画廊模板：
```yaml
MyGallery:
  Control: Gallery
  Properties:
    Items: =DataSource
    TemplateSize: =100
  Children:
    - GalleryTemplate:  # 每个画廊项的模板
        Children:
          - TitleLabel:
              Control: Label
              Properties:
                Text: =ThisItem.Title
                Width: =Parent.TemplateWidth - 20
```

### 4. 表单控件和数据卡：
```yaml
MyForm:
  Control: Form
  Properties:
    DataSource: =DataSource
    DefaultMode: =FormMode.New
  Children:
    - DataCard1:
        Control: DataCard
        Properties:
          DataField: ="Title"
        Children:
          - DataCardValue1:
              Control: TextInput
              Properties:
                Default: =Parent.Default
```

### 5. 公式中的错误处理：
```yaml
Properties:
  Text: =IfError(LookUp(DataSource, ID = 123).Name, "Not Found")
  Visible: =!IsError(DataSource)
  OnSelect: =IfError(
    Navigate(DetailScreen, ScreenTransition.Cover),
    Notify("Navigation failed", NotificationType.Error)
  )
```

## Power Apps 源代码管理

### 访问源代码文件：
Power Apps YAML 文件可以通过几种方法获取：

1. **Power Platform CLI**:
   ```powershell
   # 列出环境中的 canvas 应用
   pac canvas list

   # 下载并提取 YAML 文件
   pac canvas download --name "MyApp" --extract-to-directory "C:\path\to\destination"
   ```

2. **从 .msapp 手动提取**:
   ```powershell
   # 使用 PowerShell 提取 .msapp 文件
   Expand-Archive -Path "C:\path\to\yourFile.msapp" -DestinationPath "C:\path\to\destination"
   ```

3. **Dataverse Git 集成**: 无需 .msapp 文件直接访问源文件

### .msapp 中的文件结构：
- `\src\App.pa.yaml` - 表示主要的应用配置
- `\src\[ScreenName].pa.yaml` - 每个屏幕一个文件
- `\src\Component\[ComponentName].pa.yaml` - 组件定义

**重要说明**：
- 只有 `\src` 文件夹中的文件用于源代码控制
- .pa.yaml 文件是**只读的**，仅供查看目的
- 不支持外部编辑、合并和冲突解决
- .msapp 中的 JSON 文件对于源代码控制不稳定

### 架构版本演进：
1. **实验格式**（*.fx.yaml）：不再开发
2. **早期预览**：临时格式，不再使用
3. **源代码**（*.pa.yaml）：当前活跃格式，支持版本控制

## Power Fx 公式参考

### 公式类别：

#### **函数**：接受参数，执行操作，返回值
```yaml
Properties:
  Text: =Concatenate("Hello ", User().FullName)
  X: =Sum(10, 20, 30)
  Items: =Filter(DataSource, Status = "Active")
```

#### **信号**：返回环境信息（无参数）
```yaml
Properties:
  Text: =Location.Latitude & ", " & Location.Longitude
  Visible: =Connection.Connected
  Color: =If(Acceleration.X > 5, Color.Red, Color.Blue)
```

#### **枚举**：预定义常量值
```yaml
Properties:
  Fill: =Color.Blue
  Transition: =ScreenTransition.Fade
  Align: =Align.Center
```

#### **命名操作符**：访问容器信息
```yaml
Properties:
  Text: =ThisItem.Title        # 在画廊中
  Width: =Parent.Width - 20    # 在容器中
  Height: =Self.Height / 2     # 自引用
```

### YAML 的基本 Power Fx 函数：

#### **导航和应用控制**：
```yaml
OnSelect: =Navigate(NextScreen, ScreenTransition.Cover)
OnSelect: =Back()
OnSelect: =Exit()
OnSelect: =Launch("https://example.com")
```

#### **数据操作**：
```yaml
Items: =Filter(DataSource, Category = "Active")
Text: =LookUp(Users, ID = 123).Name
OnSelect: =Patch(DataSource, ThisItem, {Status: "Complete"})
OnSelect: =Collect(LocalCollection, {Name: TextInput1.Text})
```

#### **条件逻辑**：
```yaml
Visible: =If(Toggle1.Value, true, false)
Text: =Switch(Status, "New", "🆕", "Complete", "✅", "❓")
Fill: =If(Value < 0, Color.Red, Color.Green)
```

#### **文本操作**：
```yaml
Text: =Concatenate("Hello ", User().FullName)
Text: =Upper(TextInput1.Text)
Text: =Substitute(Label1.Text, "old", "new")
Text: =Left(Title, 10) & "..."
```

#### **数学运算**：
```yaml
Text: =Sum(Sales[Amount])
Text: =Average(Ratings[Score])
Text: =Round(Calculation, 2)
Text: =Max(Values[Number])
```

#### **日期和时间函数**：
```yaml
Text: =Text(Now(), "mm/dd/yyyy")
Text: =DateDiff(StartDate, EndDate, Days)
Text: =Text(Today(), "dddd, mmmm dd, yyyy")
Visible: =IsToday(DueDate)
```

### 公式语法指导原则：

#### **基本语法规则**：
- 所有公式以 `=` 开头
- 没有前置的 `+` 或 `=` 符号（与 Excel 不同）
- 文本字符串使用双引号：`="Hello World"`
- 属性引用：`ControlName.PropertyName`
- 在 YAML 上下文中不支持注释

#### **公式元素**：
```yaml
# 字面值
Text: ="Static Text"
X: =42
Visible: =true

# 控件属性引用
Text: =TextInput1.Text
Visible: =Checkbox1.Value

# 函数调用
Text: =Upper(TextInput1.Text)
Items: =Sort(DataSource, Title)

# 复杂表达式
Text: =If(IsBlank(TextInput1.Text), "Enter text", Upper(TextInput1.Text))
```

#### **行为与属性公式**：
```yaml
# 属性公式（计算值）
Properties:
  Text: =Concatenate("Hello ", User().FullName)
  Visible: =Toggle1.Value

# 行为公式（执行操作 - 使用分号分隔多个操作）
Properties:
  OnSelect: =Set(MyVar, true); Navigate(NextScreen); Notify("Done!")
```

### 高级公式模式：

#### **使用集合**：
```yaml
Properties:
  Items: =Filter(MyCollection, Status = "Active")
  OnSelect: =ClearCollect(MyCollection, DataSource)
  OnSelect: =Collect(MyCollection, {Name: "New Item", Status: "Active"})
```

#### **错误处理**：
```yaml
Properties:
  Text: =IfError(Value(TextInput1.Text), 0)
  OnSelect: =IfError(
    Patch(DataSource, ThisItem, {Field: Value}),
    Notify("Error updating record", NotificationType.Error)
  )
```

#### **动态属性设置**：
```yaml
Properties:
  Fill: =ColorValue("#" & HexInput.Text)
  Height: =Parent.Height * (Slider1.Value / 100)
  X: =If(Alignment = "Center", (Parent.Width - Self.Width) / 2, 0)
```

## 使用公式的最佳实践

### 公式组织：
- 将复杂公式分解为更小、可读的部分
- 使用变量存储中间计算
- 使用描述性控件名称注释复杂逻辑
- 将相关计算分组在一起

### 性能优化：
- 在处理大型数据集时使用委托友好的函数
- 避免在频繁更新的属性中使用嵌套函数调用
- 为复杂数据转换使用集合
- 最小化对外部数据源的调用

## Power Fx 数据类型和操作

### 数据类型类别：

#### **基本类型**：
- **Boolean**: `=true`, `=false`
- **Number**: `=123`, `=45.67`
- **Text**: `="Hello World"`
- **Date**: `=Date(2024, 12, 25)`
- **Time**: `=Time(14, 30, 0)`
- **DateTime**: `=Now()`

#### **复杂类型**：
- **Color**: `=Color.Red`, `=RGBA(255, 128, 0, 1)`
- **Record**: `={Name: "John", Age: 30}`
- **Table**: `=Table({Name: "John"}, {Name: "Jane"})`
- **GUID**: `=GUID()`

#### **类型转换**：
```yaml
Properties:
  Text: =Text(123.45, "#,##0.00")        # 数字转文本
  Text: =Value("123.45")                 # 文本转数字
  Text: =DateValue("12/25/2024")         # 文本转日期
  Visible: =Boolean("true")              # 文本转布尔值
```

#### **类型检查**：
```yaml
Properties:
  Visible: =Not(IsBlank(OptionalField))
  Visible: =Not(IsError(Value(TextInput1.Text)))
  Visible: =IsNumeric(TextInput1.Text)
```

### 表操作：

#### **创建表**：
```yaml
Properties:
  Items: =Table(
    {Name: "Product A", Price: 10.99},
    {Name: "Product B", Price: 15.99}
  )
  Items: =["Option 1", "Option 2", "Option 3"]  # 单列表
```

#### **过滤和排序**：
```yaml
Properties:
  Items: =Filter(Products, Price > 10)
  Items: =Sort(Products, Name, Ascending)
  Items: =SortByColumns(Products, "Price", Descending, "Name", Ascending)
```

#### **数据转换**：
```yaml
Properties:
  Items: =AddColumns(Products, "Total", Price * Quantity)
  Items: =RenameColumns(Products, "Price", "Cost")
  Items: =ShowColumns(Products, "Name", "Price")
  Items: =DropColumns(Products, "InternalID")
```

#### **聚合**：
```yaml
Properties:
  Text: =Sum(Products, Price)
  Text: =Average(Products, Rating)
  Text: =Max(Products, Price)
  Text: =CountRows(Products)
```

### 变量和状态管理：

#### **全局变量**：
```yaml
Properties:
  OnSelect: =Set(MyGlobalVar, "Hello World")
  Text: =MyGlobalVar
```

#### **上下文变量**：
```yaml
Properties:
  OnSelect: =UpdateContext({LocalVar: "Screen Specific"})
  OnSelect: =Navigate(NextScreen, None, {PassedValue: 42})
```

#### **集合**：
```yaml
Properties:
  OnSelect: =ClearCollect(MyCollection, DataSource)
  OnSelect: =Collect(MyCollection, {Name: "New Item"})
  Items: =MyCollection
```

## Power Fx 增强连接器和外部数据

### 连接器集成：
```yaml
DataSources:
  SharePointList:
    Type: Table
    Parameters:
      TableLogicalName: "Custom List"

  Office365Users:
    Type: Actions
    ConnectorId: shared_office365users
```

### 使用外部数据：
```yaml
Properties:
  Items: =Filter(SharePointList, Status = "Active")
  OnSelect: =Office365Users.SearchUser({searchTerm: SearchInput.Text})
```

### 委托考虑：
```yaml
Properties:
  # 可委托操作（在服务器端执行）
  Items: =Filter(LargeTable, Status = "Active")    # 高效

  # 不可委托操作（可能下载所有记录）
  Items: =Filter(LargeTable, Len(Description) > 100)  # 发出警告
```

## 故障排除和常见模式

### 常见错误模式：
```yaml
# 处理空值
Properties:
  Text: =If(IsBlank(OptionalText), "Default", OptionalText)

# 优雅处理错误
Properties:
  Text: =IfError(RiskyOperation(), "Fallback Value")

# 验证输入
Properties:
  Visible: =And(
    Not(IsBlank(NameInput.Text)),
    IsNumeric(AgeInput.Text),
    IsMatch(EmailInput.Text, Email)
  )
```

### 性能优化：
```yaml
# 高效数据加载
Properties:
  Items: =Filter(LargeDataSource, Status = "Active")    # 服务器端过滤

# 使用委托友好的操作
Properties:
  Items: =Sort(Filter(DataSource, Active), Name)        # 可委托
  # 避免: Sort(DataSource, If(Active, Name, ""))       # 不可委托
```

### 内存管理：
```yaml
# 清除未使用的集合
Properties:
  OnSelect: =Clear(TempCollection)

# 限制数据检索
Properties:
  Items: =FirstN(Filter(DataSource, Status = "Active"), 50)
```

请记住：本指南提供了 Power Apps Canvas Apps YAML 结构和 Power Fx 公式的全面覆盖。始终根据官方架构验证您的 YAML，并在 Power Apps Studio 环境中测试公式。