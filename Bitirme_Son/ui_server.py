# ui_server.py
from flask import Flask
from main import maini_baslat
from texttospeech import metni_sese_cevir_ve_oynat
from main import sistemi_baslat, sistemi_durdur, sistemi_duraklat, sistemi_devam_ettir

app = Flask(__name__)

@app.route("/baslat", methods=["GET"])
def baslat():
    sistemi_baslat()
    metni_sese_cevir_ve_oynat("Sistem başlatıldı komut bekleniyor")
    return {"status": "ok", "mesaj": "Sistem başlatıldı"}

@app.route("/durdur", methods=["GET"])
def durdur():
    sistemi_durdur()
    metni_sese_cevir_ve_oynat("Sistem durduruldu")
    return {"status": "ok", "mesaj": "Sistem durduruldu"}

@app.route("/duraklat", methods=["GET"])
def duraklat():
    sistemi_duraklat()
    metni_sese_cevir_ve_oynat("Sistem duraklatıldı")
    return {"status": "ok", "mesaj": "Sistem duraklatıldı"}

@app.route("/devam", methods=["GET"])
def devam():
    sistemi_devam_ettir()
    metni_sese_cevir_ve_oynat("Sistem devam ediyor")
    return {"status": "ok", "mesaj": "Sistem devam ediyor"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
