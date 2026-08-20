#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import yaml
from jinja2 import Environment, FileSystemLoader

def strip_markdown(text):
    """
    移除 LLM 可能会输出的 ```yaml ... ``` 代码块标记
    """
    text = text.strip()
    if text.startswith("```"):
        match = re.search(r"^```\w*\n(.*?)\n```$", text, re.DOTALL)
        if match:
            text = match.group(1).strip()
        else:
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
    return text

def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]

def process_arch_data(data):
    """
    数据清洗与标准化，并计算布局
    """
    clean_data = {
        "title": data.get("title", "产品功能架构图"),
        "description": data.get("description", ""),
        "layers": []
    }
    
    # 定义层级顺序和默认名称及图标
    layer_configs = {
        "user_touchpoint": {"default_name": "用户渠道触点层", "order": 1, "max_cols": 4, "icon": "users"},
        "business_scenario": {"default_name": "业务场景能力层", "order": 2, "max_cols": 4, "icon": "layout"},
        "business_common": {"default_name": "业务通用能力层", "order": 3, "max_cols": 4, "icon": "box"},
        "foundation": {"default_name": "基础通用能力层", "order": 4, "max_cols": 4, "icon": "database"},
        "input_integration": {"default_name": "输入集成接口", "order": 5, "max_cols": 1, "icon": "arrow-right-circle"},
        "output_integration": {"default_name": "输出集成接口", "order": 6, "max_cols": 1, "icon": "arrow-left-circle"}
    }
    
    raw_layers = data.get("layers", [])
    if not isinstance(raw_layers, list):
        raw_layers = []
        
    processed_layers = []
    for layer in raw_layers:
        l_type = layer.get("type", "unknown")
        if l_type not in layer_configs:
            continue
            
        l_data = {
            "id": layer.get("id", f"layer-{l_type}"),
            "type": l_type,
            "name": layer.get("name", layer_configs[l_type]["default_name"]),
            "icon": layer.get("icon", layer_configs[l_type]["icon"]),
            "order": layer_configs[l_type]["order"],
            "modules": []
        }
        
        # 处理模块
        modules = ensure_list(layer.get("modules", []))
        if not modules:
            continue

        # 计算该层模块的布局
        total_functions = 0
        module_stats = []
        for i, module in enumerate(modules):
            functions = ensure_list(module.get("functions", []))
            f_count = 0
            for f in functions:
                if isinstance(f, dict):
                    # 包含子功能，权重增加
                    f_count += 1 + len(ensure_list(f.get("subFunctions", []))) * 0.2
                else:
                    f_count += 1
            
            total_functions += f_count
            module_stats.append({
                "index": i,
                "f_weight": f_count,
                "functions": functions
            })

        max_total_cols = layer_configs[l_type]["max_cols"]
        
        if l_type in ["input_integration", "output_integration"]:
            total_cols = 1
            for m in module_stats:
                m["col_span"] = 1
        else:
            # 动态计算 col_span
            if len(modules) <= 1:
                total_cols = 1
                if module_stats: module_stats[0]["col_span"] = 1
            elif len(modules) <= max_total_cols:
                # 尝试根据权重分配 span
                avg_w = total_functions / max_total_cols if total_functions > 0 else 1
                current_total = 0
                for m in module_stats:
                    span = max(1, min(max_total_cols, round(m["f_weight"] / avg_w) if avg_w > 0 else 1))
                    m["col_span"] = span
                    current_total += span
                
                # 修正：如果总 span 超过 max_cols，且模块数 <= max_cols，则全部设为 1
                if current_total > max_total_cols:
                    for m in module_stats:
                        m["col_span"] = 1
                    total_cols = len(modules)
                else:
                    total_cols = max_total_cols
            else:
                # 模块数超过 max_cols，强制全部为 1，且列数扩展
                for m in module_stats:
                    m["col_span"] = 1
                total_cols = max_total_cols # 保持 4 列，多出的换行
        
        l_data["total_cols"] = total_cols

        for m_stat in module_stats:
            module = modules[m_stat["index"]]
            m_data = {
                "name": module.get("name", "未命名模块"),
                "description": module.get("description", ""),
                "col_span": m_stat["col_span"],
                "icon": module.get("icon", ""), # 模块可选图标
                "status": module.get("status", ""), # 模块状态 (MVP, Phase 2 等)
                "importance": module.get("importance", "normal"), # normal, high
                "functions": []
            }
            
            for func in m_stat["functions"]:
                if isinstance(func, str):
                    f_data = {"name": func, "subFunctions": [], "status": ""}
                else:
                    f_data = {
                        "name": func.get("name", "未命名功能"),
                        "subFunctions": ensure_list(func.get("subFunctions", [])),
                        "status": func.get("status", ""),
                        "importance": func.get("importance", "normal")
                    }
                m_data["functions"].append(f_data)
            
            l_data["modules"].append(m_data)
        
        processed_layers.append(l_data)
    
    # 分组：中央层、左侧层、右侧层、底部层
    groups = {
        "central": [],
        "left": [],
        "right": [],
        "bottom": []
    }
    
    for layer in processed_layers:
        if layer["type"] == "input_integration":
            groups["left"].append(layer)
        elif layer["type"] == "output_integration":
            groups["right"].append(layer)
        elif layer["type"] == "foundation":
            groups["bottom"].append(layer)
        else:
            groups["central"].append(layer)
            
    # 排序
    groups["central"].sort(key=lambda x: x["order"])
    
    clean_data["groups"] = groups
    return clean_data

def compile_arch(yaml_path, output_html_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    clean_yaml_str = strip_markdown(raw_content)

    try:
        data = yaml.safe_load(clean_yaml_str)
    except Exception as e:
        print(f"❌ YAML 解析失败: {e}")
        sys.exit(1)

    arch_data = process_arch_data(data)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(script_dir), "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    try:
        template = env.get_template("arch_layout.html")
    except Exception as e:
        print(f"❌ 找不到模板文件 arch_layout.html")
        sys.exit(1)

    # Read raw yaml for embedding
    with open(yaml_path, "r", encoding="utf-8") as f:
        raw_yaml_content = f.read()

    html_content = template.render(data=arch_data, raw_yaml=raw_yaml_content)

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Functional Architecture 编译成功！")
    print(f"📄 输出文件: {output_html_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 build_arch.py <input.yaml> <output.html>")
        sys.exit(1)
        
    input_yaml = sys.argv[1]
    output_html = sys.argv[2]
    compile_arch(input_yaml, output_html)
