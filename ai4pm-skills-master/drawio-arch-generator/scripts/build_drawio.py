import json
import sys
import os
import html

# Enhanced Morandi Theme Styles
THEME = {
    "colors": {
        "person": "#B0BEC5",
        "system": "#EACBCB",
        "container": "#B8CADD",
        "component": "#CAD6D2",
        "external": "#F5F5F5",
        "infra": "#EFEBE0",
        "relation": "#B0BEC5",
        "boundary": "#F8FAFC",
        "app": "#455A64", 
        "bff": "#ECEFF1",
        "panel": "#F8FAFC"
    }
}

STYLES = {
    "person": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['person']};fontColor=#FFFFFF;strokeColor=none;arcSize=4;fontSize=14;fontStyle=1;",
    "system": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['system']};fontColor=#2C3E50;strokeColor=none;arcSize=6;fontSize=14;",
    "container": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['container']};fontColor=#2C3E50;strokeColor=none;arcSize=6;fontSize=14;",
    "component": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['component']};fontColor=#2C3E50;strokeColor=none;arcSize=4;fontSize=14;",
    "external": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['external']};fontColor=#606F7B;strokeColor=#E1E8ED;arcSize=6;fontSize=14;strokeWidth=1;",
    "infra": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['infra']};fontColor=#2C3E50;strokeColor=none;arcSize=4;fontSize=14;",
    "boundary": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['boundary']};fontColor=#64748b;strokeColor=#cbd5e1;strokeWidth=2;dashed=1;align=left;verticalAlign=top;spacingLeft=10;spacingTop=5;fontSize=12;fontStyle=1;",
    "relation": f"endArrow=blockThin;html=1;fontSize=11;fontColor=#606F7B;strokeWidth=1;endFill=1;strokeColor={THEME['colors']['relation']};rounded=1;edgeStyle=orthogonalEdgeStyle;dashed=1;endSize=6;jumpStyle=line;",
    "app": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['app']};fontColor=#FFFFFF;strokeColor=none;arcSize=6;fontSize=14;fontStyle=1;",
    "bff": f"rounded=1;whiteSpace=wrap;html=1;fillColor={THEME['colors']['bff']};fontColor=#455A64;strokeColor=none;arcSize=4;fontSize=13;",
    "svc": "rounded=1;whiteSpace=wrap;html=1;fillColor={color};fontColor=#2C3E50;strokeColor=none;arcSize=6;fontSize=14;fontStyle=1;",
    "boundary_dashed": "rounded=1;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#cbd5e1;strokeWidth=2;dashed=1;dashPattern=8 8;align=left;verticalAlign=top;spacingLeft=10;spacingTop=5;fontSize=12;fontColor=#94a3b8;",
    "panel": "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#e2e8f0;strokeWidth=1;align=center;verticalAlign=top;spacingTop=20;fontSize=14;fontStyle=1;fontColor=#475569;",
    "text_item": "text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=12;fontColor=#64748b;"
}

LAYER_MAP = {
    "actor": 0, "frontend": 1, "gateway": 1, "core": 2, "service": 2, "component": 2, "data": 3, "infra": 3, "external": 1.5
}

def generate_drawio_xml(data):
    level = data.get("level", "l1")
    xml_header = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" modified="2024-01-01T00:00:00.000Z" agent="5.0" etag="xxx" version="22.1.2" type="device">
  <diagram id="diagram_1" name="Page-1">
    <mxGraphModel dx="1422" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1000" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
