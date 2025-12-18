# AI Product Opportunity Researcher - LLM Base Model 选型指南 (2025 Edition)

## 1. 任务特征与技术背景 (Context & Landscape)

本 Agent 是一个**复合型认知智能体**，运行在 2025 年末的 AI 技术环境中。相较于 2024 年，当前的 LLM 已普遍具备“System 2”推理能力（Thinking Mode）。
本任务的核心难点在于：
1.  **高保真侧写 (High-Fidelity Profiling)**：需在 50 轮长对话中维持“社会学家”的敏锐度，不出现机器味。
2.  **隐形结构化 (Invisible Structuring)**：在对话同时，后台需进行复杂的 JSON 抽取与校验，且不能干扰前台对话节奏。
3.  **动态推理 (Dynamic Reasoning)**：需实时判断用户的痛点强度（Pain Intensity）和技术可行性（AI-Native Index），这需要模型具备自我反思（Self-Correction）能力。

---

## 2. Base Model 最低准入标准 (Minimum Viable Requirements)

鉴于 2025 年的模型能力跃升，任何用于驱动本 Agent 的模型**必须**满足以下硬性指标：

| 维度 | 最低标准 (Baseline) | 推荐标准 (Recommended) | 2025 新特性要求 |
| :--- | :--- | :--- | :--- |
| **能力评级** | **GPT-5 / Claude 4 级别** | **Gemini 3 Pro / Claude 4.5 Sonnet** | 必须具备 **System 2 Thinking** (慢思考) 能力，以处理复杂的意图推断。 |
| **上下文窗口** | **128k** | **1M+ (Native)** | 支持全量历史回溯 + 外部知识库挂载，无需频繁截断。 |
| **指令遵循** | **Structured Output 2.0** | **Native Schema Enforcement** | 必须支持 100% 严格的 JSON Schema 输出，容错率需 < 0.1%。 |
| **推理成本** | < $2 / 1M Tokens | < $0.5 / 1M Tokens | 50 轮对话 x 完整 Context 消耗巨大，必须考虑 Token 经济性。 |
| **中文能力** | **Native Chinese Reasoning** | **Cultural Nuance Understanding** | 能理解中文互联网的“梗”、“黑话”及复杂的社会语境。 |

---

## 3. 推荐模型梯队 (Model Selection Tier - Nov 2025)

### Tier 1: 极致体验 (SOTA Performance)
*适用于追求最高访谈质量、最强逻辑推理的场景。*

*   **Anthropic Claude 4.5 Sonnet / Opus 4**
    *   **状态**：当前 Agent 领域的王者。
    *   **核心优势**：
        *   **SWE-bench Verified > 80%**：极强的逻辑与工具使用能力。
        *   **Human-like Interaction**：目前市面上拟人化程度最高的模型，非常适合“社会学家”这种需要共情的角色。
        *   **Thinking Mode**：内置的思维链使其在处理“痛点深挖”时能进行深度反思。
    *   **适用性**：首选推荐。

*   **Google Gemini 3 Pro**
    *   **状态**：综合能力最强（AIME 100%, GPQA 91.9%）。
    *   **核心优势**：
        *   **超长上下文 (2M+)**：可以把整本社会学著作或用户的历史文档全部扔进去作为背景知识。
        *   **Multimodal**：如果用户上传图片/截图，Gemini 3 的理解力是断层领先的。
    *   **适用性**：适合需要处理大量背景资料的重型访谈。

### Tier 2: 性价比与推理特化 (Reasoning & Efficiency)
*适用于需要深度逻辑判断，但对成本敏感的场景。*

*   **OpenAI o3 / o4-mini**
    *   **状态**：推理特化模型 (Reasoning Models)。
    *   **核心优势**：通过强化学习（RL）极大增强了逻辑链条。对于 `pain_intensity`（痛点强度）和 `tech_feasibility`（技术可行性）的打分，o3 系列比通用模型更精准。
    *   **注意**：延迟可能略高（因为要“思考”），不太适合秒回的即时聊天，但适合异步生成的后台分析。

*   **xAI Grok 3 (Beta)**
    *   **状态**：实时性与逻辑并重。
    *   **核心优势**：如果访谈涉及最新的市场动态或新闻，Grok 3 结合实时搜索的能力是独特的。且其推理能力（Think Mode）已追平 GPT-5。

### Tier 3: 最佳开源与私有化 (Open Weights & Privacy)
*适用于数据隐私极其敏感，或预算有限的场景。*

*   **DeepSeek-V3 / R1 (DeepSeek-V3.2-Exp)**
    *   **状态**：**2025 年的价格屠夫与性能黑马**。
    *   **核心优势**：
        *   **成本极低**：Input 仅需约 $0.03 / 1M Tokens（缓存命中后更低），几乎是免费的。
        *   **中文理解 SOTA**：作为国产模型，对中文语境的理解甚至优于 GPT-5。
        *   **R1 Reasoning**：具备与 o1/o3 类似的推理链能力，适合做复杂的 JSON 清洗。
    *   **适用性**：**私有化部署或低成本大规模并发的首选**。

*   **Meta Llama 4 (Scout/Maverick)**
    *   **状态**：开源基座标杆。
    *   **核心优势**：生态最丰富，支持各种微调和量化版本。如果需要针对特定行业（如医疗、法律）微调 Agent，Llama 4 是最佳底座。

---

## 4. Agent 架构级优化建议 (2025 Update)

在 2025 年，单纯依赖 Prompt Engineering 已经不够，建议采用 **"Flow Engineering"**：

### A. 双模型策略 (Dual-Model Strategy)
*   **前台 (Frontend)**: 使用 **Claude 4.5 Sonnet** 或 **DeepSeek-V3** 进行对话，保持高情商和流畅度。
*   **后台 (Backend)**: 使用 **OpenAI o3-mini** 或 **DeepSeek-R1** 这种推理模型，专门负责在每一轮对话后，根据对话历史生成/更新 JSON 数据。
    *   *理由*：推理模型擅长结构化任务，而对话模型擅长聊天。解耦后互不干扰，效果最佳。

### B. 思维流注入 (Stream of Thought Injection)
利用 2025 年模型普遍支持的 **"Thinking Block"**，在 System Prompt 中强制要求：
```markdown
<thinking>
1. Detect Intent: Is the user expressing a new pain point?
2. Profile Update: Does this contradict previous tags?
3. Strategy: Should I dig deeper or move to the next topic?
</thinking>
<response>
...自然语言回复...
</response>
```
*注意：大多数 2025 API 支持隐藏 `<thinking>` 块，只对用户展示最终回复。*

## 5. 最终推荐 (Final Verdict)

*   **如果不差钱，追求极致效果**：
    *   **Claude 4.5 Sonnet** (System Prompt 驱动全能型)
*   **如果关注极高性价比与中文体验**：
    *   **DeepSeek-V3 / R1** (API 或 私有化)
*   **如果需要超长记忆与多模态**：
    *   **Gemini 3 Pro**

**特别警告**：请勿再使用 2024 年初的 GPT-4 Turbo 或 Claude 3 Opus，它们在指令遵循和推理深度上已无法满足本 Agent 的高保真需求。
