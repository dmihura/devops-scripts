#!/bin/bash

# Nom du fichier .env
ENV_FILE=".env"

# Vérifier si le fichier .env existe, sinon le créer avec un commentaire et une valeur par défaut
if [ ! -f "$ENV_FILE" ]; then
    echo "# Token à créer sur GitHub" > "$ENV_FILE"
    echo "GITHUB_TOKEN=to_be_defined" >> "$ENV_FILE"
fi

# Charger les variables d'environnement depuis le fichier .env
source "${ENV_FILE}"

# Vérifier si le token est défini
if [ "$GITHUB_TOKEN" == "to_be_defined" ]; then
    echo "Le token GitHub n'est pas défini dans le fichier .env. Veuillez le définir et réessayer."
    exit 1
fi

# Nom du repository (obligatoire)
REPO_NAME=""

# Fonction pour afficher l'usage
usage() {
    echo "Usage: $0 -r|--repository <repository_name>"
    echo "Options:"
    echo "  -r, --repository    Spécifie le nom du repository (obligatoire)"
    echo "  -h, --help          Affiche ce message d'aide"
}

# Analyser les options de ligne de commande
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -r|--repository) REPO_NAME="$2"; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Option inconnue: $1"; usage; exit 1 ;;
    esac
    shift
done

# Vérifier si le nom du repository est défini
if [ -z "$REPO_NAME" ]; then
    echo "Le nom du repository est obligatoire."
    usage
    exit 1
fi

# Construire la commande curl
curl_cmd="curl -L -s -X POST \
    -H \"Authorization: token $GITHUB_TOKEN\" \
    -H \"Accept: application/vnd.github+json\" \
    -d '{\"name\": \"$REPO_NAME\", \"private\": true}' \
    \"https://api.github.com/user/repos\""

# Exécuter la commande curl et capturer la réponse
response=$(eval $curl_cmd)

# Vérifier si la création a réussi
if echo "$response" | grep -q '"full_name"'; then
    ssh_url=$(echo "$response" | jq -r '.ssh_url')
    echo "Repository '$REPO_NAME' créé avec succès."
    echo "Pour cloner le repository, utilisez la commande suivante :"
    echo "git clone $ssh_url"
else
    echo "Erreur lors de la création du repository: $response"
    exit 1
fi