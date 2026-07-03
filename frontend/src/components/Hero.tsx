import { Panel } from "@/components/ui";

export function Hero() {
  return (
    <Panel>
      <p className="mb-2 text-xs font-medium uppercase tracking-[0.18em] text-(--color-text-muted)">
        FastAPI + React
      </p>
      <h1 className="text-3xl font-semibold tracking-tight text-(--color-text-primary)">
        Customer dashboard scaffold
      </h1>
      <p className="mt-3 max-w-2xl text-sm leading-6 text-(--color-text-secondary)">
        Minimal typed frontend wired to the FastAPI customer API, bearer auth,
        and TanStack Query hooks.
      </p>
    </Panel>
  );
}
