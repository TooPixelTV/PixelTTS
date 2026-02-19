"""
Module TTS : chargement du modèle XTTS v2 et génération audio.
Une seule génération à la fois (géré par le sémaphore dans main).
"""
import emoji

import torch
from TTS.api import TTS

# Modèle multilingue avec clonage de voix (référence WAV). Chargé au démarrage.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(DEVICE)


def remove_emojis(text: str) -> str:
    """Retire les emojis du texte pour éviter les artefacts XTTS."""
    return emoji.replace_emoji(text, replace="")


def generate_tts_chunked(
    text: str,
    ref_wav: str,
    voice_cfg: dict,
    voice_description: str,
    output_path: str,
) -> None:
    """
    Génère un fichier audio avec XTTS v2 à partir du texte et d'une voix de référence.
    XTTS découpe le texte en phrases en interne ; pas de chunking manuel.
    """
    print("--------- BEGIN TTS (XTTS v2) -----------")
    print("Voice:", voice_description)

    text = remove_emojis(text).strip()
    if not text:
        raise ValueError("Text is empty after cleanup")

    language = voice_cfg.get("language", "fr")

    model.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=ref_wav,
        language=language,
    )

    print("---------- END TTS ------------")
