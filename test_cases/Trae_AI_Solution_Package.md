<think>**Considering User Needs**

I've been meticulously analyzing the user's profile, focusing on their role as a graduate student in HCI. I'm prioritizing their values, specifically aesthetics, usability, system thinking, and structure. These are key to shaping my approach, given their HCI background, and will strongly influence the deliverables, with their skills in interface design and information architecture.


**Mapping the Core Flow**

I'm now zeroing in on the core user flow: reading, processing, and writing. The aim is to address pain points like potential AI hallucinations and the disconnect between these phases, particularly the recall difficulties. The pivotal feature request is clear: a staging area for review before any data sync. A web app form factor is preferred, using Feishu Bitable as the backend, leveraging its ecosystem and a pro-code (React/Vue) approach.


**Adjusting the Approach**

I'm revisiting the proposed tech stack with a more pragmatic eye. While a custom React app is the ultimate aim, I now think **a Low-Code Frontend with Strong API Integration** is a better starting point, potentially leveraging Streamlit or Vercel AI SDK + Next.js templates to speed things up. I'm prioritizing the user's interface design expertise, but want to make sure the effort is manageable. The "Staging Area" remains the standout feature.


**Designing the Workbench**

I'm now drafting the UX/UI concept. I'm visualizing the user interface as "The Workbench" – a staging area that enables careful review and editing before syncing any information to Feishu. The core features are now becoming clearer, emphasizing a web-based interface and leveraging the user's interface expertise. I'm focusing on creating an intuitive, flexible, and powerful user experience.


**Structuring the Workbench**

I'm now detailing the Workbench's layout, aiming for a clean, spacious interface separate from storage. I'm settling on a three-column structure: Input (drop zone), Processing/Staging (review card), and Visualization (graph). The "Commit" action is the key interaction, positioning the user as the Editor and the AI as the Intern. I also have an evolving mental model for a force-directed graph combined with simpler cards for the Staging Area.

**Finalizing the Data Schema**

I've outlined the data schema, defining entities like Literature (Source), Atomic Note (Insight), and Author. It needs to map to Feishu Bitable's data types. The workflow involves converting PDFs to JSON, allowing user edits, and then updating Feishu records. I'm focusing on simplicity, as requested, specifically the basic database logic. Also I am ensuring the final formatting is strict. I will specifically use HCI terminology in the final delivery.


**Refining Output Structure**

I'm now prioritizing the Staging Area, ensuring it remains the focal point in the final deliverable. I'm focusing on simplicity in the data schema and formatting, as requested, while maintaining a relational structure. HCI terminology will be used consistently. This "Staging Area" will be showcased prominently to reflect its critical role, ensuring a seamless user experience. I will now generate the final Markdown content.


</think>

Based on the comprehensive interview analysis and the user's specific background (HCI major, System Thinking) and needs (Human-in-the-Loop, Feishu integration), here is the highly customized solution package.

The solution is named **"Scholar's Airlock"** (implying a safe transition zone between raw reading and permanent knowledge).

---

### DOC_01_PRD.md

```markdown
# 📄 DOC 01: Product Requirement Document (PRD)
## Project Name: Scholar's Airlock (Feishu-Integrated Knowledge OS)

### 1. 核心价值主张 (Value Proposition)
为追求高信度知识管理的学术研究者，打造一个**"带有人工质检环节的智能中转站"**。它隔离了 AI 的幻觉与知识库的纯净性，通过全屏可视化交互，让用户在将文献存入飞书（Feishu）之前，完成对元数据、摘要和关键洞察的审核与修正。

### 2. 用户故事 (User Stories)

*   **As an HCI Researcher (The Curator),**
    *   I want to drag-and-drop a PDF research paper into a web interface,
    *   So that the AI automatically extracts the title, authors, year, abstract, and 3 key methodologies.
    
*   **As a "Human-in-the-Loop" (The Editor),**
    *   I want to see a **"Staging Card" (预处理卡片)** where I can verify and edit the AI-generated tags and summary *before* they are saved,
    *   So that I don't pollute my pristine Feishu database with "garbage" or hallucinations.

*   **As a Visual Thinker,**
    *   I want to view my existing Feishu literature database as an interactive **Knowledge Graph** on a full screen,
    *   So that I can identify connections between my current reading and previous papers without being constrained by a sidebar.

### 3. 功能清单 (Feature List)

#### P0: Core Loop (The "Airlock" Workflow)
1.  **Ingestion Canvas**: 全屏拖拽上传区，支持 PDF 解析（针对双栏学术论文优化）。
2.  **AI Analysis Engine**: 自动提取元数据（Title, Author, Year, DOI）并生成结构化摘要（Background, Method, Result）。
3.  **The Staging Area (核心功能)**:
    *   一个"待入库"的中间态界面。
    *   提供 Diff 视图或高亮编辑区。
    *   "Confirm & Sync" 按钮：点击后才调用飞书 API 写入多维表格。
4.  **Feishu Connector**: 单向写入飞书多维表格（Bitable）。

#### P1: Insight & Visualization (The "Graph")
1.  **Graph Visualizer**: 读取飞书多维表格中的关联字段，渲染全屏力导向图（Force-Directed Graph）。
2.  **Retrieval Chat**: 基于飞书已有数据的 QA 问答（"我之前哪篇文章提到过 Fitts' Law?"）。

### 4. 验收标准 (Success Metrics)
*   **Data Hygiene**: 存入飞书的数据准确率达到 100%（经过人工确认）。
*   **Efficiency**: 从 PDF 上传到确认入库的平均耗时 < 30秒。
*   **Satisfaction**: 用户不再需要频繁 Alt+Tab 切换飞书和阅读器，所有元数据处理在 Web App 一站式完成。

```

