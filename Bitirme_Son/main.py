import threading
import asyncio
import time
import json
import os

from gyro_ws_server import start_gyro_server
from status_ws_server import start_status_server, send_status
from stt_ws_server import start_stt_server
from gpt_chat import chat
from command import json_komut_listesini_uygula
from speechtotext import dinle_ve_donustur_otomatik
from loop import run_loop


# ... mevcut importlar ...
import state  # Bu importu ekleyin

def sistemi_baslat():
    if state.sistem_durumunu_al() == 'CALISIYOR':
        print("[UYARI] Sistem zaten çalışıyor.")
        return

    state.sistem_durumunu_ayarla('CALISIYOR')
    print("[SİSTEM] Başlatılıyor...")

    if not state.ws_baslatildi_mi():
        threading.Thread(target=lambda: asyncio.run(start_gyro_server('0.0.0.0', 5680)), daemon=True).start()
        threading.Thread(target=lambda: asyncio.run(start_status_server('0.0.0.0', 5678)), daemon=True).start()
        threading.Thread(target=lambda: asyncio.run(start_stt_server('0.0.0.0', 5679)), daemon=True).start()
        state.ws_baslatildi_ayarla(True)
        time.sleep(0.5)
    
    print("[SİSTEM] Mikrofon komut sistemi başlıyor...")
    threading.Thread(target=run_loop, daemon=True).start()

def sistemi_durdur():
    if state.sistem_durumunu_al() == 'HAZIR':
        print("[UYARI] Sistem zaten durdurulmuş.")
        return

    state.sistem_durumunu_ayarla('HAZIR')
    print("[SİSTEM] Durduruluyor...")

def sistemi_duraklat():
    if state.sistem_durumunu_al() == 'CALISIYOR':
        state.sistem_durumunu_ayarla('DURAKLATILDI')
        print("[SİSTEM] Duraklatılıyor...")

def sistemi_devam_ettir():
    if state.sistem_durumunu_al() == 'DURAKLATILDI':
        state.sistem_durumunu_ayarla('CALISIYOR')
        print("[SİSTEM] Devam ediliyor...")
