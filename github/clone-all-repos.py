#!/usr/bin/env python3
"""
Script pour cloner ou mettre à jour tous les dépôts GitHub visibles par un jeton
dans un répertoire de sortie.

Utilisation:
    python clone_all_repos.py --token <TOKEN> --output ../output

Le script recherche le jeton dans la variable d'environnement `GITHUB_TOKEN`
si `--token` n'est pas fourni. Le répertoire de sortie par défaut est `output`
dans le même répertoire que ce script.

Les variables d'environnement sont chargées depuis le fichier `.env` situé
dans le répertoire du script.

Pré-requis:
    pip install requests python-dotenv

Comportement important:
    - Si un dépôt existe déjà localement, le script NE le reclone PAS ;
        il exécute `git fetch --all --prune` pour le mettre à jour.
"""

from __future__ import annotations

import argparse
import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional

try:
    import requests
except Exception:
    print("Dépendance manquante 'requests'. Installez avec : pip install requests", file=sys.stderr)
    raise

try:
    from dotenv import load_dotenv
except Exception:
    print("Dépendance manquante 'python-dotenv'. Installez avec : pip install python-dotenv", file=sys.stderr)
    raise


API_URL = "https://api.github.com"


def iter_repos(token: str) -> List[dict]:
    """Récupère la liste complète des dépôts visibles pour l'utilisateur authentifié.

    Le résultat est paginé par l'API GitHub ; cette fonction suit les en-têtes
    `Link` pour itérer sur toutes les pages et retourne la liste complète.
    """
    # Préparer les en-têtes d'authentification pour l'API GitHub
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    repos = []
    # Demander 100 dépôts par page et inclure tous les types accessibles
    url = f"{API_URL}/user/repos?per_page=100&type=all"

    # Parcourir toutes les pages tant que l'API renvoie un lien "next"
    while url:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        repos.extend(resp.json())
        # Gérer la pagination via l'en-tête Link
        link = resp.headers.get("Link")
        url = None
        if link:
            parts = link.split(",")
            for part in parts:
                if 'rel="next"' in part:
                    url = part[part.find("<") + 1:part.find(">")]
                    break

    return repos


def run_git(args: List[str], cwd: Optional[Path] = None) -> int:
    """Exécute une commande `git`.
    
    Note: Avec les URLs SSH, l'authentification se fait via la clé SSH,
    pas via un token bearer.
    """
    cmd = ["git"] + args
    return subprocess.run(cmd, cwd=cwd).returncode


def clone_repo(ssh_url: str, path: Path) -> None:
    # S'assurer que le répertoire parent existe
    path_parent = path.parent
    path_parent.mkdir(parents=True, exist_ok=True)
    print(f"Clonage de {ssh_url} -> {path}")
    # Cloner le dépôt dans le chemin local spécifié
    rc = run_git(["clone", ssh_url, str(path)])
    if rc != 0:
        raise RuntimeError(f"Échec du clonage pour {ssh_url}")


def update_repo(path: Path) -> None:
    # Mettre à jour un dépôt existant en récupérant toutes les branches et en
    # supprimant les refs supprimées à distance (prune)
    print(f"Mise à jour de {path}")
    rc = run_git(["-C", str(path), "fetch", "--all", "--prune"])
    if rc != 0:
        raise RuntimeError(f"Échec de la mise à jour dans {path}")


def main(argv: Optional[List[str]] = None) -> int:
    # Charger les variables d'environnement depuis le fichier .env
    script_dir = Path(__file__).resolve().parent
    env_file = script_dir / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    parser = argparse.ArgumentParser(description="Cloner ou mettre à jour tous les repos GitHub visibles par un jeton")
    parser.add_argument("--token", help="Jeton GitHub (remplace la variable d'environnement GITHUB_TOKEN)")
    parser.add_argument("--output", default=None, help="Répertoire de sortie pour les clones (par défaut: ./output)")
    args = parser.parse_args(argv)

    # Récupérer le token depuis l'argument ou la variable d'environnement
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Erreur : Jeton GitHub requis via --token ou variable d'environnement GITHUB_TOKEN", file=sys.stderr)
        return 2

    # Calculer et préparer le répertoire de sortie
    output_dir = Path(args.output) if args.output else script_dir / "output"
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Répertoire de sortie utilisé : {output_dir}")

    # Interroger l'API pour récupérer la liste des dépôts
    try:
        repos = iter_repos(token)
    except Exception as e:
        print(f"Échec de la récupération des dépôts : {e}", file=sys.stderr)
        return 3

    if not repos:
        print("Aucun dépôt trouvé ou le jeton n'a pas d'accès.")
        return 0

    # Parcourir chaque dépôt et cloner ou mettre à jour selon l'existence locale
    cloned_count = 0
    updated_count = 0
    error_count = 0

    for r in repos:
        owner = r.get("owner", {}).get("login") or r.get("full_name", "unknown").split("/")[0]
        name = r.get("name")
        # Utiliser l'URL SSH au lieu de l'URL HTTPS
        ssh_url = r.get("ssh_url")
        if not name or not ssh_url:
            # Ignorer les entrées malformées
            continue

        local_path = output_dir / owner / name

        try:
            if local_path.exists() and (local_path / ".git").exists():
                # Si le dépôt existe déjà, on l'actualise
                update_repo(local_path)
                updated_count += 1
            else:
                # Sinon on le clone depuis l'URL SSH
                clone_repo(ssh_url, local_path)
                cloned_count += 1
        except Exception as e:
            error_count += 1
            print(f"Erreur lors du traitement de {owner}/{name}: {e}", file=sys.stderr)

    # Synthèse
    print("")
    print("=== Synthèse ===")
    print(f"Repos mis à jour (fetch): {updated_count}")
    print(f"Repos clonés        : {cloned_count}")
    print(f"Repos en erreur     : {error_count}")
    print("")
    print("Terminé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
