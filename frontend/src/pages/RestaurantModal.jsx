import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { getRestaurant, getImageUrl } from '../api/api';
import Stars from '../components/shared/Stars';
import MapEmbed from '../components/shared/MapEmbed';

export default function RestaurantModal({ restaurantId, onClose }) {
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getRestaurant(restaurantId).then(data => {
      setRestaurant(data || null);
      setLoading(false);
    });
  }, [restaurantId]);

  useEffect(() => {
    const handler = e => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  const [rLng, rLat] = restaurant?.location?.coordinates || [-74.006, 40.7128];

  const node = (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-modal="true">
        <button className="modal-close" onClick={onClose} type="button">✕</button>

        {loading ? (
          <div className="modal-loading">Loading…</div>
        ) : !restaurant ? (
          <div className="modal-loading">Restaurant not found.</div>
        ) : (
          <>
            <div className="modal-hero-wrap">
              <img className="modal-hero" src={getImageUrl(restaurant.imageId)} alt={restaurant.name}
                onError={e => { e.target.src = 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=60'; }} />
              <div className="modal-hero-overlay" />
            </div>

            <div className="modal-body">
              <div className="modal-title-row">
                <h2 className="modal-name">{restaurant.name}</h2>
                <span className="modal-price">{restaurant.priceRange}</span>
              </div>

              <div className="modal-meta">
                <Stars rating={restaurant.rating} />
                <span className="tag">{restaurant.cuisine.split(',')[0]}</span>
                <span className="modal-address">📍 {restaurant.address}, {restaurant.city}, {restaurant.state}</span>
              </div>

              <div className="modal-grid">
                {[['🕐 Hours', restaurant.hours || 'Not listed'],
                  ['📞 Phone', restaurant.phone || 'Not listed'],
                  ['🍽️ Cuisine', restaurant.cuisine || 'Various'],
                  ['🏙️ City', `${restaurant.city}, NY`] 
                ].map(([label, value]) => (
                  <div key={label} className="modal-info-card">
                    <div className="modal-info-label">{label}</div>
                    <div className="modal-info-value">{value}</div>
                  </div>
                ))}
              </div>

              <MapEmbed lat={rLat} lng={rLng} name={restaurant.name} />

              {restaurant.description && (
                <div className="modal-description">
                  <div className="modal-section-title">About</div>
                  <p>{restaurant.description}</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );

  return typeof document !== 'undefined' ? createPortal(node, document.body) : node;
}