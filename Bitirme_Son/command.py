import time
import asyncio
import state

from motor import motor_calistir
from ultrasonic_sensor import mesafe_oku, mesafe_oku_arka
from gyro_controller import don_aci_hedefli
from pid_controller import PIDController
from texttospeech import metni_sese_cevir_ve_oynat
from status_ws_server import send_status

pid = PIDController(Kp=50.0, Ki=0.1, Kd=0.05, setpoint=0.2)

def komut_uygula(komut_dict):
    if state.sistem_durumunu_al() in ['DURAKLATILDI', 'HAZIR']:
        print("[UYARI] Komut iptal edildi - Sistem duraklatılmış veya durdurulmuş")
        return
    komut = komut_dict.get("komut")
    kosul = komut_dict.get("kosul")

    status_bildirimleri = {
    "ileri_git": {
        "hareket": "Araç ileri gidiyor...",
        "tamamlandi": "Araç ileri gitti."
        },
    "geri_git": {
        "hareket": "Araç geri gidiyor...",
        "tamamlandi": "Araç geri gitti."
        },
    "saga_don": {
        "hareket": "Araç sağa dönüyor...",
        "tamamlandi": "Araç sağa döndü."
        },
    "sola_don": {
        "hareket": "Araç sola dönüyor...",
        "tamamlandi": "Araç sola döndü."
        },
    "dur": {
        "hareket": "Araç duruyor...",
        "tamamlandi": "Araç durdu."
        },
    "tanimsiz_komut": {
        "hareket": "Araç duruyor...",
        "tamamlandi": "Tanımsız komut. Araç bu komutu gerçekleştiremez."
        }        
    }

    
    if komut in ["ileri_git", "geri_git"]:
        ileri_mi = komut == "ileri_git"
        mesafe_fonk = mesafe_oku if ileri_mi else mesafe_oku_arka
        yon = "ileri" if ileri_mi else "geri"
        yon_etiket = "[İLERİ]" if ileri_mi else "[GERİ]"

        mesafe = mesafe_fonk()
        if mesafe <= 0.3:
            print(f"[DUR] Engel çok yakın! {yon_etiket} gidilemez. Mesafe:", mesafe)
            asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
            motor_calistir(0, "dur")
            metni_sese_cevir_ve_oynat("Bu komutu gerçekleştiremem. Önümde engel var.")
            return

        if kosul == "engel_algilayana_kadar":
            print(f"{yon_etiket} PID ile engel algılayana kadar {yon} gidiliyor...")
            metni_sese_cevir_ve_oynat(f"Engel algılayana kadar {yon} gidiyorum.")
            pid.reset()
            while True:
                mesafe = mesafe_fonk()
                pwm = pid.update(mesafe)
                if pwm <= 80:
                   pwm = 80
                elif pwm > 200:
                   pwm = 200
                if mesafe <= 0.3:
                    motor_calistir(0, "dur")
                    asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
                    break
                hiz = (pwm / 255) * 100
                asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
                motor_calistir(hiz, yon)
                print(f"Mesafe: {mesafe:.2f} m | PWM: {pwm} | Hız: %{hiz:.1f}")
                time.sleep(0.1)

        elif kosul and "_saniye" in kosul:
            saniye = int(kosul.replace("_saniye", ""))
            print(f"{yon_etiket} {saniye} saniye boyunca {yon} gidiliyor, engel kontrolü aktif...")
            metni_sese_cevir_ve_oynat(kosul if kosul else f"{saniye} boyunca {yon_etiket} gidiyorum.")
            asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
            motor_calistir(70, yon)
            baslangic_zaman = time.time()

            while time.time() - baslangic_zaman < saniye:
                mesafe = mesafe_fonk()
                if mesafe <= 0.5:
                    print("[DUR] Engel algılandı, hareket durduruluyor.")
                    motor_calistir(0, "dur")
                    asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
                    time.sleep(1)
                    asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri["dur"]["tamamlandi"]}))
                    break
                asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri[komut]["tamamlandi"]}))
                time.sleep(0.1)
            else:
                motor_calistir(0, "dur")
                asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
                time.sleep(1)
                asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri["dur"]["tamamlandi"]}))

        else:
            print(f"{yon_etiket} 1.5 saniye sabit hızla {yon} gidiliyor.")
            metni_sese_cevir_ve_oynat(kosul if kosul else f"Sabit hızla {yon_etiket} gidiyorum.")
            asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))         
            motor_calistir(70, yon)
            time.sleep(1.5)
            motor_calistir(0, "dur")
            asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
            time.sleep(1)
            asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri["dur"]["tamamlandi"]}))

    elif komut == "saga_don":
        print("[DÖNÜŞ] Sağa dönülüyor...")
        if kosul and "_derece" in kosul:
            donus_aci = int(kosul.replace("_derece", ""))
        else:
            donus_aci = 90  # varsayılan
        print(f"[DÖNÜŞ] Hedef açı: {donus_aci} derece (Yön: sağ)")
        asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
        metni_sese_cevir_ve_oynat(kosul if kosul else f"Sağa {donus_aci} derece dönüyorum.")
        don_aci_hedefli(donus_aci, yon="sag")
        asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri[komut]["tamamlandi"]}))

    elif komut == "sola_don":
        print("[DÖNÜŞ] Sola dönülüyor...")
        if kosul and "_derece" in kosul:
            donus_aci = int(kosul.replace("_derece", ""))
        else:
            donus_aci = 90
        print(f"[DÖNÜŞ] Hedef açı: {donus_aci} derece (Yön: sol)")
        asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
        metni_sese_cevir_ve_oynat(kosul if kosul else f"Sola {donus_aci} derece dönüyorum.")
        don_aci_hedefli(donus_aci, yon="sol")
        asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri[komut]["tamamlandi"]}))

    elif komut == "dur":
        print("[DUR] Hareket durduruldu.")
        metni_sese_cevir_ve_oynat(kosul if kosul else "Duruyorum.")
        asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
        motor_calistir(0, "dur")
        asyncio.run(send_status(status_bildirimleri["dur"]["hareket"]))
        time.sleep(1)
        asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri["dur"]["tamamlandi"]}))
            
    elif komut == "tanimsiz_komut":
        print(f"[UYARI] Tanımsız komut: {komut}")
        metni_sese_cevir_ve_oynat(kosul if kosul else "Komut anlaşılmadı")
        asyncio.run(send_status(status_bildirimleri[komut]["hareket"]))
        time.sleep(1)
        asyncio.run(send_status({"status": "tamamlandi", "mesaj": status_bildirimleri[komut]["tamamlandi"]}))

def json_komut_listesini_uygula(komutlar):
        
    for komut in komutlar:
        komut_uygula(komut)
