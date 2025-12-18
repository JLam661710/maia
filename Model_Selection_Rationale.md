# 模型选型策略与理由 (Model Selection Strategy & Rationale)

为了满足不同场景的需求，我们提供了两种顶级的模型选型方案。

---

## 方案 A: 旗舰级性能优先 (Flagship Performance)
*追求各领域的“单项冠军”，混搭最强模型。*

*   **访谈专员**: `claude-3-7-sonnet-20250219` (拟人体验最佳)
*   **后台分析师**: `o3` (逻辑推理最强)
*   **架构师**: `claude-opus-4-5-20251101` (文档生成最强)

---

## 方案 B: 全员 Gemini 家族 (All-Gemini Ecosystem)
*Google 生态纯血组合，主打超长上下文 (Long Context) 和原生多模态。*

如果你希望 Agent 能记住“从盘古开天辟地以来”的所有对话细节，或者需要处理极长的参考资料，Gemini 家族是无可替代的选择。

### 1. 访谈专员 (Interviewer Agent)
*   **选型**: **`gemini-2.5-flash`**
*   **理由**:
    *   **唯快不破**: Flash 系列是目前大模型界的“速度之王”，延迟极低，给用户“秒回”的快感。
    *   **能力溢出**: 2.5 版本的 Flash 能力已经超过了早期的 GPT-4，处理日常访谈绰绰有余。

### 2. 后台分析师 (Backend Analyst Agent)
*   **选型**: **`gemini-3-pro-preview-thinking`**
*   **理由**:
    *   **原生思考 (Native Thinking)**: 类似于 o1/R1，Gemini 3 也引入了思维链（Thinking Process）。这对于后台复杂的 JSON 状态维护至关重要。
    *   **海量记忆**: 即使分析过程需要回溯前 100 轮对话，Gemini 的 Context Window 也能轻松装下，不会遗忘任何细节。

### 3. 解决方案架构师 (Solution Architect Agent)
*   **选型**: **`gemini-3-pro-preview`**
*   **理由**:
    *   **无限上下文**: Gemini 3 Pro 支持超百万级的 Token 输入。这意味着它可以一次性读取用户提供的几十份 PDF 文档、整个项目的历史对话、以及所有的参考资料，然后生成一份包罗万象的 PRD。
    *   **生态一致性**: 与前面的 Gemini 模型配合，风格更统一。

---

## 选型建议 (Recommendation)

*   如果你更看重**逻辑的严密性**和**文档的精美度**，请选择 **方案 A**。
*   如果你更看重**上下文的长度**（比如对话非常长，或者有大量背景资料）和**响应速度**，请选择 **方案 B**。

> **当前状态**: 已在 `.env.example` 中配置为 **方案 B (All-Gemini)**，以便体验 Google 最新模型的强大能力。
