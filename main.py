import streamlit as st
import json
import time
from dotenv import load_dotenv
import os

# Load env vars BEFORE importing db_client
load_dotenv(override=True)

from utils.db_client import db_client 
from utils.analytics import analytics
from utils.i18n import get_text as t, TRANSLATIONS
from utils.deliverables import split_deliverables
from utils.tool_catalog import load_tool_catalog, build_catalog_injection

from agents.interviewer import InterviewerAgent
from agents.analyst import AnalystAgent
from agents.architect import ArchitectAgent
from agents.summary import SummaryAgent
from agents.judge import JudgeAgent

# Page Config
st.set_page_config(page_title="Maia", page_icon="🤖", layout="wide")

# Load Custom CSS
def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Default JSON State (v2, backward-compatible)
def default_json_state():
    return {
        "schema_version": "v2.1",
        "user_profile": {},
        "project_needs": {},
        "needs_analysis": {},
        "product_assessment": {},
        "tech_strategy": {},
        "status": "In Progress",
        "completion_readiness": 0,
        "blockers": [],
        "missing_info": [
            "User Role",
            "Project Goal",
            "Scenario Clarity",
            "Loss Magnitude",
            "Preferred Platform (Form)",
        ],
        "product_framework": {
            "form": {},
            "data": {},
            "service": {},
            "distribution": {},
            "touch": {},
        },
        "versioning_and_delivery": {
            "mvp_shell_plan": None,
            "git_workflow": None,
            "release_strategy": None,
        },
        "deployment": {
            "channels": [],
            "domain_visibility": None,
            "environments": {},
        },
        "observability": {
            "analytics_tools": [],
            "key_events": [],
            "key_metrics": [],
        },
        "growth": {
            "seo_plan": None,
            "acquisition_channels": [],
        },
        "monetization": {
            "pricing": None,
            "payment_methods": [],
            "charge_timing": None,
        },
        "evaluation": {
            "distilled_pain": None,
            "evidence_gaps": [],
            "scenario_gaps": [],
            "next_questions": [],
            "red_flags": [],
            "last_judge_notice": None,
        },
        "decision_log": [],
        "interview_session": {
            "stage": "initial",
            "system_notice": None,
        },
    }

# Initialize Session State
if "page_mode" not in st.session_state: st.session_state.page_mode = "LANDING" # LANDING, AUTH, DASHBOARD, CHAT
if "user_info" not in st.session_state: st.session_state.user_info = None # None for Guest
if "session_id" not in st.session_state: st.session_state.session_id = None
if "messages" not in st.session_state: st.session_state.messages = []
if "lang" not in st.session_state: st.session_state.lang = "zh" # Default to Chinese
if "json_state" not in st.session_state:
    st.session_state.json_state = default_json_state()
if "system_notice" not in st.session_state: st.session_state.system_notice = "Start the interview. Ask the user who they are and what they want to build."
if "conversation_summary" not in st.session_state: st.session_state.conversation_summary = ""
if "archived_count" not in st.session_state: st.session_state.archived_count = 0
if "total_cost_tokens" not in st.session_state: st.session_state.total_cost_tokens = 0
if "processing_analyst" not in st.session_state: st.session_state.processing_analyst = False
if "judge_gate_counts" not in st.session_state:
    st.session_state.judge_gate_counts = {"initial": 0, "correction": 0, "pre_completion": 0, "delivery_pre_draft": 0}
if "judge_last_gate" not in st.session_state: st.session_state.judge_last_gate = None
if "tool_catalog" not in st.session_state:
    catalog, err, record = load_tool_catalog(db_client)
    st.session_state.tool_catalog = catalog
    st.session_state.tool_catalog_error = err
    st.session_state.tool_catalog_record = record
if "tool_catalog_injection" not in st.session_state:
    if isinstance(st.session_state.tool_catalog, dict):
        st.session_state.tool_catalog_injection = build_catalog_injection(st.session_state.tool_catalog)
    else:
        st.session_state.tool_catalog_injection = ""

# Initialize Agents
if "agents_loaded" not in st.session_state:
    st.session_state.interviewer = InterviewerAgent()
    st.session_state.analyst = AnalystAgent()
    st.session_state.architect = ArchitectAgent()
    st.session_state.summary_agent = SummaryAgent()
    st.session_state.judge = JudgeAgent()
    st.session_state.agents_loaded = True

