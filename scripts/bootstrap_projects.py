#!/usr/bin/env python3
"""Provision private Bilgin Apps GitHub Projects V2.

Requirements: Python 3.9+, GitHub CLI (gh) and an authenticated GitHub
account authorized to manage bilgin-apps Projects.
Run: python3 scripts/bootstrap_projects.py

This script is intentionally additive and repeatable. It does not edit or
delete product code, repositories, branches, project items or workflows.
"""

from __future__ import annotations

import datetime as dt
import json
import shutil
import subprocess
import sys
from typing import Any

OWNER = "bilgin-apps"

PROJECTS = {
    "Bilgin Exam TR": {
        "description": "Private delivery board for Exam TR backend, admin, mobile, web, learning content and release readiness.",
        "readme": """# Bilgin Exam TR

This project tracks the delivery of Bilgin Exam TR across four private repositories.

**Workflow:** Backlog -> Todo -> In Progress -> In Review -> Testing -> Done.

**Priority:** P0 (release-blocking), P1 (important), P2 (planned), P3 (later).

Use Issues as the source of implementation scope. Changes move through main, test-env and prod only after applicable review and checks. Branch names do not themselves publish software.

Review P0 blockers weekly; never move a task to Done solely because its issue was assigned or a pull request was opened.
""",
        "repos": ["bilgin-exam-tr-backend", "bilgin-exam-tr-admin", "bilgin-exam-tr-mobile", "bilgin-exam-tr-web"],
    },
    "Bilgin ABC": {
        "description": "Private roadmap for the Turkish early-literacy learning app, from curriculum and content to mobile delivery.",
        "readme": """# Bilgin ABC

Private planning for a playful Turkish-language early-literacy product.

Focus on age-appropriate literacy progression, Turkish phonics, child safety, accessibility, lesson quality and delightful mobile experiences.

Work starts as Project draft items until product repositories are actually created. Convert drafts into repository Issues when implementation ownership is clear. The product is planned without advertising inside the ABC app.

**Workflow:** Backlog -> Todo -> In Progress -> In Review -> Testing -> Done.
""",
        "repos": [],
    },
    "Bilgin Apps Roadmap": {
        "description": "Private portfolio roadmap for cross-product engineering, quality, platform operations, launch and shared decisions.",
        "readme": """# Bilgin Apps Roadmap

Organization-wide, private portfolio view across Bilgin Exam TR and Bilgin ABC.

Track delivery milestones, launch blockers, security/privacy readiness, release governance, resourcing and shared infrastructure here.

Link to implementation Issues in product repositories instead of duplicating engineering tasks. Set Start Date and Target Date once targets have been explicitly agreed; do not invent launch dates.

Hold a weekly roadmap review and record decisions, owners, risks, dependencies and next actions.
""",
        "repos": [".github"],
    },
}

