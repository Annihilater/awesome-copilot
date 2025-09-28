# GitHub Copilot Chat 高级定制化使用指南

GitHub Copilot 不仅仅是一个代码补全工具，通过其聊天功能，您可以利用强大的定制化选项来增强其能力，使其更贴合您的项目需求和个人工作流。本文将详细介绍四种核心定制化功能：**Prompts**、**Instructions**、**Chat Modes** 和 **Collections** 的使用方法及安装级别。

---

## 1. 各类定制化功能详解

### 1.1 Prompts (提示)

- **功能**：Prompts 是预设好的、针对特定任务的指令模板。当您需要重复执行某个特定操作时（例如“为我的函数生成单元测试”、“解释这段代码的复杂度”），使用 Prompts 可以大大提高效率。
- **使用方法**：在 Copilot Chat 聊天框中，输入 `/` 即可唤出可用的 Prompts 列表。选择您需要的 Prompt（例如 `/explain`），然后 Copilot 就会按照该模板执行任务。像 `awesome-copilot` 这样的项目，提供了大量自定义的 Prompts，安装后即可在列表中看到。

  ```shell
  # 示例：使用一个自定义的 Prompt 来创建 README
  /awesome-copilot create-readme
  ```

### 1.2 Instructions (指令)

- **功能**：Instructions 是一系列编码规范、最佳实践或上下文信息，它们会**自动应用**于您正在编辑的文件。Copilot 会在后台读取这些指令，并在生成代码或提供建议时遵循其中的规则。
- **使用方法**：您无需主动调用。一旦配置好，只要您打开或编辑符合指令文件中 `applyTo` 字段所定义模式（例如 `**/*.ts`, `**/pom.xml`）的文件，Copilot 就会自动加载并遵循这些指令。这对于统一团队编码风格、遵循特定框架（如 React, Angular）的最佳实践非常有用。

### 1.3 Chat Modes (聊天模式)

- **功能**：Chat Modes 赋予了 Copilot 一个特定的“专家人格”或“角色”。激活某个模式后，Copilot 的回答风格和知识重点都会发生改变，以更好地匹配该角色。例如，您可以让它扮演“数据库管理员”、“安全专家”或“资深架构师”。
- **使用方法**：在 Copilot Chat 中，通过点击聊天框旁边的“火花”✨ 图标，或输入 `@workspace` 并选择相应的模式来激活。激活后，Copilot 的后续对话都将基于该模式进行。

### 1.4 Collections (集合)

- **功能**：Collections 是一个围绕特定技术栈或工作流打包的资源集合。它本身不是一个直接使用的功能，而是一个组织方式，将相关的 Prompts、Instructions 和 Chat Modes 组合在一起，方便用户一次性安装和管理。
- **使用方法**：通常，您会安装一个 Collection，然后使用其中包含的各种 Prompts、Instructions 和 Chat Modes。

---

## 2. 安装级别与目录详解

对于这些定制化功能，GitHub Copilot 支持两个主要的安装级别，这与 VS Code 的设置层级完全对应：

1. **用户级 (User Level)**：全局生效。
2. **工作区级 (Workspace Level)**：仅在当前项目（文件夹）中生效。

没有其他更高级别的安装目录了（例如系统级）。下面我们详细说明如何在这两个级别上进行配置。

### 2.1 用户级安装 (全局配置)

- **适用场景**：当您希望某些定制化功能在您所有的项目中都可用时（例如，通用的代码审查指令、您个人常用的提示）。
- **配置文件位置**：VS Code 的用户 `settings.json` 文件。
  - 您可以通过快捷键 `Cmd + ,` (macOS) 或 `Ctrl + ,` (Windows) 打开设置界面，然后点击右上角的 `{}` 图标进入 `settings.json`。
- **配置方法**：
  在这个 JSON 文件中，您可以添加或修改以下字段，将 `.md` 文件的**绝对路径**添加进去：

  ```json
  {
    // 用户级的其他设置...

    // 配置自定义 Prompts
    "github.copilot.chat.prompts.files": ["/path/to/your/prompts/my-custom-prompt.prompt.md"],

    // 配置自定义 Instructions
    "github.copilot.instructions.files": ["/path/to/your/instructions/react-best-practices.instructions.md"],

    // 配置自定义 Chat Modes
    "github.copilot.chat.modes.files": ["/path/to/your/chatmodes/dba-expert.chatmode.md"]
  }
  ```

  **注意**：`awesome-copilot` 项目推荐的 **MCP Server** 安装方式，就是自动将服务配置添加到您的**用户级 `settings.json`** 中，从而实现全局可用。

### 2.2 工作区级安装 (项目级配置)

- **适用场景**：当某些定制化功能仅与特定项目相关时（例如，某个项目独有的 API 设计规范、针对该项目技术栈的指令）。这种方式非常适合团队协作，因为配置可以提交到版本控制中，团队成员共享。
- **配置文件位置**：项目根目录下的 `.vscode/settings.json` 文件。
  - 如果该文件或目录不存在，您可以手动创建它。
- **配置方法**：
  与用户级配置类似，在 `.vscode/settings.json` 文件中添加相同的字段。路径可以是绝对路径，也可以是相对于项目根目录的**相对路径**。

  ```json
  {
    // 项目级的其他设置...

    // 使用相对路径引用项目内的定制文件
    "github.copilot.instructions.files": ["./.copilot/instructions/project-specific-rules.instructions.md"],
    "github.copilot.chat.modes.files": ["./.copilot/chatmodes/project-api-architect.chatmode.md"]
  }
  ```

---

## 总结

| 级别         | 配置文件                | 生效范围   | 优点                                           | 缺点                                 |
| :----------- | :---------------------- | :--------- | :--------------------------------------------- | :----------------------------------- |
| **用户级**   | 全局 `settings.json`    | 所有项目   | 一次配置，处处可用，适合个人通用工具。         | 无法与团队共享，不适合项目特定规则。 |
| **工作区级** | `.vscode/settings.json` | 仅当前项目 | 随项目共享，确保团队一致性，适合项目特定规则。 | 需要为每个项目单独配置。             |

希望这篇详细的文档能帮助您更好地理解和使用 GitHub Copilot 的高级定制化功能！
