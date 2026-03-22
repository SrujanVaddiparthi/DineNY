import { useState, useEffect } from 'react';
import { searchRestaurants, searchGeo } from '../api/api';
import Stars from '../components/shared/Stars';
import RestaurantModal from './RestaurantModal';

function SkeletonRows() {
  return Array.from({ length: 5 }).map((_, i) => (
    <tr key={i} className="skeleton">
      {[140, 160, 80, 90, 60, 70].map((w, j) => (
        <td key={j}><div className="skeleton-bar" style={{ width: w }} /></td>
      ))}
    </tr>
  ));
}

export default function ResultsList({ query, lat, lng, radius, onBack, onNewSearch }) {
  const [results,    setResults]    = useState([]);
  const [loading,    setLoading]    = useState(true);
  const [selectedId, setSelectedId] = useState(null);
  const [searchInput, setSearchInput] = useState(query || '');

  useEffect(() => {
    setLoading(true);
    const fetch = (lat != null && lng != null)
      ? searchGeo(query, lat, lng, radius || 10)
      : searchRestaurants(query);
    fetch.then(data => { setResults(data); setLoading(false); });
  }, [query, lat, lng, radius]);

  const handleInlineSearch = (e) => {
    e.preventDefault();
    searchInput.trim() && onNewSearch(searchInput.trim());
  };

  return (
    <main className="results-page">
      <div className="results-header">
        <div>
          <h2 className="results-heading">
            Results for <em>"{query}"</em>
            {lat != null && <span style={{ fontSize: '1rem', fontStyle: 'normal', color: 'var(--muted)' }}> near selected area</span>}
          </h2>
          <p className="results-count">
            {loading ? 'Searching…' : `${results.length} restaurant${results.length !== 1 ? 's' : ''} found`}
          </p>
        </div>
        <button className="back-btn" onClick={onBack}>
          <svg width="14" height="14" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd"/>
          </svg>
          Back / New Search
        </button>
      </div>

      <div className="results-search-bar">
        <form onSubmit={handleInlineSearch}>
          <div className="results-input-group">
            <span className="results-search-icon">
              <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd"/>
              </svg>
            </span>
            <input className="results-search-input" value={searchInput} onChange={e => setSearchInput(e.target.value)} placeholder="Refine your search…" />
            <button className="results-search-btn" type="submit">Search</button>
          </div>
        </form>
      </div>

      <div className="grid-wrap">
        {!loading && results.length === 0 ? (
          <div className="empty">
            <div className="empty-icon">🍽️</div>
            <h3>No restaurants found for "{query}"</h3>
            <p>Try a broader term — e.g. "pizza" instead of "deep dish pizza"</p>
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                {['Restaurant', 'Address', 'City', 'Cuisine', 'Rating', 'Actions'].map(h => (
                  <th key={h}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading
                ? <SkeletonRows />
                : results.map(r => (
                  <tr key={r._id} onClick={() => setSelectedId(r._id)}>
                    <td className="td-name">{r.name}</td>
                    <td className="td-muted">{r.address}</td>
                    <td className="td-muted">{r.city}</td>
                    <td><span className="tag">{r.cuisine.split(',')[0].trim()}</span></td>
                    <td><Stars rating={r.rating} /></td>
                    <td onClick={e => e.stopPropagation()}>
                      <button className="view-btn" onClick={() => setSelectedId(r._id)}>View →</button>
                    </td>
                  </tr>
                ))
              }
            </tbody>
          </table>
        )}
      </div>

      {selectedId && <RestaurantModal restaurantId={selectedId} onClose={() => setSelectedId(null)} />}
    </main>
  );
}