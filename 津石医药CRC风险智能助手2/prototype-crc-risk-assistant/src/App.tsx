import { useMemo, useRef, useState } from 'react'
import type { ChangeEvent, ReactNode } from 'react'
import {
  Activity,
  AlertCircle,
  AlertTriangle,
  ArrowRight,
  BadgeCheck,
  BookOpen,
  CalendarClock,
  Check,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Circle,
  ClipboardCheck,
  Clock3,
  Database,
  FileCheck2,
  FileSearch,
  FileText,
  FlaskConical,
  History,
  Info,
  Layers3,
  ListChecks,
  LoaderCircle,
  LockKeyhole,
  Paperclip,
  Plus,
  RefreshCcw,
  RotateCcw,
  Scale,
  Search,
  Send,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  Upload,
  UserRoundCheck,
  UsersRound,
} from 'lucide-react'
import {
  doctorTemplates,
  evidenceTimeline,
  labIndicators,
  permissionBoundary,
  personas,
  ragReferences,
  reviewQuestions,
  visitCases,
} from './data'
import type { LabIndicator, Persona, VisitCase } from './data'

type Scenario = 'main' | 'conflict' | 'missing'
type ActionItem = {
  id: string
  title: string
  detail: string
  priority: '紧急' | '高' | '中'
  due: string
  close: string
  selected: boolean
}

const steps = [
  { id: 1, title: '访视上下文', subtitle: '范围与资料核对', icon: FileSearch },
  { id: 2, title: 'AE/SAE/CM 预识别', subtitle: '证据抽取与候选映射', icon: Activity },
  { id: 3, title: '医生确认', subtitle: '线下指令结构化', icon: UserRoundCheck },
  { id: 4, title: '动作与 EDC 建议', subtitle: '闭环执行草稿', icon: ClipboardCheck },
  { id: 5, title: '反馈学习', subtitle: '知识优化候选', icon: Sparkles },
]

const scenarioMeta: Record<Scenario, { label: string; caption: string }> = {
  main: { label: '主流程', caption: '完整资料，高风险人工确认路径' },
  conflict: { label: '数据冲突', caption: 'LIS 与检查单采样时间不一致' },
  missing: { label: '资料缺失', caption: '缺少 CM 与症状起止时间' },
}

const initialActions: ActionItem[] = [
  {
    id: 'repeat',
    title: '补充体温与血常规复测',
    detail: '记录复测时间、设备来源与 ANC/PLT 结果',
    priority: '紧急',
    due: '今日 15:30 前',
    close: '复测报告上传且研究者完成复核',
    selected: true,
  },
  {
    id: 'symptom',
    title: '补全症状起止时间',
    detail: '向受试者核实发热、乏力、皮疹的发生与缓解时间',
    priority: '高',
    due: '今日 17:00 前',
    close: '症状时间线完整并经 CRC 核对',
    selected: true,
  },
  {
    id: 'cm',
    title: '核对合并用药 CM 记录',
    detail: '补充退热药名称、剂量、频次与首次用药时间',
    priority: '高',
    due: '今日下班前',
    close: '源文件与 CM 表记录一致',
    selected: true,
  },
  {
    id: 'edc',
    title: '生成 EDC 回填草稿',
    detail: '基于人工结论预填 AE/CM 字段，等待 CRC 二次核对',
    priority: '中',
    due: '证据补齐后 2h',
    close: 'CRC 核对字段；仍需人工登录 EDC 提交',
    selected: true,
  },
]

const priorityClass = (priority: ActionItem['priority']) =>
  priority === '紧急' ? 'danger' : priority === '高' ? 'warning' : 'info'

const riskLabel = (visitCase: VisitCase) => {
  if (visitCase.level === 'critical') return '高优先级'
  if (visitCase.level === 'medium') return '待关注'
  return '常规'
}

function SectionTitle({
  eyebrow,
  title,
  description,
  aside,
}: {
  eyebrow: string
  title: string
  description: string
  aside?: ReactNode
}) {
  return (
    <div className="section-heading">
      <div>
        <span className="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      {aside}
    </div>
  )
}

function StatusBadge({
  tone,
  children,
}: {
  tone: 'danger' | 'warning' | 'success' | 'info' | 'neutral'
  children: ReactNode
}) {
  return <span className={`status-badge ${tone}`}>{children}</span>
}

