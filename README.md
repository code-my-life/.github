# code-my-life/.github

Les fichiers communs aux dépôts de l'organisation code-my-life. GitHub les applique à tout dépôt qui n'a pas les siens.

## Ce que contient ce dépôt

- **Modèles d'issues** (`.github/ISSUE_TEMPLATE/`) : un formulaire par type. Bug, Interface, Fonctionnalité,
  Diagnostic, Tests, Maintenance, Documentation. Chaque formulaire pose le label `type:…` de son type.
- **Modèle de pull request** (`.github/pull_request_template.md`) : les sections attendues, dont une ligne de preuve par
  critère de l'issue.
- **Conventions** (`.github/workflows/conventions.yml`, `conventions/`) : un workflow réutilisable qui vérifie qu'une
  pull request suit le type de son issue. Chaque dépôt l'appelle depuis son propre workflow `Conventions`.
- **Modèles de workflows** (`workflow-templates/`) : la CI des dépôts publics, réutilisable depuis l'onglet Actions,
  « New workflow ».
- **Sécurité** (`SECURITY.md`) : comment signaler une faille sans issue publique.

## Les types

| Type | Branche | Titre de PR | Ce qui prouve que c'est fait |
|---|---|---|---|
| Bug | `fix/<n°>-<sujet>` | `fix: …` | un test rouge avant la correction, vert après |
| Interface | `interface/<n°>-<sujet>` | `interface: …` | idem, plus les captures de référence refaites |
| Fonctionnalité | `feat/<n°>-<sujet>` | `feat: …` | un test rouge avant, vert après |
| Diagnostic | aucune | aucune PR | la cause trouvée et un test qui reproduit le problème |
| Tests | `test/<n°>-<sujet>` | `test: …` | les sabotages de l'auteur rejoués : chaque test attrape le sien |
| Maintenance | `chore/<n°>-<sujet>` | `chore: …` | aucun test existant modifié ni retiré, suite verte |
| Documentation | `docs/<n°>-<sujet>` | `docs: …` | seuls des documents changent |

Le type vient de l'issue. La branche, le titre, le texte de la PR et les contrôles en découlent. Une issue incomplète
reçoit le label `à cadrer` et ne part pas en fabrication.

## Modifier ces fichiers

Les modèles d'issues, le modèle de PR et `conventions/types.json` et `conventions/factory_types.py` sont générés depuis
la définition des types de la software factory (hermes-software-factory, `config/types.yaml`). Ils se modifient
là-bas, puis sont régénérés ici. Les autres fichiers s'éditent directement.
