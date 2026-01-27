import os
import streamlit as st
from utils.llm_client import llm_client
from utils.analytics import analytics

class ArchitectAgent:
    def __init__(self):
        # Read System Prompt
        try:
            with open("docs/prompts/SP_system_prompt_solution_architect.md", "r", encoding="utf-8") as f:
                self.system_prompt_template = f.read()
        except FileNotFoundError:
            self.system_prompt_template = "You are a solution architect."

        # Get Model Config (Dynamic Load)
        # self.model = os.getenv("MODEL_ARCHITECT", "gemini-3-pro-preview")
        self.reasoning_effort = os.getenv("REASONING_EFFORT_ARCHITECT", None)
        pass

    def run(self, final_json_state, tool_catalog_injection=None):
        """
        Generates the final 4 deliverables based on the completed JSON state.
        """
        # Reload model from env to support dynamic config changes
        self.model = os.getenv("MODEL_ARCHITECT", "gemini-3-pro-preview")
        self.reasoning_effort = os.getenv("REASONING_EFFORT_ARCHITECT", None)
        
        prompt = self.system_prompt_template
        
        input_content = f"""
        The interview is complete. Here is the Final JSON State collected from the user:
        
        ```json
        {final_json_state}
        ```
        
        Please generate the 4 required deliverables (PRD, Tech Architecture, UX, Data Schema) as per your system instructions.
        """

        messages = [
            {"role": "system", "content": prompt},
            {"role": "system", "content": str(tool_catalog_injection)} if tool_catalog_injection else None,
            {"role": "user", "content": input_content}
        ]
        messages = [m for m in messages if m is not None]

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

        # Analytics
        try:
            user_id = "guest"
            if hasattr(st, "session_state") and "user_info" in st.session_state and st.session_state.user_info:
                user_id = st.session_state.user_info.id
                
            analytics.track_event(user_id, "architect_run", {
                "model": self.model
            })
        except Exception:
            pass

        kwargs = {}
        if self.reasoning_effort and self.reasoning_effort.lower() != "none":
            kwargs["reasoning_effort"] = self.reasoning_effort

        top_p = _env_float("TOP_P_ARCHITECT", None)
        if top_p is not None:
            kwargs["top_p"] = top_p

        presence_penalty = _env_float("PRESENCE_PENALTY_ARCHITECT", None)
        if presence_penalty is not None:
            kwargs["presence_penalty"] = presence_penalty

        frequency_penalty = _env_float("FREQUENCY_PENALTY_ARCHITECT", None)
        if frequency_penalty is not None:
            kwargs["frequency_penalty"] = frequency_penalty

        seed = _env_int("SEED_ARCHITECT", None)
        if seed is not None:
            kwargs["seed"] = seed

        max_tokens = _env_int("MAX_TOKENS_ARCHITECT", 8000) or 8000
        temperature = _env_float("TEMPERATURE_ARCHITECT", 0.5) or 0.5

        response_text, _ = llm_client.get_completion(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
            
        return response_text
