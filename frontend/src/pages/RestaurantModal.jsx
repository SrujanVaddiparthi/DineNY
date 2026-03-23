import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { getRestaurant, getImageUrl, postComment } from '../api/api';
import Stars from '../components/shared/Stars';
import MapEmbed from '../components/shared/MapEmbed';

export default function RestaurantModal({ restaurantId, onClose }) {
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [commentAuthor, setCommentAuthor] = useState('');
  const [commentText, setCommentText] = useState('');
  const [submitting, setSubmitting] = useState(false);

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

  const handleSubmitComment = async (e) => {
    e.preventDefault();
    if (!commentText.trim()) return;
    try {
      setSubmitting(true);
      const updated = await postComment(restaurantId, commentAuthor.trim(), commentText.trim());
      setRestaurant(prev => prev ? { ...prev, comments: updated } : prev);
      setCommentText('');
    } finally {
      setSubmitting(false);
    }
  };

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
              <img
                className="modal-hero"
                src={getImageUrl(restaurant.primaryImage)}
                alt={restaurant.name}
                onError={e => { e.target.src = 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=60'; }}
              />
              <div className="modal-hero-overlay" />
            </div>

            <div className="modal-body">
              <div className="modal-title-row">
                <h2 className="modal-name">{restaurant.name}</h2>
                <span className="modal-price">{restaurant.cuisine}</span>
              </div>

              <div className="modal-meta">
                <Stars rating={restaurant.rating} />
                <span className="modal-address">📍 {restaurant.address}</span>
                {restaurant.phone && <span className="modal-address">📞 {restaurant.phone}</span>}
              </div>

              <div className="modal-grid">
                {[['🍽️ Cuisine', restaurant.cuisine || 'Various'],
                  ['🌐 Website', restaurant.website || 'Not listed'],
                  ['🏙️ City', restaurant.city || 'Not listed'],
                  ['⭐ Rating', restaurant.rating ?? 'N/A']
                ].map(([label, value]) => (
                  <div key={label} className="modal-info-card">
                    <div className="modal-info-label">{label}</div>
                    <div className="modal-info-value">{value}</div>
                  </div>
                ))}
              </div>

              <MapEmbed lat={rLat} lng={rLng} name={restaurant.name} />

              <div className="modal-description">
                <div className="modal-section-title">Comments</div>
                {restaurant.comments?.length ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    {restaurant.comments.map((c, idx) => (
                      <div key={idx} style={{ padding: '0.65rem 0.75rem', borderRadius: '10px', background: 'var(--surface)', border: '1px solid var(--border)' }}>
                        <div style={{ fontWeight: 600, color: 'var(--navy)' }}>{c.author || 'Anonymous'}</div>
                        <div style={{ color: 'var(--muted)', fontSize: '0.9rem' }}>{c.text}</div>
                        {c.createdAt && <div style={{ color: 'var(--light)', fontSize: '0.75rem', marginTop: '4px' }}>{new Date(c.createdAt).toLocaleString()}</div>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ color: 'var(--muted)' }}>No comments yet.</p>
                )}

                <form onSubmit={handleSubmitComment} style={{ marginTop: '1rem', display: 'grid', gap: '0.6rem' }}>
                  <input
                    className="field"
                    placeholder="Your name (optional)"
                    value={commentAuthor}
                    onChange={e => setCommentAuthor(e.target.value)}
                  />
                  <textarea
                    className="field"
                    rows={3}
                    placeholder="Add a comment"
                    required
                    value={commentText}
                    onChange={e => setCommentText(e.target.value)}
                  />
                  <button className="btn-navy" type="submit" disabled={submitting || !commentText.trim()}>
                    {submitting ? 'Posting…' : 'Post Comment'}
                  </button>
                </form>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );

  return typeof document !== 'undefined' ? createPortal(node, document.body) : node;
}