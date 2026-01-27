import json
import os
import re
import streamlit as st
from typing import Optional
from utils.llm_client import llm_client
from utils.analytics import analytics

class AnalystAgent:
    def __init__(self):
        # Read System Prompt
        try:
            with open("docs/prompts/SP_system_prompt_backend_analyst.md", "r", encoding="utf-8") as f:
                self.system_prompt_template = f.read()
        except FileNotFoundError:
            self.system_prompt_template = "You are a backend analyst."

        # Get Model Config
        self.model = os.getenv("MODEL_ANALYST", "gemini-3-pro-preview-thinking")
        self.reasoning_effort = os.getenv("REASONING_EFFORT_ANALYST", None)

    def run(self, chat_history, current_json_state, context_summary=None, tool_catalog_injection=None):
        """
        Analyzes the conversation and updates the JSON state.
        Also generates a System Notice for the Interviewer.
        """
        
        prompt = self.system_prompt_template
        
        # We need to force it to output JSON. 
        # The prompt already asks for it, but let's reinforce it.
        
        def _compact_json(obj, max_chars: int):
            try:
                text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            except Exception:
                text = str(obj)
            if len(text) <= max_chars:
                return text
            return text[:max_chars] + "...(truncated)"

        def _compact_state(state, max_chars: int):
            if not isinstance(state, dict):
                return _compact_json(state, max_chars)
            trimmed = dict(state)
            if "decision_log" in trimmed and isinstance(trimmed.get("decision_log"), list) and len(trimmed["decision_log"]) > 20:
                trimmed["decision_log"] = trimmed["decision_log"][-20:]
            text = _compact_json(trimmed, max_chars)
            if len(text) <= max_chars:
                return text
            trimmed.pop("decision_log", None)
            return _compact_json(trimmed, max_chars)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "system", "content": str(tool_catalog_injection)} if tool_catalog_injection else None,
            {"role": "system", "content": f"[PAST CONVERSATION SUMMARY]\n{context_summary}"} if context_summary else None,
            {"role": "user", "content": f"""
            Here is the conversation history so far:
            {_compact_json(chat_history, 14000)}
            
            Current JSON State:
            {_compact_state(current_json_state, 14000)}
            
            Please analyze the latest updates and output ONLY a single JSON object: the updated JSON State (v2).
            Put your instruction for the Interviewer into interview_session.system_notice.
            Output format requirement:
            - Return ONLY JSON
            - No markdown, no extra text
            """}
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

        def _response_format_from_env(raw_value: Optional[str]):
            if raw_value is None:
                return None
            raw_value = raw_value.strip()
            if not raw_value:
                return None
            if raw_value.lower() == "json_object":
                return {"type": "json_object"}
            try:
                obj = json.loads(raw_value)
                if isinstance(obj, dict) and str(obj.get("type", "")).strip().lower() == "json_object":
                    return {"type": "json_object"}
            except Exception:
                return None
            return None

        def _extract_json_object(text: str):
            if "<JSON>" in text and "</JSON>" in text:
                segment = text.split("<JSON>", 1)[1].split("</JSON>", 1)[0].strip()
                if segment:
                    text = segment

            start = text.find("{")
            if start < 0:
                return text

            depth = 0
            in_str = False
            esc = False
            for i in range(start, len(text)):
                ch = text[i]
                if in_str:
                    if esc:
                        esc = False
                    elif ch == "\\":
                        esc = True
                    elif ch == "\"":
                        in_str = False
                    continue
                if ch == "\"":
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return text[start : i + 1]
            return text[start:]

        with st.spinner(f"Analyst ({self.model}) is thinking & updating state..."):
            # Note: response_format={"type": "json_object"} is NOT supported by Thinking models on some APIs
            # We rely on the prompt and post-processing.
            kwargs = {}
            if self.reasoning_effort and self.reasoning_effort.lower() != "none":
                kwargs["reasoning_effort"] = self.reasoning_effort

            top_p = _env_float("TOP_P_ANALYST", None)
            if top_p is not None:
                kwargs["top_p"] = top_p

            presence_penalty = _env_float("PRESENCE_PENALTY_ANALYST", None)
            if presence_penalty is not None:
                kwargs["presence_penalty"] = presence_penalty

            frequency_penalty = _env_float("FREQUENCY_PENALTY_ANALYST", None)
            if frequency_penalty is not None:
                kwargs["frequency_penalty"] = frequency_penalty

            seed = _env_int("SEED_ANALYST", None)
            if seed is not None:
                kwargs["seed"] = seed

            response_format = _response_format_from_env(os.getenv("RESPONSE_FORMAT_ANALYST"))

            max_tokens = _env_int("MAX_TOKENS_ANALYST", None)
            temperature = _env_float("TEMPERATURE_ANALYST", 0.0)
            temperature = 0.0 if temperature is None else temperature

            response_text, _ = llm_client.get_completion(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
                **kwargs
            )
            
        # Parse JSON
        try:
            if response_text:
                # Robust cleaning for Thinking models (often wrap in ```json ... ```)
                text = response_text.strip()
                json_str = _extract_json_object(text)
                
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
            repaired = None
            if response_text:
                try:
                    st.session_state["last_analyst_raw_output"] = response_text[:8000]
                except Exception:
                    pass
                fixer_messages = [
                    {"role": "system", "content": "You fix JSON. Return ONLY a single valid JSON object. No markdown, no extra text."},
                    {"role": "user", "content": response_text},
                ]
                fixer_text, _ = llm_client.get_completion(
                    model=self.model,
                    messages=fixer_messages,
                    temperature=0,
                    max_tokens=_env_int("MAX_TOKENS_ANALYST", 1024),
                    response_format=_response_format_from_env(os.getenv("RESPONSE_FORMAT_ANALYST")),
                )
                if fixer_text:
                    try:
                        repaired = json.loads(_extract_json_object(fixer_text.strip()))
                    except Exception:
                        repaired = None
            if isinstance(repaired, dict):
                system_notice = repaired.get("interview_session", {}).get("system_notice", "Continue the interview.")
                return {"json_state": repaired, "system_notice": system_notice}

            st.error("Analyst failed to produce valid JSON.")
            system_notice = None
            if isinstance(current_json_state, dict):
                system_notice = current_json_state.get("interview_session", {}).get("system_notice")
            return {"json_state": current_json_state, "system_notice": system_notice or "Continue the interview."}
