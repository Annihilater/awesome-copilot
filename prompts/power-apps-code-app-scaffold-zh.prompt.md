---
description: "使用 PAC CLI、SDK 集成与连接器配置脚手架化完整的 Power Apps Code App 项目。"
mode: "agent"
tools: ["changes", "codebase", "editFiles", "problems", "search"]
model: GPT-4.1
---

# Power Apps Code Apps 项目脚手架

你是一名精通 Power Platform 的开发者，专长于创建 Power Apps Code Apps。你的任务是根据微软的最佳实践与当前预览能力，搭建一个完整的 Power Apps Code App 项目。

## 背景

Power Apps Code Apps（预览版）让开发者能够使用代码优先的方式构建自定义 Web 应用，同时整合 Power Platform 能力。这些应用可以访问 1500+ 连接器，使用 Microsoft Entra 进行身份验证，并运行在托管的 Power Platform 基础设施上。

## 任务

搭建一个包含以下组件的完整 Power Apps Code App 项目结构：

### 1. 项目初始化
- 通过 Vite + React + TypeScript 创建符合 Code Apps 要求的项目。
- 将项目配置为运行在 3000 端口（Power Apps SDK 要求）。
- 安装并配置 Power Apps SDK（`@microsoft/power-apps` ^0.3.1）。
- 使用 PAC CLI 执行 `pac code init` 初始化项目。

### 2. 核心配置文件
- **vite.config.ts**：满足 Power Apps Code Apps 要求的配置。
- **power.config.json**：PAC CLI 生成的 Power Platform 元数据。
- **PowerProvider.tsx**：初始化 Power Platform 的 React Provider 组件。
- **tsconfig.json**：兼容 Power Apps SDK 的 TypeScript 配置。
- **package.json**：包含开发与部署脚本。

### 3. 项目结构
请创建清晰的目录结构：
```
src/
├── components/          # 可复用 UI 组件
├── services/           # PAC CLI 生成的连接器服务
├── models/            # PAC CLI 生成的 TypeScript 模型
├── hooks/             # 与 Power Platform 集成的自定义 React hooks
├── utils/             # 工具函数
├── types/             # TypeScript 类型定义
├── PowerProvider.tsx  # Power Platform 初始化组件
└── main.tsx          # 应用入口
```

### 4. 开发脚本配置
参考微软官方示例为 `package.json` 配置脚本：
- `dev`: `"concurrently \"vite\" \"pac code run\""`（并行运行）
- `build`: `"tsc -b && vite build"`（TypeScript 编译 + Vite 构建）
- `preview`: `"vite preview"`（生产预览）
- `lint`: `"eslint ."`（代码质量检测）

### 5. 示例实现
需包含的基础示例：
- 使用 PowerProvider 组件完成 Power Platform 身份验证与初始化。
- 接入至少一个官方支持的连接器（推荐 Office 365 Users）。
- 利用生成的模型与服务开展 TypeScript 开发。
- 使用 try/catch 处理错误与加载状态。
- 采用 Fluent UI React 组件构建响应式界面（与官方示例保持一致）。
- 使用 `useEffect` 与异步初始化正确实现 PowerProvider。

#### 可选高级模式
- **多环境配置**：为开发/测试/生产设置环境变量。
- **离线优先架构**：利用 Service Worker 与本地存储实现离线能力。
- **无障碍支持**：添加 ARIA 属性、键盘导航与屏幕阅读支持。
- **国际化架构**：搭建基础的多语言支持结构。
- **主题系统基础**：实现明/暗模式切换。
- **响应式设计模式**：采用移动优先与断点系统。
- **动画框架集成**：例如集成 Framer Motion 提升过渡效果。

### 6. 文档
编写详尽的 README.md，包含：
- 前置条件与安装步骤
- 身份验证与环境配置
- 连接器设置与数据源配置
- 本地开发与部署流程
- 常见问题排查

## 实施指南

### 需要提及的前置条件
- 安装 VS Code 及 Power Platform Tools 扩展。
- Node.js（建议 LTS：v18.x 或 v20.x）。
- Git 版本控制。
- 最新版本的 Power Platform CLI（PAC CLI）。
- 已启用 Code Apps 的 Power Platform 环境（需管理员配置）。
- 终端用户需要 Power Apps Premium 许可证。
- Azure 账号（若使用 Azure SQL 等连接器）。

### 需包含的 PAC CLI 命令
- `pac auth create --environment {environment-id}`：与指定环境做身份验证。
- `pac env select --environment {environment-url}`：选择目标环境。
- `pac code init --displayName "App Name"`：初始化 Code App 项目。
- `pac connection list`：列出可用连接。
- `pac code add-data-source -a {api-name} -c {connection-id}`：添加连接器。
- `pac code push`：部署到 Power Platform。

### 官方支持的连接器（示例配置）
- **SQL Server（含 Azure SQL）**：CRUD、存储过程。
- **SharePoint**：文档库、列表与站点。
- **Office 365 Users**：用户信息、头像、组成员。
- **Office 365 Groups**：团队信息与协作。
- **Azure Data Explorer**：分析与大数据查询。
- **OneDrive for Business**：文件存储与共享。
- **Microsoft Teams**：团队协作与通知。
- **MSN Weather**：天气数据。
- **Microsoft Translator V2**：多语言翻译。
- **Dataverse**：CRUD、关系与业务逻辑。

### 连接器集成示例
```typescript
// 示例：获取当前用户档案
const profile = await Office365UsersService.MyProfile_V2("id,displayName,jobTitle,userPrincipalName");

// 示例：获取用户头像
const photoData = await Office365UsersService.UserPhoto_V2(profile.data.id);
```

### 需要记录的现有限制
- 目前不支持 Content Security Policy (CSP)。
- 不支持存储 SAS IP 限制。
- 暂无 Power Platform Git 集成。
- 不支持 Dataverse 解决方案。
- 无原生 Azure Application Insights 集成。

### 应纳入的最佳实践
- 本地开发使用 3000 端口（Power Apps SDK 要求）。
- 在 TypeScript 配置中设置 `verbatimModuleSyntax: false`。
- 在 vite.config.ts 中配置 `base: "./"` 及合适的路径别名。
- 将敏感数据保存在数据源中，而非应用代码。
- 遵守 Power Platform 托管平台策略。
- 为连接器操作实现完善的错误处理。
- 使用 PAC CLI 生成的 TypeScript 模型与服务。
- 使用带异步初始化与错误处理的 PowerProvider。

## 交付物

1. 包含所有必要文件的完整项目脚手架。
2. 带有连接器集成的可运行示例应用。
3. 完整的文档与使用说明。
4. 开发与部署脚本。
5. 面向 Power Apps Code Apps 优化的 TypeScript 配置。
6. 最佳实践示例。

请确保生成的项目遵循微软官方 Power Apps Code Apps 文档与示例（https://github.com/microsoft/PowerAppsCodeApps），并能通过 `pac code push` 成功部署到 Power Platform。

