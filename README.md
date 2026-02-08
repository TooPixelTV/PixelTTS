# Chatterbox TTS API

Projet : API TTS asynchrone pour générer des voix de personnages avec styles/emotions
Basé sur Chatterbox (Open-source)

## Structure du projet

chatterbox-api/
├─ app/
│ ├─ main.py : API FastAPI (async interne)
│ ├─ tts.py : Wrapper Chatterbox + styles
│ ├─ audio_fx.py : Post-processing audio
│ ├─ models.py : Schémas Pydantic pour l'API
│ └─ config.py : Constantes et chemins
├─ voices/ : dossiers par voix
│ ├─ pirate/
│ │ ├─ reference.wav
│ │ └─ config.json (styles)
│ ├─ mage/
│ │ ├─ reference.wav
│ │ └─ config.json
├─ output/ : fichiers WAV générés
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.txt : ce fichier

## Installation

## Option 1 : Python + venv

1. Dézippez le projet
   unzip chatterbox-api.zip
   cd chatterbox-api

2. Créez un environnement virtuel
   python3 -m venv venv
   source venv/bin/activate # Windows: venv\Scripts\activate

3. Installez les dépendances
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

4. Installez Chatterbox
   git clone https://github.com/resemble-ai/chatterbox.git
   pip install chatterbox-tts

5. Lancez le serveur
   uvicorn app.main:app --host 0.0.0.0 --port 8000

## Option 2 : Docker (recommandé)

1. Construisez l'image
   docker compose build

2. Lancez le container
   docker compose up

Le serveur sera accessible sur http://localhost:8000

## Utilisation de l'API

1. Lister les voix disponibles
   curl http://localhost:8000/voices

2. Générer un fichier WAV
   curl -X POST http://localhost:8000/tts \
    -H "Content-Type: application/json" \
    -d '{
   "voice": "pirate",
   "style": "angry",
   "text": "À L’ABORDAGE !!!"
   }' --output pirate.wav

- Le fichier WAV est généré dans le dossier output/
- Les styles et émotions sont définis dans config.json de chaque voix

## Ajout d'une nouvelle voix

1. Créez un dossier sous voices/nom_voix/
2. Ajoutez :
   - reference.wav : fichier audio de référence
   - config.json : définition des styles et style par défaut

Exemple de style dans config.json :

{
"name": "pirate",
"description": "Vieux pirate bourru",
"styles": {
"normal": {"gain_db": 2, "pitch": -1},
"angry": {"gain_db": 6, "pitch": -3, "distortion": 0.4}
},
"default_style": "normal"
}

## Intégration avec Twitch / Bot

- Envoyez un POST vers /tts avec "voice", "style" et "text"
- Récupérez le WAV renvoyé directement
- Jouez-le via OBS, VLC ou soundboard
- Aucun polling nécessaire : le serveur renvoie le WAV quand prêt
- Le sémaphore interne gère 1 génération à la fois pour éviter les blocages GPU

## Bonnes pratiques

- Nettoyer régulièrement le dossier output/ pour éviter d'accumuler les WAV
- Précharger le serveur au lancement pour réduire la latence
- Ajouter de nouveaux styles directement dans config.json pour multiplier les émotions sans recloner la voix

## Avantages Docker

- Reproductibilité (même setup sur n'importe quelle machine)
- Isolation des dépendances et du GPU
- Redémarrage rapide
- Facile à scaler si plusieurs bots / streamers
