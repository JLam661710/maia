import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Load env vars
load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL")
        
        if not self.api_key:
            st.error("⚠️ OPENAI_API_KEY is missing in .env file.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def _call_api(self, params):
        """Wrapped API call with retry logic"""
        return self.client.chat.completions.create(**params)

    def get_completion(self, model, messages, temperature=0.7, max_tokens=None, response_format=None, **kwargs):
        """
        Generic function to get completion from LLM.
        Tracks token usage in Streamlit session state.
        """
        if not self.client:
            return None, 0

        try:
            params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            
            if max_tokens:
                params["max_tokens"] = max_tokens
                
            # Note: response_format={"type": "json_object"} is supported by some models (like GPT-4o, Gemini 2.5)
            # but deepseek/gemini-thinking might behave differently. We'll use it if passed.
            if response_format:
                params["response_format"] = response_format

            # Add any extra arguments (e.g. reasoning_effort)
            if kwargs:
                params.update(kwargs)

            # Call with retry
            response = self._call_api(params)
            
            content = response.choices[0].message.content
            
            # Track Usage
            usage = response.usage
            total_tokens = 0
            if usage:
                total_tokens = usage.total_tokens
                # Update global session counter
                if "total_cost_tokens" not in st.session_state:
                    st.session_state["total_cost_tokens"] = 0
                st.session_state["total_cost_tokens"] += total_tokens
                
                # Debug info
                # st.toast(f"Used {total_tokens} tokens for this call ({model})")

            return content, total_tokens

        except Exception as e:
            st.error(f"系统繁忙，请稍后再试 (System Busy): {str(e)}")
            return None, 0

# Singleton instance
llm_client = LLMClient()
