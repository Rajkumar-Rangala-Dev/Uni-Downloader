import re

def validate_url(url):
    yt = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+"
    ig = r"(https?://)?(www\.)?instagram\.com/.+"
    wa = r"(https?://)?(www\.)?wa\.me/.+|whatsapp\.com/.+"
    return bool(re.match(yt, url) or re.match(ig, url) or re.match(wa, url))

def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if "instagram.com" in url:
        return "instagram"
    if "wa.me" in url or "whatsapp.com" in url:
        return "whatsapp"
    return None
