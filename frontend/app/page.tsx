import { ToolCard } from "../components/ToolCard";

const tools = [
  {
    title: "PDF to LaTeX",
    description: "Extract equations and structure into editable LaTeX.",
    href: "/tools/pdf-to-latex",
  },
  {
    title: "Word to LaTeX",
    description: "Convert Word documents into clean LaTeX source.",
    href: "/tools/word-to-latex",
  },
  {
    title: "LaTeX to PDF",
    description: "Compile LaTeX into high-quality PDFs.",
    href: "/tools/latex-to-pdf",
  },
  {
    title: "LaTeX to Word",
    description: "Turn LaTeX into professional Word documents.",
    href: "/tools/latex-to-word",
  },
  {
    title: "PDF to Word",
    description: "Convert PDFs into editable Word documents.",
    href: "/tools/pdf-to-word",
  },
  {
    title: "Word to PDF",
    description: "Export Word files to secure PDFs.",
    href: "/tools/word-to-pdf",
  },
];

export default function HomePage() {
  return (
    <div className="space-y-12">
      <section className="rounded-3xl bg-gradient-to-r from-primary-600 to-rose-500 px-10 py-14 text-white shadow-xl">
        <h1 className="text-3xl font-bold md:text-4xl">LaTeX conversions made effortless.</h1>
        <p className="mt-4 max-w-2xl text-sm text-rose-50">
          ILoveLaTeX brings Word, PDF, and LaTeX conversions together with secure processing,
          progress tracking, and production-grade workflows for academics and professionals.
        </p>
      </section>

      <section>
        <h2 className="text-xl font-semibold text-slate-900">Choose your tool</h2>
        <div className="mt-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {tools.map((tool) => (
            <ToolCard key={tool.title} {...tool} />
          ))}
        </div>
      </section>
    </div>
  );
}
