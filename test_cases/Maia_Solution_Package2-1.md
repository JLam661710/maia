基于您提供的 JSON State，特别是用户作为“全栈开发者”兼“平台创始人”的背景，以及核心痛点“非标品匹配难”和“混合匹配模式（Hybrid Matching）”的架构决策，我为您制定了以下四份深度定制的交付文档。

---

### 1. `DOC_01_PRD.md`

```markdown
# 🚀 产品需求文档 (PRD): AI Native 定制交易平台 (MVP)

## 1. 核心价值主张 (Value Proposition)
**产品定义**：一个基于“意图翻译”的非标品定制交易平台。
**核心价值**：通过 LLM 将买家模糊的自然语言需求（"我要一个赛博朋克风的灯"），实时转译为工业级的结构化参数（"材质:亚克力, 工艺:激光切割, 光源:RGB LED"），从而精准匹配具备相应制造能力的 Maker，解决非标品交易中“供需语言不通”的核心痛点。

## 2. 目标用户与核心场景 (User Stories)

### 2.1 买家 (The Dreamer)
*   **As a** 不懂技术的定制买家，
*   **I want to** 用大白话描述我的想法（甚至上传一张草图），
*   **So that** 我能找到真正能做这件事的 Maker，而不是在一堆无关的商品列表中翻找。

### 2.2 卖家/Maker (The Creator)
*   **As a** 拥有特定工艺（如3D打印、皮具制作）的 Maker，
*   **I want to** 上传我的过往案例图和简单的设备清单，让系统自动分析我的“能力边界”，
*   **So that** 我不需要手动填写复杂的 SEO 关键词，也能被精准推送到有对应需求的买家面前。

### 2.3 平台运营 (The Matchmaker)
*   **As a** 平台管理员，
*   **I want to** 监控“匹配失败”的查询（即有需求无供给），
*   **So that** 我可以定向邀请特定领域的 Maker 入驻（如发现大量人搜“钛合金键帽”，则去站外招募相关工匠）。

## 3. 功能清单 (Feature List)

### P0: 核心闭环 (MVP Scope - The "Hybrid Matcher")
| 模块 | 功能点 | 描述 | 优先级 |
| :--- | :--- | :--- | :--- |
| **供给端** | **AI 能力建模** | Maker 上传案例图/文，后台自动提取“工艺标签”、“材质库”、“风格向量”并存入数据库。 | **Must-have** |
| **需求端** | **意图翻译器** | 买家输入自然语言，LLM 实时解析为 JSON 格式的“需求规格书”（包含硬性参数和软性风格）。 | **Must-have** |
| **匹配层** | **混合搜索引擎** | 执行 `Vector Search` (风格相似度) + `Filter` (硬参数匹配，如尺寸、材质)。 | **Must-have** |
| **交互层** | **询价单生成** | 基于匹配结果，自动生成标准化的询价单（RFQ），买家确认后一键分发给 Top 5 匹配的 Maker。 | **Must-have** |

### P1: 信任增强 (Phase 2 - The "Visual Contract")
| 模块 | 功能点 | 描述 | 优先级 |
| :--- | :--- | :--- | :--- |
| **交易层** | **AI 视觉预演** | 在 Maker 接单前，利用 GenAI 生成“预期交付物”的概念图，作为双方确认的“视觉合同”。 | Nice-to-have |
| **交易层** | **争议仲裁凭证** | 将“视觉合同”与最终交付物照片进行 AI 比对，作为退款/验收的客观依据。 | Nice-to-have |

## 4. 验收标准 (Success Metrics)
1.  **匹配准确率 (Match Precision)**：买家发起询价后，至少有 3 个 Maker 响应且具备真实承接能力。
2.  **意图解析成功率**：LLM 能正确将 80% 的模糊需求转化为包含至少 2 个硬性参数（如材质、尺寸）的结构化数据。
3.  **Maker 入驻效率**：Maker 通过上传案例完成资料建档的时间 < 5 分钟。
```

---

### 2. `DOC_02_Tech_Architecture.md`

