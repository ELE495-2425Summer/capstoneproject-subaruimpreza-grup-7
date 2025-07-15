# texttospeech.py
import requests
import tempfile
import subprocess
import os
from pydub import AudioSegment  # pip install pydub

ELEVEN_API_KEY = "sk_de5bbadcf2b337f584e37826873fa652e46307f1b129f4b5"
VOICE_ID        = "PVbzZmwmdI99VcmuRK7G"
MODEL_ID        = "eleven_multilingual_v2"

# Oynatma öncesi MP3 dosyasının başına eklenecek sessizlik süresi (ms)
PRE_SILENCE_MS = 100
# mpg123 için varsayılan gain (scale factor)
DEFAULT_SCALE  = 131072  # ~+12 dB

def metni_sese_cevir_ve_oynat(metin: str, scale: int = DEFAULT_SCALE):
    """
    metin: oynatılacak metin
    scale: mpg123 için çarpan; default DEFAULT_SCALE (~+12 dB)
    """
    # 1) ElevenLabs API’den MP3 al
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    data = {
        "text": metin,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code != 200:
        raise RuntimeError(f"TTS hatası: {resp.status_code} – {resp.text}")

    # 2) Geçici MP3 dosyasına yaz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tf:
        tf.write(resp.content)
        mp3_path = tf.name

    try:
        # 3) Baş kısmına sessizlik ekle
        sound   = AudioSegment.from_file(mp3_path, format="mp3")
        silence = AudioSegment.silent(duration=PRE_SILENCE_MS)
        padded  = silence + sound
        padded.export(mp3_path, format="mp3")

        # 4) mpg123 ile çal (-q sessiz mod, -f scale factor)
        subprocess.run([
            "mpg123",
            "-q",
            "-f", str(scale),
            mp3_path
        ], check=True)

    finally:
        # 5) Geçici dosyayı sil
        try:
            os.remove(mp3_path)
        except OSError:
            pass
