import numpy as np

def apply_fx(audio, sr, fx):
    audio = audio.copy()

    if "gain_db" in fx:
        gain = 10 ** (fx["gain_db"] / 20)
        audio *= gain

    if "distortion" in fx:
        audio = np.tanh(audio * (1 + fx["distortion"] * 10))

    # pitch / speed volontairement simples
    # (safe CPU, stable stream)

    return audio