export function ChatLoadingIndicator() {
  return (
    <div
      className="flex items-center gap-1.5 px-1 py-2"
      aria-label="Assistant is thinking"
      role="status"
      aria-live="polite"
    >
      <span className="sr-only">Assistant is generating a response…</span>
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="h-2 w-2 rounded-full bg-[#38BDF8]/70 animate-bounce"
          style={{ animationDelay: `${i * 0.15}s`, animationDuration: '0.9s' }}
          aria-hidden="true"
        />
      ))}
    </div>
  );
}
