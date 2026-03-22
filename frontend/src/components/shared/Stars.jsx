// filepath: src/components/shared/Stars.jsx
export default function Stars({ rating }) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5;
  return (
    <span>
      <span className="stars">{'★'.repeat(full)}{half ? '½' : ''}{'☆'.repeat(5 - full - (half ? 1 : 0))}</span>
      <span className="stars-num"> {rating.toFixed(1)}</span>
    </span>
  );
}
