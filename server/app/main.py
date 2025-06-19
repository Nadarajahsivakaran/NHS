from fastapi import FastAPI, WebSocket
from app.websocket import handle_stream

app = FastAPI()

@app.websocket("/ws/audio-stream")
async def stream_endpoint(websocket: WebSocket):
    await handle_stream(websocket)
