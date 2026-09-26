import type { Components } from 'react-markdown';

/** Tailwind-styled renderers shared by chat answers and the source viewer. */
export const markdownComponents: Components = {
  // Headings
  h1: ({ children }) => (
    <h1 className="mb-3 mt-4 text-lg font-bold text-[#F8FAFC] first:mt-0">{children}</h1>
  ),
  h2: ({ children }) => (
    <h2 className="mb-2 mt-4 text-base font-semibold text-[#F8FAFC] first:mt-0">{children}</h2>
  ),
  h3: ({ children }) => (
    <h3 className="mb-1.5 mt-3 text-sm font-semibold text-[#F8FAFC] first:mt-0">{children}</h3>
  ),
  // Paragraph
  p: ({ children }) => (
    <p className="mb-2 last:mb-0">{children}</p>
  ),
  // Lists
  ul: ({ children }) => (
    <ul className="mb-2 ml-4 list-disc space-y-1">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="mb-2 ml-4 list-decimal space-y-1">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="text-[#F8FAFC]">{children}</li>
  ),
  // Blockquote
  blockquote: ({ children }) => (
    <blockquote className="my-2 border-l-2 border-[#38BDF8]/40 pl-3 text-[#94A3B8] italic">
      {children}
    </blockquote>
  ),
  // Inline code
  code: ({ children, className }) => {
    const isBlock = className?.includes('language-');
    if (isBlock) {
      return (
        <code className={className}>
          {children}
        </code>
      );
    }
    return (
      <code className="rounded bg-[#0F2138] px-1.5 py-0.5 font-mono text-xs text-[#38BDF8]">
        {children}
      </code>
    );
  },
  // Code block wrapper
  pre: ({ children }) => (
    <pre className="my-3 overflow-x-auto rounded-xl border border-[#28415D] bg-[#081426] p-4 font-mono text-xs leading-relaxed text-[#94A3B8]">
      {children}
    </pre>
  ),
  // Table
  table: ({ children }) => (
    <div className="my-3 overflow-x-auto rounded-xl border border-[#28415D]">
      <table className="w-full text-xs">{children}</table>
    </div>
  ),
  thead: ({ children }) => (
    <thead className="border-b border-[#28415D] bg-[#0F2138]">{children}</thead>
  ),
  tbody: ({ children }) => <tbody>{children}</tbody>,
  tr: ({ children }) => (
    <tr className="border-b border-[#28415D]/50 last:border-0">{children}</tr>
  ),
  th: ({ children }) => (
    <th className="px-3 py-2 text-left font-semibold text-[#94A3B8]">{children}</th>
  ),
  td: ({ children }) => (
    <td className="px-3 py-2 text-[#F8FAFC]">{children}</td>
  ),
  // Links — open in new tab, sanitised by no javascript: hrefs
  a: ({ href, children }) => {
    const safe = href?.startsWith('http') || href?.startsWith('/') || href?.startsWith('mailto:');
    return safe ? (
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-[#38BDF8] underline decoration-[#38BDF8]/40 hover:decoration-[#38BDF8]"
      >
        {children}
      </a>
    ) : (
      <span className="text-[#38BDF8]">{children}</span>
    );
  },
  // Strong / em
  strong: ({ children }) => (
    <strong className="font-semibold text-[#F8FAFC]">{children}</strong>
  ),
  em: ({ children }) => (
    <em className="italic text-[#94A3B8]">{children}</em>
  ),
  // HR separator
  hr: () => <hr className="my-4 border-[#28415D]" />,
};
