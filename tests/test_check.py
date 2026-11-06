"""The « Conventions » check of code-my-life (conventions/check.py): python3 -m unittest discover -s tests

Moved from hermes-software-factory (tests/test_factory_types.py, ConventionsJob, issue #50): the check is the code of
this repository, so its tests live here. Standard library only, like the check.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_check():
    spec = importlib.util.spec_from_file_location("conventions_check", ROOT / "conventions" / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


INTERFACE = """### Constat

Les badges de l'app ne suivent pas de standard commun.

### Impact

Rien ne distingue deux éléments d'un même type.

### Maquette

Validée : https://claude.ai/artifact/UwkFqQqtU42nyneQXREq7e

### Inventaire

- Agents : skills, toolsets, plugins.

### Règles chiffrées

20 px de haut, une seule ligne à 390 et 1440 px, thèmes clair et sombre.

### Attendu

Chaque élément est un badge à deux parties, teinté de sa couleur.

### Critères d'acceptation

- C1 : chaque ligne du tableau 1 est un badge à deux parties
- C2 : la largeur du badge égale celle de l'étiquette plus celle de la valeur

### Tests

- `apps/web/src/ui/badge/badges.test.tsx` : « chaque ligne du tableau 1 est un badge »

### Captures

_No response_

### Ne change pas

Les liens et les traductions.
"""

PR_BODY = """Fixes #11

## Ce qui a été fait
Le standard des badges.

## Critères
- C1 : badges.test.tsx, « chaque ligne du tableau 1 est un badge »
- C2 : e2e/captures.spec.ts, largeur mesurée à 1 px près

## Preuves
evidence/01-test-fails-on-base.txt

## Ce qui n'est pas prouvé
Rien.

## Version
mineure (0.2.0)

## Captures
e2e/captures.spec.ts-snapshots refaites.
"""


class ConventionsJob(unittest.TestCase):
    def setUp(self):
        self.check = load_check()
        self.d = self.check.ft.load(ROOT / "conventions" / "types.json")
        self.issue = {"number": 11, "body": INTERFACE, "labels": [{"name": "type:interface"}, {"name": "factory"}]}

    def judge(self, branch, title="interface: standard des badges", body=PR_BODY, issue=None):
        pr = {"head": {"ref": branch}, "title": title, "body": body}
        return self.check.judge(pr, "code-my-life/factory-live", self.d,
                                fetch=lambda path: issue if issue is not None else self.issue)

    def test_pr_conforme_a_son_issue(self):
        self.assertEqual(self.judge("interface/11-badges-standard")[0], [])

    def test_prefixe_qui_ne_suit_pas_le_type_de_l_issue(self):
        problems, _ = self.judge("feat/11-badges-standard", title="feat: standard des badges")
        self.assertIn("est de type Interface", problems[0])

    def test_issue_incomplete_refusee(self):
        issue = {**self.issue, "body": INTERFACE.replace("https://claude.ai/artifact/UwkFqQqtU42nyneQXREq7e", "à venir")}
        problems, _ = self.judge("interface/11-badges-standard", issue=issue)
        self.assertIn("issue #11 pas prête", problems[0])

    def test_dependabot_laisse_passer(self):
        self.assertEqual(self.judge("dependabot/npm_and_yarn/vite-8.1.0", title="Bump vite")[0], [])

    def test_branche_hors_convention(self):
        self.assertIn("attendu", self.judge("bugfix-issue-2")[0][0])


if __name__ == "__main__":
    unittest.main()
