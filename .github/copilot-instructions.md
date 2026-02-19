# Instructions Copilot pour devops-scripts

## Vue d'ensemble

Ce repository contient des **scripts utilitaires généralistes en Python et Bash** pour
les opérations DevOps. Toutes les contributions doivent suivre les conventions et bonnes
pratiques définies ci-dessous.

## Directives pour la génération de code

### 1. Complaisance Linter (OBLIGATOIRE)

Tout code généré **DOIT être conforme** aux linters standards des langages utilisés :

#### Python
- **PEP 8** (style code)
- **pylint** : pas d'erreurs critiques
- **flake8** : pas de violations
- **black** : formatage cohérent (si configuration présente)
- Docstrings en français (selon contexte du repo)
- Type hints quand applicable (`typing` module)

Exemple:
```bash
make install
pylint github/mon_script.py
flake8 github/mon_script.py
```

#### Bash
- **shellcheck** : pas d'avertissements (SC warnings)
- Utiliser `set -euo pipefail` en début de script
- Indentation cohérente (2 ou 4 espaces)
- Documenter les entrées/sorties principales

Exemple:
```bash
shellcheck scripts/mon_script.sh
```

### 2. Structure du code

- **Modularité** : séparation claire des fonctions/responsabilités
- **Commentaires** : au minimum en français pour les sections clés
- **Gestion d'erreurs** : toujours prévoir les cas d'échec (try/except, exit codes)
- **Logs/Output** : messages clairs pour l'utilisateur final
- **Variables d'environnement** : documenter celles requises ou optionnelles

### 3. Format et conventions

- **Noms de fichiers** : snake_case pour Python/Bash (ex: `clone_all_repos.py`)
- **Répertoire** : 
  - Scripts Python → `github/` ou `scripts/` selon contexte
  - Scripts Bash → `scripts/`
- **Exécutabilité** : ajouter le shebang (`#!/usr/bin/env python3` ou `#!/bin/bash`)
- **README** : documenter chaque nouvelle commande (voir section 4)

### 4. Mise à jour du README (OBLIGATOIRE)

Pour chaque nouveau script généré :

1. **Ajouter une section** dans `README.md` avec :
   - Nom et description du script
   - Usage (commandes d'appel)
   - Pré-requis (dépendances)
   - Exemple exécution

2. **Conformité Markdown** : le `README.md` **DOIT être conforme** avec `markdownlint`
   - Pas d'erreurs de formatage Markdown
   - Indentation cohérente
   - En-têtes et listes correctement structurées
   
   Exemple:
   ```bash
   markdownlint README.md
   ```

3. **Mettre à jour** le fichier `requirements.txt` si nouvelles dépendances Python ajoutées

4. **Mettre à jour** le `Makefile` si nouvelle cible/tâche pertinente

Exemple de section README:
```markdown
### mon_script

Description courte de ce que fait le script.

**Pré-requis**: `requests>=2.28.0`

**Usage**:
\`\`\`bash
python github/mon_script.py --help
\`\`\`

**Exemple**:
\`\`\`bash
python github/mon_script.py --param valeur
\`\`\`
```

## Checklist avant de soumettre

- [ ] Code généré conforme PEP 8 / Bash standards
- [ ] `pylint` / `shellcheck` passent sans erreurs critiques
- [ ] Docstrings/commentaires en français
- [ ] Gestion d'erreurs robuste (try/except, exit codes)
- [ ] README.md mis à jour avec nouvelle section
- [ ] README.md conforme `markdownlint` (pas d'erreurs de formatage)
- [ ] `requirements.txt` et `Makefile` mis à jour si nécessaire
- [ ] Aucune information sensible (tokens, passwords) dans le code
- [ ] Tests locaux exécutés avec succès

## Ressources

- [PEP 8 – Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [ShellCheck – Shell script analysis tool](https://www.shellcheck.net/)
- [Pylint Documentation](https://www.pylint.org/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
