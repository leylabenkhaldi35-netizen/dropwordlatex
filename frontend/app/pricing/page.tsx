const plans = [
  {
    title: "Free",
    price: "$0",
    description: "For light conversions and quick experiments.",
    features: ["20 MB max file size", "Up to 5 conversions per day", "Community support"],
  },
  {
    title: "Premium",
    price: "$19",
    description: "Unlimited conversions for research teams.",
    features: ["200 MB max file size", "Unlimited conversions", "Priority support"],
  },
];

export default function PricingPage() {
  return (
    <section className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Pricing</h1>
        <p className="mt-2 text-slate-600">
          Simple subscriptions with PayPal or credit card billing.
        </p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        {plans.map((plan) => (
          <div key={plan.title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">{plan.title}</h2>
            <p className="mt-2 text-3xl font-bold text-primary-600">{plan.price}</p>
            <p className="mt-2 text-sm text-slate-500">{plan.description}</p>
            <ul className="mt-4 space-y-2 text-sm text-slate-600">
              {plan.features.map((feature) => (
                <li key={feature}>• {feature}</li>
              ))}
            </ul>
            <button className="mt-6 w-full rounded-full bg-primary-600 px-4 py-2 text-sm font-semibold text-white">
              Choose {plan.title}
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}
