import asyncio
import json
import os
import signal
import time
from pathlib import Path
from enum import Enum

import soundfile as sf
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydub import AudioSegment

from app.config import OUTPUT_DIR, VOICES_DIR
from app.models import TTSRequest
from app.tts import generate_tts_chunked

"""API FastAPI pour la synthèse vocale (XTTS v2, voix personnalisées)."""
STOP_FILE = "stop.flag"

app = FastAPI(title="Pixel TTS API (XTTS v2)")

# Une seule génération à la fois (évite saturation GPU / mémoire).
tts_lock = asyncio.Semaphore(1)

@app.on_event("startup")
async def on_startup():
    # Lance la surveillance du stop.flag
    asyncio.create_task(watch_stop_flag())

async def watch_stop_flag():
    while True:
        if os.path.exists(STOP_FILE):
            print("Stop flag detected, shutting down server...", flush=True)
            os.remove(STOP_FILE)

            os.kill(os.getpid(), signal.SIGINT)

        await asyncio.sleep(0.5)

def generate_tts_file(req: TTSRequest):
    """Charge la config de la voix et prépare le chemin de sortie. Lève 404 si voix inconnue."""
    voice_dir = VOICES_DIR / req.voice
    if not voice_dir.exists():
        raise HTTPException(404, "Voice not found")

    with open(voice_dir / "config.json") as f:
        cfg = json.load(f)

    voice_config = cfg.get("config", {})
    voice_description = cfg.get("description", "Not found")

    output = OUTPUT_DIR / f"{round(time.time())}_{req.voice}.wav"

    return voice_dir, voice_config, voice_description, output

async def run_tts(req: TTSRequest) -> Path:
    voice_dir, voice_config, voice_description, output = generate_tts_file(req)

    async with tts_lock:
        await asyncio.to_thread(
            generate_tts_chunked,
            req.text,
            str(voice_dir / "reference.wav"),
            voice_config,
            voice_description,
            str(output)
        )

    return output

def get_wav_duration(path: Path) -> float:
    data, samplerate = sf.read(str(path))
    return len(data) / samplerate

@app.get("/voices")
def list_voices():
    result = []
    for d in VOICES_DIR.iterdir():
        cfg = d / "config.json"
        if d.is_dir() and cfg.exists():
            with open(cfg) as f:
                result.append(json.load(f))
    return result

class TTSMode(str, Enum):
    file = "file"
    path = "path"

class TTSFormat(str, Enum):
    wav = "wav"
    mp3 = "mp3"

@app.post("/tts")
async def tts_endpoint(
    req: TTSRequest,
    mode: TTSMode = Query(TTSMode.file),
    format: TTSFormat = Query(TTSFormat.wav)
):
    output_wav = await run_tts(req)

    final_output = output_wav

    if format == TTSFormat.mp3:
        mp3_path = output_wav.with_suffix(".mp3")
        AudioSegment.from_wav(str(output_wav)).export(str(mp3_path), format="mp3")
        final_output = mp3_path

    duration = get_wav_duration(output_wav)

    if mode == TTSMode.path:
        return {
            "success": True,
            "path": final_output.as_posix(),
            "filename": final_output.name,
            "duration": duration
        }

    return FileResponse(final_output, media_type=f"audio/{format.value}")