import Link from "next/link";

interface ToolCardProps {
  title: string;
  description: string;
  href: string;
}

export function ToolCard({ title, description, href }: ToolCardProps) {
  return (
    <Link
      href={href}
      className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:border-primary-500 hover:shadow-lg"
    >
      <h3 className="text-lg font-semibold text-slate-900 group-hover:text-primary-600">
        {title}
      </h3>
      <p className="mt-2 text-sm text-slate-600">{description}</p>
    </Link>
  );
}
