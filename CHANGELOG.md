# Changelog

Toutes les modifications notables par rapport à la branche `main` sont listées ici.

---

## [Unreleased] – migration XTTS v2

### Changements majeurs

- **Moteur TTS** : passage de **Chatterbox** (Resemble AI) à **XTTS v2** (Coqui).
  - Un seul modèle multilingue, chargé au démarrage.
  - Voix personnalisées via un fichier **reference.wav** par voix (clonage).
  - Pas de chunking manuel : XTTS gère le texte long en interne.
  - Temps de réponse en général plus courts pour des textes moyens/longs.

### API

- **Routes inchangées** : `GET /voices`, `POST /tts` avec corps `{"voice": "...", "text": "..."}`.
- **Paramètres de requête** : `mode` (file | path), `format` (wav | mp3) conservés.
- **Config voix** : seul `config.language` est utilisé par XTTS (défaut `"fr"`). Les anciens champs Chatterbox (`exaggeration`, `cfg_weight`, `temperature`, `max_chars`, `repetition_penalty`) ne sont plus lus.

### Dépendances

- **requirements.txt**
  - Remplacement de `chatterbox-tts` par **`coqui-tts`**.
  - Ajout de **`transformers>=4.33,<=4.46.2`** pour compatibilité avec coqui-tts (présence de `isin_mps_friendly`).
  - Conservation de : `fastapi`, `uvicorn`, `pydantic`, `soundfile`, `numpy`, `pydub`, `emoji`, `torch`, `torchaudio`.

### Code

- **app/tts.py**
  - Réécrit pour XTTS : chargement du modèle `tts_models/multilingual/multi-dataset/xtts_v2`, appel à `model.tts_to_file(...)` avec `speaker_wav` et `language`.
  - Suppression du chunking manuel, de la gestion des paramètres Chatterbox et du crossfade.
  - Nettoyage des imports et ajout de docstrings / typage.
- **app/main.py**
  - Titre de l’API : « Pixel TTS API (XTTS v2) ».
  - Import de `generate_tts_chunked` uniquement (plus `generate_tts`).
  - Suppression de l’import inutilisé `JSONResponse`, commentaires et logs superflus.
- **app/config.py** : ajout d’une docstring.
- **app/models.py** : docstring et commentaire sur `TTSRequest`.

### Voix

- **Structure conservée** : chaque voix reste un dossier `voices/<nom>/` avec **reference.wav** et **config.json**.
- **config.json** : format simplifié pour XTTS (`name`, `description`, `config.language`). Exemples mis à jour pour `narrateur` et `francis`.

### Documentation

- **README.md** : réécrit pour Pixel TTS et XTTS v2 (structure, installation, API, ajout de voix, bonnes pratiques). Suppression des références à Chatterbox et à une structure type « chatterbox-api ».
- **CHANGELOG.md** : ajout de ce fichier pour résumer les changements par rapport à `main`.

### Scripts / outillage

- **setup.bat** : inchangé (création venv, `pip install -r requirements.txt`, proposition PyTorch CUDA).
- **start.bat** : inchangé (activation venv, `uvicorn app.main:app --host 0.0.0.0 --port 8000`).
- **stop.bat** : inchangé (création de `stop.flag`).
- **test.bat** : exemple d’appel curl vers `/tts` (variable `VOICE` selon besoin).

---

## Référence branche main (avant migration)

- Moteur : **Chatterbox** (multilingue, clonage via `reference.wav`).
- Config voix : `exaggeration`, `cfg_weight`, `temperature`, `max_chars`, `repetition_penalty`, etc.
- Génération par chunks avec assemblage (silence / crossfade).
- Dépendance : `chatterbox-tts`.
