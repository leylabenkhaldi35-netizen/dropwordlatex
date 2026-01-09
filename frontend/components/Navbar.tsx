import Link from "next/link";

export function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-xl font-bold text-primary-600">
          ILoveLaTeX
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
          <Link href="/pricing">Pricing</Link>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/account">Account</Link>
          <Link
            href="/login"
            className="rounded-full bg-primary-600 px-4 py-2 text-white hover:bg-primary-500"
          >
            Sign In
          </Link>
        </nav>
      </div>
    </header>
  );
}
