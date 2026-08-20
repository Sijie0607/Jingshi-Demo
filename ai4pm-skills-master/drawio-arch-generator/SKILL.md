---
name: drawio-arch-generator
description: |
  根据系统描述，自动创建符合 C4 模型标准的高颜值 Draw.io 架构图。

  Triggers when user mentions:
  - "生成 drawio 架构图"
  - "画一个系统架构图"
  - "create a drawio architecture diagram"
  - "generate C4 diagram"
author: KK
---

# Drawio Architecture Generator

基于 `AIFlow` 架构设计规范提取的 Draw.io 专用生成技能。支持分层架构设计（L1-L3），并自动应用莫兰迪高级色系风格。

> [!IMPORTANT]
> **双重输出规范 (Dual Output Standard)**: 
> 当你使用此 Skill 时，必须**同时**输出两个部分：
> 1. **结构化 JSON**: 用于下一步的自动化处理和数据存档。
> 2. **可编辑 Draw.io (XML/HTML)**: 用于最终用户的直观审查与演示。HTML 预览页已集成“复制 JSON”功能，确保数据可溯源。
> 
> **输出路径与命名规范 (Output Path & Naming Convention)**:
> - **目录**: 所有输出文件必须放在当前工作目录下的一个新子目录中，目录名为 `[公司/业务名]` (例如：`张雪机车海外销售/`)。
> - **文件名**: HTML 文件名必须反映内容，格式为 `[公司/业务名]-[业务类型].html` (例如：`张雪机车海外销售-系统架构图.html`)。
> 
> **视觉设计规范 (Visual Design Standard)**:
> - **样式风格**: 默认按照 `ai4pm-skills/design.md` 进行样式输出。
> - **底色模式**: 默认使用 **浅色底 (Light Mode)**。
> - **页面布局**: HTML 内容占据页面 **85%** 宽度，保持简洁的 Header 设计（参考简洁 Header 规范）。


---

## 工作流 SOP

### Step 1 · 层级确认 (Mandatory)
在开始设计前，必须先向用户展示以下层级定义，并询问用户需要哪一层：
- **L0 (Landscape)**: 全景图模式，关注业务全貌、用户、集成与技术栈。
- **L1 (System Context)**: 关注用户、核心系统与外部系统的关系。
- **L2 (Container)**: 关注系统内部的逻辑容器（如 Web 应用、API 网关、数据库、微服务）。
- **L3 (Component)**: 关注单个容器内部的组件结构（如 DDD 四层架构、展示层、领域层等）。

### Step 2 · 架构方案设计
根据用户选择的层级，参考 `references/l1_prompts.md` 等文档，生成对应的 JSON 结构数据。

### Step 3 · 编译 .drawio 文件
使用 Python 脚本将 JSON 数据转化为标准 Draw.io XML：
```bash
python3 scripts/build_drawio.py examples/<name>.json examples/<name>.drawio
```

### Step 4 · 交付
告知用户文件已生成，用户可将其直接拖入 [draw.io](https://app.diagrams.net/) 或飞书文档中继续编辑。

---

## 目录结构

```
drawio-arch-generator/
├── SKILL.md                # 本指南
├── references/
│   ├── l1_prompts.md       # L1 层级专家提示词
│   ├── l2_prompts.md       # L2 层级专家提示词
│   ├── l3_prompts.md       # L3 层级专家提示词
│   └── theme_config.json   # 莫兰迪色系配置
├── scripts/
│   └── build_drawio.py     # JSON to Drawio XML 编译器
├── templates/
│   └── preview_layout.html # 预览页面模板
└── examples/               # 成果存放地 (数据已与 AIFlow sample-drawio.ts 同步)
    ├── global_mall_l0.json # GlobalMall L0 全景图
    ├── global_mall_l1.json # GlobalMall L1 上下文
    └── ai_chatbot_l0.json  # AI Chatbot L0 全景图
```

## 视觉规范

本技能统一采用 **Morandi** 高级色系：
- **Person**: `#B0BEC5` (灰蓝)
- **System**: `#EACBCB` (莫兰迪粉)
- **Container**: `#B8CADD` (莫兰迪蓝)
- **Component**: `#CAD6D2` (莫兰迪绿)
- **External**: `#F5F5F5` (浅灰)
- **Infra**: `#EFEBE0` (莫兰迪黄)
