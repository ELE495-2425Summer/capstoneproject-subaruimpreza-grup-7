# loop.py
import json
import asyncio
import time  
import state

from gpt_chat import chat
from command import json_komut_listesini_uygula
from speechtotext import dinle_ve_donustur_otomatik
from status_ws_server import send_status
from stt_ws_server import send_stt

# Ana döngü
def run_loop():
    while state.sistem_durumunu_al() != 'HAZIR':
        if state.sistem_durumunu_al() == 'DURAKLATILDI':
            time.sleep(0.1)
            continue
        try:
            result = dinle_ve_donustur_otomatik()
            komut_metni = result["text"]
            konusmaci = result["speaker"] or "tanimsiz_konusmaci"  # None veya boşsa düzelt

            # STT sonucunu ve konuşmacıyı UI'a gönder
            asyncio.run(send_stt({
                "text": komut_metni,
                "speaker": konusmaci
            }))

            # GPT'ye komut verilmesi (komut boş değilse devam et)
            if komut_metni:
                print(f"[SES] Algılanan komut: {komut_metni} | Konuşmacı: {konusmaci}")
                json_komut = chat(komut_metni)

                if json_komut:
                    print(f"[GPT] Yorumlanan komut: {json_komut}")
                    komut_listesi = json.loads(json_komut)

                    # UI'a status gönder (konusmaci her durumda yazdırılır)
                    asyncio.run(send_status({
                        "status": "komut_listesi",
                        "komutlar": komut_listesi,
                        "konusmaci": konusmaci,
                        "zaman": time.time()
                    }))

                    # Komutları uygula
                    json_komut_listesini_uygula(komut_listesi)
                else:
                    print("[HATA] GPT'den yanıt alınamadı")
            else:
                print(f"[UYARI] Boş komut algılandı | Konuşmacı: {konusmaci}")

        except KeyboardInterrupt:
            print("\n[SİSTEM] Çıkılıyor...")
            break
        except Exception as e:
            print(f"[HATA] {e}")
