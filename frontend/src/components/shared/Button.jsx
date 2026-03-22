// filepath: src/components/shared/Button.jsx
export default function Button({ variant = 'accent', className = '', ...props }) {
  const btnClass = `btn-${variant} ${className}`;
  return <button className={btnClass} {...props} />;
}
