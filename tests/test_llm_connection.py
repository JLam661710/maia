import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
import unittest

# 1. Load environment variables
load_dotenv()

# 2. Get configuration
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# Model definitions (from .env or default fallback)
# Note: In .env we might have set specific models.
# Let's try to read them, or default to the ones we discussed.
model_interviewer = os.getenv("MODEL_INTERVIEWER", "gemini-2.5-flash")
model_analyst = os.getenv("MODEL_ANALYST", "gemini-3-pro-preview-thinking")
model_architect = os.getenv("MODEL_ARCHITECT", "gemini-3-pro-preview")

print("==================================================")
print("  API Connection Test (Dual-Agent / Triple-Agent) ")
print("==================================================")
print(f"Base URL: {base_url}")
print(f"API Key:  {f'{api_key[:8]}...{api_key[-4:]}' if api_key else 'None'}")
print("--------------------------------------------------")
print(f"Target Models:")
print(f"1. Interviewer: {model_interviewer}")
print(f"2. Analyst:     {model_analyst}")
print(f"3. Architect:   {model_architect}")
print("==================================================\n")

def _can_run_connection_test() -> bool:
    if os.getenv("RUN_LLM_CONNECTION_TESTS") != "1":
        return False
    if not api_key or "your-apiyi-key-here" in api_key:
        return False
    if not base_url:
        return False
    return True

def test_model(client: OpenAI, role_name: str, model_name: str) -> bool:
    print(f"🔄 Testing [{role_name}] using model: {model_name}...")
    # Try to call the model
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": "Hello! Please reply with 'OK' if you can hear me."}
            ],
            max_tokens=10
        )
        if response and response.choices:
            content = response.choices[0].message.content
            if content:
                print(f"✅ SUCCESS: {role_name} responded: {content.strip()}")
                return True
            else:
                print(f"⚠️ WARNING: {role_name} responded with empty content.")
                return False
        else:
            print(f"❌ FAILED: {role_name} returned no response object.")
            return False

    except Exception as e:
        print(f"❌ FAILED: {role_name} error: {e}")
        return False

class TestLLMConnection(unittest.TestCase):
    @unittest.skipUnless(
        _can_run_connection_test(),
        "Set RUN_LLM_CONNECTION_TESTS=1 and configure OPENAI_API_KEY/OPENAI_BASE_URL to run.",
    )
    def test_models(self):
        client = OpenAI(api_key=api_key, base_url=base_url)
        self.assertTrue(test_model(client, "Interviewer", model_interviewer))
        print("--------------------------------------------------")
        self.assertTrue(test_model(client, "Analyst", model_analyst))
        print("--------------------------------------------------")
        self.assertTrue(test_model(client, "Architect", model_architect))


if __name__ == "__main__":
    if not _can_run_connection_test():
        print("❌ ERROR: Missing config. Set RUN_LLM_CONNECTION_TESTS=1 and valid OPENAI_API_KEY/OPENAI_BASE_URL.")
        sys.exit(1)
    unittest.main()
