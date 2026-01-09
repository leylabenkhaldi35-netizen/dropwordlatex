export default function AccountPage() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Account settings</h1>
        <p className="text-sm text-slate-500">Manage your subscription and profile details.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-slate-900">Plan</h2>
          <p className="mt-2 text-sm text-slate-500">Free plan · 20 MB uploads</p>
          <button className="mt-4 rounded-full bg-primary-600 px-4 py-2 text-sm font-semibold text-white">
            Upgrade to Premium
          </button>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-lg font-semibold text-slate-900">Security</h2>
          <p className="mt-2 text-sm text-slate-500">Update password and session preferences.</p>
          <button className="mt-4 rounded-full border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700">
            Update password
          </button>
        </div>
      </div>
    </section>
  );
}
