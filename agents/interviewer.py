import os
import streamlit as st
from utils.llm_client import llm_client

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

    def run(self, history, system_notice, context_summary=None):
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

        with st.spinner(f"Interviewer ({self.model}) is typing..."):
            kwargs = {}
            if self.reasoning_effort and self.reasoning_effort.lower() != "none":
                kwargs["reasoning_effort"] = self.reasoning_effort
                
            response_text, tokens = llm_client.get_completion(
                model=self.model,
                messages=messages,
                temperature=0.7,
                **kwargs
            )
            
        return response_text
