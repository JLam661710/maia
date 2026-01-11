import streamlit as st
import json
import time
from dotenv import load_dotenv
import os

# Load env vars BEFORE importing db_client
load_dotenv(override=True)

from utils.db_client import db_client 
from utils.i18n import get_text as t, TRANSLATIONS

from agents.interviewer import InterviewerAgent
from agents.analyst import AnalystAgent
from agents.architect import ArchitectAgent
from agents.summary import SummaryAgent

# Page Config
st.set_page_config(page_title="Maia", page_icon="🤖", layout="wide")

# Load Custom CSS
def load_css():
    with open("assets/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize Session State
if "page_mode" not in st.session_state: st.session_state.page_mode = "LANDING" # LANDING, AUTH, DASHBOARD, CHAT
if "user_info" not in st.session_state: st.session_state.user_info = None # None for Guest
if "session_id" not in st.session_state: st.session_state.session_id = None
if "messages" not in st.session_state: st.session_state.messages = []
if "lang" not in st.session_state: st.session_state.lang = "zh" # Default to Chinese
if "json_state" not in st.session_state:
    st.session_state.json_state = {
        "user_profile": {},
        "project_needs": {},
        "status": "In Progress",
        "missing_info": ["User Role", "Project Goal", "Preferred Platform"]
    }
if "system_notice" not in st.session_state: st.session_state.system_notice = "Start the interview. Ask the user who they are and what they want to build."
if "conversation_summary" not in st.session_state: st.session_state.conversation_summary = ""
if "archived_count" not in st.session_state: st.session_state.archived_count = 0
if "total_cost_tokens" not in st.session_state: st.session_state.total_cost_tokens = 0
if "processing_analyst" not in st.session_state: st.session_state.processing_analyst = False

# Initialize Agents
if "agents_loaded" not in st.session_state:
    st.session_state.interviewer = InterviewerAgent()
    st.session_state.analyst = AnalystAgent()
    st.session_state.architect = ArchitectAgent()
    st.session_state.summary_agent = SummaryAgent()
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
            st.session_state.session_id = sid
            # Reset Chat State
            st.session_state.messages = []
            st.session_state.json_state = {"user_profile": {}, "project_needs": {}, "status": "In Progress"}
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
        else:
            # For normal users, show nothing or minimal info
            pass

    st.markdown(f"<h2 style='text-align: center; margin-bottom: 2rem;'>{text('chat_header')}</h2>", unsafe_allow_html=True)

    # Auto-start logic
    if not st.session_state.messages:
        interviewer = st.session_state.interviewer
        response = interviewer.run(
            history=[], 
            system_notice=st.session_state.system_notice,
            context_summary=st.session_state.conversation_summary
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
            new_analysis = analyst.run(st.session_state.messages, st.session_state.json_state)
            if new_analysis:
                if "json_state" in new_analysis: st.session_state.json_state = new_analysis["json_state"]
                if "system_notice" in new_analysis: st.session_state.system_notice = new_analysis["system_notice"]
                
                db_client.update_analysis_state(st.session_state.session_id, st.session_state.json_state, st.session_state.system_notice)
                st.toast(text('status_updated'), icon="✅")
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
                    st.session_state.conversation_summary
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
    missing_info = st.session_state.json_state.get("missing_info", [])
    has_missing_info = len(missing_info) > 0 if isinstance(missing_info, list) else False
    
    is_completed = status_completed and user_turns >= MIN_TURNS and not has_missing_info
    
    # Correction Logic: If Analyst thinks it's done but conditions aren't met, revert status
    if status_completed and not is_completed:
        st.session_state.json_state["status"] = "In Progress"
        if "interview_session" in st.session_state.json_state:
            st.session_state.json_state["interview_session"]["status"] = "In Progress"
        # Force system notice to continue
        st.session_state.system_notice = "The interview is too short or missing info. Continue asking questions."
    
    if is_completed:
        st.success(text('msg_completed'))
        db_client.update_session_status(st.session_state.session_id, status="Completed")
        
        if "final_deliverables" not in st.session_state: st.session_state.final_deliverables = None
        
        if st.button(text('btn_draft_docs')):
            architect = ArchitectAgent()
            with st.spinner(text('spinner_drafting')):
                result = architect.run(st.session_state.json_state)
                if result:
                    st.session_state.final_deliverables = result
                    db_client.save_deliverable(st.session_state.session_id, result)
                    st.rerun()
        
        if st.session_state.final_deliverables:
            st.markdown(text('header_deliverables'))
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
