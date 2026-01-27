import unittest

from utils.deliverables import split_deliverables


class TestDeliverablesSplit(unittest.TestCase):
    def test_single_doc_when_no_headers(self):
        docs = split_deliverables("# Title\nHello")
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["file_name"], "Maia_Deliverables.md")

    def test_multi_docs_with_headers(self):
        raw = (
            "=== FILE: DOC_01_PRD.md ===\n# PRD\nA\n\n"
            "=== FILE: DOC_02_Tech_Architecture.md ===\n# Tech\nB\n"
        )
        docs = split_deliverables(raw)
        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]["file_name"], "DOC_01_PRD.md")
        self.assertIn("# PRD", docs[0]["content"])


if __name__ == "__main__":
    unittest.main()