EXAM_ISSUES = [
    ("bilgin-exam-tr-backend", 2, "P0", "Security", "Backend"),
    ("bilgin-exam-tr-backend", 3, "P0", "Security", "Backend"),
    ("bilgin-exam-tr-backend", 4, "P0", "Technical Task", "Backend"),
    ("bilgin-exam-tr-backend", 5, "P1", "Content", "Content"),
    ("bilgin-exam-tr-admin", 19, "P0", "Security", "Admin"),
    ("bilgin-exam-tr-admin", 20, "P1", "Technical Task", "Admin"),
    ("bilgin-exam-tr-admin", 21, "P1", "Release", "Admin"),
    ("bilgin-exam-tr-mobile", 1, "P0", "Technical Task", "Mobile"),
    ("bilgin-exam-tr-mobile", 2, "P0", "Feature", "Mobile"),
    ("bilgin-exam-tr-mobile", 3, "P1", "Feature", "Mobile"),
    ("bilgin-exam-tr-mobile", 4, "P1", "Release", "Mobile"),
    ("bilgin-exam-tr-web", 9, "P1", "Release", "Web"),
    ("bilgin-exam-tr-web", 10, "P1", "Technical Task", "Web"),
]
ROADMAP_ISSUES = [
    (".github", 1, "P0", "Technical Task", "Shared"),
    (".github", 2, "P1", "Technical Task", "Shared"),
    (".github", 3, "P1", "Technical Task", "Infrastructure"),
]
ABC_DRAFTS = [
    ("[P0] Define age-appropriate literacy outcomes and scope", "Set learning objectives by developmental stage, letter-sound progression, Turkish orthography and content review policy.", "P0", "Product", "Content"),
    ("[P0] Establish child-safety, data privacy and parental consent requirements", "Define privacy-by-design guardrails, parental controls, safe metrics and age-appropriate disclosures.", "P0", "Security", "Product"),
    ("[P0] Approve ABC brand, characters and mobile design system", "Keep the Bilgin mascot recognizable; document scalable UI tokens, character usage and accessible components.", "P0", "Feature", "Product"),
    ("[P0] Specify Bilgin ABC technical architecture and repositories", "Confirm mobile framework, backend reuse boundaries, offline requirements and secure environments before creating repos.", "P0", "Technical Task", "Infrastructure"),
    ("[P1] Design a ten-world early-learning curriculum map", "Outline 10 connected learning worlds with age-appropriate goals, gradual difficulty and review loops.", "P1", "Content", "Content"),
    ("[P1] Prototype Turkish letter, sound and word exercises", "Design interactive matching, tracing/recognition and phonics activities with feedback and accessibility.", "P1", "Feature", "Mobile"),
    ("[P1] Build a reviewed audio and content production workflow", "Specify recording standards, pronunciation quality checks, licensing and editorial approval.", "P1", "Content", "Content"),
    ("[P1] Design the ad-free parent experience and subscriptions", "Define guardians' progress visibility, accessibility, clear subscription terms and an ad-free child experience.", "P1", "Feature", "Product"),
    ("[P1] Plan iOS beta testing and feedback collection", "Define internal device testing, TestFlight readiness, crash monitoring and parent feedback with privacy safeguards.", "P1", "Release", "Mobile"),
    ("[P2] Define offline usability and inclusive-learning QA", "Validate slow networks, device constraints, text-to-speech needs, accessibility and graceful recovery.", "P2", "Technical Task", "Mobile"),
]
ROADMAP_DRAFTS = [
    ("[P1] Align Bilgin Apps product architecture and brand boundaries", "Define shared and product-specific design, infrastructure and documentation ownership.", "P1", "Product", "Shared"),
    ("[P1] Establish launch-readiness scorecards for both products", "Track approved release criteria rather than guessed dates: content, store, security, privacy and support readiness.", "P1", "Release", "Shared"),
    ("[P2] Define privacy-conscious product analytics and observability", "Select minimum necessary metrics, consent requirements, service alerts and incident ownership.", "P2", "Technical Task", "Infrastructure"),
]

SINGLE_FIELDS = {
    "Priority": ["P0", "P1", "P2", "P3"],
    "Type": ["Feature", "Bug", "Technical Task", "Content", "Release", "Security", "Research"],
    "Area": ["Backend", "Admin", "Mobile", "Web", "Content", "Infrastructure", "Product", "Shared"],
    "Product": ["Bilgin Exam TR", "Bilgin ABC", "Shared"],
}
OTHER_FIELDS = {
    "Release": "TEXT",
    "Start Date": "DATE",
    "Target Date": "DATE",
    "Effort": "NUMBER",
}
STATES = [
    ("Backlog", "Untriaged or accepted work not yet scheduled.", "GRAY"),
    ("Todo", "Ready to begin with clear acceptance criteria.", "BLUE"),
    ("In Progress", "Implementation is actively underway.", "YELLOW"),
    ("In Review", "Awaiting peer review and required checks.", "PURPLE"),
    ("Testing", "Under QA or beta validation.", "ORANGE"),
    ("Done", "Accepted and fully validated.", "GREEN"),
]

WARNINGS: list[str] = []