# Helper to get text with current lang
def text(key, **kwargs) -> str:
    val = t(key, lang=st.session_state.lang, **kwargs)
    return str(val) if val is not None else ""

# Global Sidebar for Language
with st.sidebar:
    st.markdown(f"### 🌐 {text('sidebar_lang')}")
    lang_code = st.radio(
        "Language", 
        options=["zh", "en"], 
        format_func=lambda x: "中文" if x == "zh" else "English",
        index=0 if st.session_state.lang == "zh" else 1,
        label_visibility="collapsed"
    )
    if lang_code != st.session_state.lang:
        st.session_state.lang = lang_code
        st.rerun()

# ==========================================
# 1. LANDING PAGE
# ==========================================
def render_landing():
    analytics.track_event("guest", "page_view", {"page": "landing"})
    st.markdown(f"<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0.5rem;'>{text('landing_title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header'>{text('landing_subtitle')}<br><span style='font-size: 0.9em; opacity: 0.8'>{text('landing_subtitle_desc')}</span></p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div class='maia-card'>
            <h3>{text('mode_guest_title')}</h3>
            <p>{text('mode_guest_desc')}</p>
            <p style='color: #F59E0B; font-size: 0.9em;'>{text('mode_guest_warn')}</p>
        </div>
        """, unsafe_allow_html=True)
        # GUEST MODE DISABLED FOR LAUNCH
        # if st.button(text('btn_start_guest'), use_container_width=True, type="primary"):
        #     st.session_state.user_info = None
        #     # Create Guest Session
        #     sid = db_client.create_session(user_id=None)
        #     st.session_state.session_id = sid
        #     st.session_state.page_mode = "CHAT"
        #     st.rerun()
        st.info("游客模式已暂停开放 (Guest Mode Disabled)")

    with col2:
        st.markdown(f"""
        <div class='maia-card'>
            <h3>{text('mode_member_title')}</h3>
            <p>{text('mode_member_desc')}</p>
            <p style='color: #10B981; font-size: 0.9em;'>{text('mode_member_feat')}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(text('btn_login_reg'), use_container_width=True):
            st.session_state.page_mode = "AUTH"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. AUTH PAGE
# ==========================================
def render_auth():
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{text('auth_title')}</h2>", unsafe_allow_html=True)
    
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        if st.button(text('btn_back_home')):
            st.session_state.page_mode = "LANDING"
            st.rerun()

        st.markdown("<div class='maia-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs([text('tab_login'), text('tab_register')])
        
        with tab1:
            email = st.text_input(text('lbl_email'), key="login_email")
            password = st.text_input(text('lbl_password'), type="password", key="login_pass")
            if st.button(text('btn_signin'), type="primary", use_container_width=True):
                user, error = db_client.sign_in(email, password)
                if user:
                    st.success(text('success_welcome'))
                    st.session_state.user_info = user
                    st.session_state.page_mode = "DASHBOARD"
                    st.rerun()
                else:
                    st.error(f"Login Failed: {error}")

        with tab2:
            r_nickname = st.text_input(text('lbl_nickname'), key="reg_nick")
            r_email = st.text_input(text('lbl_email'), key="reg_email")
            r_pass = st.text_input(text('lbl_password'), type="password", key="reg_pass")
            r_pass_conf = st.text_input(text('lbl_pass_confirm'), type="password", key="reg_pass_conf")
            r_invite_code = st.text_input("邀请码 (Invitation Code)", key="reg_invite")
            
            if st.button(text('btn_create_account'), use_container_width=True):
                # 1. Check Invite Code
                valid_code = os.getenv("INVITE_CODE")
                if not r_invite_code or r_invite_code.strip() != valid_code:
                    st.error("邀请码无效 (Invalid Invitation Code)")
                elif r_pass != r_pass_conf:
                    st.error(text('err_pass_mismatch'))
                else:
                    user, error = db_client.sign_up(r_email, r_pass, r_nickname)
                    if user:
                        analytics.identify_user(user.id, {"email": r_email, "nickname": r_nickname})
                        st.success(text('success_created'))
                        st.session_state.user_info = user
                        st.session_state.page_mode = "DASHBOARD"
                        st.rerun()
                    else:
                        st.error(f"Registration Failed: {error}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. DASHBOARD PAGE
# ==========================================
def render_dashboard():
    user = st.session_state.user_info
    nickname = user.user_metadata.get('nickname', 'User') if user else 'User'
    
    st.markdown("<div class='animate-fade-in'>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-header'>{text('dash_hi', nickname=nickname)}</div>", unsafe_allow_html=True)
    
    col_act, col_info = st.columns([3, 1], gap="large")
    
    with col_info:
        st.markdown(f"""
        <div class='maia-card'>
            <h3>{text('dash_profile')}</h3>
            <p><strong>{text('lbl_email')}:</strong><br>{user.email}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(text('btn_logout'), use_container_width=True):
            db_client.sign_out()
            st.session_state.user_info = None
            st.session_state.page_mode = "LANDING"
            st.rerun()
            
    with col_act:
        st.markdown(f"### {text('dash_actions')}")
        if st.button(text('btn_new_chat'), type="primary", use_container_width=True):
            # Create User Session
            sid = db_client.create_session(user_id=user.id)
            analytics.track_event(user.id, "session_start", {"session_id": sid})
            st.session_state.session_id = sid
            # Reset Chat State
            st.session_state.messages = []
            st.session_state.json_state = default_json_state()
            st.session_state.system_notice = "Start the interview."
            st.session_state.page_mode = "CHAT"
            st.rerun()
            
        st.markdown(f"### {text('dash_history')}")
        sessions = db_client.get_user_sessions(user.id)
        
        if not sessions:
            st.info(text('msg_no_history'))
        else:
            for s in sessions:
                with st.container():
                    st.markdown(f"""
                    <div class='maia-card' style='margin-bottom: 10px; padding: 15px;'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <h4 style='margin:0;'>📅 {s['created_at'][:10]}</h4>
                            <span style='background: #E0E7FF; color: #4338CA; padding: 2px 8px; border-radius: 10px; font-size: 0.8em;'>{s['status']}</span>
                        </div>
                        <p style='color: #6B7280; margin-top: 5px;'>{s.get('conversation_summary') or '...'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(text('btn_load_session', sid=str(s['id'])[:8]), key=s['id']):
                        # Load History
                        msgs, state = db_client.load_session_history(s['id'])
                        st.session_state.session_id = s['id']
                        st.session_state.messages = msgs
                        if state: st.session_state.json_state = state
                        st.session_state.page_mode = "CHAT"
                        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 4. CHAT PAGE
# ==========================================
def render_chat():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("---")
        if st.session_state.user_info:
            if st.button(text('btn_back_dash'), use_container_width=True):
                st.session_state.page_mode = "DASHBOARD"
                st.rerun()
        else:
            if st.button(text('btn_exit_guest'), use_container_width=True):
                st.session_state.page_mode = "LANDING"
                st.rerun()
                
        st.markdown(f"### {text('sidebar_control')}")
        
        # ADMIN VIEW LOGIC
        # Only show metrics to admins
        current_email = st.session_state.user_info.email if st.session_state.user_info else ""
        ADMIN_EMAILS = ["1037078681@qq.com", "linxuan1037078681@gmail.com"]
        
        if current_email in ADMIN_EMAILS:
            st.metric(text('metric_tokens'), st.session_state.total_cost_tokens)
            
            if st.session_state.session_id:
                st.caption(f"{text('status_saving')} (ID: ...{str(st.session_state.session_id)[-6:]})")
            
            with st.expander(text('expander_state'), expanded=False):
                st.json(st.session_state.json_state)

            with st.expander("选型清单 (Human-in-the-loop)", expanded=False):
                record = st.session_state.tool_catalog_record if isinstance(st.session_state.tool_catalog_record, dict) else {}
                version = record.get("version")
                updated_at = record.get("updated_at")
                updated_by = record.get("updated_by")
                if version:
                    st.caption(f"在线版本: v{version}  更新: {updated_at or '-'}  更新人: {updated_by or '-'}")
                elif st.session_state.tool_catalog_error:
                    st.warning(f"选型清单加载失败: {st.session_state.tool_catalog_error}")
                else:
                    st.caption("当前使用本地默认清单（DB 未启用或暂无在线版本）")

                current_text = ""
                if isinstance(record, dict) and isinstance(record.get("content_text"), str):
                    current_text = record["content_text"]
                elif isinstance(st.session_state.tool_catalog, dict):
                    current_text = json.dumps(st.session_state.tool_catalog, ensure_ascii=False, indent=2)

                edited = st.text_area("编辑清单（JSON）", value=current_text, height=260)
                col_a, col_b = st.columns([1, 2])
                with col_a:
                    if st.button("保存清单", use_container_width=True):
                        try:
                            parsed = json.loads(edited or "")
                            if not isinstance(parsed, dict):
                                raise ValueError("必须是 JSON 对象")
                            who = st.session_state.user_info.email if st.session_state.user_info else None
                            rec = db_client.upsert_admin_config("tool_catalog", edited, content_json=parsed, updated_by=who)
                            st.session_state.tool_catalog = parsed
                            st.session_state.tool_catalog_record = rec
                            st.session_state.tool_catalog_error = None
                            st.session_state.tool_catalog_injection = build_catalog_injection(parsed)
                            analytics.track_event(
                                st.session_state.user_info.id if st.session_state.user_info else "guest",
                                "tool_catalog_saved",
                                {"config_key": "tool_catalog", "version": rec.get("version") if isinstance(rec, dict) else None},
                            )
                            st.toast("选型清单已保存", icon="✅")
                        except Exception as e:
                            st.error(f"保存失败: {e}")
                with col_b:
                    st.text_area("注入预览", value=st.session_state.tool_catalog_injection or "", height=180)

            with st.expander("导出诊断包 (Diagnostic Bundle)", expanded=False):
                payload = {
                    "session_id": st.session_state.session_id,
                    "messages": st.session_state.messages,
                    "json_state": st.session_state.json_state,
                    "system_notice": st.session_state.system_notice,
                    "conversation_summary": st.session_state.conversation_summary,
                    "archived_count": st.session_state.archived_count,
                    "judge_gate_counts": st.session_state.judge_gate_counts,
                    "tool_catalog_record": st.session_state.tool_catalog_record,
                    "tool_catalog_injection": st.session_state.tool_catalog_injection,
                    "deliverables_docs": st.session_state.final_deliverables_docs if "final_deliverables_docs" in st.session_state else None,
                }
                data = json.dumps(payload, ensure_ascii=False, indent=2)
                name = f"maia_diagnostic_{str(st.session_state.session_id)[:8] if st.session_state.session_id else 'no_session'}.json"
                st.download_button("下载诊断包", data=data, file_name=name, mime="application/json")
        else:
            # For normal users, show nothing or minimal info
            pass

        raw_analyst = st.session_state.get("last_analyst_raw_output") if hasattr(st, "session_state") else None
        if isinstance(raw_analyst, str) and raw_analyst.strip():
            with st.expander("诊断：最近一次 Analyst 原始输出（截断）", expanded=False):
                st.text_area("Raw Output", value=raw_analyst, height=220)

    st.markdown(f"<h2 style='text-align: center; margin-bottom: 2rem;'>{text('chat_header')}</h2>", unsafe_allow_html=True)

    # Auto-start logic
    if not st.session_state.messages:
        interviewer = st.session_state.interviewer
        response = interviewer.run(
            history=[], 
            system_notice=st.session_state.system_notice,
            context_summary=st.session_state.conversation_summary,
            tool_catalog_injection=st.session_state.tool_catalog_injection
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        db_client.save_message(st.session_state.session_id, "assistant", response)
        st.rerun()

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Analyst Logic (Blocking)
    if st.session_state.processing_analyst:
        analyst = st.session_state.analyst
        
        # Custom thinking animation
        st.markdown(f"""
        <div class='thinking-pulse' style='
            text-align: center; 
            padding: 20px; 
            background: rgba(255,255,255,0.5); 
            border-radius: 12px; 
            margin: 20px 0;
            color: #6366F1;
            font-weight: 500;
        '>
            {text('status_analyst')}
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.2)
        try:
            recent_messages = st.session_state.messages[st.session_state.archived_count:]
            new_analysis = analyst.run(
                recent_messages,
                st.session_state.json_state,
                context_summary=st.session_state.conversation_summary,
                tool_catalog_injection=st.session_state.tool_catalog_injection,
            )
            if new_analysis:
                if "json_state" in new_analysis: st.session_state.json_state = new_analysis["json_state"]
                if "system_notice" in new_analysis: st.session_state.system_notice = new_analysis["system_notice"]
                
                db_client.update_analysis_state(st.session_state.session_id, st.session_state.json_state, st.session_state.system_notice)
                st.toast(text('status_updated'), icon="✅")

                user_turns = sum(1 for m in st.session_state.messages if m.get("role") == "user")
                last_user_msg = ""
                for m in reversed(st.session_state.messages):
                    if m.get("role") == "user":
                        last_user_msg = m.get("content") or ""
                        break

                json_state = st.session_state.json_state if isinstance(st.session_state.json_state, dict) else {}
                missing_info = json_state.get("missing_info", [])
                missing_set = set(missing_info) if isinstance(missing_info, list) else set()
                blockers = json_state.get("blockers", [])
                blockers_set = set(blockers) if isinstance(blockers, list) else set()
                completion_readiness = json_state.get("completion_readiness", None)

                status_completed_now = (
                    json_state.get("status") == "Completed"
                    or json_state.get("interview_session", {}).get("status") == "Completed"
                )

                tool_keywords = [
                    "cursor", "trae", "claude", "codex", "github", "git", "supabase",
                    "vercel", "cloudflare", "zeabur", "posthog", "google analytics", "seo",
                    "支付", "stripe", "paypal", "支付宝", "微信",
                ]
                mentions_tools = any(k.lower() in last_user_msg.lower() for k in tool_keywords) if last_user_msg else False

                gate = None
                gate_counts = st.session_state.judge_gate_counts if isinstance(st.session_state.judge_gate_counts, dict) else {}
                if gate_counts.get("initial", 0) == 0 and user_turns >= 2:
                    gate = "initial"
                elif gate_counts.get("pre_completion", 0) == 0:
                    readiness_high = isinstance(completion_readiness, (int, float)) and completion_readiness >= 80
                    if status_completed_now or readiness_high:
                        gate = "pre_completion"
                elif gate_counts.get("correction", 0) == 0 and user_turns >= 4 and mentions_tools:
                    has_scenario_gap = "Scenario Clarity" in missing_set or "Scenario Clarity" in blockers_set
                    has_loss_gap = "Loss Magnitude" in missing_set or "Loss Magnitude" in blockers_set
                    if has_scenario_gap or has_loss_gap:
                        gate = "correction"

                if gate:
                    judge = st.session_state.judge
                    recent_history = st.session_state.messages[-12:] if len(st.session_state.messages) > 12 else st.session_state.messages
                    judge_data = judge.run(
                        chat_history=recent_history,
                        current_json_state=json_state,
                        context_summary=st.session_state.conversation_summary,
                        tool_catalog_injection=st.session_state.tool_catalog_injection
                    )

                    if judge_data:
                        eval_state = json_state.get("evaluation", {})
                        if not isinstance(eval_state, dict):
                            eval_state = {}

                        for key in [
                            "distilled_pain",
                            "surface_need",
                            "essence_need",
                            "concreteness_signals",
                            "reality_signals",
                            "evidence_gaps",
                            "scenario_gaps",
                            "red_flags",
                            "next_questions",
                            "correction_tone",
                            "judge_notice",
                        ]:
                            if key in judge_data:
                                eval_state[key] = judge_data[key]

                        notice = eval_state.get("judge_notice") or judge_data.get("judge_notice") or ""
                        questions = eval_state.get("next_questions") or judge_data.get("next_questions") or []
                        if not isinstance(questions, list):
                            questions = []

                        compressed = ""
                        if notice:
                            compressed += f"[JUDGE]\n{notice}".strip()
                        if questions:
                            top_q = [q for q in questions if isinstance(q, str) and q.strip()][:6]
                            if top_q:
                                if compressed:
                                    compressed += "\n\n"
                                compressed += "[JUDGE_NEXT_QUESTIONS]\n" + "\n".join(f"- {q.strip()}" for q in top_q)

                        if compressed:
                            st.session_state.system_notice = (st.session_state.system_notice or "").strip()
                            if st.session_state.system_notice:
                                st.session_state.system_notice += "\n\n" + compressed
                            else:
                                st.session_state.system_notice = compressed

                        eval_state["last_judge_notice"] = compressed or notice or None
                        json_state["evaluation"] = eval_state
                        if gate == "pre_completion":
                            evidence_gaps = eval_state.get("evidence_gaps", [])
                            scenario_gaps = eval_state.get("scenario_gaps", [])
                            red_flags = eval_state.get("red_flags", [])
                            has_gaps = (isinstance(evidence_gaps, list) and len(evidence_gaps) > 0) or (isinstance(scenario_gaps, list) and len(scenario_gaps) > 0)
                            has_red = isinstance(red_flags, list) and len(red_flags) > 0
                            if has_gaps or has_red:
                                json_state["status"] = "In Progress"
                                if "interview_session" not in json_state or not isinstance(json_state.get("interview_session"), dict):
                                    json_state["interview_session"] = {}
                                json_state["interview_session"]["status"] = "In Progress"
                                json_state["interview_session"]["system_notice"] = "Evidence is insufficient. Continue the interview with low-burden questions."
                                st.session_state.system_notice = (st.session_state.system_notice or "").strip()
                                if st.session_state.system_notice:
                                    st.session_state.system_notice += "\n\n[JUDGE_GATE]\nDo not complete yet. Fill the missing evidence with low-burden questions."
                                else:
                                    st.session_state.system_notice = "[JUDGE_GATE]\nDo not complete yet. Fill the missing evidence with low-burden questions."
                        st.session_state.json_state = json_state
                        st.session_state.judge_last_gate = gate
                        if isinstance(st.session_state.judge_gate_counts, dict):
                            st.session_state.judge_gate_counts[gate] = st.session_state.judge_gate_counts.get(gate, 0) + 1
                        db_client.update_analysis_state(st.session_state.session_id, st.session_state.json_state, st.session_state.system_notice)
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        st.session_state.processing_analyst = False
        time.sleep(0.5)
        st.rerun()

    # Chat Input
    if not st.session_state.processing_analyst:
        if prompt := st.chat_input(text('input_placeholder')):
            st.session_state.messages.append({"role": "user", "content": prompt})
            db_client.save_message(st.session_state.session_id, "user", prompt)
            
            # Summary Logic
            total_msgs = len(st.session_state.messages)
            if total_msgs - st.session_state.archived_count > 10:
                end_index = total_msgs - 4
                chunk = st.session_state.messages[st.session_state.archived_count : end_index]
                if chunk:
                    with st.spinner(text('spinner_compress')):
                        new_sum = st.session_state.summary_agent.update_summary(st.session_state.conversation_summary, chunk)
                        st.session_state.conversation_summary = new_sum
                        st.session_state.archived_count = end_index
                        db_client.update_session_status(st.session_state.session_id, "In Progress", summary=new_sum, archived_count=end_index)

            # Interviewer Reply
            interviewer = st.session_state.interviewer
            with st.spinner(text('spinner_typing')):
                response = interviewer.run(
                    st.session_state.messages[st.session_state.archived_count:], 
                    st.session_state.system_notice,
                    st.session_state.conversation_summary,
                    tool_catalog_injection=st.session_state.tool_catalog_injection
                )
            
            if response:
                st.session_state.messages.append({"role": "assistant", "content": response})
                db_client.save_message(st.session_state.session_id, "assistant", response)
            
            st.session_state.processing_analyst = True
            st.rerun()

    # Final Deliverables
    # CHECK COMPLETION CONDITIONS
    # 1. Status must be "Completed"
    # 2. Minimum dialogue turns (to prevent premature completion)
    # 3. No missing critical info
    
    status_completed = st.session_state.json_state.get("status") == "Completed" or st.session_state.json_state.get("interview_session", {}).get("status") == "Completed"
    
    # Count user turns
    user_turns = sum(1 for m in st.session_state.messages if m["role"] == "user")
    MIN_TURNS = 6
    
    # Check missing info
    json_state = st.session_state.json_state if isinstance(st.session_state.json_state, dict) else {}
    missing_info = json_state.get("missing_info", [])
    blockers = json_state.get("blockers", None)
    completion_readiness = json_state.get("completion_readiness", None)
    if blockers is None:
        blockers = missing_info

    has_blockers = len(blockers) > 0 if isinstance(blockers, list) else False
    readiness_ok = True
    if isinstance(completion_readiness, (int, float)):
        readiness_ok = completion_readiness >= 70
    
    is_completed = status_completed and user_turns >= MIN_TURNS and readiness_ok and not has_blockers
    
    # Correction Logic: If Analyst thinks it's done but conditions aren't met, revert status
    if status_completed and not is_completed:
        json_state["status"] = "In Progress"
        if "interview_session" in json_state and isinstance(json_state.get("interview_session"), dict):
            json_state["interview_session"]["status"] = "In Progress"
        st.session_state.json_state = json_state
        blockers_list = blockers if isinstance(blockers, list) else []
        blockers_list = [b for b in blockers_list if isinstance(b, str) and b.strip()][:8]
        msg = "Continue the interview with low-burden questions."
        if blockers_list:
            msg += "\nMissing items:\n" + "\n".join(f"- {b.strip()}" for b in blockers_list)
        st.session_state.system_notice = msg
    
    if not is_completed:
        if st.button("我已经说完了，直接生成方案"):
            json_state = st.session_state.json_state if isinstance(st.session_state.json_state, dict) else {}
            json_state["status"] = "Completed"
            if "interview_session" not in json_state or not isinstance(json_state.get("interview_session"), dict):
                json_state["interview_session"] = {}
            json_state["interview_session"]["status"] = "Completed"
            json_state["interview_session"]["system_notice"] = "Session completed. Generate deliverables."
            json_state["completion_readiness"] = 100
            if isinstance(json_state.get("missing_info"), list):
                json_state["missing_info"] = []
            if isinstance(json_state.get("blockers"), list):
                json_state["blockers"] = []
            st.session_state.json_state = json_state
            st.session_state.system_notice = "Session completed. Generate deliverables."
            try:
                db_client.update_session_status(st.session_state.session_id, status="Completed")
                db_client.update_analysis_state(st.session_state.session_id, st.session_state.json_state, st.session_state.system_notice)
            except Exception:
                pass

            if "final_deliverables" not in st.session_state: st.session_state.final_deliverables = None
            if "final_deliverables_docs" not in st.session_state: st.session_state.final_deliverables_docs = None

            try:
                judge = st.session_state.judge
                recent_history = st.session_state.messages[-12:] if len(st.session_state.messages) > 12 else st.session_state.messages
                judge_data = judge.run(
                    chat_history=recent_history,
                    current_json_state=st.session_state.json_state,
                    context_summary=st.session_state.conversation_summary,
                    tool_catalog_injection=st.session_state.tool_catalog_injection
                )
                if judge_data and isinstance(st.session_state.json_state, dict):
                    eval_state = st.session_state.json_state.get("evaluation", {})
                    if not isinstance(eval_state, dict):
                        eval_state = {}
                    for key in [
                        "distilled_pain",
                        "surface_need",
                        "essence_need",
                        "concreteness_signals",
                        "reality_signals",
                        "evidence_gaps",
                        "scenario_gaps",
                        "red_flags",
                        "next_questions",
                        "correction_tone",
                        "judge_notice",
                    ]:
                        if key in judge_data:
                            eval_state[key] = judge_data[key]
                    eval_state["last_judge_notice"] = eval_state.get("judge_notice") or None
                    st.session_state.json_state["evaluation"] = eval_state
            except Exception:
                pass

            architect = ArchitectAgent()
            with st.spinner(text('spinner_drafting')):
                result = architect.run(st.session_state.json_state, tool_catalog_injection=st.session_state.tool_catalog_injection)
                if result:
                    st.session_state.final_deliverables = result
                    docs = split_deliverables(result)
                    st.session_state.final_deliverables_docs = docs
                    try:
                        save_bundle = getattr(db_client, "save_deliverable_bundle", None)
                        if callable(save_bundle):
                            save_bundle(st.session_state.session_id, result, meta_info={"doc_count": len(docs)})
                        else:
                            db_client.save_deliverable(st.session_state.session_id, result)

                        save_docs = getattr(db_client, "save_deliverable_documents", None)
                        if docs and callable(save_docs):
                            save_docs(st.session_state.session_id, docs)
                    except Exception:
                        db_client.save_deliverable(st.session_state.session_id, result)
            st.rerun()

    if is_completed:
        st.success(text('msg_completed'))
        db_client.update_session_status(st.session_state.session_id, status="Completed")
        
        if "final_deliverables" not in st.session_state: st.session_state.final_deliverables = None
        if "final_deliverables_docs" not in st.session_state: st.session_state.final_deliverables_docs = None
        
        if st.button(text('btn_draft_docs')):
            gate_counts = st.session_state.judge_gate_counts if isinstance(st.session_state.judge_gate_counts, dict) else {}
            if gate_counts.get("delivery_pre_draft", 0) == 0:
                try:
                    judge = st.session_state.judge
                    json_state = st.session_state.json_state if isinstance(st.session_state.json_state, dict) else {}
                    recent_history = st.session_state.messages[-12:] if len(st.session_state.messages) > 12 else st.session_state.messages
                    judge_data = judge.run(
                        chat_history=recent_history,
                        current_json_state=json_state,
                        context_summary=st.session_state.conversation_summary,
                        tool_catalog_injection=st.session_state.tool_catalog_injection
                    )
                    if judge_data:
                        eval_state = json_state.get("evaluation", {})
                        if not isinstance(eval_state, dict):
                            eval_state = {}
                        for key in [
                            "distilled_pain",
                            "surface_need",
                            "essence_need",
                            "concreteness_signals",
                            "reality_signals",
                            "evidence_gaps",
                            "scenario_gaps",
                            "red_flags",
                            "next_questions",
                            "correction_tone",
                            "judge_notice",
                        ]:
                            if key in judge_data:
                                eval_state[key] = judge_data[key]
                        eval_state["last_judge_notice"] = eval_state.get("judge_notice") or None
                        json_state["evaluation"] = eval_state
                        st.session_state.json_state = json_state
                        if isinstance(st.session_state.judge_gate_counts, dict):
                            st.session_state.judge_gate_counts["delivery_pre_draft"] = st.session_state.judge_gate_counts.get("delivery_pre_draft", 0) + 1
                        db_client.update_analysis_state(st.session_state.session_id, st.session_state.json_state, st.session_state.system_notice)
                except Exception:
                    pass

            architect = ArchitectAgent()
            with st.spinner(text('spinner_drafting')):
                result = architect.run(st.session_state.json_state, tool_catalog_injection=st.session_state.tool_catalog_injection)
                if result:
                    st.session_state.final_deliverables = result
                    docs = split_deliverables(result)
                    st.session_state.final_deliverables_docs = docs
                    try:
                        save_bundle = getattr(db_client, "save_deliverable_bundle", None)
                        if callable(save_bundle):
                            save_bundle(st.session_state.session_id, result, meta_info={"doc_count": len(docs)})
                        else:
                            db_client.save_deliverable(st.session_state.session_id, result)

                        save_docs = getattr(db_client, "save_deliverable_documents", None)
                        if docs and callable(save_docs):
                            save_docs(st.session_state.session_id, docs)
                    except Exception:
                        db_client.save_deliverable(st.session_state.session_id, result)
                    current_user_id = st.session_state.user_info.id if st.session_state.user_info else "guest"
                    analytics.track_event(current_user_id, "deliverable_generated", {
                        "session_id": st.session_state.session_id,
                        "length": len(result)
                    })
                    st.rerun()
        
        if st.session_state.final_deliverables:
            st.markdown(text('header_deliverables'))
            docs = st.session_state.final_deliverables_docs if isinstance(st.session_state.final_deliverables_docs, list) else []
            if docs:
                for d in docs:
                    file_name = d.get("file_name", "doc.md")
                    content = d.get("content", "")
                    if content:
                        st.download_button(
                            label=f"下载 {file_name}",
                            data=content,
                            file_name=file_name,
                            mime="text/markdown"
                        )
            st.download_button(
                label=text('btn_download_md'),
                data=st.session_state.final_deliverables,
                file_name=f"Maia_Strategy_{st.session_state.session_id[:8]}.md",
                mime="text/markdown"
            )
            st.markdown(st.session_state.final_deliverables)

# ==========================================
# MAIN ROUTER
# ==========================================
if st.session_state.page_mode == "LANDING":
    render_landing()
elif st.session_state.page_mode == "AUTH":
    render_auth()
elif st.session_state.page_mode == "DASHBOARD":
    render_dashboard()
elif st.session_state.page_mode == "CHAT":
    render_chat()
