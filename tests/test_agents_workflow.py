import os
import sys
import json
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
load_dotenv()

from agents.interviewer import InterviewerAgent
from agents.analyst import AnalystAgent
from agents.architect import ArchitectAgent
from agents.summary import SummaryAgent
from agents.judge import JudgeAgent

def test_workflow():
    print("🚀 Starting Agent Workflow Test (Doubao 1.8 Config)...")
    print(f"API Base: {os.getenv('OPENAI_BASE_URL')}")
    print("-" * 50)

    # 1. Test Interviewer
    print("\n[1/5] Testing Interviewer Agent...")
    try:
        interviewer = InterviewerAgent()
        history = [{"role": "user", "content": "我想做一个AI驱动的个人助理应用。"}]
        system_notice = "Understand the user's basic idea."
        
        start_time = time.time()
        response = interviewer.run(history, system_notice)
        duration = time.time() - start_time
        
        if response:
            print(f"✅ Interviewer Success ({duration:.2f}s)")
            print(f"Response Preview: {response[:100]}...")
        else:
            print("❌ Interviewer Failed: No response")
            return
    except Exception as e:
        print(f"❌ Interviewer Error: {e}")
        return

    # 2. Test Summary
    print("\n[2/5] Testing Summary Agent...")
    try:
        summary_agent = SummaryAgent()
        current_summary = "User wants an AI assistant."
        new_msgs = [
            {"role": "user", "content": "我想做一个AI驱动的个人助理应用。"},
            {"role": "assistant", "content": response}
        ]
        
        start_time = time.time()
        summary = summary_agent.update_summary(current_summary, new_msgs)
        duration = time.time() - start_time
        
        if summary:
            print(f"✅ Summary Success ({duration:.2f}s)")
            print(f"Summary Preview: {summary[:100]}...")
        else:
            print("❌ Summary Failed: No response")
    except Exception as e:
        print(f"❌ Summary Error: {e}")

    # 3. Test Analyst
    print("\n[3/5] Testing Analyst Agent...")
    try:
        analyst = AnalystAgent()
        current_state = {
            "interview_session": {
                "system_notice": "Start interview",
                "stage": "initial"
            },
            "project_info": {}
        }
        
        start_time = time.time()
        result = analyst.run(history + [{"role": "assistant", "content": response}], current_state)
        duration = time.time() - start_time
        
        if result and "json_state" in result:
            print(f"✅ Analyst Success ({duration:.2f}s)")
            print(f"Updated State Keys: {result['json_state'].keys()}")
            final_state = result['json_state']
        else:
            print("❌ Analyst Failed: Invalid response")
            return
    except Exception as e:
        print(f"❌ Analyst Error: {e}")
        return

    # 4. Test Judge
    print("\n[4/5] Testing Judge Agent...")
    try:
        judge = JudgeAgent()
        start_time = time.time()
        judge_result = judge.run(
            chat_history=history + [{"role": "assistant", "content": response}],
            current_json_state=final_state if isinstance(final_state, dict) else {},
        )
        duration = time.time() - start_time
        if judge_result:
            print(f"✅ Judge Success ({duration:.2f}s)")
            preview = str(judge_result)[:120].replace("\n", " ")
            print(f"Judge Preview: {preview}...")
        else:
            print("⚠️  Judge returned no result (may be due to configuration).")
    except Exception as e:
        print(f"❌ Judge Error: {e}")

    # 5. Test Architect
    print("\n[5/5] Testing Architect Agent...")
    try:
        architect = ArchitectAgent()
        # Use a dummy finalized state for testing
        final_mock_state = {
            "project_name": "AI Personal Assistant",
            "core_features": ["Task Management", "Chat Interface"],
            "tech_stack": ["Python", "React"]
        }
        
        start_time = time.time()
        deliverables = architect.run(json.dumps(final_mock_state))
        duration = time.time() - start_time
        
        if deliverables:
            print(f"✅ Architect Success ({duration:.2f}s)")
            print(f"Deliverables Preview: {deliverables[:100]}...")
        else:
            print("❌ Architect Failed: No response")
    except Exception as e:
        print(f"❌ Architect Error: {e}")

    print("\n" + "=" * 50)
    print("🎉 All Tests Completed!")

if __name__ == "__main__":
    test_workflow()
