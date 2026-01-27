import os
import sys
import unittest
from contextlib import nullcontext
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.judge import JudgeAgent


class TestJudgeAgent(unittest.TestCase):
    def test_response_format_env_json_string_enables_json_object(self):
        os.environ["RESPONSE_FORMAT_JUDGE"] = "{\"type\":\"json_object\"}"
        try:
            agent = JudgeAgent()
            with patch("agents.judge.llm_client.get_completion") as mock_get_completion:
                mock_get_completion.return_value = ("{\"judge_notice\":\"n\"}", 1)
                with patch("agents.judge.st.spinner", return_value=nullcontext()):
                    agent.run(chat_history=[], current_json_state={}, context_summary=None)
                call = mock_get_completion.call_args
                if call is None:
                    self.fail("llm_client.get_completion was not called")
                _, kwargs = call
                self.assertEqual(kwargs.get("response_format"), {"type": "json_object"})
        finally:
            os.environ.pop("RESPONSE_FORMAT_JUDGE", None)

    @patch("agents.judge.llm_client.get_completion")
    def test_parses_wrapped_json(self, mock_get_completion):
        mock_get_completion.return_value = (
            "Here is the result:\n```json\n{\"judge_notice\":\"n\",\"next_questions\":[\"q1\"],\"evidence_gaps\":[\"g\"]}\n```\n",
            10,
        )
        agent = JudgeAgent()
        with patch("agents.judge.st.spinner", return_value=nullcontext()):
            data = agent.run(
                chat_history=[{"role": "user", "content": "我想用AI做个工具。"}],
                current_json_state={"missing_info": ["Core Scenario (3-min story)"]},
                context_summary=None,
            )
        self.assertTrue(isinstance(data, dict))
        data_dict = data if isinstance(data, dict) else {}
        self.assertEqual(data_dict.get("judge_notice"), "n")
        self.assertEqual(data_dict.get("next_questions"), ["q1"])

    @patch("agents.judge.llm_client.get_completion")
    def test_returns_none_on_invalid_json(self, mock_get_completion):
        mock_get_completion.return_value = ("not a json", 0)
        agent = JudgeAgent()
        with patch("agents.judge.st.spinner", return_value=nullcontext()):
            data = agent.run(chat_history=[], current_json_state={}, context_summary=None)
        self.assertIsNone(data)


if __name__ == "__main__":
    unittest.main()
