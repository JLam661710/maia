import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

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
print(f"API Key:  {api_key[:8]}...{api_key[-4:] if api_key else 'None'}")
print("--------------------------------------------------")
print(f"Target Models:")
print(f"1. Interviewer: {model_interviewer}")
print(f"2. Analyst:     {model_analyst}")
print(f"3. Architect:   {model_architect}")
print("==================================================\n")

if not api_key or "your-apiyi-key-here" in api_key:
    print("❌ ERROR: Please set your valid OPENAI_API_KEY in .env file first!")
    sys.exit(1)

# 3. Initialize Client
try:
    client = OpenAI(api_key=api_key, base_url=base_url)
except Exception as e:
    print(f"❌ ERROR: Failed to initialize OpenAI client: {e}")
    sys.exit(1)

def test_model(role_name, model_name):
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

# 4. Run Tests
success_count = 0
total_tests = 3

if test_model("Interviewer", model_interviewer):
    success_count += 1
print("--------------------------------------------------")

if test_model("Analyst", model_analyst):
    success_count += 1
print("--------------------------------------------------")

if test_model("Architect", model_architect):
    success_count += 1

print("\n==================================================")
if success_count == total_tests:
    print("🎉 All systems operational! We are ready to code.")
else:
    print(f"⚠️  Warning: Only {success_count}/{total_tests} models passed. Please check configuration.")
print("==================================================")
