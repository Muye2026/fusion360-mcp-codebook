import os
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepoHygieneTests(unittest.TestCase):
    def test_archived_gateway_not_in_mainline(self):
        self.assertFalse((REPO_ROOT / "server").exists())
        self.assertFalse((REPO_ROOT / "start.sh").exists())

    def test_no_local_cache_dirs(self):
        forbidden = {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", ".workbuddy", ".venv"}
        found = []
        for root, dirs, _files in os.walk(REPO_ROOT):
            root_path = Path(root)
            if ".git" in root_path.parts:
                dirs[:] = []
                continue
            for dirname in list(dirs):
                if dirname in forbidden:
                    found.append(str(root_path / dirname))
        self.assertEqual(found, [])

    def test_no_macos_metadata_files(self):
        found = [
            str(path.relative_to(REPO_ROOT))
            for path in REPO_ROOT.rglob(".DS_Store")
            if ".git" not in path.parts
        ]
        self.assertEqual(found, [])

    def test_no_copied_official_docs_directory(self):
        self.assertFalse((REPO_ROOT / "api_docs").exists())


if __name__ == "__main__":
    unittest.main()