def run(*args: str, input_data: str | None = None, quiet: bool = False) -> str:
    cmd = ["gh", *args]
    process = subprocess.run(cmd, input=input_data, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if process.returncode:
        raise RuntimeError(f"{' '.join(cmd[:5])}: {process.stderr.strip()}")
    if not quiet and process.stderr.strip():
        print(process.stderr.strip(), file=sys.stderr)
    return process.stdout.strip()


def json_command(*args: str) -> dict[str, Any]:
    output = run(*args, quiet=True)
    return json.loads(output) if output else {}


def graphql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    response = json_command("api", "graphql", "--input", "-") if False else run(
        "api", "graphql", "--input", "-",
        input_data=json.dumps({"query": query, "variables": variables}),
        quiet=True,
    )
    data = json.loads(response)
    if data.get("errors"):
        raise RuntimeError(str(data["errors"]))
    return data.get("data", {})


def warn(message: str) -> None:
    WARNINGS.append(message)
    print(f"WARNING: {message}", file=sys.stderr)


def project_number(title: str) -> int | None:
    data = json_command("project", "list", "--owner", OWNER, "--limit", "100", "--format", "json")
    matches = [p for p in data.get("projects", []) if p.get("title") == title]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple projects share the title {title!r}. Resolve duplicates manually.")
    return int(matches[0]["number"]) if matches else None


def ensure_project(title: str, config: dict[str, Any]) -> tuple[int, bool]:
    number = project_number(title)
    new = number is None
    if new:
        created = json_command("project", "create", "--owner", OWNER, "--title", title, "--format", "json")
        number = int(created["number"])
        print(f"CREATED project: {title} (#{number})")
    else:
        print(f"REUSING project: {title} (#{number})")
    run(
        "project", "edit", str(number), "--owner", OWNER,
        "--description", config["description"],
        "--readme", config["readme"],
        "--visibility", "PRIVATE", quiet=True,
    )
    return number, new


def project_id(number: int) -> str:
    return str(json_command("project", "view", str(number), "--owner", OWNER, "--format", "json")["id"])


def project_meta(pid: str) -> dict[str, Any]:
    query = """query($id:ID!) {
      node(id:$id) { ... on ProjectV2 {
        fields(first:100) { nodes {
          ... on ProjectV2FieldCommon { id name }
          ... on ProjectV2SingleSelectField { id name options { id name } }
        }}
        views(first:40) { nodes { id name layout } }
      }}
    }"""
    return graphql(query, {"id": pid}).get("node") or {}


def ensure_field(number: int, name: str, field_type: str, options: list[str] | None = None) -> None:
    fields = json_command("project", "field-list", str(number), "--owner", OWNER, "--format", "json").get("fields", [])
    if any(f.get("name") == name for f in fields):
        return
    cmd = ["project", "field-create", str(number), "--owner", OWNER, "--name", name, "--data-type", field_type]
    if options:
        cmd.extend(["--single-select-options", ",".join(options)])
    run(*cmd, quiet=True)
    print(f"  + Field: {name}")


def ensure_sprint_field(pid: str) -> None:
    meta = project_meta(pid)
    if any(f.get("name") == "Sprint" for f in meta.get("fields", {}).get("nodes", [])):
        return
    today = dt.date.today()
    first_monday = today + dt.timedelta(days=(7 - today.weekday()) % 7)
    input_value = {
        "projectId": pid,
        "name": "Sprint",
        "dataType": "ITERATION",
        "iterationConfiguration": {"duration": 14, "startDate": first_monday.isoformat(), "iterations": []},
    }
    query = """mutation($input:CreateProjectV2FieldInput!) {
      createProjectV2Field(input:$input) {
        projectV2Field { ... on ProjectV2FieldCommon { id name } }
      }
    }"""
    try:
        graphql(query, {"input": input_value})
        print("  + Native two-week Sprint field")
    except Exception as exc:
        warn(f"Could not configure native Sprint field: {exc}. Create an Iteration field in GitHub UI.")


def configure_status(pid: str, is_new: bool) -> None:
    meta = project_meta(pid)
    status = next((f for f in meta.get("fields", {}).get("nodes", []) if f.get("name") == "Status"), None)
    if not status:
        warn("Default Status field not found. Configure six status options in the project UI.")
        return
    existing = {x["name"] for x in status.get("options", [])}
    if all(name in existing for name, _, _ in STATES):
        return
    if not is_new:
        warn("Existing project Status options were left untouched to avoid resetting item values.")
        return
    query = """mutation($input:UpdateProjectV2FieldInput!) {
      updateProjectV2Field(input:$input) {
        projectV2Field { ... on ProjectV2SingleSelectField { id name } }
      }
    }"""
    payload = {"fieldId": status["id"], "singleSelectOptions": [
        {"name": name, "description": description, "color": color} for name, description, color in STATES
    ]}
    try:
        graphql(query, {"input": payload})
        print("  + Six-stage Status workflow")
    except Exception as exc:
        warn(f"Could not update six-stage Status: {exc}. Configure options manually.")


def ensure_views(pid: str) -> None:
    layouts = {"Board": "BOARD_LAYOUT", "Table": "TABLE_LAYOUT", "Roadmap": "ROADMAP_LAYOUT"}
    meta = project_meta(pid)
    views = meta.get("views", {}).get("nodes", [])
    by_name = {v.get("name"): v for v in views}
    # New GitHub Projects can start with a default unnamed view.
    if "Table" not in by_name:
        default = next((v for v in views if v.get("name", "").lower().startswith("view ") and v.get("layout") == "TABLE_LAYOUT"), None)
        if default:
            query = """mutation($input:UpdateProjectV2ViewInput!) {
              updateProjectV2View(input:$input) { projectV2View { id name } }
            }"""
            try:
                graphql(query, {"input": {"viewId": default["id"], "name": "Table"}})
                by_name["Table"] = default
                print("  ~ Renamed default view to Table")
            except Exception as exc:
                warn(f"Could not rename default view: {exc}")
    query = """mutation($input:CreateProjectV2ViewInput!) {
      createProjectV2View(input:$input) { projectV2View { id name layout } }
    }"""
    for name, layout in layouts.items():
        if name in by_name:
            continue
        try:
            graphql(query, {"input": {"projectId": pid, "name": name, "layout": layout}})
            print(f"  + View: {name}")
        except Exception as exc:
            warn(f"Could not create {name} view: {exc}. Add it from GitHub UI.")


def set_single(pid: str, item_id: str, field_name: str, name: str) -> None:
    field = next(
        (f for f in project_meta(pid).get("fields", {}).get("nodes", []) if f.get("name") == field_name),
        None
    )
    if not field:
        warn(f"Field {field_name} is missing, cannot set it for item {item_id}")
        return
    option = next((o for o in field.get("options", []) if o.get("name") == name), None)
    if not option:
        warn(f"Option {field_name}={name} missing, cannot set it for item {item_id}")
        return
    query = """mutation($input:UpdateProjectV2ItemFieldValueInput!) {
      updateProjectV2ItemFieldValue(input:$input) { projectV2Item { id } }
    }"""
    try:
        graphql(query, {"input": {
            "projectId": pid, "itemId": item_id, "fieldId": field["id"],
            "value": {"singleSelectOptionId": option["id"]},
        }})
    except Exception as exc:
        warn(f"Cannot set {field_name}={name} for {item_id}: {exc}")


def current_items(number: int) -> list[dict[str, Any]]:
    data = json_command("project", "item-list", str(number), "--owner", OWNER, "--limit", "500", "--format", "json")
    return data.get("items", [])


def add_issue(number: int, pid: str, url: str, priority: str, kind: str, area: str, product: str, items: list[dict[str, Any]]) -> None:
    found = next((i for i in items if (i.get("content") or {}).get("url") == url), None)
    if found:
        return
    try:
        item = json_command("project", "item-add", str(number), "--owner", OWNER, "--url", url, "--format", "json")
        item_id = item.get("id")
        if item_id:
            for field, value in (("Status", "Backlog"), ("Priority", priority), ("Type", kind), ("Area", area), ("Product", product)):
                set_single(pid, item_id, field, value)
        print(f"  + Linked Issue: {url}")
    except Exception as exc:
        warn(f"Could not add Issue {url}: {exc}")


def add_draft(number: int, pid: str, title: str, body: str, priority: str, kind: str, area: str, product: str, items: list[dict[str, Any]]) -> None:
    if any(i.get("title") == title for i in items):
        return
    try:
        item = json_command("project", "item-create", str(number), "--owner", OWNER,
                            "--title", title, "--body", body, "--format", "json")
        item_id = item.get("id")
        if item_id:
            for field, value in (("Status", "Backlog"), ("Priority", priority), ("Type", kind), ("Area", area), ("Product", product)):
                set_single(pid, item_id, field, value)
        print(f"  + Draft: {title}")
    except Exception as exc:
        warn(f"Could not create draft {title!r}: {exc}")


def ensure_links(number: int, config: dict[str, Any]) -> None:
    for repo in config["repos"]:
        try:
            run("project", "link", str(number), "--owner", OWNER, "--repo", repo, quiet=True)
        except Exception as exc:
            # Re-linking an existing repo can be rejected; do not delete or reassign it.
            warn(f"Project/repo link needs a manual check for {repo}: {exc}")


def main() -> int:
    if shutil.which("gh") is None:
        print("GitHub CLI not found. Install from https://cli.github.com/ and run gh auth login.", file=sys.stderr)
        return 2
    try:
        run("auth", "status", quiet=True)
        run("api", f"orgs/{OWNER}", quiet=True)
        # Check Projects authorization before creating anything.
        run("project", "list", "--owner", OWNER, "--limit", "1", quiet=True)
    except Exception as exc:
        print(f"GitHub authentication or Projects access failed: {exc}\n"
              "Run: gh auth refresh -s project -s repo\n"
              "Sign in as an organization member with Projects write permission.", file=sys.stderr)
        return 2

    results: dict[str, int] = {}
    for title, cfg in PROJECTS.items():
        print(f"\n=== {title} ===")
        try:
            number, newly_created = ensure_project(title, cfg)
            pid = project_id(number)
            configure_status(pid, newly_created)
            for name, options in SINGLE_FIELDS.items():
                ensure_field(number, name, "SINGLE_SELECT", options)
            for name, field_type in OTHER_FIELDS.items():
                ensure_field(number, name, field_type)
            ensure_sprint_field(pid)
            ensure_views(pid)
            ensure_links(number, cfg)
            items = current_items(number)
            if title == "Bilgin Exam TR":
                for repo, issue_number, priority, kind, area in EXAM_ISSUES:
                    url = f"https://github.com/{OWNER}/{repo}/issues/{issue_number}"
                    add_issue(number, pid, url, priority, kind, area, title, items)
            elif title == "Bilgin ABC":
                for draft in ABC_DRAFTS:
                    add_draft(number, pid, *draft, title, items)
            else:
                for repo, issue_number, priority, kind, area in ROADMAP_ISSUES:
                    url = f"https://github.com/{OWNER}/{repo}/issues/{issue_number}"
                    add_issue(number, pid, url, priority, kind, area, "Shared", items)
                for draft in ROADMAP_DRAFTS:
                    add_draft(number, pid, *draft, "Shared", items)
            results[title] = number
            print(f"  Project: https://github.com/orgs/{OWNER}/projects/{number}")
        except Exception as exc:
            warn(f"Could not finish {title}: {exc}")

    print("\n=== Verification ===")
    for title, number in results.items():
        print(f"\n{title}: https://github.com/orgs/{OWNER}/projects/{number}")
        try:
            fields = json_command("project", "field-list", str(number), "--owner", OWNER, "--format", "json")
            items = current_items(number)
            print(f"  Fields: {', '.join(f.get('name', '?') for f in fields.get('fields', []))}")
            print(f"  Items: {len(items)}")
            print("  Visibility: configured PRIVATE; confirm through the GitHub UI.")
        except Exception as exc:
            warn(f"Could not verify project #{number}: {exc}")
    if WARNINGS:
        print(f"\nCompleted with {len(WARNINGS)} warning(s). Review them above.", file=sys.stderr)
        return 1
    print("\nProvisioning finished. Review view grouping, workflows, and privacy in GitHub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
