import os
import sys
import unittest
from contextlib import nullcontext
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.architect import ArchitectAgent
from utils.deliverables import split_deliverables


class TestArchitectMultiFileOutput(unittest.TestCase):
    @patch("agents.architect.llm_client.get_completion")
    def test_architect_output_can_be_split(self, mock_get_completion):
        mock_get_completion.return_value = (
            "\n".join(
                [
                    "=== FILE: DOC_01_PRD.md ===",
                    "# PRD",
                    "x",
                    "=== FILE: DOC_02_Tech_Architecture.md ===",
                    "# Tech",
                    "y",
                    "=== FILE: DOC_03_UX_Concept.md ===",
                    "# UX",
                    "z",
                    "=== FILE: DOC_04_Data_Schema.md ===",
                    "# Data",
                    "w",
                    "=== FILE: DOC_05_Distribution_Deployment.md ===",
                    "# Deploy",
                    "a",
                    "=== FILE: DOC_06_Growth_Monetization.md ===",
                    "# Growth",
                    "b",
                ]
            ),
            123,
        )
        agent = ArchitectAgent()
        with patch("agents.architect.st.spinner", return_value=nullcontext()):
            out = agent.run({"k": "v"})
        docs = split_deliverables(out)
        self.assertEqual(len(docs), 6)
        self.assertEqual(docs[0]["file_name"], "DOC_01_PRD.md")


if __name__ == "__main__":
    unittest.main()

