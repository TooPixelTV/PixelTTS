@echo off
REM -----------------------------
REM Script de setup
REM -----------------------------

REM Vérifier si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installe. Veuillez l'installer et relancer le script.
    pause
    exit /b
)

REM Créer l'environnement virtuel s'il n'existe pas
IF NOT EXIST "venv" (
    echo Creation de l'environnement virtuel...
    python -m venv venv
) ELSE (
    echo Environnement virtuel existe deja.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre pip a jour
echo Mise a jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
IF EXIST "requirements.txt" (
    echo Installation des packages depuis requirements.txt...
    pip install -r requirements.txt --use-deprecated=legacy-resolver
) ELSE (
    echo Fichier requirements.txt introuvable.
)

REM Installer PyTorch (CUDA 11.8)
echo Installation de PyTorch...
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118

pause