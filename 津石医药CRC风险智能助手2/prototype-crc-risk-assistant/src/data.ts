export type RiskLevel = 'critical' | 'high' | 'medium' | 'low'

export interface Persona {
  id: 'crc' | 'lead' | 'doctor'
  name: string
  role: string
  initials: string
  description: string
  goals: string[]
  painPoints: string[]
  skillLevel: '初级' | '中级' | '高级'
}

export interface LabIndicator {
  id: string
  name: string
  code: string
  value: string
  reference: string
  trend: string
  status: 'danger' | 'warning' | 'normal'
  ctcae: string
  confidence: number
  evidence: string
}

export interface VisitCase {
  id: string
  subject: string
  project: string
  site: string
  visit: string
  window: string
  status: string
  score: number
  level: RiskLevel
  sla: string
  summary: string
  tags: string[]
  scope?: 'mvp' | 'roadmap'
}

export const personas: Persona[] = [
  {
    id: 'crc',
    name: '林晓',
    role: '中心 CRC',
    initials: '林',
    description: '负责当天访视资料收集、风险复核与 EDC 回填',
    goals: ['尽早识别安全线索', '减少资料整理时间', '所有动作可追溯'],
    painPoints: ['多任务并行易遗漏', '规则检索耗时', '医生指令难结构化留痕'],
    skillLevel: '中级',
  },
  {
    id: 'lead',
    name: '周敏',
    role: 'CRC 组长',
    initials: '周',
    description: '复核高风险反馈与知识库优化候选',
    goals: ['控制误报漏报', '统一中心执行口径', '审核规则更新'],
    painPoints: ['反馈样本分散', '规则适用边界不清', '缺少版本审计'],
    skillLevel: '高级',
  },
  {
    id: 'doctor',
    name: '侯医生',
    role: '研究者（确认来源）',
    initials: '侯',
    description: '本 Demo 中不直接操作系统，其线下指令由 CRC 结构化回填',
    goals: ['快速获得完整证据', '保留最终医学判断权', '避免重复沟通'],
    painPoints: ['信息碎片化', '原始证据定位慢', 'AI 结论边界不清'],
    skillLevel: '高级',
  },
]

export const visitCases: VisitCase[] = [
  {
    id: 'PV-031',
    subject: 'JSM-1024',
    project: 'JS-ONC-III',
    site: '天津中心 A03',
    visit: 'V3 / D15',
    window: '窗口第 2 天',
    status: '已到访 · 资料待复核',
    score: 86,
    level: 'critical',
    sla: '03:15:42',
    summary: '体温升高、新增乏力与皮疹，合并用药记录待补齐',
    tags: ['AE/SAE/CM', '检查单待识别'],
    scope: 'mvp',
  },
  {
    id: 'PV-019',
    subject: 'JSM-1008',
    project: 'JS-ONC-III',
    site: '天津中心 A03',
    visit: 'V2 / D8',
    window: '窗口第 1 天',
    status: '已执行 · 资料补传',
    score: 58,
    level: 'medium',
    sla: '18:40:00',
    summary: 'ICF 版本不一致，需补传 v1.2 并更新资料状态',
    tags: ['资料完整性'],
    scope: 'roadmap',
  },
  {
    id: 'PV-044',
    subject: 'JSM-1120',
    project: 'JS-ONC-III',
    site: '北京中心 B02',
    visit: 'V1 / D1',
    window: '固定窗口日',
    status: '预约待到访',
    score: 24,
    level: 'low',
    sla: '26:20:00',
    summary: '确认受试者今日到访并上传预约确认记录',
    tags: ['轻量提醒'],
    scope: 'roadmap',
  },
]

export const labIndicators: LabIndicator[] = [
  {
    id: 'temp',
    name: '体温',
    code: 'TEMP',
    value: '38.3 °C',
    reference: '36.0–37.2 °C',
    trend: '较 V2 +1.1 °C',
    status: 'danger',
    ctcae: '发热条目 · 候选 Grade 1',
    confidence: 96,
    evidence: '检查单第 1 页 · 生命体征',
  },
  {
    id: 'anc',
    name: '中性粒细胞绝对值',
    code: 'ANC',
    value: '0.82 ×10⁹/L',
    reference: '1.80–6.30 ×10⁹/L',
    trend: '较 V2 -48%',
    status: 'danger',
    ctcae: '中性粒细胞计数降低 · 候选 Grade 3',
    confidence: 94,
    evidence: '检查单第 1 页 · 血常规',
  },
  {
    id: 'plt',
    name: '血小板',
    code: 'PLT',
    value: '72 ×10⁹/L',
    reference: '125–350 ×10⁹/L',
    trend: '较 V2 -39%',
    status: 'warning',
    ctcae: '血小板计数降低 · 候选 Grade 2',
    confidence: 98,
    evidence: '检查单第 1 页 · 血常规',
  },
  {
    id: 'alt',
    name: '丙氨酸氨基转移酶',
    code: 'ALT',
    value: '128 U/L',
    reference: '9–40 U/L',
    trend: '3.2 × ULN',
    status: 'warning',
    ctcae: 'ALT 升高 · 候选 Grade 2',
    confidence: 97,
    evidence: '检查单第 2 页 · 肝功能',
  },
  {
    id: 'crea',
    name: '肌酐',
    code: 'CREA',
    value: '79 μmol/L',
    reference: '41–81 μmol/L',
    trend: '较 V2 +3%',
    status: 'normal',
    ctcae: '未命中异常阈值',
    confidence: 99,
    evidence: '检查单第 2 页 · 肾功能',
  },
]

