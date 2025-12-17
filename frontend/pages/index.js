import { useState } from 'react';
import axios from 'axios';
import PlatformIcon from '../components/PlatformIcon';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';

export default function Home() {
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState('video');
  const [platform, setPlatform] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [info, setInfo] = useState(null);
  const [error, setError] = useState('');
  const [fileId, setFileId] = useState(null);
  const [filename, setFilename] = useState('');

  function detectPlatform(url) {
    if (/youtube\.com|youtu\.be/.test(url)) return 'youtube';
    if (/instagram\.com/.test(url)) return 'instagram';
    if (/wa\.me|whatsapp\.com/.test(url)) return 'whatsapp';
    return null;
  }

  const handleAnalyze = async () => {
    setError('');
    setInfo(null);
    setFileId(null);
    setFilename('');
    setPlatform(detectPlatform(url));
    if (!platform) {
      setError('Unsupported or invalid URL.');
      return;
    }
    setAnalyzing(true);
    try {
      const res = await axios.post(`${API_BASE}/analyze`, { url });
      setInfo(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to analyze URL.');
    }
    setAnalyzing(false);
  };

  const handleDownload = async () => {
    setError('');
    setDownloading(true);
    try {
      const res = await axios.post(`${API_BASE}/download`, { url, mode });
      setFileId(res.data.file_id);
      setFilename(res.data.filename);
    } catch (e) {
      setError(e.response?.data?.detail || 'Download failed.');
    }
    setDownloading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-50">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-6">
        <h1 className="text-2xl font-bold mb-4 text-center">Universal Media Downloader</h1>
        <div className="flex items-center mb-2">
          <input
            className="flex-1 border rounded px-3 py-2 mr-2"
            placeholder="Paste YouTube, Instagram, or WhatsApp link"
            value={url}
            onChange={e => setUrl(e.target.value)}
            disabled={analyzing || downloading}
          />
          <PlatformIcon platform={platform} />
        </div>
        <div className="flex justify-center mb-4">
          <button
            className={`px-4 py-2 rounded-l ${mode==='video' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setMode('video')}
            disabled={analyzing || downloading}
          >
            🎥 Video
          </button>
          <button
            className={`px-4 py-2 rounded-r ${mode==='mp3' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setMode('mp3')}
            disabled={analyzing || downloading}
          >
            🎧 MP3
          </button>
        </div>
        <button
          className="w-full bg-blue-600 text-white py-2 rounded mb-2 disabled:opacity-50"
          onClick={handleAnalyze}
          disabled={analyzing || downloading || !url}
        >
          {analyzing ? 'Analyzing...' : 'Fetch Info'}
        </button>
        {info && (
          <div className="mb-2 text-sm text-gray-700">
            <div><b>Title:</b> {info.title}</div>
            <div><b>Uploader:</b> {info.uploader}</div>
            <div><b>Duration:</b> {info.duration ? `${Math.floor(info.duration/60)}m ${info.duration%60}s` : 'N/A'}</div>
            {info.thumbnail && <img src={info.thumbnail} alt="thumbnail" className="mt-2 rounded w-full" />}
          </div>
        )}
        <button
          className="w-full bg-green-600 text-white py-2 rounded mb-2 disabled:opacity-50"
          onClick={handleDownload}
          disabled={downloading || !info}
        >
          {downloading ? 'Processing...' : `Download ${mode === 'mp3' ? 'MP3' : 'Video'}`}
        </button>
        {fileId && (
          <a
            href={`${API_BASE}/file/${fileId}`}
            className="block w-full bg-indigo-600 text-white py-2 rounded text-center mt-2"
            download={filename}
          >
            ⬇️ Download {filename}
          </a>
        )}
        {error && <div className="text-red-600 mt-2 text-sm">{error}</div>}
        <div className="text-xs text-gray-500 mt-4 text-center">
          Downloads are for personal use only. Respect copyright laws.
        </div>
      </div>
    </div>
  );
}