```markdown
# 🛠 技术落地架构 (Technical Implementation Guide)

鉴于您是全栈开发者，本方案采用 **Pro-Code** 路线，重点构建“混合检索（Hybrid Search）”架构。

## 1. 系统架构图 (Architecture Diagram)

```mermaid
graph TD
    User[Buyer Client] -->|1. Natural Language Query| API[API Gateway / Backend]
    
    subgraph "Intelligent Processing Layer"
        API -->|2. Raw Query| LLM_Trans[LLM Translator Agent]
        LLM_Trans -->|3. Extract Specs| Structured_Query[{"style": "cyberpunk", "material": "acrylic"}]
        LLM_Trans -->|4. Generate Embedding| Query_Vector[Vector Embedding]
    end
    
    subgraph "Data & Matching Engine"
        Structured_Query -->|5. Hard Filter (SQL)| DB[(PostgreSQL + pgvector)]
        Query_Vector -->|6. Similarity Search (ANN)| DB
        DB -->|7. Ranked Candidates| ReRanker[Re-Ranking Logic]
    end
    
    subgraph "Supply Side Ingestion"
        Maker[Maker Client] -->|Upload Portfolio| Ingest_Service[Ingestion Service]
        Ingest_Service -->|Image Analysis| Vision_Model[Vision LLM (GPT-4o/Claude 3.5)]
        Vision_Model -->|Extract Capabilities| DB
    end
    
    ReRanker -->|8. Final Match List| API
    API -->|9. Response| User
```

## 2. 技术栈选型 (Tech Stack)

*   **前端/交互层**:
    *   **Framework**: `Next.js` (React) - 兼顾 SEO 和复杂的交互逻辑。
    *   **UI Lib**: `Tailwind CSS` + `Shadcn/ui` - 快速构建现代界面。
*   **逻辑/编排层 (Backend)**:
    *   **Language**: `Python` (FastAPI) - Python 是 AI 生态的首选，方便集成 LLM 库。
    *   **Orchestration**: `LangChain` 或 `LlamaIndex` - 用于构建“意图翻译”和“参数提取”的 Agent 流程。
*   **数据/存储层 (The Hybrid Core)**:
    *   **Primary DB**: `PostgreSQL` with `pgvector` extension.
    *   **Why?** 您需要同时处理**关系型数据**（订单、用户、库存硬参数）和**向量数据**（风格、语义）。Postgres 是目前做混合检索（Hybrid Search）的最佳单体方案，避免维护两套数据库（如 MySQL + Pinecone）的同步成本。
*   **模型层**:
    *   **Reasoning/Translation**: `DeepSeek-V3` (高性价比) 或 `GPT-4o` (处理复杂逻辑)。
    *   **Embedding**: `OpenAI text-embedding-3-small` 或 `BGE-M3` (开源，支持多语言)。

## 3. 关键难点攻克 (Key Challenges)

### 难点 A：非标品的参数提取 (The "Unstructured to Structured" Problem)
*   **挑战**: Maker 上传一张图，怎么知道他能做“5微米精度”？
*   **解决方案**: **多模态推断 + 交互确认**。
    1.  Vision Model 分析图片：“这是一张高精度的光固化 3D 打印模型”。
    2.  系统自动生成 Tag，但标记为 `Unverified`。
    3.  Maker 在后台看到 Tag，点击确认或修正具体数值。**不要完全依赖 AI，AI 只是辅助填表。**

### 难点 B：幻觉匹配 (Hallucination in Matching)
*   **挑战**: LLM 可能会把“想要一个像苹果一样的灯”理解为“水果灯”而不是“极简风格”。
*   **解决方案**: **CoT (Chain of Thought) + 用户确认环**。
    *   在搜索前，前端先展示 AI 的理解：“您是想要【极简主义风格】且【材质为光面塑料】的灯具吗？”
    *   用户点击“是”再进行数据库检索。

### 难点 C：冷启动 (Cold Start)
*   **挑战**: 只有 10 个 Maker 时，搜索很容易为空。
*   **解决方案**: **泛化匹配策略**。
    *   当精准匹配（Hard Filter）无结果时，自动降级为纯向量搜索（Vector Search），并提示用户：“没有完全符合参数的 Maker，但这些 Maker 的风格很接近，建议咨询。”
```

---

### 3. `DOC_03_UX_Concept.md`

