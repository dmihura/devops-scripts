#!/bin/bash

# Remplacez par le nom de l'organisation
ORG_NAME="dmihura"

# Remplacez par votre token d'accès personnel GitHub
GITHUB_TOKEN="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"

# création d'un répertoire workspace par organisation
mkdir -p "workspace/${ORG_NAME}"
cd "workspace/${ORG_NAME}"

# Fonction pour cloner les repositories
clone_repos() {
    page=1
    while :; do
        response=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                       "https://api.github.com/user/repos?per_page=100&page=$page")

        # Si la réponse est vide, on arrête la boucle
        [ "$(echo "${response}" | jq '. | length')" -eq 0 ] && break

        # Cloner les dépôts
        for repo in $(echo "$response" | jq -r '.[].ssh_url'); do
            git clone "${repo}"
        done

        # Passer à la page suivante
        page=$((page + 1))
    done
}

# Appeler la fonction
clone_repos
