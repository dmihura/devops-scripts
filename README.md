# devops-scripts

Scriptes utilitaires pour opérations DevOps.

## clone-all-repos

Un script Python pour cloner (ou mettre à jour) tous les dépôts GitHub visibles par un jeton.

### Pré-requis système

Avant d'utiliser ce repository, assurez-vous que les outils suivants sont installés :

- **Python 3.8+** : interpréteur Python
- **python3-venv** : module pour créer les environnements virtuels (WSL/Linux)
- **make** : gestionnaire de tâches (optionnel, mais recommandé)
- **git** : contrôle de version

#### Installation sur WSL/Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-venv git make
```

#### Installation sur macOS

```bash
brew install python3 git make
```

#### Installation sur Windows

- Python 3.8+ : [python.org](https://www.python.org/downloads/)
- Git : [git-scm.com](https://git-scm.com/)
- Make : via Chocolatey (`choco install make`) ou via WSL

### Pré-requis Python

- `requests>=2.28.0` (installé automatiquement avec `make install`)
- `python-dotenv>=0.19.0` (installé automatiquement avec `make install`)

## Configuration

### Token GitHub

Le script `clone-all-repos.py` a besoin d'un **token GitHub** pour accéder à vos dépôts.

1. **Créer un token sur GitHub** :
   - Aller sur [https://github.com/settings/tokens](https://github.com/settings/tokens)
   - Cliquer sur **"Generate new token"** (ou "Generate new token (classic)" pour plus de contrôle)
   - Donner un nom descriptif (ex: `devops-scripts`)
   - Sélectionner les scopes :
     - ✅ **repo** (accès complet aux dépôts privés et publics)
     - ✅ **read:org** (optionnel, pour les dépôts des organisations)
   - Générer le token et le **copier**

2. **Configurer le token localement** :
   - Copier le fichier [`.env.exemple`](github/.env.exemple) vers `.env` :
     ```bash
     cp github/.env.exemple github/.env
     ```
   - Éditer `github/.env` et remplacer `votre_token_ici` par votre token réel :
     ```env
     GITHUB_TOKEN=ghp_xxxxx...
     ```
   - ⚠️ **Important** : Le fichier `.env` est dans `.gitignore` et ne doit **jamais** être versionné

Usage:



```bash
# depuis le répertoire devops-scripts/github
python github/clone-all-repos.py --token $GITHUB_TOKEN --output ./github/output

# ou définir la variable d'environnement
export GITHUB_TOKEN=ghp_xxx
python github/clone-all-repos.py --output ./github/output
```

Comportement:
- Le script récupère la liste des repositories accessibles par le token.
- Il clone chaque repository dans le répertoire `output` (paramétrable).
- Si le dépôt existe déjà, il n'est pas recloné : le script lance un `git fetch --all --prune` pour le tenir à jour.

Sécurité:
- Le token peut être transmis via `--token` ou via la variable d'environnement `GITHUB_TOKEN`.
- Le script utilise `git -c http.extraHeader=...` pour transmettre le token au besoin sans l'enregistrer dans la config.
