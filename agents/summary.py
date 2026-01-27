from utils.llm_client import llm_client
import os

class SummaryAgent:
    def __init__(self, model_name=None):
        # Default to Flash for speed/cost, but allow override via Env or Init
        self.model_name = model_name or os.getenv("MODEL_SUMMARY", "gemini-2.5-flash")
        self.reasoning_effort = os.getenv("REASONING_EFFORT_SUMMARY", None)
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        try:
            with open("docs/prompts/SP_system_prompt_summary.md", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "You are a helpful assistant that summarizes conversations."

    def update_summary(self, current_summary, new_messages):
        """
        Updates the running summary with new messages.
        
        Args:
            current_summary (str): The existing summary string.
            new_messages (list): List of dicts [{"role":..., "content":...}, ...]
        
        Returns:
            str: The updated summary.
        """
        if not new_messages:
            return current_summary

        # Format new messages for the LLM
        conversation_text = ""
        for msg in new_messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            conversation_text += f"{role}: {content}\n"

        user_prompt = f"""
        [Current Summary]
        {current_summary if current_summary else "No summary yet."}

        [New Dialogue Chunk to Process]
        {conversation_text}

        Please update the summary to include insights from the new chunk. Keep it concise.
        """

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt}
        ]

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

        # Call LLM
        try:
            kwargs = {}
            if self.reasoning_effort and self.reasoning_effort.lower() != "none":
                kwargs["reasoning_effort"] = self.reasoning_effort

            top_p = _env_float("TOP_P_SUMMARY", None)
            if top_p is not None:
                kwargs["top_p"] = top_p

            presence_penalty = _env_float("PRESENCE_PENALTY_SUMMARY", None)
            if presence_penalty is not None:
                kwargs["presence_penalty"] = presence_penalty

            frequency_penalty = _env_float("FREQUENCY_PENALTY_SUMMARY", None)
            if frequency_penalty is not None:
                kwargs["frequency_penalty"] = frequency_penalty

            seed = _env_int("SEED_SUMMARY", None)
            if seed is not None:
                kwargs["seed"] = seed

            max_tokens = _env_int("MAX_TOKENS_SUMMARY", None)
            temperature = _env_float("TEMPERATURE_SUMMARY", 0.3) or 0.3

            response, _ = llm_client.get_completion(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            if response:
                return response.strip()
            else:
                return current_summary
        except Exception as e:
            print(f"Error in SummaryAgent: {e}")
            return current_summary # Fallback: return old summary if update fails
