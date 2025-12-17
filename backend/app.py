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

@app.get("/")
async def root():
    return {"status": "ok", "message": "Universal Media Downloader API"}

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
async def download(request: DownloadRequest):
    url = request.url
    mode = request.mode
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="Invalid or unsupported URL.")
    file_id = str(uuid.uuid4())
    try:
        file_path, filename = await process_download(url, mode, file_id)
        # Return file directly to avoid ephemeral storage issues
        if not os.path.exists(file_path):
            raise HTTPException(status_code=500, detail="File processing failed.")
        response = FileResponse(
            file_path, 
            filename=filename,
            media_type='application/octet-stream',
            background=BackgroundTasks()
        )
        # Schedule cleanup after response is sent
        response.background.add_task(cleanup_file, file_path)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
