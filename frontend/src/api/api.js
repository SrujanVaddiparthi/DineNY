import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const client = axios.create({ baseURL: API_BASE, withCredentials: false });

const cityFromAddress = (addr = '') => {
  if (!addr) return '';
  const parts = addr.split(',').map(p => p.trim()).filter(Boolean);
  // Prefer second-to-last part, but guard against numeric ZIPs being treated as city
  if (parts.length >= 2) {
    const candidate = parts[parts.length - 2];
    return candidate;
  }
  return parts[0] || '';
};

const toNum = (v) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
};

const normalizeSearchResult = (r) => ({
  _id: r.id,
  name: r.title || 'Untitled',
  cuisine: r.category || 'Unspecified',
  address: r.address || 'Address not provided',
  city: cityFromAddress(r.address || ''),
  rating: r.rating ?? 0,
  latitude: toNum(r.latitude ?? (r.location?.coordinates?.[1])),
  longitude: toNum(r.longitude ?? (r.location?.coordinates?.[0])),
  distanceMeters: r.distance_meters,
});

const normalizeDetail = (r) => {
  const lat = toNum(r.latitude ?? (r.location?.coordinates?.[1]));
  const lon = toNum(r.longitude ?? (r.location?.coordinates?.[0]));
  return {
    _id: r.id,
    name: r.title || 'Untitled',
    cuisine: r.category || 'Unspecified',
    rating: r.rating ?? 0,
    address: r.address || 'Address not provided',
    city: cityFromAddress(r.address || ''),
    phone: r.phone || '',
    website: r.website || '',
    primaryImage: r.primary_image_src || r.image_urls?.[0]?.thumbnail || null,
    location: r.location || (lat && lon ? { type: 'Point', coordinates: [lon, lat] } : null),
    latitude: lat,
    longitude: lon,
    comments: (r.comments || []).map(c => ({
      author: c.author || 'Anonymous',
      text: c.text || '',
      createdAt: c.created_at || c.createdAt || '',
    })),
  };
};

export async function searchRestaurants(q, minRating, maxRating) {
  const params = { q: q || '' };
  if (minRating != null && minRating !== '') params.min_rating = minRating;
  if (maxRating != null && maxRating !== '') params.max_rating = maxRating;
  const { data } = await client.get('/api/search', { params });
  return (data?.results || []).map(normalizeSearchResult);
}

export async function searchGeo(q, lat, lng, radiusMiles = 10, minRating, maxRating) {
  const params = {
    q: q || '',
    lat,
    lon: lng,
    radius: Math.round(radiusMiles * 1609.34),
  };
  if (minRating != null && minRating !== '') params.min_rating = minRating;
  if (maxRating != null && maxRating !== '') params.max_rating = maxRating;
  const { data } = await client.get('/api/search', { params });
  return (data?.results || []).map(normalizeSearchResult);
}

export async function getRestaurant(id) {
  const { data } = await client.get(`/api/restaurants/${id}`);
  return normalizeDetail(data);
}

export function getImageUrl(url) {
  return url || '';
}

export async function postComment(restaurantId, author, text) {
  const payload = { author: author || 'Anonymous', text };
  const { data } = await client.post(`/api/restaurants/${restaurantId}/comments`, payload);
  return (data?.comments || []).map(c => ({
    author: c.author || 'Anonymous',
    text: c.text || '',
    createdAt: c.created_at || c.createdAt || '',
  }));
}