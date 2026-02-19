# Pixel TTS

API de synthèse vocale (TTS) avec **voix personnalisées** (clonage à partir d’un fichier audio). Basée sur **XTTS v2** (Coqui) : rapide, multilingue, un seul modèle pour toutes les voix.

## Prérequis

- **Python 3.12** (seule version testée)
- **GPU NVIDIA** recommandé (CUDA) pour des temps de réponse corrects
- Optionnel : PyTorch avec CUDA (`cu118` ou `cu121` selon ta carte)

## Structure du projet

```
PixelTTS/
├── app/
│   ├── main.py      # API FastAPI (routes /tts, /voices)
│   ├── tts.py       # Chargement XTTS v2 + génération
│   ├── config.py    # Chemins (voices/, output/)
│   └── models.py    # Schéma TTSRequest
├── voices/          # Une voix = un dossier
│   ├── narrateur/
│   │   ├── reference.wav   # Extrait vocal de référence (~6 s idéal)
│   │   └── config.json     # name, description, config.language
│   └── francis/
│       ├── reference.wav
│       └── config.json
├── output/          # Fichiers WAV générés (nommés par timestamp_voix.wav)
├── requirements.txt
├── setup.bat        # Création venv + installation des deps
├── start.bat        # Démarrage du serveur (port 8000)
├── stop.bat         # Création de stop.flag pour arrêt propre
└── test.bat         # Exemple d’appel curl vers /tts
```

## Installation

1. **Cloner ou dézipper** le projet, puis à la racine :

2. **Environnement virtuel et dépendances** (Windows) :
   ```bat
   setup.bat
   ```
   Ou à la main :
   ```bat
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
   Pour une **GPU NVIDIA**, installe PyTorch avec CUDA après :
   ```bat
   pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

3. **Premier lancement** : au premier appel TTS, le modèle XTTS v2 est téléchargé automatiquement (plusieurs centaines de Mo).

## Démarrer le serveur

```bat
start.bat
```

Le serveur écoute sur **http://0.0.0.0:8000**. Pour l’arrêter proprement : lancer `stop.bat` ou laisser le processus écouter le fichier `stop.flag`.

## Utilisation de l’API

### Lister les voix

```bash
curl http://localhost:8000/voices
```

Réponse : liste des voix avec `name`, `description`, `config` (dont `language`).

### Générer un WAV

```bash
curl -X POST http://localhost:8000/tts \
  -H "Content-Type: application/json" \
  -d "{\"voice\": \"narrateur\", \"text\": \"Votre texte ici.\"}" \
  --output sortie.wav
```

**Paramètres de requête (query)** :

| Paramètre | Valeurs      | Défaut | Description                          |
|----------|--------------|--------|--------------------------------------|
| `mode`   | `file`, `path` | `file` | `file` = retourne le fichier audio ; `path` = retourne JSON avec chemin et durée |
| `format` | `wav`, `mp3` | `wav`  | Format de sortie (WAV ou MP3)        |

Exemple avec MP3 et mode path :

```bash
curl -X POST "http://localhost:8000/tts?format=mp3&mode=path" \
  -H "Content-Type: application/json" \
  -d "{\"voice\": \"francis\", \"text\": \"Bonjour.\"}"
```

## Ajouter une nouvelle voix

1. Créer un dossier sous `voices/` (ex. `voices/ma_voix/`).
2. Y mettre :
   - **reference.wav** : extrait audio de la voix cible (idéalement ~6 s, propre, une seule personne).
   - **config.json** :
     ```json
     {
       "name": "ma_voix",
       "description": "Courte description",
       "config": {
         "language": "fr"
       }
     }
     ```
3. Redémarrer le serveur n’est pas nécessaire : les voix sont lues à chaque requête depuis le disque.

Langues supportées par XTTS v2 (ex. dans `config.language`) : `fr`, `en`, `es`, `de`, `it`, `pt`, `pl`, `tr`, `ru`, `nl`, `cs`, `ar`, `zh-cn`, `ja`, `hu`, `ko`, `hi`.

## Bonnes pratiques

- **reference.wav** : 16–24 kHz, mono ou stéréo, sans bruit excessif ; ~6 s suffisent pour un bon clonage.
- Nettoyer régulièrement le dossier **output/** pour éviter d’accumuler des fichiers.
- Une seule requête TTS à la fois (sémaphore côté serveur) pour rester stable sur GPU.

## Licence / crédits

- **XTTS v2** : [Coqui TTS](https://github.com/coqui-ai/TTS) (Mozilla Public License 2.0).
- **Pixel TTS** : structure et API du projet.
