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

        # Call LLM
        try:
            response, _ = llm_client.get_completion(
                model=self.model_name,
                messages=messages,
                temperature=0.3 # Low temperature for factual consistency
            )
            if response:
                return response.strip()
            else:
                return current_summary
        except Exception as e:
            print(f"Error in SummaryAgent: {e}")
            return current_summary # Fallback: return old summary if update fails
