# state.py
import threading

# Durum yönetim modülü
_kilit = threading.Lock()
_sistem_durumu = 'HAZIR'  # 'HAZIR', 'CALISIYOR', 'DURAKLATILDI'
_ws_baslatildi = False

def sistem_durumunu_ayarla(yeni_durum):
    with _kilit:
        global _sistem_durumu
        _sistem_durumu = yeni_durum

def sistem_durumunu_al():
    with _kilit:
        return _sistem_durumu

def ws_baslatildi_ayarla(deger):
    with _kilit:
        global _ws_baslatildi
        _ws_baslatildi = deger

def ws_baslatildi_mi():
    with _kilit:
        return _ws_baslatildi