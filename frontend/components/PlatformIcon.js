export default function PlatformIcon({ platform }) {
  if (platform === 'youtube') return <span title="YouTube">▶️</span>;
  if (platform === 'instagram') return <span title="Instagram">📸</span>;
  if (platform === 'whatsapp') return <span title="WhatsApp">🟢</span>;
  return <span className="text-gray-300">❓</span>;
}
