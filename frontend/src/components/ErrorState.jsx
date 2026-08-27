export default function ErrorState({ title = "Something went wrong", message }) {
  return (
    <div className="error-state">
      <h2>{title}</h2>
      <p>{message || "Please try again."}</p>
    </div>
  );
}
