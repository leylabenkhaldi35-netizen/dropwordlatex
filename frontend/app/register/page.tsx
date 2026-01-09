export default function RegisterPage() {
  return (
    <section className="mx-auto max-w-md space-y-6 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="text-2xl font-semibold text-slate-900">Create your account</h1>
      <form className="space-y-4">
        <label className="block text-sm font-medium text-slate-700">
          Email
          <input
            type="email"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
            placeholder="you@example.com"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Password
          <input
            type="password"
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
            placeholder="••••••••"
          />
        </label>
        <button className="w-full rounded-full bg-primary-600 px-4 py-2 text-sm font-semibold text-white">
          Create account
        </button>
      </form>
      <p className="text-sm text-slate-500">Already have an account? Sign in.</p>
    </section>
  );
}
