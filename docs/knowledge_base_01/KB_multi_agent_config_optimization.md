# Multi-Agent 配置增项与性能优化指南（2025）

## 1. 总览（易懂版）

- 多 Agent 系统的三要素：`模型（Brain）`、`工具（Hands）`、`编排（Orchestration）`，以及面向生产的 `部署与服务（Body & Legs）`。
- 参考知识库 Agent 设计方法：强调“能思考、会用工具、可观察与自我纠错”的闭环；在生产中通过 Agent Ops 度量与治理。
- 架构建议：采用双智体协同（前台访谈 + 后台分析），必要时按需创建专长 Agent（如情绪分析）。

---

## 2. 配置增项（可直接照着做）

- 角色分工（Agents）
  - `Frontend Interviewer`：负责自然语言交互与节奏控制，不维护结构化数据。
  - `Backend Analyst`：负责从对话中抽取结构化 JSON、一致性校验、推理打分。
  - `SentimentAnalysisAgent`（按需创建）：用于识别用户情绪与语气，动态加入团队（参考“可在运行时创建新专长 Agent”的模式）。

- 模型路由（Models）
  - 前台优先选对话/共情强的模型；后台选推理/结构化输出强的模型（双模型策略）。
  - 开启“Thinking/Reasoning”块，仅对系统可见，用户只看到最终回复（Stream of Thought 隐藏）。

- 工具清单（Tools）
  - 记忆加载：内置 `LoadMemoryTool`（示例）
    - `tools: [LoadMemoryTool()]`
  - 检索与事实接地（RAG/Search）：连接文档库或向量库，支撑长时记忆与背景知识。
  - JSON 校验器：强制 Schema 验证，降低结构化输出错误。
  - 动作工具：对外 API（如日历、数据库写入）置于 Orchestrator 审批与白名单内。

- 上下文工程（Context Engineering）
  - 清晰的 System Persona 与任务边界，避免前台“填表”。
  - 引入 `[System Notice]` 通道：由后台在每轮前注入“缺失字段/冲突提示/下一步建议”。
  - 控制注入长度：仅摘要关键字段，避免上下文爆炸。

- 记忆与会话（Memory & Sessions）
  - 短期记忆：会话线程的 `(Action, Observation)` 轨迹，作为活跃上下文。
  - 长期记忆：Memory Bank/RAG，提供跨会话的个性化“记住用户”能力。
  - Memory Bank 配置（示例）
    ```python
    memory_bank_config = {
      "customization_configs": [{
        "memory_topics": [
          { "managed_memory_topic": {"managed_topic_enum": "USER_PERSONAL_INFO"} },
          { "managed_memory_topic": {"managed_topic_enum": "PREFERENCES"} }
        ]
      }]
    }
    ```

- 安全与治理（Safety & Governance）
  - 工具白名单与高风险动作审批（如外部写入、支付）。
  - Prompt 注入防护：对外部内容做净化与边界提示；限制系统指令暴露。
  - 数据隐私与合规：明确存储位置与保留策略。

---

## 3. 性能优化（高效 + 省钱）

- Token 经济与上下文控制
  - 摘要注入：使用“滚动摘要”替代全量历史；关键字段单点注入。
  - Schema 压缩：字段命名短、层级浅；对话中引用键名而非长文本。

- 调度策略（Async Observer Loop）
  - 后台分析异步执行，容忍轻微延迟，前台继续对话不阻塞。
  - 触发策略：
    - 每 `3–5` 轮执行一次全量分析；
    - 检测到“关键意图切换/信息冲突”即触发增量分析。

- 模型路由与降级
  - 轻任务走便宜模型（分类、抽取）；重推理才调用高端模型。
  - 超时、失败重试、熔断与降级（Fallback to cached/last-known-state）。

- 并发与背压
  - 设置后台并发上限与队列；过载时丢弃低优先任务或延迟执行。

- 缓存与批处理
  - 工具结果缓存（如同一检索在短期内复用）。
  - 将多条轻量抽取并批量提交（降低 API 次数）。

- 质量度量（Agent Ops）
  - 使用 LM Judge 进行“质量而非对错”的评估（完整性、无越界、语气）。
  - 运行指标：`latency_ms`、`token_cost`、`tool_success_rate`、`json_validity_rate`。

