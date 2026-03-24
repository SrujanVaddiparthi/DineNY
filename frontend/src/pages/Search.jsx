import { useState } from 'react';

export default function SearchPage({ onSearch, onGeoSearch }) {
  const [query, setQuery] = useState('');
  const [minRating, setMinRating] = useState('');
  const [maxRating, setMaxRating] = useState('');

  const submit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSearch(query.trim(), minRating || null, maxRating || null);
  };

  return (
    <main className="search-page">
      <div className="hero">
        <div className="brand-mark">DineNY</div>
        <span className="eyebrow">NY State Restaurant Search</span>
        <h1 className="title">Find your next great <em>meal</em></h1>
        <p className="subtitle">Search thousands of restaurants across New York State</p>
      </div>

      <div className="form-wrap">
        <form onSubmit={submit}>
          <div className="input-group">
            <span className="search-icon">
              <svg viewBox="0 0 20 20" fill="currentColor" width="18" height="18">
                <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd"/>
              </svg>
            </span>
            <input
              className="search-input"
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Search by name, cuisine, city… (e.g. pizza, halal, sushi)"
              autoFocus
            />
            <button className="search-button" type="submit">Search</button>
          </div>
        </form>
        <div className="filter-row">
          <div className="filter-field">
            <label>Min rating</label>
            <input
              type="number"
              min="0"
              max="5"
              step="0.1"
              className="field"
              value={minRating}
              onChange={e => setMinRating(e.target.value)}
              placeholder="e.g. 3.5"
            />
          </div>
          <div className="filter-field">
            <label>Max rating</label>
            <input
              type="number"
              min="0"
              max="5"
              step="0.1"
              className="field"
              value={maxRating}
              onChange={e => setMaxRating(e.target.value)}
              placeholder="e.g. 5"
            />
          </div>
        </div>
      </div>
    </main>
  );
}