function Sidebar({
  activeCase,
  onCaseChange,
  persona,
  onPersonaChange,
}: {
  activeCase: VisitCase
  onCaseChange: (visitCase: VisitCase) => void
  persona: Persona
  onPersonaChange: (persona: Persona) => void
}) {
  const [searchTerm, setSearchTerm] = useState('')
  const filteredCases = visitCases.filter((item) =>
    `${item.id}${item.subject}${item.summary}`.toLowerCase().includes(searchTerm.toLowerCase()),
  )

  return (
    <aside className="left-panel">
      <div className="brand-block">
        <div className="brand-mark"><Activity size={20} /></div>
        <div>
          <strong>Medix AI</strong>
          <span>CRC 风险智能助手</span>
        </div>
      </div>

      <div className="demo-label"><FlaskConical size={14} /> 模拟演示数据 · 非真实患者</div>

      <div className="persona-block">
        <label htmlFor="persona">当前角色视角</label>
        <div className="select-wrap">
          <select
            id="persona"
            value={persona.id}
            onChange={(event) => {
              const next = personas.find((item) => item.id === event.target.value)
              if (next) onPersonaChange(next)
            }}
          >
            {personas.map((item) => (
              <option key={item.id} value={item.id}>{item.role} · {item.name}</option>
            ))}
          </select>
          <ChevronDown size={15} />
        </div>
        <div className="persona-note">
          <div className="avatar">{persona.initials}</div>
          <div><strong>{persona.description}</strong><span>熟练度：{persona.skillLevel}</span></div>
        </div>
        {persona.id === 'doctor' && (
          <div className="boundary-note"><LockKeyhole size={14} /> 医生不是本工具直接用户，仅作为线下医学确认来源。</div>
        )}
      </div>

      <div className="queue-head">
        <div><span>今日风险队列</span><b>{visitCases.length}</b></div>
        <button className="icon-button" title="刷新队列"><RefreshCcw size={15} /></button>
      </div>
      <div className="queue-search">
        <Search size={15} />
        <input
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          placeholder="检索访视 / 受试者编号"
        />
      </div>
      <div className="case-list">
        {filteredCases.map((visitCase) => (
          <button
            key={visitCase.id}
            className={`case-card ${activeCase.id === visitCase.id ? 'active' : ''}`}
            onClick={() => onCaseChange(visitCase)}
          >
            <div className="case-top">
              <span className={`risk-dot ${visitCase.level}`} />
              <strong>{visitCase.id}</strong>
              <span className={`risk-text ${visitCase.level}`}>{riskLabel(visitCase)}</span>
              {visitCase.scope && (
                <span className={`scope-tag ${visitCase.scope}`}>
                  {visitCase.scope === 'mvp' ? 'MVP' : '路线图'}
                </span>
              )}
              <ChevronRight size={15} />
            </div>
            <div className="case-subject">{visitCase.subject} · {visitCase.visit}</div>
            <p>{visitCase.summary}</p>
            <div className="case-meta">
              <span><Clock3 size={12} /> SLA {visitCase.sla}</span>
              <span>{visitCase.score} 分</span>
            </div>
          </button>
        ))}
      </div>
      <div className="sidebar-foot">
        <ShieldCheck size={15} />
        <span>AI 仅辅助整理证据与建议，不作医学诊断或最终安全性判定。</span>
      </div>
    </aside>
  )
}

function WorkflowHeader({
  activeStep,
  setActiveStep,
}: {
  activeStep: number
  setActiveStep: (step: number) => void
}) {
  return (
    <div className="workflow-rail">
      {steps.map((step, index) => {
        const Icon = step.icon
        const state = step.id === activeStep ? 'active' : step.id < activeStep ? 'done' : ''
        return (
          <div className="step-wrap" key={step.id}>
            <button className={`step-button ${state}`} onClick={() => setActiveStep(step.id)}>
              <span className="step-icon">{step.id < activeStep ? <Check size={16} /> : <Icon size={16} />}</span>
              <span><b>0{step.id}</b><strong>{step.title}</strong><small>{step.subtitle}</small></span>
            </button>
            {index < steps.length - 1 && <div className={`step-line ${step.id < activeStep ? 'done' : ''}`} />}
          </div>
        )
      })}
    </div>
  )
}