---

### DOC_02_Tech_Architecture.md

```markdown
# 🏗️ DOC 02: Technical Architecture & Implementation Guide

## 1. 系统架构图 (Architecture Diagram)

```mermaid
graph TD
    User((User / Researcher))
    
    subgraph "Frontend (Standalone Web App)"
        UI_Input[Ingestion UI (Drag & Drop)]
        UI_Stage[Staging Area (Editor Interface)]
        UI_Viz[Knowledge Graph Canvas]
    end
    
    subgraph "Logic Layer (Next.js / Python)"
        Parser[PDF Parsing Service]
        LLM[LLM Agent (Extraction & Structuring)]
        Transformer[JSON Formatter]
    end
    
    subgraph "Storage Ecosystem"
        Feishu_API[Feishu Open API]
        Feishu_Base[(Feishu Bitable / Multidimensional Table)]
        Feishu_App[Feishu Desktop Client]
    end

    User -->|Upload PDF| UI_Input
    UI_Input -->|Raw File| Parser
    Parser -->|Text Chunks| LLM
    LLM -->|Structured JSON| UI_Stage
    
    User -->|Review & Edit| UI_Stage
    UI_Stage -->|Confirmed JSON| Transformer
    Transformer -->|Create Record| Feishu_API
    Feishu_API -->|Store| Feishu_Base
    
    Feishu_Base -->|Read Records| Feishu_API
    Feishu_API -->|Graph Data| UI_Viz
    UI_Viz -->|Explore| User
```

## 2. 技术栈选型 (Tech Stack)

鉴于用户具有 HCI 背景（懂设计和逻辑）但非硬核后端开发，推荐 **"Modern Frontend + BaaS (Backend as a Service)"** 模式：

*   **前端/交互层 (Frontend)**: 
    *   **Next.js (React)**: 利用 Vercel 部署。React 生态拥有最好的拖拽库 (`react-dropzone`) 和 图可视化库 (`react-force-graph`)。
    *   **Tailwind CSS**: 快速构建极简、高审美的学术风界面。
*   **逻辑/编排层 (Logic)**:
    *   **Vercel AI SDK**: 处理 LLM 流式输出。
    *   **LangChain / LlamaIndex**: 用于 PDF 解析管道（建议使用 `Unstructured` 或 `Nougat` 针对学术论文优化的解析器）。
*   **模型层 (Model)**:
    *   **GPT-4o / Claude 3.5 Sonnet**: 必须使用高智商模型以确保提取的学术概念准确。
*   **数据/存储层 (Storage)**:
    *   **Feishu Bitable (飞书多维表格)**: 作为 Headless CMS 和数据库。

## 3. 关键难点与攻克 (Key Challenges & Solutions)

### A. 学术 PDF 的解析精度 (PDF Parsing)
*   **痛点**: 学术论文通常是双栏排版，含有图表公式，普通 OCR 容易乱序。
*   **解决方案**: 使用专门针对论文训练的解析库（如 `Grobid` 或 `Mathpix API`）。如果预算有限，使用 `PyPDF2` + LLM 自我纠错（Prompt: "Reconstruct this broken text flow from a two-column layout"）。

### B. 飞书 API 的鉴权与频率 (API Auth & Rate Limits)
*   **痛点**: 飞书 OpenAPI 需要处理 `tenant_access_token` 的时效性。
*   **解决方案**: 
    1.  创建一个飞书企业自建应用 (Custom App)。
    2.  在 Next.js API Route 中封装一个 `getFeishuToken()` 函数，利用 Redis (如 Upstash) 缓存 Token 2小时，避免频繁请求。

### C. 知识图谱的渲染性能
*   **痛点**: 如果文献超过 500 篇，前端渲染可能会卡顿。
*   **解决方案**: 使用 WebGL 渲染图谱 (利用 `react-force-graph-3d` 或 `Sigma.js`)，而不是 SVG。只加载元数据，不加载全文。

```