"""
    xml_footer = """      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

    cells_xml = []
    
    if level == "l0":
        # --- L0 LANDSCAPE LAYOUT ---
        actors = data.get("actors", [])
        actor_w, actor_h, start_x = 160, 40, 450
        for i, actor in enumerate(actors):
            x = start_x + i * 250
            cells_xml.append(f'<mxCell id="actor_{i}" value="{html.escape(actor["label"])}" style="text;html=1;align=center;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=16;fontStyle=1;fontColor=#1e293b;" vertex="1" parent="1"><mxGeometry x="{x}" y="40" width="{actor_w}" height="{actor_h}" as="geometry" /></mxCell>')

        for panel_key, x_pos, width, height in [("left_panel", 40, 180, 500), ("right_panel", 1180, 180, 500)]:
            panel = data.get(panel_key, {})
            cells_xml.append(f'<mxCell id="{panel_key}" value="{html.escape(panel.get("title",""))}" style="{STYLES["panel"]}" vertex="1" parent="1"><mxGeometry x="{x_pos}" y="220" width="{width}" height="{height}" as="geometry" /></mxCell>')
            for i, item in enumerate(panel.get("items", [])):
                cells_xml.append(f'<mxCell id="{panel_key}_i_{i}" value="{html.escape(item)}" style="{STYLES["text_item"]}" vertex="1" parent="{panel_key}"><mxGeometry x="0" y="{60 + i*40}" width="{width}" height="30" as="geometry" /></mxCell>')

        center = data.get("center", {})
        app_layer = center.get("app_layer", {})
        cells_xml.append(f'<mxCell id="app_boundary" value="{html.escape(app_layer.get("title",""))}" style="{STYLES["boundary_dashed"]}" vertex="1" parent="1"><mxGeometry x="260" y="260" width="880" height="240" as="geometry" /></mxCell>')
        
        apps = [n for n in app_layer.get("nodes", []) if n["type"] == "app"]
        for i, node in enumerate(apps):
            cells_xml.append(f'<mxCell id="{node["id"]}" value="{html.escape(node["label"])}" style="{STYLES["app"]}" vertex="1" parent="app_boundary"><mxGeometry x="{20 + i*280}" y="80" width="180" height="70" as="geometry" /></mxCell>')
        
        bffs = [n for n in app_layer.get("nodes", []) if n["type"] == "bff"]
        for i, node in enumerate(bffs):
            cells_xml.append(f'<mxCell id="{node["id"]}" value="{html.escape(node["label"])}" style="{STYLES["bff"]}" vertex="1" parent="app_boundary"><mxGeometry x="{20 + i*215}" y="170" width="160" height="50" as="geometry" /></mxCell>')

        svc_layer = center.get("service_layer", {})
        cells_xml.append(f'<mxCell id="svc_title" value="{html.escape(svc_layer.get("title",""))}" style="text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;fontSize=12;fontColor=#94a3b8;" vertex="1" parent="1"><mxGeometry x="260" y="530" width="100" height="30" as="geometry" /></mxCell>')
        for i, svc in enumerate(svc_layer.get("nodes", [])):
            style = STYLES["svc"].format(color=svc.get("color", "#E2F0FF"))
            cells_xml.append(f'<mxCell id="{svc["id"]}" value="{html.escape(svc["label"])}" style="{style}" vertex="1" parent="1"><mxGeometry x="{260 + (i%4)*225}" y="{570 + (i//4)*110}" width="180" height="80" as="geometry" /></mxCell>')

    else:
        # L1/L2/L3 Layout logic
        groups, nodes, edges = data.get("groups", []), data.get("nodes", []), data.get("edges", [])
        for g in groups:
            cells_xml.append(f'<mxCell id="{g["id"]}" value="{html.escape(g["label"])}" style="{STYLES["boundary"]}" vertex="1" parent="1"><mxGeometry x="50" y="50" width="1000" height="600" as="geometry" /></mxCell>')
        
        layer_counts = {}
        for node in sorted(nodes, key=lambda n: LAYER_MAP.get(n.get("layer", "core"), 2)):
            l_idx = LAYER_MAP.get(node.get("layer", "core"), 2)
            pos = layer_counts.get(l_idx, 0); layer_counts[l_idx] = pos + 1
            label = node["label"] + (f"<br/><i>({node['technology']})</i>" if "technology" in node else "")
            cells_xml.append(f'<object label="{html.escape(label)}" id="{node["id"]}"><mxCell style="{STYLES.get(node.get("type", "system"), STYLES["system"])}" vertex="1" parent="{node.get("parentId", "1")}"><mxGeometry x="{100 + pos*280}" y="{100 + l_idx*200}" width="180" height="80" as="geometry" /></mxCell></object>')

        for i, edge in enumerate(edges):
            cells_xml.append(f'<object label="{html.escape(edge.get("label", ""))}" id="edge_{i}"><mxCell style="{STYLES["relation"]}" edge="1" parent="1" source="{edge["from"]}" target="{edge["to"]}"><mxGeometry relative="1" as="geometry" /></mxCell></object>')

    return xml_header + "\n".join(cells_xml) + "\n" + xml_footer

from jinja2 import Environment, FileSystemLoader

def generate_html(xml_content, raw_json, output_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(script_dir, '..', 'templates')
    
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('preview_layout.html')
    
    html_content = template.render(
        DRAWIO_XML=xml_content,
        raw_json=raw_json
    )
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(1)
    input_path = sys.argv[1]
    output_drawio = sys.argv[2]
    
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_json = f.read()
        data = json.loads(raw_json)
        
    xml_content = generate_drawio_xml(data)
    
    with open(output_drawio, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    generate_html(xml_content, raw_json, output_drawio.replace('.drawio', '.html'))