function ContextStep({ activeCase, scenario }: { activeCase: VisitCase; scenario: Scenario }) {
  const checks = [
    ['访视窗口', activeCase.window, true],
    ['检查单', scenario === 'missing' ? '待上传' : '2 页 · 已核验来源', scenario !== 'missing'],
    ['症状记录', scenario === 'missing' ? '起止时间缺失' : '发热、乏力、皮疹', scenario !== 'missing'],
    ['合并用药', scenario === 'main' ? '新增退热药，待补剂量' : 'CM 记录缺失', false],
  ]
  return (
    <div className="step-content">
      <SectionTitle
        eyebrow="STEP 01 · SCOPE"
        title="建立本次访视上下文"
        description="先限定项目、访视与资料范围，避免跨访视证据误关联。"
        aside={<StatusBadge tone="info">上下文置信度 92%</StatusBadge>}
      />
      <div className="context-hero">
        <div className="subject-avatar">{activeCase.subject.slice(-2)}</div>
        <div className="subject-main">
          <span>模拟受试者编号</span>
          <h3>{activeCase.subject}</h3>
          <p>{activeCase.project} · {activeCase.site}</p>
        </div>
        <div className="visit-kpi"><span>当前访视</span><strong>{activeCase.visit}</strong><small>{activeCase.window}</small></div>
        <div className="visit-kpi"><span>风险分</span><strong className="danger-text">{activeCase.score}</strong><small>规则 + 资料完整性</small></div>
      </div>
      <div className="check-grid">
        {checks.map(([label, value, ok]) => (
          <div className="check-card" key={String(label)}>
            {ok ? <CheckCircle2 className="success-text" size={18} /> : <AlertCircle className="warning-text" size={18} />}
            <div><span>{label}</span><strong>{value}</strong></div>
          </div>
        ))}
      </div>
      <div className={`scenario-alert ${scenario}`}>
        {scenario === 'main' ? <BadgeCheck size={19} /> : <AlertTriangle size={19} />}
        <div>
          <strong>{scenarioMeta[scenario].label}：{scenarioMeta[scenario].caption}</strong>
          <p>
            {scenario === 'main' && '已锁定 V3/D15 范围，可进入 AE/SAE/CM 预识别。'}
            {scenario === 'conflict' && 'LIS 接口显示 07:46，检查单显示 08:12；进入预识别前需保留两侧原始时间。'}
            {scenario === 'missing' && '允许继续预识别，但结果必须标记“证据不完整”，不能将未观察到解释为无风险。'}
          </p>
        </div>
      </div>
    </div>
  )
}

function SimulatedReport({
  activeIndicator,
  setActiveIndicator,
}: {
  activeIndicator: string
  setActiveIndicator: (id: string) => void
}) {
  const marker = (id: string, text: string) => (
    <button
      className={`report-marker ${activeIndicator === id ? 'active' : ''}`}
      onClick={() => setActiveIndicator(id)}
    >
      {text}
    </button>
  )
  return (
    <div className="report-paper">
      <div className="paper-watermark">SIMULATED</div>
      <div className="report-head">
        <div><strong>津石临床中心检验报告</strong><span>仅供产品演示 · 模拟检查单</span></div>
        <span>报告编号 LAB-DEMO-0730</span>
      </div>
      <div className="report-info">
        <span>受试者：JSM-1024</span><span>访视：V3 / D15</span><span>采样：2026-07-30 08:12</span>
      </div>
      <div className="paper-section">生命体征</div>
      <div className="paper-row"><span>体温 TEMP</span>{marker('temp', '38.3 °C ↑')}<span>36.0–37.2</span></div>
      <div className="paper-section">血常规</div>
      <div className="paper-row"><span>中性粒细胞绝对值 ANC</span>{marker('anc', '0.82 ×10⁹/L ↓')}<span>1.80–6.30</span></div>
      <div className="paper-row"><span>血小板 PLT</span>{marker('plt', '72 ×10⁹/L ↓')}<span>125–350</span></div>
      <div className="paper-section">生化检查</div>
      <div className="paper-row"><span>丙氨酸氨基转移酶 ALT</span>{marker('alt', '128 U/L ↑')}<span>9–40</span></div>
      <div className="paper-row"><span>肌酐 CREA</span>{marker('crea', '79 μmol/L')}<span>41–81</span></div>
      <div className="report-sign">审核：检验师（模拟）　报告时间：2026-07-30 09:03</div>
    </div>
  )
}

function IndicatorCard({
  indicator,
  active,
  onClick,
}: {
  indicator: LabIndicator
  active: boolean
  onClick: () => void
}) {
  return (
    <button className={`indicator-card ${indicator.status} ${active ? 'active' : ''}`} onClick={onClick}>
      <div className="indicator-top">
        <span className="indicator-code">{indicator.code}</span>
        <span className={`confidence ${indicator.confidence >= 95 ? 'high' : ''}`}>{indicator.confidence}% 置信度</span>
      </div>
      <strong>{indicator.name}</strong>
      <div className="indicator-value">{indicator.value}</div>
      <div className="indicator-trend"><Activity size={13} /> {indicator.trend}</div>
      <div className="candidate-map">
        <span>CTCAE 候选映射</span>
        <b>{indicator.ctcae}</b>
      </div>
      <small><FileText size={12} /> {indicator.evidence}</small>
    </button>
  )
}

