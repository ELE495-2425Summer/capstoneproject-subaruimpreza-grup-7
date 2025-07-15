#!/usr/bin/env python3
"""
Gyro WebSocket sunucusu modülü.
Bu modül, gyro_controller.get_z_angle() kullanarak
BNO055 sensöründen okunan heading açısını
WebSocket üzerinden JSON olarak yayınlar.
"""
import asyncio
import json
import time
import gyro_controller
import websockets

async def publish(ws):
    """
    Bağlı her istemci için açı verisini periyodik olarak gönderir.
    """
    print("[GyroWS] İstemci bağlandı, veri gönderimi başlıyor...")
    try:
        while True:
            angle = gyro_controller.get_z_angle()
            if angle is not None:
                # JSON formatında açı verisini gönder
                await ws.send(json.dumps({"angle": angle}))
            # 50 ms aralıkla veri gönder
            await asyncio.sleep(0.05)
    except websockets.ConnectionClosed:
        print("[GyroWS] İstemci bağlantısı kapandı.")

async def start_gyro_server(host: str = '172.20.10.2', port: int = 5680):
    """
    Gyro WebSocket sunucusunu başlatır.
    host: Dinleme yapılacak IP (örn. Raspberry Pi IP)
    port: TCP port
    """
    server = await websockets.serve(publish, host, port)
    print(f"[GyroWS] Sunucu {host}:{port} adresinde çalışıyor...")
    # Sonsuz bekleme, sunucuyu ayakta tut
    await server.wait_closed()

if __name__ == '__main__':
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else '172.20.10.2'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5680
    try:
        asyncio.run(start_gyro_server(host, port))
    except KeyboardInterrupt:
        print("[GyroWS] Sunucu durduruldu.")
