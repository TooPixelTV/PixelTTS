"""Chemins du projet : voix (reference.wav + config.json) et sortie audio."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
VOICES_DIR = BASE_DIR / "voices"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)