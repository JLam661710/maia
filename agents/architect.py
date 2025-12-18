import os
import streamlit as st
from utils.llm_client import llm_client

class ArchitectAgent:
    def __init__(self):
        # Read System Prompt
        try:
            with open("SP_system_prompt_solution_architect.md", "r", encoding="utf-8") as f:
                self.system_prompt_template = f.read()
        except FileNotFoundError:
            self.system_prompt_template = "You are a solution architect."

        # Get Model Config
        self.model = os.getenv("MODEL_ARCHITECT", "gemini-3-pro-preview")

    def run(self, final_json_state):
        """
        Generates the final 4 deliverables based on the completed JSON state.
        """
        
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
            {"role": "user", "content": input_content}
        ]

        with st.spinner(f"Architect ({self.model}) is drafting the final documents... This may take a minute."):
            # High max_tokens because we expect a LONG output
            response_text, tokens = llm_client.get_completion(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=8000 
            )
            
        return response_text
