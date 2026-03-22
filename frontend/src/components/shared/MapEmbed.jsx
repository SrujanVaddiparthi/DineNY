// filepath: src/components/shared/MapEmbed.jsx
const MAPS_KEY = 'YOUR_GOOGLE_MAPS_API_KEY';

export default function MapEmbed({ lat, lng, name }) {
  const src = (!MAPS_KEY || MAPS_KEY === 'YOUR_GOOGLE_MAPS_API_KEY')
    ? `https://www.openstreetmap.org/export/embed.html?bbox=${lng-.01}%2C${lat-.01}%2C${lng+.01}%2C${lat+.01}&layer=mapnik&marker=${lat}%2C${lng}`
    : `https://www.google.com/maps/embed/v1/place?key=${MAPS_KEY}&q=${lat},${lng}&zoom=15`;
  
  return (
    <div className="modal-map">
      <iframe title={`Map of ${name}`} src={src} loading="lazy" allowFullScreen referrerPolicy="no-referrer-when-downgrade" />
    </div>
  );
}
