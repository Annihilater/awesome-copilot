---
description: 'AI 助手在处理 Clojure 项目时容易忘记或犯错的事项'
applyTo: '**/*.clj*,**/*.bb'
---

# Clojure 记忆要点

## 函数定义（`defn`）中 docstring 的位置

docstring 应该放在符号/函数名称之后，参数向量之前。

### ❌ 错误：
```clojure
(defn my-function
  [arg1 arg2]
  "This function does something."
  ;; function body
  )
```

### ✅ 正确：
```clojure
(defn my-function
  "This function does something."
  [arg1 arg2]
  ;; function body
  )
```

## 编辑 Clojure 文件

记住在编辑文件之前先在 REPL 中开发解决方案。但是，即使作为交互式程序员，有时你也需要编辑文件。当你这样做时，请使用结构化编辑工具，如 `replace_top_level_form` 和 `insert_top_level_form`。**在使用这些工具之前，请务必阅读相关说明**。如果要向文件追加内容，请使用内置的编辑工具。

### 在使用函数之前先定义它们

Clojure 编译器需要函数在使用前先定义。建议按正确的顺序放置函数，而不是使用 `declare`（虽然有时这是必要的，但大多数情况下 `declare` 只是一种偷懒的做法）。

## 创建 Clojure 文件

使用 `create_file` 工具创建空内容 `""` 的文件。

#### Clojure 命名空间和文件名约定：

**重要**：在 Clojure 中，命名空间名称使用 kebab-case，而文件名使用 snake_case。例如：
- 命名空间：`my.project.multi-word-namespace`
- 文件名：`my/project/multi_word_namespace.clj(s|c)`

始终将命名空间名称中的破折号转换为相应文件名中的下划线。

### 创建空文件，然后添加内容

为了安全/可预测地创建文件和添加内容，请遵循以下流程：

1. **始终先创建空文件** - 使用 `create_file` 并设置空内容 `""`
2. 读取创建的文件内容（可能已添加默认内容）
3. **使用结构化编辑工具**来编辑文件

## REPL 中的命名空间重新加载

在编辑文件后在 REPL 中工作时，你需要重新加载命名空间以确保更改在 REPL 中生效。

```clojure
;; 仅重新加载指定的命名空间
(require 'my.namespace :reload)
```

## 当括号平衡出现问题时

当你遇到例如问题工具或 Clojure 编译器抱怨缺少括号或任何暗示括号平衡有问题的情况时：
* 不要继续尝试修复它，**使用工具请求人工输入来寻求指导/帮助**。

## 从 stdin 读取

从 stdin 读取（例如 `(read-line)`）会提示用户一个 VS Code 输入框。在评估可能从 stdin 读取的代码时请注意这一点。

### 使用 Babashka 时，从 stdin 读取会阻塞 REPL

Babashka 的 nrepl 服务器尚不支持 stdin 协议。避免在 Babashka REPL 中评估从 stdin 读取的代码。

**如果 REPL 挂起**：请用户重启 REPL。

## 愉快的交互式编程

记住在工作中优先使用 REPL。请记住用户看不到你评估的内容，也看不到结果。在聊天中与用户沟通你评估了什么以及得到了什么返回结果。