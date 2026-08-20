# L3 组件架构 (Component Diagram)

## 关注点
- 单个容器内部的代码组件（Components）。
- 常用架构模式（如 Onion Architecture, DDD Layers）。
- 关注接口定义与依赖关系。

## 输出 JSON 结构要求
```json
{
  "level": "l3",
  "title": "服务名称",
  "nodes": [
    { "id": "p1", "label": "展示层", "type": "component", "description": "Controllers" },
    { "id": "a1", "label": "应用层", "type": "component", "description": "Use Cases" },
    { "id": "d1", "label": "领域层", "type": "system", "description": "Aggregates" },
    { "id": "i1", "label": "基础设施", "type": "external", "description": "DB Impl" }
  ],
  "edges": [
    { "from": "p1", "to": "a1", "label": "调用" },
    { "from": "a1", "to": "d1", "label": "处理" },
    { "from": "i1", "to": "d1", "label": "依赖反转" }
  ]
}
```

## 设计规范
- 通常用于详细设计阶段。
- 区分业务组件与基础设施组件。
