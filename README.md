# Universal Media Downloader

A powerful web application for downloading videos and audio from Instagram, YouTube, and WhatsApp Status.

## Features

- ✅ Download videos from YouTube, Instagram, and WhatsApp
- ✅ Convert videos to MP3 audio
- ✅ Bot protection bypass with rotating user agents
- ✅ Browser cookie support for authenticated content
- ✅ FFmpeg integration for video/audio processing
- ✅ Modern Next.js frontend with Tailwind CSS
- ✅ FastAPI backend with async support
- ✅ **Ready for Railway deployment**

## Tech Stack

### Frontend
- Next.js 14
- React 18
- Tailwind CSS
- Axios for API calls

### Backend
- FastAPI (Python 3.11)
- yt-dlp for media extraction
- FFmpeg for video/audio processing
- Docker & Docker Compose

## Deployment

### 🚂 Railway (Recommended)
Deploy to Railway in minutes with automatic scaling and HTTPS:

**See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed instructions**

Quick deploy:
1. Deploy backend: `./railway-deploy.sh backend`
2. Copy backend URL
3. Deploy frontend: `./railway-deploy.sh frontend <backend-url>`

### 🐳 Local Development

1. **Prerequisites**
   ```bash
   docker
   docker-compose
   ```

2. **Clone the repository**
   ```bash
   git clone https://github.com/Rajkumar-Rangala-Dev/Uni-Downloader.git
   cd Uni-Downloader
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Cookie Support (Optional)

To download private or login-required content from Instagram/YouTube, you can enable browser cookie support:

1. **Edit docker-compose.yml**
   ```yaml
   backend:
     environment:
       - COOKIE_BROWSER=chrome  # or firefox, edge, etc.
     volumes:
       # Add your browser's cookie directory
       - ~/.config/google-chrome:/root/.config/google-chrome:ro
       # Or for Firefox
       - ~/.mozilla:/root/.mozilla:ro
   ```

2. **Restart containers**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Supported Browsers
- `chrome` - Google Chrome
- `firefox` - Mozilla Firefox  
- `edge` - Microsoft Edge
- `chromium` - Chromium
- Leave empty (`COOKIE_BROWSER=`) to disable cookie support

## API Endpoints

### POST /analyze
Analyzes a URL and returns media information.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 213,
  "platform": "youtube",
  "thumbnail": "https://...",
  "uploader": "Channel Name"
}
```

### POST /download
Downloads media from a URL.

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "mode": "video"  // or "mp3"
}
```

**Response:**
```json
{
  "file_id": "uuid-here",
  "filename": "video.mp4"
}
```

### GET /file/{file_id}
Retrieves the downloaded file.

## Bot Protection Features

The application includes several bot protection bypass mechanisms:

- **Rotating User Agents**: Randomly selects from 4 different browser signatures
- **Enhanced HTTP Headers**: Includes Accept, DNT, Sec-Fetch headers
- **Retry Logic**: 5 extractor retries, 10 download retries
- **Cookie Support**: Optional browser cookie integration
- **Better Error Messages**: User-friendly error handling

## Known Limitations

- Instagram content may require authentication (use cookie support)
- YouTube may block requests without cookies in some cases
- WhatsApp Status downloads depend on URL accessibility
- Downloaded files are automatically cleaned up after download

## Development

### Project Structure
```
.
├── backend/
│   ├── app.py              # FastAPI application
│   ├── downloader.py       # Media download logic
│   ├── validators.py       # URL validation
│   ├── ffmpeg_utils.py     # FFmpeg operations
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── pages/
│   │   └── index.js        # Main page
│   ├── components/
│   │   └── PlatformIcon.js # Platform icons
│   └── package.json        # Node dependencies
├── downloads/              # Downloaded files (gitignored)
└── docker-compose.yml      # Container orchestration
```

### Environment Variables

**Backend (.env file):**
```bash
TEMP_DIR=/tmp
COOKIE_BROWSER=  # chrome, firefox, edge, or empty
```

**Frontend:**
```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Troubleshooting

### "IndentationError" in downloader.py
Clear Python cache and restart:
```bash
docker-compose exec backend find /app -name "*.pyc" -delete
docker-compose restart backend
```

### "Method Not Allowed" error
Ensure you're using the correct HTTP method:
- `/analyze` and `/download` require POST
- `/file/{file_id}` requires GET

### Instagram "not available" error
The content may be private or require authentication. Enable cookie support in docker-compose.yml.

### FFmpeg error
FFmpeg is automatically installed in the backend container. If errors occur, check logs:
```bash
docker-compose logs backend
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is for educational purposes only. Respect copyright and terms of service of the platforms you download from.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Media extraction library
- [FFmpeg](https://ffmpeg.org/) - Video/audio processing
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework

A web app to download high-quality video or MP3 from YouTube, Instagram, and WhatsApp public links.

## Features
- Paste a link, auto-detect platform
- Download best quality video+audio (MP4) or MP3 (192kbps+)
- Progress, merging, error handling
- No DRM/private content, no login scraping
- Dockerized, deployable anywhere

## Quick Start

```sh
docker-compose up --build
```

## Legal
Downloads are for personal use only. Respect copyright laws.