---
mode: "agent"
description: "根据指定文件夹生成索引/目录表，更新 Markdown 文件中的相关章节。"
tools: ["changes", "codebase", "editFiles", "extensions", "fetch", "findTestFiles", "githubRepo", "openSimpleBrowser", "problems", "runCommands", "runTasks", "runTests", "search", "searchResults", "terminalLastCommand", "terminalSelection", "testFailure", "usages", "vscodeAPI"]
---
# 更新 Markdown 文件索引

为 Markdown 文件 `${file}` 生成 `${input:folder}` 文件夹内的文件索引/表格，可使用 `${input:pattern}` 过滤。

## 流程

1. **扫描**：阅读目标 Markdown 文件 `${file}`，了解现有结构。
2. **发现**：列出 `${input:folder}` 中符合 `${input:pattern}` 的所有文件。
3. **分析**：判断是否已有索引/表格部分可更新，或需新建结构。
4. **结构**：根据文件类型与现有内容选择合适的表格/列表格式。
5. **更新**：替换既有部分或新增章节，写入文件索引。
6. **校验**：确保 Markdown 语法正确、格式一致。

## 文件分析

对每个发现的文件提取：

- **Name**：根据上下文决定是否保留扩展名。
- **Type**：文件扩展名与类别（如 `.md`、`.js`、`.py`）。
- **Description**：首行注释、标题或推断用途。
- **Size**：可选，文件大小。
- **Modified**：可选，最后修改时间。

## 表格结构选项

可根据情况选择以下格式：

### 选项 1：简单列表

```markdown
## Files in ${folder}

- [filename.ext](path/to/filename.ext) - Description
- [filename2.ext](path/to/filename2.ext) - Description
```

### 选项 2：详细表格

| File | Type | Description |
|------|------|-------------|
| [filename.ext](path/to/filename.ext) | Extension | Description |
| [filename2.ext](path/to/filename2.ext) | Extension | Description |

### 选项 3：按类别分节

根据类型/类别分组，分别创建子章节或子表格。

## 更新策略

- 🔄 **更新既有**：若已有索引/表格，保留结构并替换内容。
- ➕ **新增**：若不存在相关部分，选择最合适格式新建章节。
- 📋 **保持**：维持原有 Markdown 格式、标题层级与文档流。
- 🔗 **链接**：使用仓库内的相对路径。

## 章节识别

可通过以下模式寻找既有章节：

- 标题包含 "index"、"files"、"contents"、"directory"、"list"。
- 含有文件相关列的表格。
- 以文件链接组成的列表。
- 标注文件索引的 HTML 注释。

## 要求

- 保留既有 Markdown 结构与格式。
- 使用相对路径链接。
- 尽量提供文件描述。
- 默认按字母顺序排序。
- 妥善处理文件名中的特殊字符。
- 校验生成的 Markdown 语法。

