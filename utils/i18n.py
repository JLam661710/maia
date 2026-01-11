
# Internationalization Dictionary for Maia

TRANSLATIONS = {
    "en": {
        # Global
        "app_title": "Maia - Product Strategy Interviewer",
        "sidebar_control": "🛠️ Control Panel",
        "sidebar_lang": "Language / 语言",
        
        # Landing Page
        "landing_title": "Maia · Strategy Analyst",
        "landing_subtitle": "Your Intellectual Midwife for Product Strategy",
        "landing_subtitle_desc": "From vague ideas to concrete blueprints. A responsive AI partner.",
        "mode_guest_title": "🚀 Guest Mode",
        "mode_guest_desc": "Instant access. No strings attached.",
        "mode_guest_warn": "⚠️ History clears on exit.",
        "btn_start_guest": "Start as Guest",
        "mode_member_title": "🔐 Member Mode",
        "mode_member_desc": "Cloud sync & history tracking.",
        "mode_member_feat": "✅ Features: Cloud Sync, History, Project Mgmt.",
        "btn_login_reg": "Login / Register",
        
        # Auth Page
        "auth_title": "Account Access",
        "btn_back_home": "← Back to Home",
        "tab_login": "Login",
        "tab_register": "Register",
        "lbl_email": "Email",
        "lbl_password": "Password",
        "lbl_nickname": "Nickname (e.g. Feishu Name)",
        "lbl_pass_confirm": "Confirm Password",
        "btn_signin": "Sign In",
        "btn_create_account": "Create Account",
        "err_pass_mismatch": "Passwords do not match!",
        "success_welcome": "Welcome back!",
        "success_created": "Account created! You are now logged in.",
        
        # Dashboard
        "dash_hi": "👋 Hi, {nickname}",
        "dash_profile": "Profile",
        "btn_logout": "Logout",
        "dash_actions": "🌟 Actions",
        "btn_new_chat": "➕ Start New Conversation",
        "dash_history": "📜 History",
        "msg_no_history": "No history yet. Start a new conversation!",
        "btn_load_session": "Load Session {sid}",
        "status_label": "Status",
        
        # Chat
        "chat_header": "Maia: Product Strategy Interviewer",
        "btn_back_dash": "← Back to Dashboard",
        "btn_exit_guest": "🏠 Back to Home (Exit Guest Mode)",
        "metric_tokens": "Total Tokens Used",
        "status_saving": "💾 Saving to DB...",
        "expander_state": "View JSON State",
        "input_placeholder": "Type your response here...",
        "status_analyst": "🧠 Analyst is thinking...",
        "status_updated": "✅ State Updated",
        "spinner_compress": "Compressing...",
        "spinner_typing": "Maia is typing...",
        "msg_completed": "🎉 Interview Completed!",
        "btn_draft_docs": "Draft Final Documents",
        "spinner_drafting": "Drafting documents...",
        "header_deliverables": "## 📄 Deliverables",
        
        # Roles & System
        "role_assistant": "Maia",
        "role_user": "You"
    },
    "zh": {
        # Global
        "app_title": "Maia - 产品战略访谈助手",
        "sidebar_control": "🛠️ 控制面板",
        "sidebar_lang": "语言 / Language",
        
        # Landing Page
        "landing_title": "Maia · 响应式 AI 产品战略访谈者",
        "landing_subtitle": "你的 AI 思想助产士",
        "landing_subtitle_desc": "从模糊的灵感到具体的蓝图。响应式 AI 战略伙伴。",
        "mode_guest_title": "🚀 游客模式",
        "mode_guest_desc": "即刻体验，无需注册。",
        "mode_guest_warn": "⚠️ 关闭页面后历史记录将消失。",
        "btn_start_guest": "以游客身份开始",
        "mode_member_title": "🔐 会员模式",
        "mode_member_desc": "云端同步，历史回溯。",
        "mode_member_feat": "✅ 特性：云同步、历史记录、项目管理。",
        "btn_login_reg": "登录 / 注册",
        
        # Auth Page
        "auth_title": "账户访问",
        "btn_back_home": "← 返回首页",
        "tab_login": "登录",
        "tab_register": "注册",
        "lbl_email": "邮箱",
        "lbl_password": "密码",
        "lbl_nickname": "昵称 (例如飞书名)",
        "lbl_pass_confirm": "确认密码",
        "btn_signin": "登录",
        "btn_create_account": "创建账户",
        "err_pass_mismatch": "两次输入的密码不一致！",
        "success_welcome": "欢迎回来！",
        "success_created": "账户创建成功！已自动登录。",
        
        # Dashboard
        "dash_hi": "👋 你好, {nickname}",
        "dash_profile": "个人资料",
        "btn_logout": "退出登录",
        "dash_actions": "🌟 操作",
        "btn_new_chat": "➕ 开始新对话",
        "dash_history": "📜 历史记录",
        "msg_no_history": "暂无历史记录。开始一个新的对话吧！",
        "btn_load_session": "加载会话 {sid}",
        "status_label": "状态",
        
        # Chat
        "chat_header": "Maia: 产品战略访谈",
        "btn_back_dash": "← 返回仪表盘",
        "btn_exit_guest": "🏠 返回首页 (退出游客模式)",
        "metric_tokens": "Token 消耗量",
        "status_saving": "💾 数据保存中...",
        "expander_state": "查看内部状态 (JSON)",
        "input_placeholder": "在此输入你的回复...",
        "status_analyst": "🧠 分析师正在思考...",
        "status_updated": "✅ 状态已更新",
        "spinner_compress": "正在压缩上下文...",
        "spinner_typing": "Maia 正在输入...",
        "msg_completed": "🎉 访谈已完成！",
        "btn_draft_docs": "起草最终文档",
        "btn_download_md": "下载 Markdown 文档",
        "spinner_drafting": "正在撰写文档...",
        "header_deliverables": "## 📄 交付产物",
        
        # Roles & System
        "role_assistant": "Maia",
        "role_user": "你"
    }
}

def get_text(key, lang="zh", **kwargs):
    """Helper function to get text based on language code."""
    text = TRANSLATIONS.get(lang, TRANSLATIONS["zh"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
