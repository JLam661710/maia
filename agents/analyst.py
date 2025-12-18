import json
import os
import re
import streamlit as st
from utils.llm_client import llm_client

class AnalystAgent:
    def __init__(self):
        # Read System Prompt
        try:
            with open("SP_system_prompt_backend_analyst.md", "r", encoding="utf-8") as f:
                self.system_prompt_template = f.read()
        except FileNotFoundError:
            self.system_prompt_template = "You are a backend analyst."

        # Get Model Config
        self.model = os.getenv("MODEL_ANALYST", "gemini-3-pro-preview-thinking")

    def run(self, chat_history, current_json_state):
        """
        Analyzes the conversation and updates the JSON state.
        Also generates a System Notice for the Interviewer.
        """
        
        prompt = self.system_prompt_template
        
        # We need to force it to output JSON. 
        # The prompt already asks for it, but let's reinforce it.
        
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""
            Here is the conversation history so far:
            {json.dumps(chat_history, ensure_ascii=False, indent=2)}
            
            Current JSON State:
            {json.dumps(current_json_state, ensure_ascii=False, indent=2)}
            
            Please analyze the latest updates and output the NEW JSON State and System Notice.
            Remember to output ONLY valid JSON.
            """}
        ]

        with st.spinner(f"Analyst ({self.model}) is thinking & updating state..."):
            # Note: response_format={"type": "json_object"} is NOT supported by Thinking models on some APIs
            # We rely on the prompt and post-processing.
            response_text, tokens = llm_client.get_completion(
                model=self.model,
                messages=messages,
                temperature=0.2, # Lower temp for logic
            )
            
        # Parse JSON
        try:
            if response_text:
                # Robust cleaning for Thinking models (often wrap in ```json ... ```)
                text = response_text.strip()
                # Find the first { and the last }
                match = re.search(r"\{[\s\S]*\}", text)
                if match:
                    json_str = match.group(0)
                else:
                    json_str = text
                
                data = json.loads(json_str)
                
                # Adapt to main.py expected format
                # main.py expects: { "json_state": ..., "system_notice": ... }
                # The LLM returns the full json state as 'data'.
                
                # Extract system_notice from data if exists, or use default
                system_notice = data.get("interview_session", {}).get("system_notice", "Continue the interview.")
                
                return {
                    "json_state": data,
                    "system_notice": system_notice
                }
            else:
                return None
        except json.JSONDecodeError:
            st.error("Analyst failed to produce valid JSON. Check raw output in logs.")
            # Fallback: return old state
            return current_json_state
