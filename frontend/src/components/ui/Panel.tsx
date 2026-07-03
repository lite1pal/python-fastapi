import type { PropsWithChildren } from "react";

export function Panel({
  children,
  title,
}: PropsWithChildren<{ title?: string }>) {
  return (
    <section className="rounded-2xl border border-(--color-border) bg-(--color-surface) p-6 shadow-sm backdrop-blur">
      {title ? (
        <h2 className="mb-4 text-lg font-semibold text-(--color-text-primary)">
          {title}
        </h2>
      ) : null}
      {children}
    </section>
  );
}
