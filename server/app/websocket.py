from fastapi import WebSocket, WebSocketDisconnect
from app.transcriber import transcribe_audio
from app.translator import translate_text

async def handle_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_chunk = await websocket.receive_bytes()
            text = transcribe_audio(audio_chunk)
            translation = translate_text(text, target_lang="en")
            await websocket.send_text(translation)
    except WebSocketDisconnect:
        print("Client disconnected from stream.")
