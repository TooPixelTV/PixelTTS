#!/bin/bash
PORT=${1:-8000}

# Aller dans le dossier du script
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Lancer le serveur Uvicorn
echo "Starting Pixel TTS Server..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
