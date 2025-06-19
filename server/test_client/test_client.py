import asyncio
import websockets

async def test_audio_stream():
    uri = "ws://localhost:8000/ws/audio-stream"
    async with websockets.connect(uri) as websocket:
        with open("sample_audio.wav", "rb") as f:
            chunk = f.read()  # In production you'd send small pieces
            await websocket.send(chunk)
            translation = await websocket.recv()
            print("Translated Text:", translation)

asyncio.run(test_audio_stream())