function RecognitionStep({
  parsed,
  parsing,
  onLoadDemo,
  onUpload,
  activeIndicator,
  setActiveIndicator,
  scenario,
}: {
  parsed: boolean
  parsing: boolean
  onLoadDemo: () => void
  onUpload: (event: ChangeEvent<HTMLInputElement>) => void
  activeIndicator: string
  setActiveIndicator: (id: string) => void
  scenario: Scenario
}) {
  const fileRef = useRef<HTMLInputElement>(null)

  return (
    <div className="step-content">
      <SectionTitle
        eyebrow="STEP 02 · CORE"
        title="AE / SAE / CM 预识别"
        description="从原始检查单抽取检验指标并映射规则，所有输出仅为人工确认候选。"
        aside={<StatusBadge tone="danger">高优先级人工确认</StatusBadge>}
      />
      <div className="decision-boundary">
        <ShieldCheck size={20} />
        <div><strong>决策边界</strong><span>系统不诊断、不定级、不自动上报；研究者医学判断与 CRC 人工结论始终优先。</span></div>
      </div>
      {!parsed && !parsing && (
        <div className="upload-zone">
          <div className="upload-icon"><Upload size={24} /></div>
          <h3>载入本次访视检查资料</h3>
          <p>支持 PDF、PNG、JPG，本地文件仅在浏览器中模拟解析，不会上传服务器。</p>
          <div className="upload-actions">
            <button className="button primary" onClick={() => fileRef.current?.click()}><Paperclip size={15} /> 上传本地文件</button>
            <button className="button secondary" onClick={onLoadDemo}><FileCheck2 size={15} /> 载入模拟检查单</button>
          </div>
          <input ref={fileRef} hidden type="file" accept=".pdf,.png,.jpg,.jpeg" onChange={onUpload} />
          <small><LockKeyhole size={13} /> 纯前端模拟 · 文件不会离开当前设备</small>
        </div>
      )}
      {parsing && (
        <div className="parsing-state">
          <div className="scanner">
            <FileText size={50} />
            <span className="scan-line" />
          </div>
          <div><LoaderCircle className="spin" size={18} /><strong>正在解析检查单与访视上下文…</strong></div>
          <p>版面识别 → 检验指标标准化 → 时间对齐 → CTCAE / SOP / AE 规则检索</p>
          <div className="parse-progress"><span /></div>
        </div>
      )}
      {parsed && (
        <>
          {scenario !== 'main' && (
            <div className="inline-warning">
              <AlertTriangle size={17} />
              {scenario === 'conflict'
                ? '检测到采样时间冲突：已保留 LIS 07:46 与原单 08:12 两个值，需人工核对。'
                : '证据不完整：CM 与症状时间缺失。预识别可继续，但不能据此排除风险。'}
            </div>
          )}
          <div className="recognition-layout">
            <div>
              <div className="subhead"><span><FileText size={16} /> 模拟化验单原文</span><small>点击高亮值联动右侧指标</small></div>
              <SimulatedReport activeIndicator={activeIndicator} setActiveIndicator={setActiveIndicator} />
            </div>
            <div>
              <div className="subhead"><span><Sparkles size={16} /> 结构化抽取与趋势</span><small>5 个检验指标已抽取</small></div>
              <div className="indicator-list">
                {labIndicators.map((indicator) => (
                  <IndicatorCard
                    key={indicator.id}
                    indicator={indicator}
                    active={indicator.id === activeIndicator}
                    onClick={() => setActiveIndicator(indicator.id)}
                  />
                ))}
              </div>
            </div>
          </div>
          <div className="rag-panel">
            <div className="rag-title">
              <div><BookOpen size={18} /><span><strong>检索增强证据</strong><small>引用可追溯，不替代医学判断</small></span></div>
              <StatusBadge tone="success">3 条规则命中</StatusBadge>
            </div>
            <div className="rag-grid">
              {ragReferences.map((reference) => (
                <div className="rag-card" key={reference.id}>
                  <div><span>{reference.source}</span><b>{Math.round(reference.score * 100)}% 匹配</b></div>
                  <strong>{reference.title}</strong>
                  <p>{reference.match}</p>
                  <small><Database size={12} /> {reference.id} · 当前发布版本</small>
                </div>
              ))}
            </div>
          </div>
          <div className="human-review">
            <AlertCircle size={22} />
            <div>
              <span>预识别输出</span>
              <h3>高优先级人工确认</h3>
              <p>ANC 降低伴体温升高，且存在皮疹、乏力与新增退热药线索。建议尽快请研究者确认事件性质、严重程度、因果关系与是否满足 SAE 标准。</p>
            </div>
            <div className="not-final"><LockKeyhole size={14} /> 不是最终判定</div>
          </div>
        </>
      )}
    </div>
  )
}

