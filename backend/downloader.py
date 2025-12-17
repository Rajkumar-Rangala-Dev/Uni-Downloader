import yt_dlp
import asyncio
import os
import random
from ffmpeg_utils import merge_streams, convert_to_mp3
from validators import detect_platform

# Get browser for cookie extraction (chrome, firefox, edge, etc.) - empty string disables cookies
COOKIE_BROWSER = os.getenv("COOKIE_BROWSER", "")

# User agents to rotate and avoid bot detection
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def get_output_paths(file_id, mode):
    temp_dir = os.getenv("TEMP_DIR", "/tmp")
    if mode == "mp3":
        return os.path.join(temp_dir, f"{file_id}.mp3"), f"{file_id}.mp3"
    return os.path.join(temp_dir, f"{file_id}.mp4"), f"{file_id}.mp4"

async def analyze_url(url):
    # Enhanced options to bypass bot detection
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
        "user_agent": random.choice(USER_AGENTS),
        "extractor_retries": 5,
        "socket_timeout": 30,
        "http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    }
    
    # Only add cookies if browser is specified
    if COOKIE_BROWSER:
        ydl_opts["cookiesfrombrowser"] = (COOKIE_BROWSER,)
    
    loop = asyncio.get_event_loop()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
        return {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "platform": detect_platform(url),
            "thumbnail": info.get("thumbnail"),
            "uploader": info.get("uploader"),
        }
    except Exception as e:
        # Better error handling - show original error for debugging
        error_msg = str(e)
        print(f"DEBUG: Original error: {error_msg}")
        if "Sign in" in error_msg or "bot" in error_msg.lower():
            raise Exception("This content requires authentication or is protected. Please try a different video.")
        elif "Private" in error_msg or "private" in error_msg.lower():
            raise Exception("This content is private and cannot be downloaded.")
        elif "not available" in error_msg.lower():
            raise Exception("This content is not available or has been removed.")
        else:
            raise Exception(f"Could not analyze URL: {error_msg}")

async def process_download(url, mode, file_id):
    temp_dir = os.getenv("TEMP_DIR", "/tmp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Common options to bypass bot detection
    common_opts = {
        "quiet": False,
        "no_warnings": False,
        "ffmpeg_location": "/usr/bin",
        "user_agent": random.choice(USER_AGENTS),
        "extractor_retries": 5,
        "fragment_retries": 5,
        "socket_timeout": 30,
        "retries": 10,
        "http_headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none"
        },
        # Additional options for Instagram/YouTube
        "nocheckcertificate": True,
        "prefer_insecure": False,
        "age_limit": None,
    }
    
    # Only add cookies if browser is specified
    if COOKIE_BROWSER:
        common_opts["cookiesfrombrowser"] = (COOKIE_BROWSER,)
    
    if mode == "mp3":
        ydl_opts = {
            **common_opts,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(temp_dir, f"{file_id}.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        ydl_opts = {
            **common_opts,
            # Prefer formats that don't require merging first
            "format": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": os.path.join(temp_dir, f"{file_id}.%(ext)s"),
            "merge_output_format": "mp4",
        }
    
    loop = asyncio.get_event_loop()
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, lambda: ydl.download([url]))
    except Exception as e:
        error_msg = str(e)
        # Better error messages
        if "Sign in" in error_msg or "bot" in error_msg.lower():
            raise Exception("Access denied: This content requires authentication. YouTube/Instagram may have detected automated access.")
        elif "Private" in error_msg or "private" in error_msg.lower():
            raise Exception("This content is private and cannot be downloaded.")
        elif "ffmpeg" in error_msg.lower():
            raise Exception("FFmpeg processing error. The video format may be incompatible.")
        elif "not available" in error_msg.lower():
            raise Exception("This content is not available or has been removed.")
        elif "429" in error_msg or "rate" in error_msg.lower():
            raise Exception("Too many requests. Please wait a moment and try again.")
        else:
            raise Exception(f"Download failed: {error_msg}")
    
    output_path, filename = get_output_paths(file_id, mode)
    if not os.path.exists(output_path):
        raise Exception("Download failed or file not found.")
    return output_path, filename