---

## 4. 推荐配置模板（示例 JSON）

```json
{
  "orchestrator": {
    "workflow": "async_observer_loop",
    "context_injection": true,
    "system_notice_channel": "invisible"
  },
  "agents": [
    {
      "name": "frontend_interviewer",
      "model": "claude-3-5-sonnet-20241022",
      "tools": []
    },
    {
      "name": "backend_analyst",
      "model": "o3-mini",
      "tools": ["rag_search", "load_memory", "schema_validator"]
    },
    {
      "name": "sentiment_agent",
      "model": "gemini-3-pro",
      "tools": [],
      "activation": "on_demand"
    }
  ],
  "memory": {
    "short_term": "session_transcript",
    "long_term": "vector_db",
    "memory_bank_config": {
      "customization_configs": [{
        "memory_topics": [
          { "managed_memory_topic": {"managed_topic_enum": "USER_PERSONAL_INFO"} },
          { "managed_memory_topic": {"managed_topic_enum": "PREFERENCES"} }
        ]
      }]
    }
  },
  "routing": {
    "policy": "intent_based",
    "triggers": { "critical_intent_switch": true, "every_n_rounds": 3 }
  },
  "limits": {
    "max_tokens_per_round": 8000,
    "backend_rate_limit_rpm": 30,
    "concurrency": { "backend": 4 }
  },
  "ops": {
    "metrics": ["latency_ms", "token_cost", "tool_success_rate", "json_validity_rate"],
    "quality_eval": "lm_judge",
    "canary_percent": 10
  },
  "security": {
    "tool_allowlist": ["calendar_api", "db_write_via_orchestrator"],
    "approval_required_actions": ["external_write", "payment"]
  }
}
```

---

## 5. 编排模式建议（选型参考）

- `Dual-Agent（前台/后台）`：默认推荐，平衡体验与结构化能力。
- `Planner-Executor`：一个规划 Agent 拆解任务，多个执行 Agent 并行完成子任务。
- `Agents-as-Tools`：把专家 Agent 暴露为“工具”，由主控 Agent 按需调用。
- `Dynamic Teaming`：运行时创建/销毁专长 Agent（如情绪、合规审查）。

---

## 6. 部署与服务（生产友好）

- 部署平台：容器化 + 标准运行时（如 Cloud Run/GKE），或使用专用平台（如 Agent Engine）。
- 观察性：结构化日志、链路追踪、提示词与工具调用留痕，可 A/B 与金丝雀发布。
- 版本化与回滚：对提示词、工具 Schema、模型版本、评测数据做版本管理；一键回滚到已知良好态。
- 数据与秘密管理：禁用明文密钥；使用环境变量或密钥管理服务；避免泄露。

---

## 7. 成本与阈值（建议默认值）

- `token_cost/round` 设阈：超过告警并落入降级路径（摘要、暂停后台分析）。
- `json_validity_rate >= 99.9%`，失败自动重试一次；仍失败改走增量修复。
- `tool_success_rate >= 95%`，低于阈值触发健康检查与熔断。
- `frontend_latency_p95 <= 1200ms`，`backend_latency_p95 <= 2500ms`。

---

## 8. 快速落地步骤（Checklist）

- 明确双 Agent 职责与模型选型；开启思维块隐藏。
- 接入 RAG 与 Memory Bank；配置 `[System Notice]` 注入。
- 引入 JSON Schema 校验与工具白名单；审批高风险动作。
- 设置异步后台分析的触发策略与并发上限。
- 打通 Agent Ops：埋点、质量评估、金丝雀与回滚。
- 设定成本与性能阈值，跑一轮端到端小流量压测。

---

## 9. 常见坑与规避

- 过度上下文注入导致费用与延迟暴涨：改用摘要与关键字段注入。
- 前台被迫“填表”影响体验：把结构化任务移交后台，前台仅自然互动。
- 工具调用无治理：必须白名单 + 审批 + 观测 + 限流。
- 没有质量评估与版本化：一旦表现回退无法定位根因；建立评估与版本档案。

---

## 10. 结语

- 多 Agent 的价值在于“分工+协同+治理”。以上配置与优化策略旨在让系统既好用、又稳定、还能可控地迭代。
