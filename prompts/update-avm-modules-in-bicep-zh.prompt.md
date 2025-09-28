---
mode: "agent"
description: "将 Bicep 文件中的 Azure Verified Modules (AVM) 更新至最新版本。"
tools: ["codebase", "think", "changes", "fetch", "searchResults", "todos", "editFiles", "search", "runCommands", "bicepschema", "azure_get_schema_for_Bicep"]
---
# 更新 Bicep 文件中的 Azure Verified Modules

将 Bicep 文件 `${file}` 中引用的 Azure Verified Module (AVM) 更新至最新版本。仅针对非破坏性变更输出进度。除最终表格与总结外，不要输出其他信息。

## 流程

1. **扫描**：从 `${file}` 中提取 AVM 模块及其当前版本。
1. **识别**：使用 `#search` 工具匹配 `avm/res/{service}/{resource}`，列出所有唯一 AVM 模块。
1. **检查**：通过 `#fetch` 工具访问 `https://mcr.microsoft.com/v2/bicep/avm/res/{service}/{resource}/tags/list` 获取各模块最新版本。
1. **比较**：解析语义化版本，找出需要更新的模块。
1. **审阅**：如存在破坏性变更，使用 `#fetch` 获取文档：`https://github.com/Azure/bicep-registry-modules/tree/main/avm/res/{service}/{resource}`。
1. **更新**：使用 `#editFiles` 应用版本更新与参数调整。
1. **验证**：通过 `#runCommands` 执行 `bicep lint` 与 `bicep build`，确保符合规范。
1. **输出**：以表格形式总结变更，并附上简要总结。

## 工具使用

如可用，请始终使用 `#search`、`#searchResults`、`#fetch`、`#editFiles`、`#runCommands`、`#todos`。避免自行编写代码完成任务。

## 破坏性变更策略

⚠️ 如遇以下情况需暂停并等待批准：

- 不兼容的参数变更
- 安全或合规相关修改
- 行为变化

## 输出格式

仅输出带图标的表格：

```markdown
| Module | Current | Latest | Status | Action | Docs |
|--------|---------|--------|--------|--------|------|
| avm/res/compute/vm | 0.1.0 | 0.2.0 | 🔄 | Updated | [📖](link) |
| avm/res/storage/account | 0.3.0 | 0.3.0 | ✅ | Current | [📖](link) |

### Summary of Updates

Describe updates made, any manual reviews needed or issues encountered.
```

## 图标

- 🔄 Updated
- ✅ Current
- ⚠️ Manual review required
- ❌ Failed
- 📖 Documentation

## 要求

- 仅使用 MCR tags API 获取版本信息
- 解析 JSON 标签数组，并按语义化版本排序
- 确保 Bicep 文件仍可通过 lint 与编译

