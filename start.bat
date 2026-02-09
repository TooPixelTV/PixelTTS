@echo off
REM Activer l'environnement virtuel
call .\venv\Scripts\activate.bat

REM Lancer le serveur Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

pause