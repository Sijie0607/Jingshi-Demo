# AI4PM Skills Agent Guidelines

本文档记录了 `ai4pm-skills` 项目下所有 Skill 设计的统一特点和必须遵循的约束。在创建、更新或执行任何相关的 Skill 任务时，Agent/LLM 必须严格遵守以下规范。

## 1. 双重输出规范 (Dual Output Standard)

当你使用此项目下的 Skill 时，必须**同时**输出两个部分：
1. **结构化 YAML (Structured YAML)**: 用于下一步的自动化处理、逻辑解耦和数据存档。
2. **交互式 HTML (Interactive HTML)**: 用于最终用户的直观审查与演示，通过前端渲染代码（如 Jinja2 或直接 HTML 生成）呈现。

## 2. 输出路径与命名规范 (Output Path & Naming Convention)

为了保持项目输出的整洁和统一：
- **目录规范**: 所有输出文件必须放在当前工作目录下的一个新子目录中，目录名为 `[公司/业务名]` (例如：`张雪机车海外销售/`)。
- **文件命名**: 
  - 文件名必须反映业务内容，HTML 文件格式为 `[公司/业务名]-[业务类型].html` (例如：`张雪机车海外销售-MVP迭代计划.html`)。
  - YAML 文件同理，如 `[公司/业务名]-[业务类型].yaml`。

## 3. 视觉设计规范 (Visual Design Standard)

生成的 HTML 报告和可视化产物必须遵循统一的现代设计美学：
- **样式风格**: 默认按照本项目下的 `ai4pm-skills/design.md` 进行样式输出。设计需专业、高颜值，避免简陋的实现。
- **底色模式**: 默认使用 **浅色底 (Light Mode)**。
- **页面布局**: HTML 内容区域应占据页面 **85%** 的宽度，并保持简洁的 Header 设计（参考统一的简洁 Header 规范）。

## 4. SKILL 文档结构规范 (Skill Documentation Standard)

本项目下每个子目录的 `SKILL.md` 都必须包含一个标准的 `[!IMPORTANT]` 区块。此区块负责向执行层 Agent 强制宣告上述三大标准（双重输出、命名、视觉）。任何新增或修改的 Skill 文档都应包含这套通用提示规则。

## 5. 开发防坑指南 (Development Gotchas)

### 5.1 Jinja Inline Style IDE 报错问题
**问题描述**：在 HTML 模板中使用 Jinja 变量生成内联样式（`style="..."`）时，IDE（如 VS Code）由于将属性值作为原生 CSS 解析，遇到 `{{ }}` 会抛出 `identifier expected`, `} expected` 或 `at-rule or selector expected` 等满屏错误。这个错误历史上已经出现过 6 轮以上！

**正确做法**：必须将完整的 `style="..."` 属性及内容作为一个完整的 Jinja 字符串进行拼接和输出，使得 IDE 的 HTML 解析器根本看不到原本的 `style` 属性键值对，从而跳过 CSS 语法检查，同时 Jinja 引擎仍能正确渲染出标准的 HTML 属性。
- ❌ **错误示范**：`<div style="left:{{ node.cx }}px; top:{{ node.top }}px;">`
- ❌ **半对半错示范（IDE依然会报错）**：`<div style="{{ 'left:' ~ node.cx ~ 'px; top:' ~ node.top ~ 'px;' }}">`
- ✅ **完全正确示范**：`<div {{ 'style="left:' ~ node.cx ~ 'px; top:' ~ node.top ~ 'px;"' }}>`

请所有参与模板重构与编写的 Agent 牢记此坑，禁止再犯！
