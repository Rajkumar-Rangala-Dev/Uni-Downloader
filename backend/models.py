from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    mode: str  # 'video' or 'mp3'