function DoctorStep({
  doctorInstruction,
  setDoctorInstruction,
  conclusion,
  setConclusion,
}: {
  doctorInstruction: string
  setDoctorInstruction: (value: string) => void
  conclusion: string
  setConclusion: (value: string) => void
}) {
  return (
    <div className="step-content">
      <SectionTitle
        eyebrow="STEP 03 · HUMAN DECISION"
        title="回填线下医生确认"
        description="医生不直接登录本工具。CRC 根据线下沟通记录，结构化回填研究者指令。"
        aside={<StatusBadge tone="info">人工结论优先</StatusBadge>}
      />
      <div className="offline-flow">
        <div><Stethoscope size={20} /><span><strong>研究者线下确认</strong><small>面谈 / 电话 / 院内合规渠道</small></span></div>
        <ArrowRight size={18} />
        <div><UsersRound size={20} /><span><strong>CRC 结构化回填</strong><small>记录来源、时间与原话</small></span></div>
        <ArrowRight size={18} />
        <div><History size={20} /><span><strong>留痕并生成动作</strong><small>人工结论覆盖 AI 候选</small></span></div>
      </div>
      <div className="form-grid">
        <div className="form-card wide">
          <label htmlFor="template">医生指令模板</label>
          <div className="template-row">
            <select
              id="template"
              value={doctorInstruction}
              onChange={(event) => setDoctorInstruction(event.target.value)}
            >
              {doctorTemplates.map((template) => <option key={template} value={template}>{template}</option>)}
            </select>
            <button className="button secondary"><Plus size={14} /> 保存为中心模板</button>
          </div>
          <label htmlFor="instruction">医生指令原话 / CRC 整理</label>
          <textarea
            id="instruction"
            rows={4}
            value={doctorInstruction}
            onChange={(event) => setDoctorInstruction(event.target.value)}
          />
          <small>可编辑；系统保留所选模板与最终修改版本的差异记录。</small>
        </div>
        <div className="form-card">
          <label htmlFor="conclusion">人工结论</label>
          <select id="conclusion" value={conclusion} onChange={(event) => setConclusion(event.target.value)}>
            <option>暂不判断，补充证据后复核</option>
            <option>确认为 AE，待完成医学评估</option>
            <option>既有 AE 的补充信息</option>
            <option>排除当前候选，记录排除依据</option>
          </select>
          <div className="important-note"><AlertTriangle size={16} /><span><strong>“暂不判断”不等于“无风险”</strong>风险状态保持开放，直至补齐证据并获得明确研究者结论。</span></div>
        </div>
        <div className="form-card">
          <label>确认来源</label>
          <div className="choice-row">
            {['电话', '当面', '院内合规消息'].map((item, index) => (
              <label className="radio-label" key={item}><input type="radio" name="source" defaultChecked={index === 1} /> {item}</label>
            ))}
          </div>
          <div className="field-pair">
            <label>确认人<input defaultValue="侯医生 / PI" /></label>
            <label>确认时间<input type="datetime-local" defaultValue="2026-07-30T10:26" /></label>
          </div>
        </div>
      </div>
      <div className="structured-preview">
        <div><Layers3 size={18} /><strong>结构化回填预览</strong></div>
        <div className="preview-grid">
          <span><small>事件性质</small><b>{conclusion.includes('AE') ? 'AE 候选已人工确认' : '开放待确认'}</b></span>
          <span><small>严重程度</small><b>待研究者医学评估</b></span>
          <span><small>SAE 判定</small><b>未作最终判定</b></span>
          <span><small>优先依据</small><b>医生线下指令</b></span>
        </div>
      </div>
    </div>
  )
}

