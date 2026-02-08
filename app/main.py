from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Query
from pathlib import Path
import json
import asyncio
import time
import soundfile as sf
from enum import Enum
from pydub import AudioSegment

from app.config import VOICES_DIR, OUTPUT_DIR
from app.models import TTSRequest
from app.tts import generate_tts

app = FastAPI(title="Chatterbox Async TTS API")

# Sémaphore : 1 génération à la fois (GPU safe)
tts_lock = asyncio.Semaphore(1)


def generate_tts_file(req: TTSRequest) -> Path:
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
            generate_tts,
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
    output_wav = await run_tts(req)  # génère toujours un WAV

    final_output = output_wav

    if format == TTSFormat.mp3:
        mp3_path = output_wav.with_suffix(".mp3")
        audio = AudioSegment.from_wav(str(output_wav))
        audio.export(str(mp3_path), format="mp3")
        final_output = mp3_path
        # Optionnel : supprimer le WAV original
        # output_wav.unlink()

    duration = get_wav_duration(output_wav)  # toujours en WAV pour précision

    if mode == TTSMode.path:
        return {
            "success": True,
            "path": final_output.as_posix(),
            "filename": final_output.name,
            "duration": duration
        }

    return FileResponse(final_output, media_type=f"audio/{format.value}")