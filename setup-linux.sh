#!/bin/bash

# -----------------------------
# Script de setup
# -----------------------------

echo "Vérification de Python..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null
then
    echo "Python n'est pas installé. Veuillez l'installer et relancer le script."
    exit 1
fi

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
else
    echo "Environnement virtuel existe déjà."
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre pip à jour
echo "Mise à jour de pip..."
python -m pip install --upgrade pip

# Installer les dépendances
if [ -f "requirements.txt" ]; then
    echo "Installation des packages depuis requirements.txt..."
    pip install -r requirements.txt
else
    echo "Fichier requirements.txt introuvable."
fi

# Installer PyTorch CUDA 11.8
echo "Installation de PyTorch (CUDA 11.8)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

echo "Setup terminé."
