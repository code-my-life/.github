#!/usr/bin/env python3
"""The « Conventions » job of code-my-life (ADR 0017 of hermes-software-factory), run on every pull request.

The branch reads « <prefix>/<issue number>-<subject> », the prefix is the one of the issue's type, the issue is complete,
and the pull request carries « <prefix>: <title> », « Fixes #<n> », the sections of its type and one proof line per
criterion of the issue. Branches of Dependabot and of the factory's reverts are let through. Standard library only: the
runner's Python is enough. Messages are in French, like the issues and pull requests they judge.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).absolute().parent
sys.path.insert(0, str(HERE))
import factory_types as ft  # noqa: E402


def api(path: str) -> dict | None:
    url = os.environ.get("GITHUB_API_URL", "https://api.github.com") + path
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def judge(pr: dict, repo: str, d: dict, fetch=api) -> tuple[list[str], str]:
    """(problems, what was checked) for a pull request payload; no problem means the conventions hold."""
    branch, title, body = pr["head"]["ref"], pr.get("title") or "", pr.get("body") or ""
    if ft.skipped_branch(branch, d):
        return [], f"branche « {branch} » hors convention (Dependabot ou revert de la factory) : rien à vérifier"
    parts = ft.branch_parts(branch)
    key = ft.type_of_prefix(parts[0], d) if parts else None
    if not parts or not key:
        return [ft.branch_problem(None, branch, None, d)], "branche"
    number = parts[1]
    issue = fetch(f"/repos/{repo}/issues/{number}")
    if not issue or issue.get("pull_request"):
        return [f"branche « {branch} » : l'issue #{number} n'existe pas dans {repo}"], "issue"
    labels = [label["name"] for label in issue.get("labels") or []]
    itype, why = ft.type_of_labels(labels, d)
    if why:
        return [f"issue #{number} : {why}"], "issue"
    if itype != key:
        t = d["types"][itype]
        expected = f"« {t['prefix']}/{number}-<sujet> »" if t.get("prefix") else "aucune branche"
        return [f"branche « {branch} » : l'issue #{number} est de type {t['name']}, sa branche s'écrit {expected}"], "issue"
    problems = [f"issue #{number} pas prête : {p}" for p in ft.issue_problems(key, issue.get("body") or "", d)]
    problems += ft.pr_problems(key, title, body, number, ft.issue_criteria(issue.get("body") or "", d), d)
    return problems, f"type {d['types'][key]['name']}, issue #{number}"


def main() -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr = event.get("pull_request")
    if not pr:
        print("Pas une pull request : rien à vérifier.")
        return 0
    d = ft.load(HERE / "types.json")
    problems, scope = judge(pr, os.environ["GITHUB_REPOSITORY"], d)
    lines = [f"### Conventions : {'conformes' if not problems else f'{len(problems)} écart(s)'}", "", f"Vérifié : {scope}."]
    lines += [f"- {p}" for p in problems]
    if not problems:
        lines.append("")
        lines.append("Branche, titre et texte de la PR suivent le type de l'issue.")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("\n".join(lines) + "\n")
    for p in problems:
        print(f"::error title=Conventions::{p}")
    print("\n".join(lines))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
