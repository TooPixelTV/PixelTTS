import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from app.audio_fx import apply_fx

model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")

def generate_tts(text, ref_wav, voice_cfg, voice_description, output_path):
    print("--------- BEGIN TTS GENERATION -----------")
    print("Voice : " + voice_description)
    print("Text : \n" + text + "\n")
    print("Using configuration")
    print(voice_cfg)
    print("---------- END TTS GENERATION ------------")

    exaggeration = voice_cfg.get("exaggeration", 0.5)
    cfg_weight   = voice_cfg.get("cfg_weight", 0.5)
    temperature  = voice_cfg.get("temperature", 0.8)

    audio = model.generate(
        text,
        audio_prompt_path=ref_wav,
        language_id="fr",
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
        temperature=temperature
    )

    ta.save(output_path, audio, model.sr)