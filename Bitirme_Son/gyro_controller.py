#!/usr/bin/env python3
import time
import busio
from adafruit_blinka.board.raspberrypi.raspi_5 import SCL, SDA
from adafruit_bno055 import BNO055_I2C
from pid_controller import PIDController
from motor import motor_calistir

# I2C başlat
i2c = busio.I2C(SCL, SDA)
sensor = BNO055_I2C(i2c)

# Z ekseninden heading (0–360°) oku
def get_z_angle():
    euler = sensor.euler
    if euler is not None and euler[0] is not None:
        return euler[0] % 360
    return None

# Belirli açı kadar PID kontrollü dönüş
def don_aci_hedefli(hedef_aci, yon=None, tolerans=1):
    if yon not in ["sag", "sol"]:
        raise ValueError("Lütfen yönü 'sag' veya 'sol' olarak belirtin.")
    pid = PIDController(Kp=2.0, Ki=0.0, Kd=0.2, setpoint=0, output_limits=(-255, 255))
    pid.reset()
    
    baslangic_aci = get_z_angle()
    if baslangic_aci is None:
        print("Başlangıç açısı okunamadı!")
        return
    if yon == "sag":
        hedef_mutlak = (baslangic_aci + hedef_aci) % 360
    elif yon == "sol":
        hedef_mutlak = (baslangic_aci - hedef_aci + 360) % 360

    print(f"[DÖNÜŞ] {yon.upper()} yönüne {hedef_aci}° hedefleniyor. Başlangıç: {baslangic_aci:.2f}°, Hedef: {hedef_mutlak:.2f}°")

    while True:
        mevcut_aci = get_z_angle()
        if mevcut_aci is None:
            continue

        # Hata açısı [-180, 180] aralığına normalize edilir
        hata = (hedef_mutlak - mevcut_aci + 540) % 360 - 180
        pwm = pid.update(hata)

        if abs(hata) <= tolerans:
            break

        # PID yön kontrolü
        motor_yonu = "saga_don" if pwm > 0 else "sola_don"
        motor_calistir(100, motor_yonu)

        print(f"Açı: {mevcut_aci:.2f}°, Hedef: {hedef_mutlak:.2f}°, Hata: {hata:.2f}°, PWM: {pwm:.1f}, Yön: {motor_yonu}")
        time.sleep(0.01)

    motor_calistir(0, "dur")
    print("[DÖNÜŞ] Tamamlandı.")
