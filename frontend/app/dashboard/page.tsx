const jobs = [
  { id: 1, title: "PDF to LaTeX", status: "Completed", date: "Today" },
  { id: 2, title: "Word to PDF", status: "Processing", date: "Yesterday" },
];

export default function DashboardPage() {
  return (
    <section className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Dashboard</h1>
        <p className="text-sm text-slate-500">Track your recent conversions and downloads.</p>
      </div>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div
            key={job.id}
            className="flex items-center justify-between rounded-2xl border border-slate-200 bg-white p-4"
          >
            <div>
              <p className="font-semibold text-slate-900">{job.title}</p>
              <p className="text-xs text-slate-500">{job.date}</p>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
              {job.status}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
