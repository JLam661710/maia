import os
from openai import OpenAI
import sys

# Volcengine Configuration
API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("VOLCENGINE_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL") or os.getenv("VOLCENGINE_BASE_URL") or "https://ark.cn-beijing.volces.com/api/v3"

models_to_test = {
    "Interviewer": "doubao-1-5-pro-32k-250115",
    "Analyst": "deepseek-v3-2-251201",
    "Architect": "doubao-seed-1-8-251215",
    "Summary": "doubao-seed-1-6-flash-250828"
}

def test_model(role, model_id):
    print(f"Testing {role} ({model_id})...", end=" ", flush=True)
    if not API_KEY:
        print("⏭️ Skipped (missing API key)")
        return True
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Reply with 'OK'."}
            ],
            max_tokens=10
        )
        content = response.choices[0].message.content
        print(f"✅ Success! Response: {content}")
        return True
    except Exception as e:
        print(f"❌ Failed! Error: {e}")
        return False

if __name__ == "__main__":
    print(f"🔌 Testing Volcengine Connection...\nBase URL: {BASE_URL}\n")
    if not API_KEY:
        print("⚠️ Missing OPENAI_API_KEY/VOLCENGINE_API_KEY. Skipping connection test.")
        sys.exit(0)
    all_passed = True
    for role, model_id in models_to_test.items():
        if not test_model(role, model_id):
            all_passed = False
    
    if all_passed:
        print("\n✨ All Volcengine models are reachable!")
        sys.exit(0)
    else:
        print("\n⚠️ Some models failed to connect.")
        sys.exit(1)