```markdown
# 🎨 交互与体验设计 (UX/UI Concept)

## 1. 界面形态 (Interface Metaphor)
摒弃传统电商的“搜索框+侧边栏筛选”模式。
采用 **"AI 委托人 (AI Agent Delegate)"** 形态。

*   **首页**: 一个巨大的、居中的输入框（类似 Perplexity 或 Google 首页），配以背景流动的 Maker 案例墙。
*   **核心隐喻**: "Tell me what you dream, I'll find who can build it."

## 2. 交互流程 (User Flow: The "Translation" Journey)

### Step 1: 模糊输入 (Vague Input)
*   **User Action**: 输入 "我想给我的机械键盘做一个外壳，要那种透明的，像冰块一样的感觉，最好能透光。"
*   **System Action**: 后台 LLM 提取关键词：`Category: Keyboard Case`, `Material: Transparent/Acrylic/Resin`, `Style: Icy/Translucent`.

### Step 2: 意图确认 (Intent Confirmation - 关键一步)
*   **UI Display**: 系统弹出一个卡片（不是直接给结果）：
    > "收到。正在为您寻找擅长 **[CNC加工 / 树脂浇筑]** 工艺，且处理过 **[高透光材料]** 的 Maker。
    > 您对 **[精度]** 有要求吗？（选项：普通/严丝合缝）"
*   **Why**: 这一步即是“混合匹配”的体现，将自然语言锚定为硬性参数。

### Step 3: 匹配结果 (Smart Results)
*   **UI Display**: 展示 3-5 个 Maker 的卡片。
*   **Card Content**: 不仅展示 Maker 的名字，还要展示 **"Why Matched"**。
    > **Maker A**: 匹配度 95%。
    > *原因：他上个月刚制作过一个“树脂键帽”，材质与您描述的“冰块感”高度一致。*
*   **Action**: "一键发送询价" (将用户的描述自动打包发给这 3 个人)。

## 3. 可视化建议 (Visualization)
*   **能力雷达图**: 在 Maker 详情页，不要只列文字。用雷达图展示其能力偏向：`设计能力` vs `制造精度` vs `响应速度`。
*   **案例基因流**: 点击一个案例，展示其“基因”（Tag），点击 Tag 可以跳转到拥有相同基因的其他 Maker。
```

---

### 4. `DOC_04_Data_Schema.md`

```markdown
# 💾 数据流与 Schema 设计 (Data Flow & Schema Design)

## 1. 核心实体定义 (Entity Definition)

为了支持“非标品”和“混合检索”，我们需要一种 **Schema-less (JSONB) + Relational** 的混合设计。

### A. `Makers` (供给端主体)
存储 Maker 的基本信息和聚合能力评分。

### B. `Capabilities` (原子化能力 - 核心)
这是最关键的表。我们不把能力写死在 Maker 身上，而是通过 `Projects` (案例) 来推导能力。

### C. `Projects` (案例/作品)
Maker 的过往作品，是 AI 分析的数据源。

## 2. 数据结构 (Schema - PostgreSQL DDL Draft)

```sql
-- 启用向量扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Maker 表：基础账户
CREATE TABLE makers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL,
    bio TEXT,
    -- 核心：Maker 的综合能力向量（基于所有案例聚合生成）
    aggregate_embedding vector(1536), 
    -- 结构化标签汇总 (e.g., ["3D Printing", "CNC", "Leather"])
    tags JSONB 
);

-- 2. Project 表：案例库 (AI 分析的最小单元)
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    maker_id UUID REFERENCES makers(id),
    title TEXT,
    description TEXT, -- Maker 写的原始描述
    image_urls TEXT[],
    
    -- AI 提取的结构化参数 (Hard Filters)
    -- 示例: {"material": ["resin", "wood"], "process": "cnc", "min_tolerance": "0.1mm"}
    ai_extracted_specs JSONB, 
    
    -- AI 生成的语义向量 (Soft Search)
    embedding vector(1536),
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. RFQ 表：买家需求 (Request For Quotation)
CREATE TABLE rfqs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    buyer_id UUID,
    raw_query TEXT, -- 买家原始输入
    
    -- LLM 翻译后的需求规格
    translated_specs JSONB, 
    -- 示例: {"target_material": "acrylic", "budget_range": [100, 500]}
    
    query_embedding vector(1536), -- 用于匹配 Project 的 embedding
    status TEXT DEFAULT 'open'
);
```

## 3. 数据流转图 (Data Flow)

1.  **Ingestion (供给端)**:
    *   Maker Upload Image -> `Vision API` -> Extract Tags & Specs -> Save to `projects.ai_extracted_specs` -> Generate Embedding -> Save to `projects.embedding`.
    *   *Trigger*: Update `makers.aggregate_embedding` (重新计算该 Maker 所有案例向量的平均值，代表其核心风格)。

2.  **Matching (需求端)**:
    *   User Query -> `LLM Agent` -> 
        *   Path A: Extract Keywords (e.g., "CNC") -> SQL `WHERE ai_extracted_specs @> '{"process": "cnc"}'`
        *   Path B: Generate Vector -> Cosine Similarity with `projects.embedding`
    *   Merge Results -> Group by `maker_id` -> Return Top Makers.

## 4. 隐私与合规 (Privacy & Compliance)
*   **知识产权 (IP) 保护**: Maker 上传的案例图必须添加隐形水印（Invisible Watermark），防止被爬虫抓取用于训练其他模型。
*   **数据隔离**: 买家的定制需求（RFQ）属于私密数据，严禁公开索引，只有匹配到的 Maker 在签署保密协议（点击同意）后可见。
```