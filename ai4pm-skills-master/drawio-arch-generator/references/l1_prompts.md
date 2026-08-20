# L1 系统上下文架构 (System Context)

## 关注点
- 系统在整个业务环境中的位置。
- 哪些人（Actors）在使用这个系统。
- 这个系统依赖哪些外部系统（External Systems）。

## 输出 JSON 结构要求
```json
{
  "level": "l1",
  "title": "系统名称",
  "nodes": [
    { "id": "u1", "label": "用户角色", "type": "person", "layer": "actor" },
    { "id": "s1", "label": "核心系统", "type": "system", "layer": "core" },
    { "id": "e1", "label": "外部系统", "type": "external", "layer": "external" }
  ],
  "edges": [
    { "from": "u1", "to": "s1", "label": "使用/访问" },
    { "from": "s1", "to": "e1", "label": "调用接口" }
  ]
}
```

## 设计规范
- 保持简洁，不涉及技术实现细节。
- 使用业务语言描述连接。