function ActionsStep({
  actions,
  setActions,
}: {
  actions: ActionItem[]
  setActions: (actions: ActionItem[]) => void
}) {
  const toggle = (id: string) =>
    setActions(actions.map((action) => action.id === id ? { ...action, selected: !action.selected } : action))
  return (
    <div className="step-content">
      <SectionTitle
        eyebrow="STEP 04 · CLOSE THE LOOP"
        title="生成动作与 EDC 回填建议"
        description="将人工结论转成可执行任务；每项都包含优先级、截止时间与关闭标准。"
        aside={<StatusBadge tone="warning">{actions.filter((item) => item.selected).length} 项待执行</StatusBadge>}
      />
      <div className="action-list">
        {actions.map((action, index) => (
          <div className={`action-row ${action.selected ? 'selected' : ''}`} key={action.id}>
            <button className="check-button" onClick={() => toggle(action.id)}>
              {action.selected ? <CheckCircle2 size={20} /> : <Circle size={20} />}
            </button>
            <span className="action-index">0{index + 1}</span>
            <div className="action-copy"><strong>{action.title}</strong><p>{action.detail}</p></div>
            <StatusBadge tone={priorityClass(action.priority)}>{action.priority}</StatusBadge>
            <div className="action-time"><small>截止时间</small><b><CalendarClock size={13} /> {action.due}</b></div>
            <div className="action-close"><small>关闭标准</small><b>{action.close}</b></div>
          </div>
        ))}
      </div>
      <div className="edc-draft">
        <div className="edc-head">
          <div><FileText size={19} /><span><strong>EDC 回填草稿</strong><small>基于人工结论生成，可复制但不会自动提交</small></span></div>
          <StatusBadge tone="neutral">DRAFT</StatusBadge>
        </div>
        <div className="edc-fields">
          <label>AE 术语<input defaultValue="发热伴中性粒细胞计数降低（待研究者确认标准术语）" /></label>
          <label>开始时间<input defaultValue="待补充" /></label>
          <label>严重程度<input defaultValue="待研究者医学评估" /></label>
          <label>采取措施<input defaultValue="复测体温及血常规；补充症状时间线" /></label>
          <label>CM 记录<input defaultValue="退热药名称、剂量、频次待核对" /></label>
          <label>数据状态<input defaultValue="草稿 · 不自动写入 EDC" /></label>
        </div>
        <div className="edc-footer">
          <span><LockKeyhole size={14} /> 系统未连接 EDC 写入接口，必须由授权 CRC 人工核对并提交。</span>
          <button className="button secondary"><FileCheck2 size={14} /> 复制草稿</button>
        </div>
      </div>
    </div>
  )
}

function FeedbackStep({
  feedbackSubmitted,
  setFeedbackSubmitted,
}: {
  feedbackSubmitted: boolean
  setFeedbackSubmitted: (value: boolean) => void
}) {
  return (
    <div className="step-content">
      <SectionTitle
        eyebrow="STEP 05 · GOVERNED LEARNING"
        title="提交知识优化候选"
        description="记录 CRC 与医生反馈，进入受治理的知识优化队列，而非直接改变线上判断。"
        aside={<StatusBadge tone="success">可审计学习闭环</StatusBadge>}
      />
      <div className="learning-rule">
        <ShieldCheck size={22} />
        <div><strong>单次反馈不能直接修改线上 RAG</strong><p>候选必须经 CRC 组长复核、规则所有者批准并发布新版本，才会用于后续判断。</p></div>
      </div>
      <div className="feedback-layout">
        <div className="feedback-form">
          <label>反馈类型</label>
          <div className="feedback-types">
            {['候选映射需优化', '补充中心执行口径', '证据抽取纠正'].map((item, index) => (
              <label key={item}><input type="radio" name="feedback" defaultChecked={index === 0} /><span>{item}</span></label>
            ))}
          </div>
          <label>CRC 反馈</label>
          <textarea rows={3} defaultValue="当前候选同时命中 ANC 降低与发热条目，建议在证据包中优先展示联合线索，但不得合并为最终事件判定。" />
          <label>医生反馈（由 CRC 转录）</label>
          <textarea rows={3} defaultValue="需结合复测结果、感染排查与临床症状后再判断；当前仅可提示尽快复核。" />
          <label className="attestation"><input type="checkbox" defaultChecked /> 我确认内容已去标识化，且原始沟通记录可追溯。</label>
          <button className="button primary" onClick={() => setFeedbackSubmitted(true)} disabled={feedbackSubmitted}>
            {feedbackSubmitted ? <Check size={15} /> : <Send size={15} />}
            {feedbackSubmitted ? '已进入组长复核队列' : '提交为知识优化候选'}
          </button>
        </div>
        <div className="governance-panel">
          <h3>候选治理路径</h3>
          {[
            ['01', 'CRC 提交候选', feedbackSubmitted ? '已完成' : '当前步骤'],
            ['02', 'CRC 组长复核', feedbackSubmitted ? '待处理' : '未开始'],
            ['03', '规则所有者批准', '未开始'],
            ['04', '版本发布与回归测试', '未开始'],
            ['05', '用于后续辅助判断', '未生效'],
          ].map(([index, label, status], rowIndex) => (
            <div className={`governance-row ${rowIndex === 0 && feedbackSubmitted ? 'done' : ''}`} key={index}>
              <span>{index}</span><div><strong>{label}</strong><small>{status}</small></div>
              {rowIndex === 0 && feedbackSubmitted ? <CheckCircle2 size={17} /> : <Circle size={16} />}
            </div>
          ))}
          <div className="version-box"><Database size={17} /><span><small>当前线上知识版本</small><strong>RAG-CRC v1.6.2</strong></span><b>未变更</b></div>
        </div>
      </div>
      {feedbackSubmitted && (
        <div className="success-banner"><CheckCircle2 size={20} /><div><strong>候选 KO-2026-0730-014 已提交</strong><span>已通知 CRC 组长周敏复核。当前线上知识与本次预识别结果均未发生改变。</span></div></div>
      )}
    </div>
  )
}

