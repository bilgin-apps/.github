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
        self.assertEqual(len(MODULE.EXAM_ISSUES), 5)
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
        url = "https://github.com/bilgin-apps/bilgin-exam-tr-web/issues/9"
        items = [{"id": "item-id", "content": {"url": url}}]
        with patch.object(MODULE, "json_command") as api:
            MODULE.add_issue(1, "project-id", url, "P0", "Feature",
                             "Web", "Bilgin Exam TR", items)
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

class ImportSafetyTests(unittest.TestCase):
    def test_protected_repositories_are_never_queried_or_added(self):
        for repo in MODULE.PROTECTED_REPOSITORIES:
            with patch.object(MODULE, 'json_command') as api:
                MODULE.add_issue(1, 'p', f'https://github.com/bilgin-apps/{repo}/issues/999', 'P0', 'Bug', 'Mobile', 'Bilgin Exam TR', [])
                api.assert_not_called()

    def test_closed_issue_is_not_added(self):
        with patch.object(MODULE, 'json_command', return_value={'state': 'closed'}) as api:
            MODULE.add_issue(1, 'p', 'https://github.com/bilgin-apps/bilgin-exam-tr-web/issues/9', 'P1', 'Release', 'Web', 'Bilgin Exam TR', [])
            self.assertEqual(api.call_count, 1)
            self.assertEqual(api.call_args.args[0], 'api')

    def test_deleted_issue_fails_closed(self):
        with patch.object(MODULE, 'json_command', side_effect=RuntimeError('404')) as api:
            with self.assertRaises(RuntimeError):
                MODULE.add_issue(1, 'p', 'https://github.com/bilgin-apps/bilgin-exam-tr-web/issues/9', 'P1', 'Release', 'Web', 'Bilgin Exam TR', [])
            self.assertEqual(api.call_count, 1)

    def test_repo_links_use_qualified_name(self):
        with patch.object(MODULE, 'run') as run:
            MODULE.ensure_links(1, {'repos':['bilgin-exam-tr-web']})
            self.assertIn('bilgin-apps/bilgin-exam-tr-web', run.call_args.args)


class ApiCompatibilityTests(unittest.TestCase):
    def test_reserved_type_name_is_avoided(self):
        self.assertNotIn("Type", MODULE.SINGLE_FIELDS)
        self.assertEqual(MODULE.SINGLE_FIELDS["Work Type"],
                         ["Feature", "Bug", "Technical Task", "Content", "Release", "Security", "Research"])

    def test_draft_blueprints_reference_valid_select_options(self):
        for draft in MODULE.ABC_DRAFTS + MODULE.ROADMAP_DRAFTS:
            self.assertIn(draft[2], MODULE.SINGLE_FIELDS["Priority"])
            self.assertIn(draft[3], MODULE.SINGLE_FIELDS["Work Type"])
            self.assertIn(draft[4], MODULE.SINGLE_FIELDS["Area"])

    def test_rest_view_uses_status_columns_and_priority_sort(self):
        import json
        names = ["Title", "Status", "Priority", "Work Type", "Area", "Assignees", "Sprint", "Release", "Target Date"]
        fields = [{"id": n, "name": name} for n, name in enumerate(names, 1)]
        def api(*args, **kwargs):
            if "--method" not in args:
                return json.dumps([fields])
            return json.dumps({"value": {"node_id": "view-id"}})
        with patch.object(MODULE, "project_meta", side_effect=[{"views":{"nodes":[]}}] + [{"views":{"nodes":[{"name": n, "layout": l} for n,l in [("Board","BOARD_LAYOUT"),("Table","TABLE_LAYOUT"),("Roadmap","ROADMAP_LAYOUT")]]}}] * 3), patch.object(MODULE, "run", side_effect=api) as run:
            MODULE.ensure_views(1, "project-id")
            payloads = [json.loads(c.kwargs["input_data"]) for c in run.call_args_list if "--method" in c.args]
        board = next(p for p in payloads if p["name"] == "Board")
        self.assertEqual(board["vertical_group_by"], [2])
        self.assertEqual(board["sort_by"], [[3, "asc"]])
        self.assertNotIn("visible_fields", next(p for p in payloads if p["name"] == "Roadmap"))


class WorkflowSafetyTests(unittest.TestCase):
    def test_only_enabled_broad_subissue_intake_is_removed_and_verified(self):
        before = {"node":{"workflows":{"nodes":[
            {"id":"unsafe", "name":"Auto-add sub-issues to project", "enabled":True},
            {"id":"manual", "name":"Item closed", "enabled":False}]}}}
        after = {"node":{"workflows":{"nodes":[{"id":"manual", "name":"Item closed", "enabled":False}]}}}
        with patch.object(MODULE, "graphql", side_effect=[before, {}, after]) as api:
            MODULE.disable_unsafe_subissue_intake("project")
        self.assertIn("deleteProjectV2Workflow", api.call_args_list[1].args[0])
        self.assertEqual(api.call_args_list[1].args[1], {"id":"unsafe"})


if __name__ == "__main__":
    unittest.main()
