import { useState, useEffect } from 'react';
import axios from 'axios';
import PlatformIcon from '../components/PlatformIcon';

// Auto-detect backend URL
const getApiBase = () => {
  if (typeof window === 'undefined') {
    return process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
  }
  
  // Use environment variable if set (for Railway/production)
  if (process.env.NEXT_PUBLIC_API_BASE) {
    return process.env.NEXT_PUBLIC_API_BASE;
  }
  
  const hostname = window.location.hostname;
  const protocol = window.location.protocol;
  
  // GitHub Codespaces
  if (hostname.includes('app.github.dev')) {
    const baseUrl = hostname.replace('-3000.', '-8000.');
    return `${protocol}//${baseUrl}`;
  }
  
  // Local development
  return 'http://localhost:8000';
};

export default function Home() {
  const [apiBase, setApiBase] = useState('http://localhost:8000');
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState('video');
  const [platform, setPlatform] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [info, setInfo] = useState(null);
  const [error, setError] = useState('');
  const [fileId, setFileId] = useState(null);
  const [filename, setFilename] = useState('');

  useEffect(() => {
    setApiBase(getApiBase());
  }, []);

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
    const detectedPlatform = detectPlatform(url);
    setPlatform(detectedPlatform);
    if (!detectedPlatform) {
      setError('Unsupported or invalid URL.');
      return;
    }
    setAnalyzing(true);
    try {
      const res = await axios.post(`${apiBase}/analyze`, { url });
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
      const res = await axios.post(`${apiBase}/download`, { url, mode }, {
        responseType: 'blob'
      });
      
      // Create a download link for the blob
      const blob = new Blob([res.data]);
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = `download.${mode === 'mp3' ? 'mp3' : 'mp4'}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
      
      setFileId('downloaded');
      setFilename(`download.${mode === 'mp3' ? 'mp3' : 'mp4'}`);
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
          <div className="w-full bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mt-2">
            ✅ Download started! Check your downloads folder for {filename}
          </div>
        )}
        {error && <div className="text-red-600 mt-2 text-sm">{error}</div>}
        <div className="text-xs text-gray-500 mt-4 text-center">
          Downloads are for personal use only. Respect copyright laws.
        </div>
      </div>
    </div>
  );
}
