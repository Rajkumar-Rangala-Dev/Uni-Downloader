import yt_dlp
import asyncio
import os
from ffmpeg_utils import merge_streams, convert_to_mp3
from validators import detect_platform

def get_output_paths(file_id, mode):
    temp_dir = os.getenv("TEMP_DIR", "/tmp")
    if mode == "mp3":
        return os.path.join(temp_dir, f"{file_id}.mp3"), f"{file_id}.mp3"
    return os.path.join(temp_dir, f"{file_id}.mp4"), f"{file_id}.mp4"

async def analyze_url(url):
    ydl_opts = {"quiet": True, "skip_download": True, "forcejson": True}
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
    return {
        "title": info.get("title"),
        "duration": info.get("duration"),
        "platform": detect_platform(url),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
    }

async def process_download(url, mode, file_id):
    temp_dir = os.getenv("TEMP_DIR", "/tmp")
    os.makedirs(temp_dir, exist_ok=True)
    if mode == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(temp_dir, f"{file_id}.%(ext)s"),
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": os.path.join(temp_dir, f"{file_id}.%(ext)s"),
            "quiet": True,
            "merge_output_format": "mp4",
        }
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        await loop.run_in_executor(None, lambda: ydl.download([url]))
    output_path, filename = get_output_paths(file_id, mode)
    if not os.path.exists(output_path):
        raise Exception("Download failed or file not found.")
    return output_path, filename
