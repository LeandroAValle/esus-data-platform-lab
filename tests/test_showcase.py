import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ShowcaseTests(unittest.TestCase):
    def test_showcase_points_only_to_existing_files(self):
        data = json.loads((ROOT / "site" / "layers.json").read_text(encoding="utf-8"))
        for layer in data["layers"]:
            for relative_path in layer["files"]:
                self.assertTrue((ROOT / relative_path).is_file(), relative_path)
        self.assertTrue((ROOT / data["orchestration"]["file"]).is_file())

    def test_roadmap_is_separate_from_implemented_layers(self):
        data = json.loads((ROOT / "site" / "layers.json").read_text(encoding="utf-8"))
        self.assertEqual(5, len(data["layers"]))
        self.assertEqual(5, len(data["orchestration"]["tasks"]))
        self.assertGreater(len(data["roadmap"]), 0)
