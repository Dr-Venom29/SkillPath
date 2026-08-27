export default function ErrorState({ message }) {
  return (
    <div className="error-state">
      <h2>Something went wrong</h2>
      <p>{message || 'Unable to connect to SkillPath right now. Please try again.'}</p>
    </div>
  );
}