---

### DOC_03_UX_Concept.md

```markdown
# 🎨 DOC 03: UX/UI Concept Design
## Design Philosophy: "Cognitive Offloading" (认知卸载)

用户是 HCI 学生，界面设计必须体现**"直接操纵 (Direct Manipulation)"** 和 **"状态可见性 (Visibility of System Status)"**。

## 1. 界面形态 (Interface Metaphor)
产品形态为一个**全屏 Web 工作台 (The Workbench)**，而非聊天窗口。它模仿图书馆的"整理桌"。

## 2. 交互流程 (User Flow)

### Step 1: Ingestion (The Drop Zone)
*   **Visual**: 屏幕中央一个巨大的、极简的虚线框。背景可以是微弱的粒子动画。
*   **Action**: 用户将 PDF 拖入。
*   **Feedback**: 进度条显示 "Reading Paper..." -> "Extracting Concepts..." -> "Drafting Entry...".

### Step 2: The Airlock (The Staging Interface) - *Critical*
*   **Layout**: 双栏布局。
    *   **左侧**: PDF 原文预览（可高亮）。
    *   **右侧**: 结构化表单（Editable Cards）。
*   **Interaction**: 
    *   AI 填好的字段（标题、作者、标签）显示为浅绿色背景。
    *   用户点击任何字段即可修改。
    *   **底部浮动按钮**: 一个醒目的 **"Commit to Database" (确认入库)** 按钮。这给予用户"把关人"的心理安全感。

### Step 3: Integration (The Graph View)
*   **Trigger**: 点击 "Commit" 成功后的 Toast 提示 "Synced to Feishu!"，随后背景淡入知识图谱。
*   **Visual**: 新录入的节点在图谱中高亮闪烁，自动连线到相关的旧文献（基于关键词匹配）。

## 3. 可视化建议 (Visualization)

*   **文献节点**: 使用圆形节点，大小代表引用量或重要性（用户打分）。
*   **颜色编码**: 
    *   🔵 Theory (理论类)
    *   🟢 Methodology (方法类)
    *   🔴 Case Study (案例类)
*   **交互**: 鼠标悬停显示摘要 Tooltip，点击节点跳转回飞书记录详情页。

```

---

### DOC_04_Data_Schema.md

```markdown
# 💾 DOC 04: Data Flow & Schema Design

## 1. 核心实体定义 (Entity Definition)
我们需要在飞书多维表格中定义一张核心主表（Master Table）和一张辅助表（Tags/Authors）。

### Entity: `Literature_Item` (文献单体)
这是知识库的基本单位。

## 2. 数据结构 (Schema Strategy)

建议在飞书多维表格中建立以下字段结构。这既符合数据库逻辑，也方便 AI 填充。

| Field Name | Type (Feishu) | Description | AI Processing Logic |
| :--- | :--- | :--- | :--- |
| **Title** | Text | 论文标题 | 直接提取 |
| **Status** | Single Select | `Inbox`, `Reading`, `Archived` | 默认为 `Inbox` |
| **Authors** | Multi-Select | 作者名（用于关联聚合） | 提取并分割为数组 |
| **Year** | Number | 发表年份 | 提取 |
| **Topic Tags** | Multi-Select | 核心领域 (e.g. `HCI`, `AI`) | 基于内容生成 Top 5 标签 |
| **TL;DR** | Text (Long) | 一句话总结 | LLM 生成 (< 50 words) |
| **Key Insights** | Text (Rich) | 关键洞察/方法论 | 提取 Bullet points |
| **PDF Attachment**| Attachment | 原始文件 | 上传并关联 |
| **Related_IDs** | Text | 关联的其他文献 Record ID | 留空，由图谱分析计算后回填 |
| **Last_Modified**| Date | 最后修改时间 | System Auto |

## 3. 数据流转逻辑 (Data Flow)

```json
/* Example JSON State object passing from Web App to Feishu API */
{
  "fields": {
    "Title": "Direct Manipulation Interfaces",
    "Status": "Inbox",
    "Authors": ["Ben Shneiderman"],
    "Year": 1983,
    "Topic Tags": ["HCI", "GUI", "Interaction Design"],
    "TL;DR": "Foundational paper defining the principles of direct manipulation in UIs.",
    "Key Insights": "1. Continuous representation of the object of interest.\n2. Physical actions or labeled button presses instead of complex syntax.\n3. Rapid incremental reversible operations."
  }
}
```

## 4. 隐私与合规 (Privacy & Compliance)

*   **Personal Use**: 由于是用户个人的学术数据库，主要关注**Token Security**。确保飞书的 `App Secret` 存储在 Vercel 的环境变量中，不可暴露在前端代码里。
*   **Copyright**: 提醒用户上传的 PDF 仅供个人学术研究使用，不要在 Web App 中建立公开分享链接。
```