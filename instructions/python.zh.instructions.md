---
description: 'Python 编码规范和指南'
applyTo: '**/*.py'
---

# Python 编码规范

## Python 指令

- 为每个函数编写清晰简洁的注释。
- 确保函数有描述性的名称并包含类型提示。
- 遵循 PEP 257 约定提供文档字符串。
- 使用 `typing` 模块进行类型注解（例如，`List[str]`，`Dict[str, int]`）。
- 将复杂的函数分解为更小、更易管理的函数。

## 通用指令

- 始终优先考虑可读性和清晰度。
- 对于算法相关的代码，包含所使用方法的解释。
- 编写具有良好可维护性实践的代码，包括对某些设计决策原因的注释。
- 处理边缘情况并编写清晰的异常处理。
- 对于库或外部依赖项，在注释中提及其用途和目的。
- 使用一致的命名约定并遵循特定语言的最佳实践。
- 编写简洁、高效且惯用的代码，同时也易于理解。

## 代码风格和格式化

- 遵循 **PEP 8** Python 风格指南。
- 保持适当的缩进（每个缩进级别使用 4 个空格）。
- 确保行长度不超过 79 个字符。
- 将函数和类的文档字符串直接放在 `def` 或 `class` 关键字之后。
- 在适当的地方使用空行分隔函数、类和代码块。

## 边缘情况和测试

- 始终为应用程序的关键路径包含测试用例。
- 考虑常见的边缘情况，如空输入、无效数据类型和大数据集。
- 为边缘情况和这些情况下的预期行为包含注释。
- 为函数编写单元测试，并使用文档字符串记录测试用例的说明。

## 正确文档的示例

```python
def calculate_area(radius: float) -> float:
    """
    Calculate the area of a circle given the radius.

    Parameters:
    radius (float): The radius of the circle.

    Returns:
    float: The area of the circle, calculated as π * radius^2.
    """
    import math
    return math.pi * radius ** 2
```