参考与延伸阅读资源库

Part 1: 核心学术论文

1. 思维链 (Chain of Thought, CoT)
• 标题: Chain-of-Thought PromptingElicitsReasoning in Large Language Models
• 链接:  https://arxiv.org/abs/2201.11903 
• 简介: 首次系统性地证明，通过在提示中加入“思考过程”的范例，可以激发大语言模型解决复杂推理任务的能力，是结构化提示的奠基性工作。

2. 思维树 (Tree of Thoughts, ToT)
• 标题: Tree of Thoughts:DeliberateProblem Solving with Large Language Models
• 链接:  https://arxiv.org/abs/2305.10601 
• 简介: 将线性的思维链扩展为树状的多路径探索。它允许 Agent 在一个思考节点上探索多个不同的推理路径，并使用自我评估来决定最优解，是更强大的结构化思考流程。

3. Reflexion框架
• 标题: Reflexion: Language Agents withVerbalReinforcementLearning
• 链接:  https://arxiv.org/abs/2303.11366 
• 简介: 首次将“自我反思/复盘”这一概念框架化、自动化。它证明了 Agent 可以通过对过往失败进行“语言反思”来迭代优化自身行为，而无需重新训练模型。

4. ReAct框架
• 标题: ReAct:SynergizingReasoning and Acting in Language Models
• 链接:  https://arxiv.org/abs/2210.03629 
• 简介: 提出了里程碑式的  Thought -> Act -> Observe  框架，将“思考”（Reasoning）和“行动”（Acting）深度交织，是现代 Agent 框架与外部世界交互的理论基石。

5. CodeAct 框架
• 标题: CodeAct: A Multi-Turn Code Agent with In-Context Learning
• 链接:  https://arxiv.org/abs/2402.01030 
• 简介: 雄辩地证明了 Agent 的  Act  环节可以从“调用预定义工具”进化到“即时生成代码并执行”，极大地扩展了 Agent 的能力边界。

Part 2: 行业资料与实践资源

1. 奠基性的综述：Lilian Weng的《LLM-poweredAutonomousAgents》
• 链接:  https://lilianweng.github.io/posts/2023-06-23-agent/ 
• 类型: 博客/技术综述
• 简介: OpenAI 应用研究负责人撰写的、行业内引用最广泛的 Agent 综述文章，是建立该领域全局认知地图的第一站。

2. 核心思想：“LLM操作系统” by Andrej Karpathy
• 简介: Andrej Karpathy (OpenAI创始成员) 在多个演讲中极具前瞻性地提出，LLM 是新型计算范式的“CPU”，而 Agent 框架则扮演了“操作系统（OS）”的角色。
• 类型: 演讲/理念

3. 主流开发框架：LangGraph & LlamaIndex
• 链接:  https://www.langchain.com/langgraph  和  https://www.llamaindex.ai/ 
• 类型: 框架官网/文档
• 简介: 当下构建 Agent 应用的两大事实标准库。LangGraph 侧重于流程（Chain & Agent），LlamaIndex 侧重于数据（RAG），是开发者将理论付诸实践的首选工具。
前沿架构探索

4. 规约驱动的协同 (Specification-DrivenCollaboration)
• 简介: 解决多 Agent 协作的核心，在于建立一套机器可读的“契约”或“规约”(Specification)。这一方向的代表性项目包括 AI IDE Kiro ( https://kiro.dev/ ) 和开源工具包 SpecKit ( https://github.com/braid-work/spec-kit )。
• 类型: 产品官网与开源代码库

5. 复杂工具的智能编排 (Intelligent ToolOrchestration)
• 简介: 强大的 Agent 应能为达成一个复杂目标，自主地、多步骤地规划并调用一系列工具。Anthropic 的 “Skills” 功能 ( https://www.anthropic.com/news/skills ) 将 Agent 的工具使用能力从“单次调用”提升到了“智能编排”，是这一方向的最佳行业实践。
• 类型: 产品功能公告/新闻页面

6. 社会行为涌现：斯坦福的“西部世界小镇” (Generative Agents)
• 论文: GenerativeAgents:InteractiveSimulacraof HumanBehavior( https://arxiv.org/abs/2304.03442 )
• 简介: 一项现象级的 AI 实验，展示了当 Agent 拥有了记忆和反思能力后，在一个虚拟社会中能够涌现出多么可信的自发行为，是多 Agent 系统探索的绝佳延伸阅读。
