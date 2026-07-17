import datetime
import html
import json
import os
import sys

import yaml


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def build_html(data: dict) -> str:
    title = html.escape(data.get("title", "AI机会地图"))
    generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data_json = json.dumps(data, ensure_ascii=False)

    template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #f5f7fb;
      --panel: #ffffff;
      --panel-soft: #f8fafc;
      --text: #10213e;
      --muted: #5f6b7a;
      --border: #d9e2ec;
      --accent: #2d6cdf;
      --shadow: 0 10px 30px rgba(16, 33, 62, 0.08);
      --radius: 16px;
      --hh: #d9485f;
      --hl: #7c4dff;
      --lh: #f59e0b;
      --ll: #94a3b8;
      --nlp: #2563eb;
      --decision: #7c3aed;
      --predict: #0f766e;
      --vision: #dc2626;
      --interaction: #ea580c;
      --doc: #475569;
      --ready: #0f766e;
      --growth: #2563eb;
      --explore: #8b5cf6;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      background: linear-gradient(180deg, #f7f9fc 0%, #eef3f8 100%);
      color: var(--text);
    }
    .page {
      width: min(1500px, 92vw);
      margin: 28px auto 48px;
    }
    .hero {
      background: linear-gradient(135deg, #0f1f3d 0%, #19386f 70%, #2b5fb8 100%);
      color: #fff;
      border-radius: 24px;
      padding: 28px 30px 24px;
      box-shadow: var(--shadow);
    }
    .hero-top {
      display: flex;
      justify-content: space-between;
      gap: 20px;
      align-items: flex-start;
      flex-wrap: wrap;
    }
    .hero h1 {
      margin: 0 0 12px;
      font-size: clamp(26px, 3vw, 36px);
      line-height: 1.15;
    }
    .hero p {
      margin: 0;
      max-width: 900px;
      color: rgba(255,255,255,0.84);
      line-height: 1.7;
      font-size: 14px;
    }
    .hero-meta {
      font-size: 12px;
      color: rgba(255,255,255,0.75);
      text-align: right;
      min-width: 160px;
    }
    .metrics {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 22px;
    }
    .metric {
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 16px;
      padding: 14px 16px;
      backdrop-filter: blur(8px);
    }
    .metric .label {
      font-size: 12px;
      color: rgba(255,255,255,0.72);
      margin-bottom: 8px;
    }
    .metric .value {
      font-size: 28px;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 6px;
    }
    .metric .hint {
      font-size: 12px;
      color: rgba(255,255,255,0.78);
    }
    .section {
      margin-top: 22px;
      background: var(--panel);
      border: 1px solid rgba(148, 163, 184, 0.16);
      border-radius: 24px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }
    .section-head {
      padding: 22px 24px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: flex-start;
      flex-wrap: wrap;
    }
    .section-head h2 {
      margin: 0 0 8px;
      font-size: 22px;
    }
    .section-head p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: 14px;
      max-width: 860px;
    }
    .filters {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      padding: 18px 24px;
      border-bottom: 1px solid var(--border);
      background: var(--panel-soft);
    }
    .filters input,
    .filters select {
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      border-radius: 12px;
      padding: 10px 12px;
      font-size: 13px;
      min-height: 40px;
    }
    .filters input {
      min-width: min(320px, 100%);
      flex: 1 1 280px;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      border-radius: 999px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 600;
      line-height: 1;
      white-space: nowrap;
    }
    .quadrant-high_value_high_priority { background: rgba(217,72,95,0.12); color: var(--hh); }
    .quadrant-high_value_low_priority { background: rgba(124,77,255,0.12); color: var(--hl); }
    .quadrant-low_value_high_priority { background: rgba(245,158,11,0.14); color: #b45309; }
    .quadrant-low_value_low_priority { background: rgba(148,163,184,0.18); color: #475569; }
    .maturity-ready { background: rgba(15,118,110,0.12); color: var(--ready); }
    .maturity-growth { background: rgba(37,99,235,0.12); color: var(--growth); }
    .maturity-explore { background: rgba(139,92,246,0.12); color: var(--explore); }
    .maturity-high { background: rgba(245,158,11,0.14); color: #b45309; }
    .maturity-medium { background: rgba(37,99,235,0.12); color: #1d4ed8; }
    .maturity-low { background: rgba(148,163,184,0.18); color: #475569; }
    .tech {
      background: #f1f5f9;
      color: #334155;
      border: 1px solid #e2e8f0;
    }
    .map-layout {
      display: grid;
      grid-template-columns: minmax(0, 1.7fr) minmax(340px, 0.9fr);
      gap: 0;
      min-height: 700px;
    }
    .map-area {
      border-right: 1px solid var(--border);
      overflow: auto;
      padding: 20px;
      background:
        linear-gradient(180deg, rgba(248,250,252,0.4) 0%, rgba(248,250,252,0) 100%);
    }
    .detail-panel {
      padding: 22px;
      background: #fcfdff;
      position: sticky;
      top: 0;
      max-height: calc(100vh - 32px);
      overflow: auto;
    }
    .detail-empty {
      padding: 14px 0;
      color: var(--muted);
      line-height: 1.7;
      font-size: 14px;
    }
    .stage-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(280px, 1fr));
      gap: 16px;
      min-width: 1420px;
      align-items: start;
    }
    .stage-column {
      background: #fbfdff;
      border: 1px solid #dde6f1;
      border-radius: 18px;
      padding: 14px;
      box-shadow: 0 4px 20px rgba(31, 59, 96, 0.04);
    }
    .stage-header {
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px solid #e6edf5;
    }
    .stage-order {
      display: inline-flex;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      align-items: center;
      justify-content: center;
      background: #e8f0ff;
      color: var(--accent);
      font-weight: 700;
      font-size: 12px;
      margin-bottom: 10px;
    }
    .stage-header h3 {
      margin: 0 0 6px;
      font-size: 17px;
      line-height: 1.35;
    }
    .stage-header p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.55;
    }
    .subhead {
      font-size: 12px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #5b6f8e;
      margin: 16px 0 10px;
      font-weight: 700;
    }
    .node-card,
    .opp-card,
    .doc-card {
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 14px;
      padding: 14px;
      transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .node-card,
    .opp-card {
      cursor: pointer;
      margin-bottom: 10px;
    }
    .node-card:hover,
    .opp-card:hover,
    .doc-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
      border-color: #bfd0e3;
    }
    .node-card.active,
    .opp-card.active {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(45,108,223,0.12);
    }
    .node-card h4,
    .opp-card h4,
    .doc-card h4 {
      margin: 0 0 8px;
      font-size: 15px;
      line-height: 1.45;
    }
    .node-meta,
    .opp-meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
    .muted {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.6;
    }
    .mini-list,
    .detail-panel ul {
      margin: 0;
      padding-left: 18px;
      color: var(--text);
    }
    .mini-list li,
    .detail-panel li {
      margin-bottom: 6px;
      line-height: 1.6;
      font-size: 13px;
    }
    .node-count {
      font-size: 12px;
      color: #64748b;
      margin-top: 8px;
    }
    .opp-card {
      border-left: 6px solid #cbd5e1;
    }
    .opp-card.quadrant-high_value_high_priority { border-left-color: var(--hh); }
    .opp-card.quadrant-high_value_low_priority { border-left-color: var(--hl); }
    .opp-card.quadrant-low_value_high_priority { border-left-color: var(--lh); }
    .opp-card.quadrant-low_value_low_priority { border-left-color: var(--ll); }
    .detail-panel .section-title {
      font-size: 12px;
      color: #5b6f8e;
      margin: 18px 0 8px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .detail-panel h3 {
      margin: 0 0 10px;
      font-size: 22px;
      line-height: 1.35;
    }
    .detail-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }
    .btn {
      border: none;
      border-radius: 12px;
      padding: 10px 14px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
    }
    .btn-primary {
      background: var(--accent);
      color: #fff;
    }
    .btn-secondary {
      background: #eef4ff;
      color: var(--accent);
    }
    .doc-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 16px;
      padding: 20px 24px 26px;
    }
    .doc-card {
      scroll-margin-top: 24px;
    }
    .doc-card .doc-head {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 10px;
      align-items: center;
    }
    .doc-card p {
      margin: 8px 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }
    .footnote {
      padding: 0 24px 24px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.7;
    }
    .empty {
      color: var(--muted);
      font-size: 13px;
      padding: 10px 0 6px;
    }
    @media (max-width: 1180px) {
      .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .map-layout { grid-template-columns: 1fr; }
      .map-area { border-right: none; border-bottom: 1px solid var(--border); }
      .detail-panel { position: static; max-height: none; }
      .doc-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .page { width: min(96vw, 96vw); margin-top: 16px; }
      .hero { border-radius: 18px; padding: 20px 18px; }
      .section { border-radius: 18px; }
      .section-head, .filters, .map-area, .detail-panel, .doc-grid, .footnote { padding-left: 16px; padding-right: 16px; }
      .metrics { grid-template-columns: 1fr; }
      .filters { gap: 8px; }
      .filters input, .filters select { width: 100%; }
    }
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <div class="hero-top">
        <div>
          <h1>__TITLE__</h1>
          <p id="hero-scope"></p>
        </div>
        <div class="hero-meta">
          <div id="hero-company"></div>
          <div style="margin-top:8px;">生成时间：__GENERATED_AT__</div>
        </div>
      </div>
      <div class="metrics" id="metrics"></div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>AI机会地图</h2>
          <p>按业务流程顺序展示核心节点和AI落地场景。支持按机会分级、技术类型、业务阶段和关键词筛选，并可点击节点查看完整详情。</p>
        </div>
      </div>
      <div class="filters">
        <input id="searchInput" type="text" placeholder="搜索场景、节点、技术方向、痛点关键词" />
        <select id="quadrantFilter"></select>
        <select id="techFilter"></select>
        <select id="stageFilter"></select>
      </div>
      <div class="map-layout">
        <div class="map-area">
          <div class="stage-grid" id="stageGrid"></div>
        </div>
        <aside class="detail-panel" id="detailPanel"></aside>
      </div>
    </section>

    <section class="section">
      <div class="section-head">
        <div>
          <h2>AI场景详细说明文档</h2>
          <p>完整保留全部AI机会点的核心信息，包括应用价值、核心问题、技术实现方向、数据要求和预期指标，便于后续讨论和方案细化。</p>
        </div>
      </div>
      <div class="doc-grid" id="docGrid"></div>
      <div class="footnote" id="footnote"></div>
    </section>
  </div>

  <script>
    const data = __DATA__;
    const state = {
      quadrant: 'all',
      tech: 'all',
      stage: 'all',
      search: '',
      selectedKind: 'opportunity',
      selectedId: null
    };

    const quadrantLabel = data.quadrant_definition || {};
    const stages = data.stages || [];
    const opportunities = data.opportunities || [];
    const nodeMap = new Map();
    stages.forEach(stage => {
      (stage.nodes || []).forEach(node => {
        node.stage_id = stage.id;
        node.stage_name = stage.name;
        nodeMap.set(node.id, node);
      });
    });
    const opportunityMap = new Map(opportunities.map(opp => [opp.id, opp]));

    function quadrantText(key) {
      return quadrantLabel[key] || key;
    }

    function byId(id) {
      return document.getElementById(id);
    }

    function techOptions() {
      const set = new Set();
      opportunities.forEach(opp => (opp.tech_types || []).forEach(item => set.add(item)));
      return Array.from(set);
    }

    function countTotalNodes() {
      return stages.reduce((sum, stage) => sum + (stage.nodes || []).length, 0);
    }

    function coverageRate() {
      const covered = new Set();
      opportunities.forEach(opp => (opp.node_ids || []).forEach(id => covered.add(id)));
      const total = countTotalNodes();
      return total ? Math.round((covered.size / total) * 100) : 0;
    }

    function quadrantCounts() {
      const counts = {};
      opportunities.forEach(opp => {
        counts[opp.quadrant] = (counts[opp.quadrant] || 0) + 1;
      });
      return counts;
    }

    function linkedOpportunities(nodeId) {
      return opportunities.filter(opp => (opp.node_ids || []).includes(nodeId));
    }

    function linkedNodes(opp) {
      return (opp.node_ids || []).map(id => nodeMap.get(id)).filter(Boolean);
    }

    function matchesSearch(opp) {
      if (!state.search) return true;
      const keyword = state.search.toLowerCase();
      const nodeNames = linkedNodes(opp).map(node => node.name).join(' ');
      const haystack = [
        opp.name,
        opp.scenario_summary,
        opp.core_problem,
        opp.application_value,
        (opp.tech_types || []).join(' '),
        (opp.technical_direction || []).join(' '),
        nodeNames
      ].join(' ').toLowerCase();
      return haystack.includes(keyword);
    }

    function filteredOpportunities() {
      return opportunities.filter(opp => {
        if (state.quadrant !== 'all' && opp.quadrant !== state.quadrant) return false;
        if (state.tech !== 'all' && !(opp.tech_types || []).includes(state.tech)) return false;
        if (state.stage !== 'all' && opp.stage_id !== state.stage) return false;
        if (!matchesSearch(opp)) return false;
        return true;
      });
    }

    function renderHeader() {
      byId('hero-scope').textContent = data.analysis_scope || '';
      byId('hero-company').textContent = `${data.company || ''} · ${data.business_flow || ''}`;
      const counts = quadrantCounts();
      const metrics = [
        { label: '核心流程节点', value: countTotalNodes(), hint: `${stages.length} 个业务阶段` },
        { label: 'AI机会点', value: opportunities.length, hint: '覆盖全周期落地场景' },
        { label: '场景覆盖率', value: `${coverageRate()}%`, hint: '已覆盖流程关键节点' },
        { label: '高价值高优先级', value: counts.high_value_high_priority || 0, hint: '建议优先启动' }
      ];
      byId('metrics').innerHTML = metrics.map(item => `
        <div class="metric">
          <div class="label">${item.label}</div>
          <div class="value">${item.value}</div>
          <div class="hint">${item.hint}</div>
        </div>
      `).join('');
    }

    function renderFilters() {
      const quadrantEl = byId('quadrantFilter');
      const techEl = byId('techFilter');
      const stageEl = byId('stageFilter');

      quadrantEl.innerHTML = [
        ['all', '全部机会分级'],
        ['high_value_high_priority', quadrantText('high_value_high_priority')],
        ['high_value_low_priority', quadrantText('high_value_low_priority')],
        ['low_value_high_priority', quadrantText('low_value_high_priority')],
        ['low_value_low_priority', quadrantText('low_value_low_priority')]
      ].map(([value, label]) => `<option value="${value}">${label}</option>`).join('');

      techEl.innerHTML = ['<option value="all">全部技术类型</option>']
        .concat(techOptions().map(item => `<option value="${item}">${item}</option>`))
        .join('');

      stageEl.innerHTML = ['<option value="all">全部业务阶段</option>']
        .concat(stages.map(stage => `<option value="${stage.id}">${stage.name}</option>`))
        .join('');

      byId('searchInput').addEventListener('input', (e) => {
        state.search = e.target.value.trim();
        renderAll();
      });
      quadrantEl.addEventListener('change', (e) => {
        state.quadrant = e.target.value;
        renderAll();
      });
      techEl.addEventListener('change', (e) => {
        state.tech = e.target.value;
        renderAll();
      });
      stageEl.addEventListener('change', (e) => {
        state.stage = e.target.value;
        renderAll();
      });
    }

    function stageOpportunities(stageId) {
      return filteredOpportunities().filter(opp => opp.stage_id === stageId);
    }

    function createNodeCard(node) {
      const card = document.createElement('div');
      const linked = linkedOpportunities(node.id);
      card.className = 'node-card';
      if (state.selectedKind === 'node' && state.selectedId === node.id) {
        card.classList.add('active');
      }
      card.innerHTML = `
        <h4>${node.name}</h4>
        <div class="node-meta">
          <span class="pill tech">${node.layer}</span>
          <span class="pill maturity-${node.data_foundation.readiness}">${node.data_foundation.readiness.toUpperCase()}</span>
          <span class="pill tech">${node.decision_complexity}</span>
        </div>
        <div class="muted">${node.pain_points[0] || ''}</div>
        <div class="node-count">关联AI场景：${linked.length} 个</div>
      `;
      card.addEventListener('click', () => {
        state.selectedKind = 'node';
        state.selectedId = node.id;
        renderAll();
      });
      return card;
    }

    function createOpportunityCard(opp) {
      const card = document.createElement('div');
      card.className = `opp-card quadrant-${opp.quadrant}`;
      if (state.selectedKind === 'opportunity' && state.selectedId === opp.id) {
        card.classList.add('active');
      }
      card.innerHTML = `
        <h4>${opp.name}</h4>
        <div class="opp-meta">
          <span class="pill quadrant-${opp.quadrant}">${quadrantText(opp.quadrant)}</span>
          <span class="pill maturity-${opp.maturity}">${opp.maturity.toUpperCase()}</span>
          <span class="pill tech">${(opp.tech_types || []).join(' / ')}</span>
        </div>
        <div class="muted">${opp.scenario_summary}</div>
      `;
      card.addEventListener('click', () => {
        state.selectedKind = 'opportunity';
        state.selectedId = opp.id;
        renderAll();
      });
      return card;
    }

    function renderMap() {
      const grid = byId('stageGrid');
      grid.innerHTML = '';
      stages
        .filter(stage => state.stage === 'all' || state.stage === stage.id)
        .forEach(stage => {
          const column = document.createElement('section');
          column.className = 'stage-column';
          const opps = stageOpportunities(stage.id);
          const header = document.createElement('div');
          header.className = 'stage-header';
          header.innerHTML = `
            <div class="stage-order">${stage.order}</div>
            <h3>${stage.name}</h3>
            <p>${stage.objective}</p>
          `;
          column.appendChild(header);

          const nodeHead = document.createElement('div');
          nodeHead.className = 'subhead';
          nodeHead.textContent = '流程节点';
          column.appendChild(nodeHead);
          (stage.nodes || []).forEach(node => column.appendChild(createNodeCard(node)));

          const oppHead = document.createElement('div');
          oppHead.className = 'subhead';
          oppHead.textContent = `AI机会 (${opps.length})`;
          column.appendChild(oppHead);
          if (opps.length) {
            opps.forEach(opp => column.appendChild(createOpportunityCard(opp)));
          } else {
            const empty = document.createElement('div');
            empty.className = 'empty';
            empty.textContent = '当前筛选条件下暂无场景';
            column.appendChild(empty);
          }
          grid.appendChild(column);
        });
    }

    function renderNodeDetail(node) {
      const relatedOpps = linkedOpportunities(node.id);
      return `
        <h3>${node.name}</h3>
        <div class="opp-meta">
          <span class="pill tech">${node.stage_name}</span>
          <span class="pill tech">${node.layer}</span>
          <span class="pill maturity-${node.data_foundation.readiness}">数据就绪度 ${node.data_foundation.readiness}</span>
          <span class="pill tech">决策复杂度 ${node.decision_complexity}</span>
        </div>
        <div class="muted">${(node.primary_roles || []).join(' / ')} · ${(node.touchpoints || []).join(' / ')}</div>

        <div class="section-title">核心痛点</div>
        <ul>${(node.pain_points || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">效率瓶颈</div>
        <ul>${(node.efficiency_bottlenecks || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">体验提升空间</div>
        <ul>${(node.experience_improvement_space || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">数据基础</div>
        <div class="muted"><strong>可用数据：</strong>${(node.data_foundation.available_data || []).join(' / ')}</div>
        <ul>${(node.data_foundation.data_gaps || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">关联AI机会</div>
        <div class="detail-actions">
          ${relatedOpps.map(opp => `<button class="btn btn-secondary" data-opp-link="${opp.id}">${opp.name}</button>`).join('')}
        </div>
      `;
    }

    function renderOpportunityDetail(opp) {
      const nodes = linkedNodes(opp);
      return `
        <h3>${opp.name}</h3>
        <div class="opp-meta">
          <span class="pill quadrant-${opp.quadrant}">${quadrantText(opp.quadrant)}</span>
          <span class="pill maturity-${opp.maturity}">${opp.maturity.toUpperCase()}</span>
          <span class="pill tech">${opp.business_value_level === 'high' ? '高业务价值' : '低业务价值'}</span>
          <span class="pill tech">${opp.priority_level === 'high' ? '高实施优先级' : '低实施优先级'}</span>
        </div>
        <div class="muted">${opp.scenario_summary}</div>

        <div class="section-title">解决的核心问题</div>
        <div class="muted">${opp.core_problem}</div>

        <div class="section-title">应用价值</div>
        <div class="muted">${opp.application_value}</div>

        <div class="section-title">技术实现方向</div>
        <ul>${(opp.technical_direction || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">所需数据支撑</div>
        <ul>${(opp.required_data || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">预期业务指标</div>
        <ul>${(opp.expected_kpis || []).map(item => `<li>${item}</li>`).join('')}</ul>

        <div class="section-title">技术类型</div>
        <div class="opp-meta">${(opp.tech_types || []).map(item => `<span class="pill tech">${item}</span>`).join('')}</div>

        <div class="section-title">关联业务节点</div>
        <div class="detail-actions">
          ${nodes.map(node => `<button class="btn btn-secondary" data-node-link="${node.id}">${node.name}</button>`).join('')}
        </div>

        <div class="detail-actions">
          <button class="btn btn-primary" data-doc-link="${opp.id}">跳转详细说明</button>
        </div>
      `;
    }

    function ensureSelected() {
      const filtered = filteredOpportunities();
      const visibleStageIds = new Set(
        stages
          .filter(stage => state.stage === 'all' || stage.id === state.stage)
          .map(stage => stage.id)
      );
      const visibleNodeIds = new Set(
        stages
          .filter(stage => visibleStageIds.has(stage.id))
          .flatMap(stage => stage.nodes || [])
          .map(node => node.id)
      );
      if (state.selectedKind === 'opportunity' && state.selectedId && filtered.some(opp => opp.id === state.selectedId)) {
        return;
      }
      if (state.selectedKind === 'node' && state.selectedId && visibleNodeIds.has(state.selectedId)) {
        return;
      }
      if (filtered.length) {
        state.selectedKind = 'opportunity';
        state.selectedId = filtered[0].id;
      } else {
        const firstNode = stages
          .filter(stage => visibleStageIds.has(stage.id))
          .flatMap(stage => stage.nodes || [])[0];
        state.selectedKind = firstNode ? 'node' : 'opportunity';
        state.selectedId = firstNode ? firstNode.id : null;
      }
    }

    function renderDetailPanel() {
      ensureSelected();
      const panel = byId('detailPanel');
      if (!state.selectedId) {
        panel.innerHTML = '<div class="detail-empty">暂无可展示内容。</div>';
        return;
      }
      if (state.selectedKind === 'node') {
        const node = nodeMap.get(state.selectedId);
        panel.innerHTML = node ? renderNodeDetail(node) : '<div class="detail-empty">未找到节点详情。</div>';
      } else {
        const opp = opportunityMap.get(state.selectedId);
        panel.innerHTML = opp ? renderOpportunityDetail(opp) : '<div class="detail-empty">未找到场景详情。</div>';
      }
      panel.querySelectorAll('[data-opp-link]').forEach(btn => {
        btn.addEventListener('click', () => {
          state.selectedKind = 'opportunity';
          state.selectedId = btn.dataset.oppLink;
          renderAll();
        });
      });
      panel.querySelectorAll('[data-node-link]').forEach(btn => {
        btn.addEventListener('click', () => {
          state.selectedKind = 'node';
          state.selectedId = btn.dataset.nodeLink;
          renderAll();
        });
      });
      panel.querySelectorAll('[data-doc-link]').forEach(btn => {
        btn.addEventListener('click', () => {
          const target = document.getElementById(`doc-${btn.dataset.docLink}`);
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            target.style.boxShadow = '0 0 0 3px rgba(45,108,223,0.18)';
            setTimeout(() => { target.style.boxShadow = ''; }, 1600);
          }
        });
      });
    }

    function renderDocs() {
      const grid = byId('docGrid');
      const filtered = filteredOpportunities();
      const base = filtered.length ? filtered : opportunities;
      grid.innerHTML = '';
      base.forEach(opp => {
        const nodes = linkedNodes(opp);
        const card = document.createElement('article');
        card.className = 'doc-card';
        card.id = `doc-${opp.id}`;
        card.innerHTML = `
          <div class="doc-head">
            <h4 style="margin:0;">${opp.name}</h4>
            <span class="pill quadrant-${opp.quadrant}">${quadrantText(opp.quadrant)}</span>
            <span class="pill maturity-${opp.maturity}">${opp.maturity.toUpperCase()}</span>
          </div>
          <p><strong>所属阶段：</strong>${stages.find(stage => stage.id === opp.stage_id)?.name || ''}</p>
          <p><strong>关联节点：</strong>${nodes.map(node => node.name).join(' / ')}</p>
          <p><strong>应用价值：</strong>${opp.application_value}</p>
          <p><strong>核心问题：</strong>${opp.core_problem}</p>
          <p><strong>技术实现方向：</strong>${(opp.technical_direction || []).join('；')}</p>
          <p><strong>所需数据：</strong>${(opp.required_data || []).join('；')}</p>
          <p><strong>预期业务指标：</strong>${(opp.expected_kpis || []).join('；')}</p>
        `;
        card.addEventListener('click', () => {
          state.selectedKind = 'opportunity';
          state.selectedId = opp.id;
          renderAll(false);
        });
        grid.appendChild(card);
      });
      byId('footnote').innerHTML = `
        <strong>结论：</strong>${data.analysis_conclusion.coverage_statement}
        <br />
        <strong>建议实施顺序：</strong>${(data.analysis_conclusion.implementation_sequence || []).join('；')}
      `;
    }

    function renderAll(scrollTop = true) {
      renderMap();
      renderDetailPanel();
      renderDocs();
      if (scrollTop) {
        document.querySelector('.map-area').scrollTop = 0;
      }
    }

    renderHeader();
    renderFilters();
    renderAll(false);
  </script>
</body>
</html>
"""

    return (
        template.replace("__TITLE__", title)
        .replace("__GENERATED_AT__", generated_at)
        .replace("__DATA__", data_json)
    )


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 build_custom_ai_opportunity_map.py <input.yaml> <output.html>")
        sys.exit(1)

    input_yaml = sys.argv[1]
    output_html = sys.argv[2]

    data = load_yaml(input_yaml)
    html_content = build_html(data)

    os.makedirs(os.path.dirname(os.path.abspath(output_html)), exist_ok=True)
    with open(output_html, "w", encoding="utf-8") as f:
      f.write(html_content)

    print(f"✅ Generated custom AI opportunity map → {output_html}")


if __name__ == "__main__":
    main()
