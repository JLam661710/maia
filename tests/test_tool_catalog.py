import unittest

from utils.tool_catalog import validate_tool_catalog, build_catalog_injection


class TestToolCatalog(unittest.TestCase):
    def test_validate_ok(self):
        catalog = {
            "categories": [
                {"id": "deployment", "name": "部署", "items": [{"id": "vercel", "name": "Vercel"}]},
            ]
        }
        self.assertIsNone(validate_tool_catalog(catalog))

    def test_validate_missing_categories(self):
        self.assertIsNotNone(validate_tool_catalog({}))

    def test_build_injection_truncation(self):
        catalog = {"policies": {}, "categories": []}
        for i in range(200):
            catalog["categories"].append(
                {
                    "id": f"c{i}",
                    "name": f"分类{i}",
                    "items": [{"id": f"it{i}", "name": "x" * 30, "status": "allowed"}],
                }
            )
        text = build_catalog_injection(catalog, max_chars=500)
        self.assertTrue(len(text) <= 520)
        self.assertIn("[HUMAN_TOOL_CATALOG]", text)


if __name__ == "__main__":
    unittest.main()

