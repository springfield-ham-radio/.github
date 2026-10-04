#!/usr/bin/env python3
"""Apply labels.yml to every non-archived repository in a GitHub organization.

Creates labels that are missing and updates color and description when a
label name already exists. Labels that are not in the file are left in place.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from urllib.parse import quote

ORG = os.environ.get("LABEL_SYNC_ORG", "springfield-ham-radio")
MISSING_TOKEN_MESSAGE = (
    "LABEL_SYNC_TOKEN is missing. Create an organization fine-grained "
    "personal access token for springfield-ham-radio (repository access: "
    "All repositories; permissions: Issues read and write, Metadata read) "
    "and save it as an organization secret or a secret on this repository "
    "named LABEL_SYNC_TOKEN. See the Label sync section of the README."
)


def fail(message: str) -> None:
    print(f"::error::{message}", file=sys.stderr)
    raise SystemExit(1)


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and in_double:
            escaped = True
            continue
        if char == '"' and not in_single:
            in_double = not in_double
        elif char == "'" and not in_double:
            in_single = not in_single
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def parse_labels(text: str) -> list[dict[str, str]]:
    """Parse the small labels.yml subset this repo commits."""
    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = _strip_comment(raw).rstrip()
        if not line.strip():
            continue
        if line.startswith("- "):
            current = {}
            labels.append(current)
            key, value = _split_field(line[2:], lineno)
            current[key] = value
            continue
        if current is None or not line.startswith("  "):
            fail(f"labels.yml:{lineno}: expected a label field")
        key, value = _split_field(line.strip(), lineno)
        current[key] = value

    if not labels:
        fail("labels.yml does not define any labels")
    for index, label in enumerate(labels, start=1):
        for key in ("name", "color", "description"):
            if key not in label:
                fail(f"label {index} is missing {key}")
        label["color"] = normalize_color(label["color"])
        if len(label["description"]) > 100:
            fail(f"{label['name']!r} description is longer than 100 characters")
    names = [label["name"] for label in labels]
    if len(names) != len(set(names)):
        fail("labels.yml contains duplicate label names")
    return labels


def _split_field(text: str, lineno: int) -> tuple[str, str]:
    if ":" not in text:
        fail(f"labels.yml:{lineno}: expected key: value")
    key, raw = text.split(":", 1)
    key = key.strip()
    value = _unquote(raw.strip(), lineno)
    return key, value


def _unquote(value: str, lineno: int) -> str:
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            fail(f"labels.yml:{lineno}: invalid quoted value")
        if not isinstance(parsed, str):
            fail(f"labels.yml:{lineno}: expected a string")
        return parsed
    if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
        return value[1:-1]
    if value == "" or value[0] in {'"', "'"}:
        fail(f"labels.yml:{lineno}: invalid quoted value")
    return value


def normalize_color(color: str) -> str:
    return color.removeprefix("#").lower()


def normalize_description(description: str | None) -> str:
    return description or ""


def plan(desired: list[dict[str, str]], existing: list[dict]) -> list[dict[str, str]]:
    """Return create/update/unchanged actions. Never returns a delete."""
    by_name = {label["name"]: label for label in existing}
    actions: list[dict[str, str]] = []
    for label in desired:
        current = by_name.get(label["name"])
        if current is None:
            actions.append({**label, "action": "create"})
            continue
        same_color = normalize_color(current.get("color") or "") == label["color"]
        same_description = (
            normalize_description(current.get("description")) == label["description"]
        )
        action = "unchanged" if same_color and same_description else "update"
        actions.append({**label, "action": action})
    return actions


def gh_api(method: str, path: str, body: dict | None = None, paginate: bool = False) -> object:
    command = ["gh", "api", "--method", method]
    if paginate:
        command.append("--paginate")
    command.append(path)
    stdin = None
    if body is not None:
        command.append("--input")
        command.append("-")
        stdin = json.dumps(body)
    result = subprocess.run(
        command,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"{method} {path} failed: {detail}")
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


def list_repos(org: str) -> list[str]:
    payload = gh_api("GET", f"orgs/{quote(org, safe='')}/repos?per_page=100", paginate=True)
    if not isinstance(payload, list):
        fail(f"unexpected repository list for {org}")
    names: list[str] = []
    for repo in payload:
        if repo.get("archived"):
            continue
        names.append(repo["name"])
    return sorted(names)


def list_labels(org: str, repo: str) -> list[dict]:
    path = f"repos/{quote(org, safe='')}/{quote(repo, safe='')}/labels?per_page=100"
    payload = gh_api("GET", path, paginate=True)
    if not isinstance(payload, list):
        raise RuntimeError(f"unexpected label list for {org}/{repo}")
    return payload


def apply_action(org: str, repo: str, action: dict[str, str], dry_run: bool) -> None:
    name = action["name"]
    print(f"  {action['action']}: {name}")
    if dry_run or action["action"] == "unchanged":
        return
    body = {
        "name": name,
        "color": action["color"],
        "description": action["description"],
    }
    repo_path = f"repos/{quote(org, safe='')}/{quote(repo, safe='')}"
    if action["action"] == "create":
        gh_api("POST", f"{repo_path}/labels", body)
        return
    if action["action"] == "update":
        gh_api("PATCH", f"{repo_path}/labels/{quote(name, safe='')}", body)
        return
    raise RuntimeError(f"unknown action {action['action']}")


def sync(labels_file: str, org: str, dry_run: bool) -> None:
    desired = parse_labels(open(labels_file, encoding="utf-8").read())
    repos = list_repos(org)
    if not repos:
        fail(f"no non-archived repositories found in {org}")
    print(f"syncing {len(desired)} labels to {len(repos)} repositories in {org}")
    if dry_run:
        print("dry run: no labels will be created or updated")

    totals = {"create": 0, "update": 0, "unchanged": 0}
    failures: list[str] = []
    for repo in repos:
        print(f"{org}/{repo}")
        try:
            actions = plan(desired, list_labels(org, repo))
            for action in actions:
                apply_action(org, repo, action, dry_run)
                totals[action["action"]] += 1
        except Exception as error:  # noqa: BLE001 - report and continue
            failures.append(f"{org}/{repo}: {error}")
            print(f"  error: {error}", file=sys.stderr)

    print(
        "summary: "
        f"repositories={len(repos)} "
        f"create={totals['create']} "
        f"update={totals['update']} "
        f"unchanged={totals['unchanged']} "
        f"failed={len(failures)} "
        f"dry_run={str(dry_run).lower()}"
    )
    if failures:
        fail("label sync failed for: " + "; ".join(failures))


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: sync-labels.py <labels.yml>")
    token = os.environ.get("LABEL_SYNC_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not token.strip():
        fail(MISSING_TOKEN_MESSAGE)
    os.environ["GH_TOKEN"] = token
    dry_run = os.environ.get("DRY_RUN", "false").lower() in {"1", "true", "yes"}
    sync(sys.argv[1], ORG, dry_run)


if __name__ == "__main__":
    main()
