import streamlit as st
import json
import time
from agents.interviewer import InterviewerAgent
from agents.analyst import AnalystAgent
from agents.architect import ArchitectAgent
from agents.summary import SummaryAgent

# Page Config
st.set_page_config(page_title="Trae AI - Requirement Analyst", layout="wide")

# Custom CSS for chat interface
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stChatMessage[data-testid="user-message"] {
        background-color: #f0f2f6;
    }
    .json-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.8em;
        overflow-x: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "json_state" not in st.session_state:
    # Initial empty state structure
    st.session_state.json_state = {
        "user_profile": {},
        "project_needs": {},
        "status": "In Progress",
        "missing_info": ["User Role", "Project Goal", "Preferred Platform"]
    }

if "system_notice" not in st.session_state:
    st.session_state.system_notice = "Start the interview. Ask the user who they are and what they want to build."

if "conversation_summary" not in st.session_state:
    st.session_state.conversation_summary = ""

if "archived_count" not in st.session_state:
    st.session_state.archived_count = 0

if "total_cost_tokens" not in st.session_state:
    st.session_state.total_cost_tokens = 0

# Initialize Agents
if "agents_loaded" not in st.session_state:
    st.session_state.interviewer = InterviewerAgent()
    st.session_state.analyst = AnalystAgent()
    st.session_state.architect = ArchitectAgent()
    st.session_state.summary_agent = SummaryAgent()
    st.session_state.agents_loaded = True

# Sidebar: Debug & Info
with st.sidebar:
    st.title("🛠️ Control Panel")
    st.markdown("### 📊 Token Usage")
    st.metric("Total Tokens Used", st.session_state.total_cost_tokens)
    
    st.markdown("---")
    st.markdown("### 🧠 Backend State (Analyst)")
    
    # Show System Notice
    st.info(f"**Current System Notice**:\n\n{st.session_state.system_notice}")
    
    # Show JSON State
    with st.expander("View JSON State", expanded=True):
        st.json(st.session_state.json_state)
        
    st.markdown("---")
    if st.button("🚨 Reset Conversation"):
        st.session_state.messages = []
        st.session_state.json_state = {}
        st.session_state.total_cost_tokens = 0
        st.rerun()

# Main Chat Interface
st.title("🤖 Triple-Agent Interviewer")
st.caption("Powered by Gemini Family: Interviewer (Flash) + Analyst (Thinking) + Architect (Pro)")

# Auto-start if empty
if not st.session_state.messages:
    # Trigger Interviewer to start
    interviewer = st.session_state.interviewer
    response = interviewer.run(
        history=[], 
        system_notice=st.session_state.system_notice,
        context_summary=st.session_state.conversation_summary
    )
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Tell me about your idea..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 1. Summary Agent Trigger Logic (Sliding Window)
    # Strategy: Keep last 10 messages raw. Summarize older ones.
    # Check if we have enough unarchived messages to trigger a summary update
    total_msgs = len(st.session_state.messages)
    unarchived_count = total_msgs - st.session_state.archived_count
    
    # Trigger every 6 messages (3 turns) roughly, but keep last 4 raw
    if unarchived_count > 10:
        # We want to archive messages from [archived_count] to [total_msgs - 4]
        # Keeping the last 4 messages as immediate context
        end_index = total_msgs - 4
        chunk_to_summarize = st.session_state.messages[st.session_state.archived_count : end_index]
        
        if chunk_to_summarize:
            with st.spinner("🧠 Cognitive Compressor is extracting insights..."):
                new_summary = st.session_state.summary_agent.update_summary(
                    st.session_state.conversation_summary,
                    chunk_to_summarize
                )
                st.session_state.conversation_summary = new_summary
                st.session_state.archived_count = end_index
                # Debug notification (optional)
                # st.toast(f"Summary Updated! Archived {len(chunk_to_summarize)} messages.")

    # 2. Interviewer Run
    # Pass (Summary + Recent Messages) to Interviewer
    # Actually, Interviewer.run() takes full history but we modify it here or inside Interviewer
    # To save tokens, we only pass the unarchived messages + summary
    # But for display consistency, st.session_state.messages has ALL.
    # We construct a 'context_window' for the LLM.
    
    context_window = st.session_state.messages[st.session_state.archived_count:]
    
    interviewer = st.session_state.interviewer
    response = interviewer.run(
        history=context_window, 
        system_notice=st.session_state.system_notice,
        context_summary=st.session_state.conversation_summary
    )
    
    if response:
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
    
    # 3. Analyst Agent turn (Background)
    # We run this AFTER the interviewer replies to keep UI responsive-ish, 
    # but in Streamlit it blocks. That's fine for MVP.
    
    analyst = st.session_state.analyst
    
    # Visual indicator
    with st.status("🧠 Analyst is processing...", expanded=False) as status:
        st.write("Reading conversation history...")
        st.write("Updating JSON state...")
        st.write("Generating new System Notice...")
        
        new_analysis = analyst.run(
            chat_history=st.session_state.messages,
            current_json_state=st.session_state.json_state
        )
        
        if new_analysis:
            # Update State
            if "json_state" in new_analysis:
                st.session_state.json_state = new_analysis["json_state"]
            if "system_notice" in new_analysis:
                st.session_state.system_notice = new_analysis["system_notice"]
            
            status.update(label="✅ Analyst Updated State", state="complete", expanded=False)
            
            # Force a rerun to update the sidebar immediately
            time.sleep(0.5)
            st.rerun()
        else:
            status.update(label="⚠️ Analyst Failed", state="error")

# Check for Completion
# Check nested status first (new schema), then flat status (legacy/fallback)
is_completed = False
if st.session_state.json_state.get("interview_session", {}).get("status") == "Completed":
    is_completed = True
elif st.session_state.json_state.get("status") == "Completed":
    is_completed = True

if is_completed:
    st.success("🎉 Information Gathering Completed!")
    
    if "final_deliverables" not in st.session_state:
        st.session_state.final_deliverables = None

    if st.button("Draft Final Documents (Architect Agent)"):
        architect = st.session_state.architect
        st.session_state.final_deliverables = architect.run(st.session_state.json_state)
        st.rerun()

    if st.session_state.final_deliverables:
        st.markdown("## 📄 Final Deliverables")
        st.download_button(
            label="📥 Download Full Report (Markdown)",
            data=st.session_state.final_deliverables,
            file_name="Trae_AI_Solution_Package.md",
            mime="text/markdown"
        )
        st.markdown(st.session_state.final_deliverables)
