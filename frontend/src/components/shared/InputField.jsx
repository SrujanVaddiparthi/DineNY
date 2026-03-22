// filepath: src/components/shared/InputField.jsx
export default function InputField({ className = '', ...props }) {
  return <input className={`field ${className}`} {...props} />;
}
