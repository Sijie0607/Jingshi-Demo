---
name: functional-arch-generator
description: |
  根据业务功能描述，自动生成高颜值、专业的产品功能架构图 HTML 报告。

  Triggers when user mentions:
  - "生成功能架构图"
  - "画一个功能架构"
  - "create a functional architecture diagram"
  - "generate product architecture"
author: KK
---

# Functional Architecture Generator

该技能通过 `LLM -> YAML -> Python -> Jinja2` 的标准工作流，将非结构化的功能描述转化为结构化的、具备专业演示水准的功能架构图。

> [!IMPORTANT]
> **双重输出规范 (Dual Output Standard)**: 
> 当你使用此 Skill 时，必须**同时**输出两个部分：
> 1. **结构化 YAML**: 用于下一步的自动化处理和数据存档。
> 2. **交互式 HTML**: 用于最终用户的直观审查与演示。
> 
> **输出路径与命名规范 (Output Path & Naming Convention)**:
> - **目录**: 所有输出文件必须放在当前工作目录下的一个新子目录中，目录名为 `[公司/业务名]` (例如：`张雪机车海外销售/`)。
> - **文件名**: HTML 文件名必须反映内容，格式为 `[公司/业务名]-[业务类型].html` (例如：`张雪机车海外销售-功能架构图.html`)。
> 
> **视觉设计规范 (Visual Design Standard)**:
> - **样式风格**: 默认按照 `ai4pm-skills/design.md` 进行样式输出。
> - **底色模式**: 默认使用 **浅色底 (Light Mode)**。
> - **页面布局**: HTML 内容占据页面 **85%** 宽度，保持简洁的 Header 设计（参考简洁 Header 规范）。

## 核心特性

- **高端视觉系统**：基于 HSL 的动态调色盘，内置入场动画与 Lucide 图标支持。
- **智能布局引擎**：根据功能点密集度自动计算模块列宽，确保视觉重心平衡。
- **丰富的元数据**：支持模块级别的 `status`（状态角标）、`importance`（高亮显示）和 `icon`（自定义图标）。
- **左中右布局**：支持标准的“三明治”式架构，包含外部集成接口（左/右）与分层核心（中）。

## 快速使用

### 1. 准备输入
提供一段关于产品功能的描述，或者直接提供结构化的功能列表。

### 2. 生成 YAML
LLM 会根据描述生成符合规范的 YAML 数据。

### 3. 编译 HTML
使用内置的 Python 编译器生成可视化 HTML。

```bash
python3 scripts/build_arch.py input.yaml output.html
```

## YAML 规范

### 全局字段
- `title`: 架构图标题
- `description`: 架构图简述

### 层级字段 (layers)
- `type`: 必填。可选值：`user_touchpoint`, `business_scenario`, `business_common`, `foundation`, `input_integration`, `output_integration`
- `name`: 层级显示名称
- `icon`: 可选。Lucide 图标名称（如 `users`, `zap`, `layers`）
- `modules`: 模块列表

### 模块字段 (modules)
- `name`: 模块名称
- `status`: 可选。如 `MVP`, `Core`, `Phase 2`（显示为角标）
- `importance`: 可选。`high` 会触发高亮边框
- `functions`: 功能点列表。可以是字符串，也可以是包含 `subFunctions` 的对象。

## YAML 规范示例

```yaml
title: "智慧零售平台"
description: "全渠道零售解决方案"
layers:
  - type: "user_touchpoint"
    name: "用户触点层"
    icon: "smartphone"
    modules:
      - name: "移动端"
        importance: "high"
        status: "Core"
        functions:
          - name: "小程序商城"
            subFunctions: ["首页", "搜索", "详情"]
          - name: "App 客户端"
  - type: "business_scenario"
    name: "业务场景层"
    modules:
      - name: "订单管理"
        status: "MVP"
        functions:
          - name: "下单流程"
          - name: "售后处理"
```

## 开发者参考

- **逻辑来源**: 参考 `AIProdArch` 项目的架构设计与视觉规范。
- **视觉风格**: Premium Glassmorphism & Staggered Animations.
- **依赖**: Python 3, Jinja2, PyYAML.
