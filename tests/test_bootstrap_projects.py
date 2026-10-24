"""Unit tests for the Bilgin Apps GitHub Projects bootstrap.

No network, GitHub credentials or organization write permissions are required.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_projects.py"
SPEC = importlib.util.spec_from_file_location("bilgin_projects_tested", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ProjectsBootstrapTests(unittest.TestCase):
    def setUp(self):
        MODULE.FIELD_CACHE.clear()
        MODULE.WARNINGS.clear()

    def test_three_private_project_blueprints(self):
        self.assertEqual(
            list(MODULE.PROJECTS),
            ["Bilgin Exam TR", "Bilgin ABC", "Bilgin Apps Roadmap"],
        )
        self.assertEqual(len(MODULE.EXAM_ISSUES), 13)
        self.assertEqual(len(MODULE.ROADMAP_ISSUES), 3)
        self.assertEqual(len(MODULE.ABC_DRAFTS), 10)
        self.assertEqual(len(MODULE.ROADMAP_DRAFTS), 3)

    def test_existing_project_is_reused_and_configured_private(self):
        with patch.object(MODULE, "json_command", return_value={
            "projects": [{"title": "Bilgin Exam TR", "number": 4}]
        }), patch.object(MODULE, "run", return_value="") as command:
            number, created = MODULE.ensure_project(
                "Bilgin Exam TR", MODULE.PROJECTS["Bilgin Exam TR"]
            )
        self.assertEqual(number, 4)
        self.assertFalse(created)
        args = command.call_args.args
        self.assertIn("--visibility", args)
        self.assertIn("PRIVATE", args)

    def test_existing_issue_is_not_added_twice(self):
        url = "https://github.com/bilgin-apps/bilgin-exam-tr-mobile/issues/1"
        items = [{"id": "item-id", "content": {"url": url}}]
        with patch.object(MODULE, "json_command") as api:
            MODULE.add_issue(1, "project-id", url, "P0", "Feature",
                             "Mobile", "Bilgin Exam TR", items)
        api.assert_not_called()

    def test_existing_draft_is_not_added_twice(self):
        items = [{"title": "[P0] Define age-appropriate literacy outcomes and scope"}]
        with patch.object(MODULE, "json_command") as api:
            MODULE.add_draft(
                1, "project-id",
                "[P0] Define age-appropriate literacy outcomes and scope",
                "Draft details", "P0", "Content", "Product", "Bilgin ABC", items
            )
        api.assert_not_called()

    def test_unchanged_existing_status_options_are_safe(self):
        with patch.object(MODULE, "project_meta", return_value={
            "fields": {"nodes": [{"name": "Status", "id": "field",
                                 "options": [{"name": "Todo"}]}]}
        }), patch.object(MODULE, "graphql") as graphql:
            MODULE.configure_status("project", is_new=False)
        graphql.assert_not_called()
        self.assertTrue(MODULE.WARNINGS)

    def test_new_project_status_has_six_stages(self):
        with patch.object(MODULE, "project_meta", return_value={
            "fields": {"nodes": [{"name": "Status", "id": "field", "options": []}]}
        }), patch.object(MODULE, "graphql", return_value={}) as api:
            MODULE.configure_status("project", is_new=True)
        payload = api.call_args.args[1]["input"]
        self.assertEqual(
            [option["name"] for option in payload["singleSelectOptions"]],
            ["Backlog", "Todo", "In Progress", "In Review", "Testing", "Done"],
        )


if __name__ == "__main__":
    unittest.main()
