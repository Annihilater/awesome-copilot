---
description: '基于官方文档的 Playwright Python AI 测试生成指令。'
applyTo: '**'
---

# Playwright Python 测试生成指令

## 测试编写指南

### 代码质量标准
- **定位器**：优先使用面向用户的、基于角色的定位器（get_by_role、get_by_label、get_by_text）以获得弹性和可访问性。
- **断言**：通过 expect API 使用自动重试的 web-first 断言（例如，expect(page).to_have_title(...)）。避免使用 expect(locator).to_be_visible()，除非专门测试元素可见性的变化，因为更具体的断言通常更可靠。
- **超时**：依赖 Playwright 的内置自动等待机制。避免硬编码等待或增加默认超时时间。
- **清晰性**：使用描述性的测试标题（例如，def test_navigation_link_works():）清楚地说明其意图。只在解释复杂逻辑时添加注释，而不是描述简单操作如"点击按钮"。

### 测试结构
- **导入**：每个测试文件都应以 from playwright.sync_api import Page, expect 开始。
- **装置**：在测试函数中使用 page: Page 装置作为参数来与浏览器页面交互。
- **设置**：在每个测试函数的开头放置导航步骤如 page.goto()。对于多个测试共享的设置操作，使用标准的 Pytest 装置。

### 文件组织
- **位置**：将测试文件存储在专用的 tests/ 目录中或遵循现有项目结构。
- **命名**：测试文件必须遵循 test_<feature-or-page>.py 命名约定才能被 Pytest 发现。
- **范围**：每个主要应用功能或页面对应一个测试文件。

## 断言最佳实践
- **元素计数**：使用 expect(locator).to_have_count() 断言定位器找到的元素数量。
- **文本内容**：使用 expect(locator).to_have_text() 进行精确文本匹配，使用 expect(locator).to_contain_text() 进行部分匹配。
- **导航**：使用 expect(page).to_have_url() 验证页面 URL。
- **断言风格**：对于更可靠的 UI 测试，优先使用 `expect` 而不是 `assert`。


## 示例

```python
import re
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    # Go to the starting url before each test.
    page.goto("https://playwright.dev/")

def test_main_navigation(page: Page):
    expect(page).to_have_url("https://playwright.dev/")

def test_has_title(page: Page):
    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_get_started_link(page: Page):
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

## 测试执行策略

1. **执行**：测试通过终端使用 pytest 命令运行。
2. **调试失败**：分析测试失败并识别根本原因