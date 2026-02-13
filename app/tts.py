import emoji
import torch
import re
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

def remove_emojis(text):
    return emoji.replace_emoji(text, replace='')

def split_text_hybrid(text, max_chars=200):
    import re
    parts = re.split(r'(?<=[\.\!\?\;\:])\s+', text)
    chunks = []
    current = ""

    for part in parts:
        if len(part) > max_chars:
            # fallback mot ou slice
            words = re.findall(r'\S+|\s+', part)  # capture tout, même si pas d'espace
            for w in words:
                if len(current) + len(w) <= max_chars:
                    current += w
                else:
                    if current:
                        chunks.append(current)
                    # si w trop long, couper directement
                    while len(w) > max_chars:
                        chunks.append(w[:max_chars])
                        w = w[max_chars:]
                    current = w
            continue

        if len(current) + len(part) <= max_chars:
            current += part
        else:
            if current:
                chunks.append(current)
            current = part

    if current:
        chunks.append(current)

    return chunks

def generate_tts(text, ref_wav, voice_cfg, voice_description, output_path):
    print("--------- BEGIN TTS GENERATION -----------")
    print("Voice : " + voice_description)
    print("Text : \n" + text + "\n")
    print("Using configuration")
    print(voice_cfg)

    exaggeration = voice_cfg.get("exaggeration", 0.5)
    cfg_weight   = voice_cfg.get("cfg_weight", 0.5)
    temperature  = voice_cfg.get("temperature", 0.8)

    audio = model.generate(
        remove_emojis(text),
        audio_prompt_path=ref_wav,
        language_id="fr",
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
        temperature=temperature
    )

    ta.save(output_path, audio, model.sr)
    print("---------- END TTS GENERATION ------------")

def generate_tts_chunked(text, ref_wav, voice_cfg, voice_description, output_path):
    print("--------- BEGIN TTS GENERATION -----------")
    print("Voice :", voice_description)

    text = remove_emojis(text)
    chunks = split_text_hybrid(text)

    print(f"{len(chunks)} chunks générés")

    exaggeration = voice_cfg.get("exaggeration", 0.5)
    cfg_weight   = voice_cfg.get("cfg_weight", 0.5)
    temperature  = voice_cfg.get("temperature", 0.8)

    audios = []

    for i, chunk in enumerate(chunks):
        print(f"→ Chunk {i+1}/{len(chunks)}")
        print(chunk)

        audio = model.generate(
            chunk,
            audio_prompt_path=ref_wav,
            language_id="fr",
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            temperature=temperature
        )

        audios.append(audio)

    # petite pause entre chunks (10 ms)
    silence = torch.zeros(
        (audios[0].shape[0], int(model.sr * 0.01)),
        device=audios[0].device
    )

    final_audio = []
    for a in audios:
        final_audio.append(a)
        final_audio.append(silence)

    final_audio = torch.cat(final_audio, dim=1)

    ta.save(output_path, final_audio, model.sr)
    print("---------- END TTS GENERATION ------------")