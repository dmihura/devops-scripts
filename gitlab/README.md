# Devops tool box

![Licence Status](https://img.shields.io/badge/licence-gpl-blue)
![Author](https://img.shields.io/badge/Author-dmihura-orange)
![Git](https://img.shields.io/badge/language-git-red)
![GitLab](https://img.shields.io/badge/language-gitlab-red)
![Shell](https://img.shields.io/badge/language-shell-red)

Ce repository contient une collection de scripts utilitaires pour faciliter diverses tâches de développement et de
gestion de projets. Ces scripts sont destinés à être utilisés par toute nouvelle personne entrant sur le projet.

## Scripts Disponibles

### clone-all-gits

Ce script permet de cloner tous les repositories GitLab associés à un projet spécifique. Il est particulièrement utile
pour les nouveaux membres de l'équipe qui ont besoin de récupérer rapidement tous les repositories nécessaires.

#### Prérequis

- `curl`
- `jq`
- `git`

#### Configuration

Avant d'exécuter le script, vous devez configurer un fichier `.env` avec les informations suivantes (si ce fichier est
absent, il est généré automatiquement) :

```plaintext
# URL du GitLab
GITLAB_URL="https://mongitlab.com/gitlab/api/v4"

# Répertoire où cloner les repositories (chemin en style Linux)
OUTPUT_DIRECTORY="."

# Créer un token avec le scope "api" au minimum (cf. : https://docs.gitlab.com/user/profile/personal_access_tokens/#create-a-personal-access-token)
PRIVATE_TOKEN="<token>"

# Credentials sous la forme username:password. Indispensable dans le cas GitLab production line.
CREDENTIALS="username:password"
