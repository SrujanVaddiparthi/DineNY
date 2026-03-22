import { useState } from 'react';
import SearchPage  from './pages/Search';
import ResultsList from './pages/ResultsList';
import './index.css';

export default function App() {
  const [view, setView] = useState('search');
  const [search, setSearch] = useState({ query: '', lat: null, lng: null, radius: 10 });

  const goSearch = (q)                    => { setSearch({ query: q, lat: null, lng: null, radius: 10 }); setView('results'); };
  const goGeo    = (q, lat, lng, radius)  => { setSearch({ query: q, lat, lng, radius }); setView('results'); };

  return (
    <>
      {view === 'search'
        ? <SearchPage onSearch={goSearch} onGeoSearch={goGeo} />
        : <ResultsList {...search} onBack={() => setView('search')} onNewSearch={goSearch} />
      }
    </>
  );
}