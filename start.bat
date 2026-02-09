@echo off

cd /d "%~dp0"

REM Activer l'environnement virtuel
call .\venv\Scripts\activate.bat

REM Lancer le serveur Uvicorn
echo Starting Pixel TTS Server...
uvicorn app.main:app --host 0.0.0.0 --port 8000