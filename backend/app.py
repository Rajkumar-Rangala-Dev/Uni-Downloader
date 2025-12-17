from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from downloader import analyze_url, process_download
from validators import validate_url, detect_platform
import os
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    mode: str  # 'video' or 'mp3'

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    url = request.url
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid or unsupported URL.")
    platform = detect_platform(url)
    if not platform:
        raise HTTPException(status_code=400, detail="Unsupported platform.")
    info = await analyze_url(url)
    return info

@app.post("/download")
async def download(request: DownloadRequest, background_tasks: BackgroundTasks):
    url = request.url
    mode = request.mode
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid or unsupported URL.")
    file_id = str(uuid.uuid4())
    try:
        file_path, filename = await process_download(url, mode, file_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    background_tasks.add_task(cleanup_file, file_path)
    return {"file_id": file_id, "filename": filename}

@app.get("/file/{file_id}")
async def get_file(file_id: str):
    temp_dir = os.getenv("TEMP_DIR", "/tmp")
    for ext in [".mp4", ".mp3"]:
        file_path = os.path.join(temp_dir, f"{file_id}{ext}")
        if os.path.exists(file_path):
            return FileResponse(file_path, filename=os.path.basename(file_path))
    raise HTTPException(status_code=404, detail="File not found.")

def cleanup_file(file_path):
    try:
        os.remove(file_path)
    except Exception:
        pass
