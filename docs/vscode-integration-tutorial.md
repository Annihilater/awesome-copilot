# VSCode 集成 Awesome Copilot 资源完整教程

本文档面向希望在其他项目中复用 Awesome Copilot 仓库资源的开发者。无论你只想挑选部分 prompts、instructions、chatmodes，还是需要完整的集合配置，按照以下步骤操作即可快速在 VSCode 与 GitHub Copilot 中启用。

## 1. 了解仓库资源结构

- **Collections (`.collection.yml`)**：围绕特定主题（如前端、安全、DevOps）的资源打包集合，便于一次性导入多种资源。
- **Prompts (`.prompt.md`)**：可在 Copilot Chat 中通过 `/awesome-copilot <命令>` 调用的任务提示词。
- **Instructions (`.instructions.md`)**：为特定文件类型或目录自动生效的编码规范与约束。
- **Chat Modes (`.chatmode.md`)**：预设的专家角色，提供特定领域的对话体验。

> 提示：所有资源均可单独使用；你可以只挑选项目需要的一两个文件，而无需整包复制。

## 2. 准备目标项目的 Copilot 目录

1. 在项目根目录创建 Copilot 配置文件夹：
   ```bash
   mkdir -p .github/copilot
   ```
2. 按资源类型创建子目录，保持结构清晰：
   ```bash
   mkdir -p .github/copilot/{prompts,instructions,chatmodes,collections}
   ```
3. 可选：加入 `README` 或 `docs/copilot-usage.md` 说明团队如何使用这些资源。

## 3. 拷贝或链接所需资源

### 方法 A：手动复制（适合少量文件）

```bash
# 复制单个 prompt
cp /path/to/awesome-copilot/prompts/create-readme.prompt.md \
   .github/copilot/prompts/

# 复制指令文件
cp /path/to/awesome-copilot/instructions/python.instructions.md \
   .github/copilot/instructions/

# 复制聊天模式
cp /path/to/awesome-copilot/chatmodes/principal-software-engineer.chatmode.md \
   .github/copilot/chatmodes/
```

### 方法 B：批量导入 Collections（推荐团队使用）

1. 复制想要的集合文件到 `.github/copilot/collections/`。
2. 在 VSCode 的 Copilot Chat 中运行集合内的 prompts，或按照集合描述导入 instructions/chatmodes。
3. 若只需集合内部分资源，可打开 `.collection.yml` 查看 `items` 列表，只复制其中需要的路径。

### 方法 C：符号链接保持与上游同步

```bash
ln -s ../../path/to/awesome-copilot/prompts/update-specification.prompt.md \
      .github/copilot/prompts/update-specification.prompt.md
```

> 优点：上游仓库更新后自动生效；缺点：对 Windows 兼容性和仓库协作者可能有要求。

## 4. 在 VSCode 中启用资源

1. 打开 VSCode，确保已安装 **GitHub Copilot** 与 **Copilot Chat** 扩展。
2. 重启 VSCode（或使用 `Developer: Reload Window`）以加载新的资源文件。
3. 在 Copilot Chat 使用 `/awesome-copilot` 查看可用命令，或输入 `/awesome-copilot <prompt 名称>` 直接调用。
4. 打开受 instructions 影响的文件，验证 Copilot 是否提供了符合规范的建议。

## 5. 只选择需要的资源

- 将常用资源整理到 `.github/copilot/collections/<team>.collection.yml`，集中管理。
- 对 prompts/instructions/chatmodes 按项目模块划分子目录，例如 `prompts/frontend/`、`instructions/backend/`。
- 在集合文件中移除不需要的条目，以防团队误用。
- 记录每个资源用途与启用场景，帮助新成员快速上手。

## 6. 同步与维护

1. **定期拉取上游更新**：
   ```bash
   cd /path/to/awesome-copilot
   git pull origin main
   ```
2. **比较差异**：使用 `diff` 或 VSCode 比较目标项目中的文件与上游版本，手动合并必要更新。
3. **本地化资源**：若需要中文或其他语言版本，可参考 `prompts/*-zh.prompt.md` 的命名规则创建翻译文件。
4. **团队协作**：在项目仓库的 Pull Request 模板或开发指南中说明如何添加、更新 Copilot 资源。

## 7. 常见问题排查

- **提示词未出现**：确认文件名后缀为 `.prompt.md`，且位于 `.github/copilot/prompts/`。
- **指令未生效**：检查文件头部 YAML Frontmatter 的 `applyTo` 配置是否匹配当前文件路径。
- **聊天模式未加载**：在 Copilot Chat 输入 `/help` 查看可用模式，或检查 `.chatmode.md` 文件是否存在语法错误。
- **需要部分禁用**：临时将不需要的资源移动到 `_archive/` 等目录，避免 Copilot 自动加载。

通过以上步骤，你可以在任何新项目中高效复用 Awesome Copilot 的资源，并根据团队需求灵活裁剪、扩展、维护。