export const ragReferences = [
  {
    id: 'CTCAE-v5-FN',
    source: 'CTCAE v5.0',
    title: 'Febrile neutropenia / Neutrophil count decreased',
    match: 'ANC 0.82 ×10⁹/L + 体温 38.3°C',
    score: 0.94,
  },
  {
    id: 'SOP-CR-03',
    source: '项目 SOP',
    title: '异常检测值与症状变化复核触发规则',
    match: '异常指标 + 新增症状需生成复核证据包',
    score: 0.91,
  },
  {
    id: 'AE-02',
    source: '安全事件规则库',
    title: 'AE/SAE/CM 疑似线索进入人工确认',
    match: '发热、皮疹、实验室指标变化与新增退热药',
    score: 0.88,
  },
]

export const doctorTemplates = [
  '需补充体温复测、症状起止时间和 ANC 复查记录，暂不判断事件性质。',
  '确认记录为 AE，严重程度和因果关系待研究者完成医学评估；暂未满足 SAE 快速判断条件。',
  '该线索与既有 AE-2026-0718-01 可能重复，请先核对发生时间并合并证据。',
]

export interface ReviewQuestion {
  id: string
  text: string
  hint: string
}

/** 复核证据包（review_packet）的待确认问题清单，全部为预设演示数据。 */
export const reviewQuestions: ReviewQuestion[] = [
  { id: 'q1', text: '是否确认为新发 AE？', hint: '先核对是否与既有 AE-2026-0718-01 重复' },
  { id: 'q2', text: '严重程度与 CTCAE 等级？', hint: '由研究者医学评估，系统不定级' },
  { id: 'q3', text: '与研究药物的因果关系？', hint: '五级判断由研究者线下给出' },
  { id: 'q4', text: '是否满足 SAE 标准，是否需快速上报？', hint: '决定是否进入快速上报通道' },
  { id: 'q5', text: '复测与处置要求？', hint: '体温复测 / ANC 复查 / 症状时间线' },
]

export interface BoundaryRow {
  role: string
  can: string
  keep: string
}

/** 人机权限边界：AI、CRC、研究者各自可做与不可越过的动作。 */
export const permissionBoundary: BoundaryRow[] = [
  { role: 'AI 助手', can: '证据抽取、检验指标映射、规则命中、动作建议', keep: '不诊断、不定级、不自动上报、不写 EDC' },
  { role: 'CRC', can: '核对证据、结构化回填医生指令、勾选确认项、提交动作', keep: '最终结论须经研究者确认后留痕' },
  { role: '研究者', can: '线下医学确认：事件性质 / 严重程度 / 因果关系 / SAE 判定', keep: '结论由 CRC 转录回填' },
]

export interface TimelineEvent {
  id: string
  time: string
  label: string
  note: string
  kind: 'source' | 'ai' | 'conflict'
  conflictOnly?: boolean
}

/** 证据时间线：来自源文件（source_document）与检验指标（lab_indicator）的原始记录及 AI 加工节点。 */
export const evidenceTimeline: TimelineEvent[] = [
  { id: 'lis', time: '07:46', label: 'LIS 采样时间', note: '接口同步原始值', kind: 'source', conflictOnly: true },
  { id: 'sample', time: '08:12', label: '检查单采样时间', note: '以检查单为准 · 保留 LIS 原文', kind: 'source' },
  { id: 'review', time: '09:03', label: '检验报告审核完成', note: '检验师签核', kind: 'source' },
  { id: 'upload', time: '09:15', label: '报告上传 · 待复核', note: '进入访视上下文（source_document）', kind: 'source' },
  { id: 'parse', time: '09:20', label: 'AI 预识别完成', note: '检验指标标准化 · 3 条规则命中 · 生成复核证据包', kind: 'ai' },
]

