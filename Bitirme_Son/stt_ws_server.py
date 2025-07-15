# stt_ws_server.py
import asyncio
import websockets
import json

clients = set()
latest_stt = {"text": "Henüz bir komut alınmadı.", "speaker": "Henüz tanımlanmadı"}

async def send_stt(data):
    """
    STT sonucunu UI'a gönderir.
    """
    global latest_stt
    latest_stt = data

    for ws in clients.copy():
        try:
            await ws.send(json.dumps(latest_stt))
        except Exception as e:
            print("[STT-WS] Gönderim hatası:", e)

async def publish(ws):
    """
    Bağlı UI istemcisine düzenli olarak STT mesajı yollar.
    """
    clients.add(ws)
    print("[STT-WS] UI istemcisi bağlandı.")
    try:
        while True:
            await ws.send(json.dumps(latest_stt))
            await asyncio.sleep(0.2)
    except websockets.ConnectionClosed:
        print("[STT-WS] UI istemcisi ayrıldı.")
    finally:
        clients.remove(ws)

async def start_stt_server(host='0.0.0.0', port=5679):
    """
    STT WebSocket sunucusunu başlatır.
    """
    print(f"[STT-WS] STT sunucusu başlatıldı: ws://{host}:{port}")
    async with websockets.serve(publish, host, port):
        await asyncio.Future()
