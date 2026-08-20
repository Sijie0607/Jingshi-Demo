# L0 全景图架构 (Landscape Diagram)

## 关注点
- 业务全景展示，包含用户、外部集成、核心应用、微服务及技术栈。
- 采用典型的“三栏式”布局：左侧集成、中央核心、右侧技术栈。

## 输出 JSON 结构要求
```json
{
  "level": "l0",
  "title": "系统全景架构图",
  "layout": "landscape",
  "actors": [
    { "id": "u1", "label": "🌍 海外买家" },
    { "id": "u2", "label": "🚢 跨境商家" }
  ],
  "left_panel": {
    "title": "上游/外部集成",
    "items": ["国际支付网关", "跨境物流服务"]
  },
  "right_panel": {
    "title": "技术栈",
    "items": ["Spring Cloud", "React / Flutter"]
  },
  "center": {
    "app_layer": {
      "title": "应用与网关层",
      "nodes": [
        { "id": "app1", "label": "买家端 App", "type": "container" }
      ]
    },
    "service_layer": {
      "title": "核心微服务",
      "nodes": [
        { "id": "svc1", "label": "商品服务", "type": "system", "color": "#FFE4E1" }
      ]
    }
  }
}
```

## 设计规范
- 中央区域必须分为“应用层”和“服务层”。
- 应用层通常使用深色背景节点，服务层使用莫兰迪彩虹色。
