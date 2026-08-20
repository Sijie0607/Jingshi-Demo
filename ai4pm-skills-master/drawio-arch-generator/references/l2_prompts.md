# L2 容器架构 (Container Diagram)

## 关注点
- 系统的软件架构：Web 应用、移动应用、API、数据库等。
- 容器之间的技术协议（HTTP/gRPC/SQL）。
- 系统边界（Boundary）。

## 输出 JSON 结构要求
```json
{
  "level": "l2",
  "title": "系统名称",
  "groups": [
    { "id": "boundary1", "label": "内部网络 (Intranet)", "type": "boundary" }
  ],
  "nodes": [
    { "id": "c1", "label": "前端 App", "type": "container", "technology": "React", "layer": "frontend" },
    { "id": "c2", "label": "API 网关", "type": "container", "technology": "Nginx", "layer": "gateway" },
    { "id": "c3", "label": "业务服务", "type": "container", "technology": "Spring", "parentId": "boundary1", "layer": "service" },
    { "id": "d1", "label": "主数据库", "type": "infra", "technology": "MySQL", "parentId": "boundary1", "layer": "data" }
  ],
  "edges": [
    { "from": "c1", "to": "c2", "label": "HTTPS/JSON" },
    { "from": "c2", "to": "c3", "label": "gRPC" },
    { "from": "c3", "to": "d1", "label": "SQL" }
  ]
}
```

## 设计规范
- 明确标注技术栈（Technology）。
- 展示主要的数据流向。
