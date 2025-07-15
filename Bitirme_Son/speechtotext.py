#!/usr/bin/env python3
import os
import sys
import contextlib
import tempfile
import pickle
import torch
import torchaudio
import speech_recognition as sr
from speechbrain.inference.speaker import SpeakerRecognition
from texttospeech import metni_sese_cevir_ve_oynat

# --- Ayarlar ---
REFERENCE_DIR        = "sesler"
SCORE_THRESHOLD      = 0.3
SAMPLE_RATE          = 16000
CALIBRATE_DURATION   = 0.3       # Ortam gürültüsü kalibrasyonu (saniye)
MAX_ENERGY_THRESHOLD = 1000      # energy_threshold için üst sınır
EMB_CACHE_PATH       = "speaker_embeddings.pt"
MODEL_CACHE_PATH     = "verification_cache.pkl"

@contextlib.contextmanager
def suppress_stderr():
    with open(os.devnull, 'w') as devnull:
        old = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old


def load_speaker_references(reference_dir=REFERENCE_DIR):
    refs = {}
    for spk in os.listdir(reference_dir):
        spk_dir = os.path.join(reference_dir, spk)
        if not os.path.isdir(spk_dir):
            continue
        wavs = [os.path.join(spk_dir, f)
                for f in os.listdir(spk_dir)
                if f.lower().endswith('.wav')]
        if wavs:
            refs[spk] = wavs
    return refs


def identify_speaker(wav_path, speaker_embs, verification):
    signal, fs = torchaudio.load(wav_path)
    if fs != SAMPLE_RATE:
        signal = torchaudio.transforms.Resample(fs, SAMPLE_RATE)(signal)
    if signal.ndim > 1:
        signal = signal.mean(dim=0, keepdim=True)
    emb = verification.encode_batch(signal).flatten()

    best_spk, best_score = None, -1.0
    for spk, ref_emb in speaker_embs.items():
        ref = ref_emb.flatten()
        score = torch.dot(emb, ref) / (emb.norm() * ref.norm() + 1e-8)
        if score > best_score:
            best_spk, best_score = spk, score.item()
    return best_spk if best_score >= SCORE_THRESHOLD else "tanimsiz_konusmaci"


def init_model_and_embeddings():
    if os.path.exists(MODEL_CACHE_PATH):
        with open(MODEL_CACHE_PATH, 'rb') as f:
            verification = pickle.load(f)
        print("✅ Model önbellekten yüklendi.", flush=True)
    else:
        print("🔄 SpeechBrain ECAPA-TDNN modeli yükleniyor…", flush=True)
        verification = SpeakerRecognition.from_hparams(
            source='speechbrain/spkrec-ecapa-voxceleb',
            savedir='pretrained_models/spkrec-ecapa-voxceleb'
        )
        verification.eval()
        with open(MODEL_CACHE_PATH, 'wb') as f:
            pickle.dump(verification, f)
        print("✅ Model önbelleğe kaydedildi.", flush=True)

    if os.path.exists(EMB_CACHE_PATH):
        speaker_embs = torch.load(EMB_CACHE_PATH)
        print(f"✅ {len(speaker_embs)} konuşmacı embedding yüklendi.", flush=True)
    else:
        print("🔄 Konuşmacı embedding’leri hazırlanıyor…", flush=True)
        speaker_files = load_speaker_references()
        speaker_embs = {}
        for spk, files in speaker_files.items():
            embs = []
            for wav in files:
                sig, fs = torchaudio.load(wav)
                if fs != SAMPLE_RATE:
                    sig = torchaudio.transforms.Resample(fs, SAMPLE_RATE)(sig)
                if sig.ndim > 1:
                    sig = sig.mean(dim=0, keepdim=True)
                embs.append(verification.encode_batch(sig).flatten())
            speaker_embs[spk] = torch.mean(torch.stack(embs), dim=0)
        torch.save(speaker_embs, EMB_CACHE_PATH)
        print(f"✅ {len(speaker_embs)} konuşmacı embedding hazır.", flush=True)

    return verification, speaker_embs


def dinle_ve_donustur_otomatik():
    verification, speaker_embs = init_model_and_embeddings()
    r = sr.Recognizer()
    r.energy_threshold = MAX_ENERGY_THRESHOLD
    r.pause_threshold = 0.75
    r.dynamic_energy_threshold = False

    try:
        mic = sr.Microphone(device_index=None, sample_rate=SAMPLE_RATE)
    except Exception as e:
        print(f"⚠️ Mikrofon açılamadı: {e}", flush=True)
        return {"text": "", "speaker": "tanimsiz_konusmaci"}

    with mic as source:
        print(f"🎙️ Ortam gürültüsü ayarlanıyor ({CALIBRATE_DURATION}s)...", flush=True)
        with suppress_stderr():
            r.adjust_for_ambient_noise(source, duration=CALIBRATE_DURATION)
        r.energy_threshold = min(r.energy_threshold, MAX_ENERGY_THRESHOLD)
        print(f"🔧 energy_threshold: {r.energy_threshold}", flush=True)

        print("🟢 Konuşmaya başladığınızda otomatik algılanacak...", flush=True)
        try:
            with suppress_stderr():
                audio = r.listen(source, timeout=None)
            print("🧠 Ses alındı, işleniyor...", flush=True)
        except sr.WaitTimeoutError:
            print("⏱️ Konuşma zaman aşımına uğradı.", flush=True)
            return {"text": "", "speaker": "tanimsiz_konusmaci"}

    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    with open(tmp_wav, "wb") as f:
        f.write(audio.get_wav_data())

    speaker = identify_speaker(tmp_wav, speaker_embs, verification)
    print(f"👤 Konuşmacı: {speaker}", flush=True)

    text = ""
    if speaker != "tanimsiz_konusmaci":
        with sr.AudioFile(tmp_wav) as src:
            audio_data = r.record(src)
        try:
            with suppress_stderr():
                text = r.recognize_google(audio_data, language="tr-TR")
            print(f"📝 STT sonucu: {text}", flush=True)
        except sr.UnknownValueError:
            print("❌ Konuşma anlaşılamadı.", flush=True)
        except sr.RequestError as e:
            print(f"❌ Google STT hatası: {e}", flush=True)
    else:
        print("❌ Konuşmacı tanınamadı: tanimsiz_konusmaci", flush=True)
        text = "tanimsiz_konusmaci"

    os.remove(tmp_wav)
    return {"text": text, "speaker": speaker}
