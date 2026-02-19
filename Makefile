VENV := .venv

# Détection du système d'exploitation
# Sur Windows natif, la variable OS est définie; sur WSL/Linux/macOS elle ne l'est pas
ifdef OS
    # Windows
    PIP := $(VENV)/Scripts/pip.exe
    PYTHON := $(VENV)/Scripts/python.exe
else
    # Unix-like (WSL, Linux, macOS)
    PIP := $(VENV)/bin/pip
    PYTHON := $(VENV)/bin/python
endif

.PHONY: help install clean clone

# Cible par défaut - afficher l'aide
help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║           devops-scripts - Cibles disponibles                  ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "── INSTALLATION ────────────────────────────────────────────────"
	@echo "  install    Créer venv et installer les dépendances"
	@echo "  clean      Supprimer venv et nettoyer"
	@echo ""
	@echo "── SCRIPTS DU REPO ─────────────────────────────────────────────"
	@echo "  clone      Cloner/mettre à jour tous les repos GitHub"
	@echo ""

install:
	@echo "Création du venv à $(VENV)..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✓ Venv créé et dépendances installées"

clone:
	$(PYTHON) github/clone-all-repos.py --output /mnt/c/dev/workspace/

clean:
	@echo "Suppression du venv $(VENV)..."
	@rm -rf $(VENV)
	@echo "✓ Nettoyage terminé"
