---
description: '.NET WPF组件和应用程序模式'
applyTo: '**/*.xaml, **/*.cs'
---

## 摘要

这些指导旨在指导GitHub Copilot协助构建高质量、可维护和高性能的WPF应用程序，使用MVVM模式。包括XAML、数据绑定、UI响应性和.NET性能的最佳实践。

## 理想的项目类型

- 使用C#和WPF的桌面应用程序
- 遵循MVVM（Model-View-ViewModel）设计模式的应用程序
- 使用.NET 8.0或更高版本的项目
- 在XAML中构建的UI组件
- 强调性能和响应性的解决方案

## 目标

- 为`INotifyPropertyChanged`和`RelayCommand`生成样板代码
- 建议ViewModel和View逻辑的清晰分离
- 鼓励使用`ObservableCollection<T>`、`ICommand`和适当绑定
- 推荐性能提示（例如虚拟化、异步加载）
- 避免紧密耦合的代码后置逻辑
- 生成可测试的ViewModel

## 示例提示行为

### ✅ 良好建议
- "为登录屏幕生成ViewModel，具有用户名和密码属性，以及LoginCommand"
- "为ListView编写XAML片段，使用UI虚拟化并绑定到ObservableCollection"
- "将此代码后置点击处理程序重构为ViewModel中的RelayCommand"
- "在WPF中异步获取数据时添加加载转圈"

### ❌ 避免
- 建议在代码后置中添加业务逻辑
- 使用没有上下文的静态事件处理程序
- 生成没有绑定的紧密耦合XAML
- 建议WinForms或UWP方法

## 优先使用的技术
- 使用.NET 8.0+的C#
- 具有MVVM结构的XAML
- `CommunityToolkit.Mvvm`或自定义`RelayCommand`实现
- 用于非阻塞UI的Async/await
- `ObservableCollection`、`ICommand`、`INotifyPropertyChanged`

## 要遵循的常见模式
- ViewModel优先绑定
- 使用.NET或第三方容器（例如Autofac、SimpleInjector）的依赖注入
- XAML命名约定（控件使用PascalCase，绑定使用camelCase）
- 避免绑定中的魔术字符串（使用`nameof`）

## Copilot可以使用的示例指导片段

```csharp
public class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private string userName;

    [ObservableProperty]
    private string password;

    [RelayCommand]
    private void Login()
    {
        // Add login logic here
    }
}
```

```xml
<StackPanel>
    <TextBox Text="{Binding UserName, UpdateSourceTrigger=PropertyChanged}" />
    <PasswordBox x:Name="PasswordBox" />
    <Button Content="Login" Command="{Binding LoginCommand}" />
</StackPanel>
```