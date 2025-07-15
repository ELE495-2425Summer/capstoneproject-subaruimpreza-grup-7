# status_ws_server.py
import asyncio
import websockets
import json
import time

clients = set()
latest_message = "Araç komut bekliyor..."

async def send_status(msg):
    """
    Komut esnasında çağrılır.
    - Hareket: düz metin
    - Tamamlandı: {"status": "tamamlandi", "mesaj": "..."}
    - Komut listesi: {"status": "komut_listesi", "komutlar": [...], "konusmaci": "...", "zaman": ...}
    """
    global latest_message

    # Komut listesine zaman ekle (konuşma tanımlayıcı)
    if isinstance(msg, dict) and msg.get("status") == "komut_listesi":
        msg["zaman"] = time.time()

    # Diğer mesajlar için latest_message saklanır
    if not (isinstance(msg, dict) and msg.get("status") == "komut_listesi"):
        latest_message = msg

    # Tüm bağlı istemcilere mesaj gönder
    for ws in clients.copy():
        try:
            await ws.send(json.dumps(msg))
        except Exception as e:
            print("[StatusWS] Gönderim hatası:", e)

async def publish(ws):
    """
    UI istemcisine sürekli güncel mesajları yollar.
    """
    clients.add(ws)
    print("[StatusWS] UI istemcisi bağlandı.")
    try:
        while True:
            if isinstance(latest_message, dict):
                await ws.send(json.dumps(latest_message))
            else:
                await ws.send(latest_message)
            await asyncio.sleep(0.2)
    except websockets.ConnectionClosed:
        print("[StatusWS] UI istemcisi ayrıldı.")
    finally:
        clients.remove(ws)

async def start_status_server(host='0.0.0.0', port=5678):
    """
    WebSocket sunucusunu başlatır.
    """
    print(f"[StatusWS] Status sunucusu başlatıldı: ws://{host}:{port}")
    async with websockets.serve(publish, host, port):
        await asyncio.Future()  # sonsuz beklemede kal
