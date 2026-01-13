import os
import shutil
import uuid
import uvicorn
from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.orchestrator import Orchestrator
from backend.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="Auto Dealership Voice Assistant", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("frontend/public/audio", exist_ok=True)
os.makedirs("temp_uploads", exist_ok=True)

orchestrator = Orchestrator()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"Client {client_id} connected via WebSocket")
    
    try:
        while True:
            data = await websocket.receive_bytes()
            
            temp_filename = f"temp_uploads/{uuid.uuid4().hex}.webm"
            with open(temp_filename, "wb") as f:
                f.write(data)
                
            response = await orchestrator.process_audio(client_id, temp_filename)
            await websocket.send_json(response)
            os.remove(temp_filename)
            
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}", exc_info=True)
    finally:
        logger.info(f"Client {client_id} disconnected")

@app.get("/summary/{client_id}")
async def get_summary(client_id: str):
    return orchestrator.get_session_summary(client_id)

app.mount("/audio", StaticFiles(directory="frontend/public/audio"), name="audio")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
