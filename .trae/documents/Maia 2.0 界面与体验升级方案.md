# Maia 2.0 视觉与交互体验升级方案 (Visual & UX Redesign Plan)

本方案旨在将 Maia 从一个简单的 Streamlit 工具升级为具有**科技感、呼吸感与高级感**的现代化 AI 产品。设计灵感源自苹果设计哲学 (Human Interface Guidelines) 与 Maia "思想助产士" 的核心隐喻——**光、诞生与清晰**。

## 1. 核心视觉体系 (Visual Identity)

### 1.1 设计关键词
*   **Ethereal (空灵)**: 拒绝沉闷的纯黑背景，使用极光般的柔和渐变。
*   **Lucid (清晰)**: 高对比度文字，大留白，信息层级分明。
*   **Breathing (呼吸感)**: 元素间距宽敞，微交互动画，避免拥挤。

### 1.2 配色方案 (Color Palette)
摒弃“黑不溜秋”的默认界面，采用 **"Aurora Dawn" (极光黎明)** 主题：
*   **背景 (Canvas)**:
    *   基础底色: `#FFFFFF` (纯白) 或 `#F9FAFB` (极淡灰)。
    *   环境光氛围: 使用 CSS 伪元素添加模糊的彩色光晕 (Blur Mesh)，模拟日出时的柔光 (淡紫、淡蓝、淡粉的混合)。
*   **文字 (Typography)**:
    *   标题: `#111827` (深灰，非纯黑)。
    *   正文: `#374151` (中灰)。
    *   辅助: `#6B7280` (浅灰)。
*   **强调色 (Accent)**:
    *   主色调: `#6366F1` (Indigo) -> `#8B5CF6` (Violet) 渐变。
    *   功能按钮: 玻璃拟态 (Glassmorphism) 或 渐变胶囊按钮。

### 1.3 字体与排版
*   **字体栈**: 优先调用系统级字体 (San Francisco for Mac)，确保与 macOS 原生体验一致。
*   **排版原则**: 增加行高 (Line-height: 1.6)，增加段间距，让阅读体验像阅读杂志一样舒适。

---

## 2. 界面重构方案 (UI Redesign)

我们将通过注入自定义 CSS (`st.markdown`) 深度改造 Streamlit 的原生组件。

### 2.1 全局样式 (Global Styles)
*   **Sidebar**: 去除默认的灰色背景，改为透明或半透明磨砂玻璃效果，与主内容区融为一体。
*   **Cards (卡片)**: 所有的内容区块（如历史记录、登录框）使用白色背景 + 极淡的投影 (`box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05)`) + 大圆角 (`border-radius: 16px`)。

### 2.2 关键页面设计
1.  **Landing Page (首页)**
    *   **Hero Section**: 巨大的、渐变的 "Maia" Logo 文字，配以 "Your Intellectual Midwife" 的副标题。
    *   **入口卡片**: "Guest Mode" 和 "Member Mode" 设计为两个并排的、有悬停上浮效果的卡片。

2.  **Chat Interface (对话页)**
    *   **气泡重绘**:
        *   **User**: 极淡的灰色胶囊 (`#F3F4F6`)，右对齐。
        *   **Maia**: 白色卡片 (`#FFFFFF`) 配以左侧彩色光条 (Border-left accent)，左对齐，体现“专业与洞察”。
    *   **输入框**: 悬浮在底部的磨砂玻璃条，让对话内容在背后滚动。

3.  **Dashboard (仪表盘)**
    *   **数据可视化**: 简单的统计数字（如 Token 使用量）使用大号细体数字展示。
    *   **历史列表**: 瀑布流或网格状的卡片布局。

---

## 3. 功能升级：中英双语 (Bilingual Support)

### 3.1 技术实现
*   **状态管理**: 在 `st.session_state` 中新增 `language` 字段 (默认 'zh')。
*   **字典架构**: 新建 `utils/i18n.py`，维护一个简单的键值对字典：
    ```python
    TRANSLATIONS = {
        "zh": {"landing_title": "Maia - 战略分析师", "guest_btn": "游客模式", ...},
        "en": {"landing_title": "Maia - Strategy Analyst", "guest_btn": "Guest Mode", ...}
    }
    ```
*   **切换开关**: 在 Sidebar 顶部添加一个精美的 `Segmented Control` 或 `Toggle Switch` 来切换语言。

---

## 4. 交互体验优化 (UX Improvements)

1.  **加载动画**: 在 Agent 思考时，不再使用枯燥的 `st.spinner`，而是尝试用 CSS 模拟一个“呼吸的光点”或“律动的波纹”，暗示 Maia 正在进行深度思考。
2.  **平滑过渡**: 页面切换时尝试添加简单的 Fade-in 效果（受限于 Streamlit，尽力而为）。
3.  **空状态 (Empty States)**: 当没有历史记录时，显示一张极简的 SVG 插画，而不是冷冰冰的文字提示。

---

## 5. 执行路线图 (Roadmap)

1.  **Step 1: 基础设施搭建**
    *   创建 `utils/i18n.py` 并提取现有文案。
    *   创建 `assets/custom.css` 集中管理样式。
2.  **Step 2: 视觉皮肤开发**
    *   编写 CSS 覆盖 Streamlit 默认样式 (背景、字体、按钮)。
    *   实现“极光”背景效果。
3.  **Step 3: 页面组件重构**
    *   按 Landing -> Auth -> Dashboard -> Chat 的顺序应用新设计。
4.  **Step 4: 双语功能接入**
    *   将硬编码的英文字符串替换为 `t("key")` 函数调用。
5.  **Step 5: 细节打磨**
    *   调整间距、阴影、动画参数。

您是否同意这个设计方案？如果同意，我将开始从 Step 1 着手实施。
