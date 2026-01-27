import os
import streamlit as st
from utils.llm_client import llm_client
from utils.analytics import analytics

class InterviewerAgent:
    def __init__(self):
        # Read System Prompt
        try:
            with open("docs/prompts/SP_system_prompt_interviewer.md", "r", encoding="utf-8") as f:
                self.system_prompt_template = f.read()
        except FileNotFoundError:
            self.system_prompt_template = "You are a helpful interviewer."

        # Get Model Config
        self.model = os.getenv("MODEL_INTERVIEWER", "gemini-2.5-flash")
        self.reasoning_effort = os.getenv("REASONING_EFFORT_INTERVIEWER", None)

    def run(self, history, system_notice, context_summary=None, tool_catalog_injection=None):
        """
        Run the interviewer agent.
        
        Args:
            history (list): List of message dicts.
            system_notice (str): Current instruction from Analyst.
            context_summary (str): Compressed summary of past conversation.
            
        Returns:
            str: The response content.
        """
        # Build prompt
        messages = [{"role": "system", "content": self.system_prompt_template}]

        if tool_catalog_injection:
            messages.append({"role": "system", "content": str(tool_catalog_injection)})
        
        # Inject Context Summary if available
        if context_summary:
            summary_injection = f"""
            \n\n[PAST CONVERSATION SUMMARY]
            The following is a compressed summary of the earlier conversation. Use this context to maintain continuity but focus on the latest messages.
            {context_summary}
            """
            # Append to system prompt or insert as a system message
            messages.append({"role": "system", "content": summary_injection})

        # Inject System Notice
        notice_injection = f"\n\n[ANALYST INSTRUCTION]\n{system_notice}"
        messages.append({"role": "system", "content": notice_injection})
        
        # Append conversation history
        # Note: If summary is used, we might want to truncate history in main.py, 
        # but here we just take what's given.
        messages.extend(history)

        def _env_float(key: str, default):
            v = os.getenv(key)
            if v is None or v == "":
                return default
            try:
                return float(v)
            except Exception:
                return default

        def _env_int(key: str, default):
            v = os.getenv(key)
            if v is None or v == "":
                return default
            try:
                return int(v)
            except Exception:
                return default

        with st.spinner(f"Interviewer ({self.model}) is typing..."):
            kwargs = {}
            if self.reasoning_effort and self.reasoning_effort.lower() != "none":
                kwargs["reasoning_effort"] = self.reasoning_effort

            top_p = _env_float("TOP_P_INTERVIEWER", None)
            if top_p is not None:
                kwargs["top_p"] = top_p

            presence_penalty = _env_float("PRESENCE_PENALTY_INTERVIEWER", None)
            if presence_penalty is not None:
                kwargs["presence_penalty"] = presence_penalty

            frequency_penalty = _env_float("FREQUENCY_PENALTY_INTERVIEWER", None)
            if frequency_penalty is not None:
                kwargs["frequency_penalty"] = frequency_penalty

            seed = _env_int("SEED_INTERVIEWER", None)
            if seed is not None:
                kwargs["seed"] = seed

            max_tokens = _env_int("MAX_TOKENS_INTERVIEWER", None)
            temperature = _env_float("TEMPERATURE_INTERVIEWER", 0.7) or 0.7
                
            response_text, _ = llm_client.get_completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
        # Analytics
        try:
            user_id = "guest"
            if hasattr(st, "session_state") and "user_info" in st.session_state and st.session_state.user_info:
                user_id = st.session_state.user_info.id
            
            analytics.track_event(user_id, "interviewer_response", {
                "length": len(response_text) if response_text else 0,
                "model": self.model
            })
        except Exception:
            pass
            
        return response_text
