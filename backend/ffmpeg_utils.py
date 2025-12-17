import subprocess
import os

def merge_streams(video_path, audio_path, output_path):
    cmd = [
        "ffmpeg", "-y", "-i", video_path, "-i", audio_path,
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", output_path
    ]
    subprocess.run(cmd, check=True)

def convert_to_mp3(input_path, output_path):
    cmd = [
        "ffmpeg", "-y", "-i", input_path, "-vn", "-ar", "44100", "-ac", "2", "-b:a", "192k", output_path
    ]
    subprocess.run(cmd, check=True)