function CollaborationPanel({
  activeCase,
  activeStep,
  scenario,
}: {
  activeCase: VisitCase
  activeStep: number
  scenario: Scenario
}) {
  const [checked, setChecked] = useState<Record<string, boolean>>({})
  const checkedCount = reviewQuestions.filter((question) => checked[question.id]).length
  const timeline = evidenceTimeline.filter((event) => !event.conflictOnly || scenario === 'conflict')

  const toggle = (id: string) =>
    setChecked((current) => ({ ...current, [id]: !current[id] }))

  return (
    <aside className="chat-panel collab-panel">
      <div className="chat-head">
        <div className="collab-mark"><Layers3 size={19} /></div>
        <div><strong>访视协作侧栏</strong><span>结构化证据 · 无对话接口</span></div>
        <button className="icon-button" title="重置勾选" onClick={() => setChecked({})}><RotateCcw size={15} /></button>
      </div>
      <div className="chat-context">
        <span><FileText size={12} /> {activeCase.id} · {activeCase.visit}</span>
        <span><Layers3 size={12} /> 步骤 0{activeStep}</span>
      </div>
      <div className="collab-scroll">
        <section className="collab-section">
          <div className="collab-sec-head">
            <span className="collab-sec-icon"><ListChecks size={15} /></span>
            <strong>待确认问题清单</strong>
            <span className="collab-count">{checkedCount}/{reviewQuestions.length}</span>
          </div>
          <p className="collab-sec-desc">来自复核证据包 question_list；勾选项可在步骤 03 直接引用。</p>
          <div className="question-list">
            {reviewQuestions.map((question, index) => (
              <label className={`question-row ${checked[question.id] ? 'checked' : ''}`} key={question.id}>
                <input type="checkbox" checked={!!checked[question.id]} onChange={() => toggle(question.id)} />
                <span className="question-text">
                  <b>Q{index + 1} · {question.text}</b>
                  <small>{question.hint}</small>
                </span>
              </label>
            ))}
          </div>
          <div className={`question-echo ${checkedCount ? 'done' : ''}`}>
            {checkedCount > 0
              ? <><CheckCircle2 size={14} /> {checkedCount} 项已勾选，可作为医生确认步骤的待办引用</>
              : <><Circle size={14} /> 尚未勾选，等待研究者线下结论</>}
          </div>
        </section>

        <section className="collab-section">
          <div className="collab-sec-head">
            <span className="collab-sec-icon"><BookOpen size={15} /></span>
            <strong>规则命中依据</strong>
            <span className="collab-count">{ragReferences.length}</span>
          </div>
          {ragReferences.map((reference) => (
            <div className="collab-rule" key={reference.id}>
              <div className="collab-rule-top">
                <span>{reference.source}</span>
                <b>{Math.round(reference.score * 100)}% 匹配</b>
              </div>
              <strong>{reference.title}</strong>
              <p>{reference.match}</p>
              <small><Database size={11} /> {reference.id} · 当前发布版本</small>
            </div>
          ))}
        </section>

        <section className="collab-section">
          <div className="collab-sec-head">
            <span className="collab-sec-icon"><History size={15} /></span>
            <strong>证据时间线</strong>
          </div>
          <div className="timeline">
            {timeline.map((event) => (
              <div className={`tl-event ${event.kind}`} key={event.id}>
                <span className="tl-time">{event.time}</span>
                <span className="tl-dot" />
                <div className="tl-body">
                  <strong>{event.label}</strong>
                  <small>{event.note}</small>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="collab-section">
          <div className="collab-sec-head">
            <span className="collab-sec-icon"><Scale size={15} /></span>
            <strong>人机权限边界</strong>
          </div>
          <div className="boundary-list">
            {permissionBoundary.map((row) => (
              <div className="boundary-row" key={row.role}>
                <span className="boundary-role">{row.role}</span>
                <span className="boundary-can">{row.can}</span>
                <span className="boundary-keep"><LockKeyhole size={11} /> {row.keep}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
      <div className="chat-disclaimer"><Info size={13} /> 全为结构化预设数据，不连接 LLM 或真实 API。</div>
    </aside>
  )
}

function App() {
  const [activeCase, setActiveCase] = useState(visitCases[0])
  const [persona, setPersona] = useState(personas[0])
  const [scenario, setScenario] = useState<Scenario>('main')
  const [activeStep, setActiveStep] = useState(1)
  const [parsed, setParsed] = useState(false)
  const [parsing, setParsing] = useState(false)
  const [activeIndicator, setActiveIndicator] = useState('anc')
  const [doctorInstruction, setDoctorInstruction] = useState(doctorTemplates[0])
  const [conclusion, setConclusion] = useState('暂不判断，补充证据后复核')
  const [actions, setActions] = useState(initialActions)
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false)

  const currentStep = useMemo(() => steps.find((step) => step.id === activeStep) ?? steps[0], [activeStep])

  const loadReport = () => {
    setParsing(true)
    setParsed(false)
    window.setTimeout(() => {
      setParsing(false)
      setParsed(true)
    }, 1550)
  }

  const resetDemo = () => {
    setActiveCase(visitCases[0])
    setPersona(personas[0])
    setScenario('main')
    setActiveStep(1)
    setParsed(false)
    setParsing(false)
    setActiveIndicator('anc')
    setDoctorInstruction(doctorTemplates[0])
    setConclusion('暂不判断，补充证据后复核')
    setActions(initialActions)
    setFeedbackSubmitted(false)
  }

  const goNext = () => {
    if (activeStep < 5) setActiveStep(activeStep + 1)
  }

  return (
    <div className="app-shell min-h-screen bg-slate-50 text-slate-900">
      <Sidebar
        activeCase={activeCase}
        onCaseChange={(visitCase) => {
          setActiveCase(visitCase)
          setActiveStep(1)
          setParsed(false)
        }}
        persona={persona}
        onPersonaChange={setPersona}
      />
      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumb"><span>临床运营工作台</span><ChevronRight size={14} /><strong>{activeCase.id}</strong></div>
          <div className="top-actions">
            <div className="scenario-switch">
              {(Object.keys(scenarioMeta) as Scenario[]).map((key) => (
                <button
                  className={scenario === key ? 'active' : ''}
                  key={key}
                  onClick={() => {
                    setScenario(key)
                    setParsed(false)
                    setActiveStep(1)
                  }}
                  title={scenarioMeta[key].caption}
                >
                  {scenarioMeta[key].label}
                </button>
              ))}
            </div>
            <button className="button ghost" onClick={resetDemo}><RotateCcw size={14} /> 重置演示</button>
          </div>
        </header>
        <div className="workspace">
          <div className="page-intro">
            <div>
              <div className="intro-label"><Activity size={15} /> CRC 独立辅助工具</div>
              <h1>访视风险证据工作台</h1>
              <p>{activeCase.subject} · {activeCase.visit} · {scenarioMeta[scenario].caption}</p>
            </div>
            <div className="simulation-banner"><FlaskConical size={18} /><span><strong>模拟演示数据</strong><small>页面不包含任何真实患者信息</small></span></div>
          </div>
          <WorkflowHeader activeStep={activeStep} setActiveStep={setActiveStep} />
          <section className="work-card">
            {activeStep === 1 && <ContextStep activeCase={activeCase} scenario={scenario} />}
            {activeStep === 2 && (
              <RecognitionStep
                parsed={parsed}
                parsing={parsing}
                onLoadDemo={loadReport}
                onUpload={(event) => {
                  if (event.target.files?.length) loadReport()
                }}
                activeIndicator={activeIndicator}
                setActiveIndicator={setActiveIndicator}
                scenario={scenario}
              />
            )}
            {activeStep === 3 && (
              <DoctorStep
                doctorInstruction={doctorInstruction}
                setDoctorInstruction={setDoctorInstruction}
                conclusion={conclusion}
                setConclusion={setConclusion}
              />
            )}
            {activeStep === 4 && <ActionsStep actions={actions} setActions={setActions} />}
            {activeStep === 5 && (
              <FeedbackStep
                feedbackSubmitted={feedbackSubmitted}
                setFeedbackSubmitted={setFeedbackSubmitted}
              />
            )}
          </section>
          <div className="workflow-footer">
            <div><span>当前：0{activeStep}</span><strong>{currentStep.title}</strong><small>所有操作记录仅用于模拟演示</small></div>
            <div>
              {activeStep > 1 && <button className="button secondary" onClick={() => setActiveStep(activeStep - 1)}>上一步</button>}
              {activeStep < 5 && <button className="button primary" onClick={goNext}>保存并进入下一步 <ArrowRight size={15} /></button>}
            </div>
          </div>
        </div>
      </main>
      <CollaborationPanel activeCase={activeCase} activeStep={activeStep} scenario={scenario} />
    </div>
  )
}

export default App
