import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  PropsWithChildren,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";

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

export function Field({ children }: PropsWithChildren) {
  return <div className="grid gap-2">{children}</div>;
}

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className="w-full rounded-xl border border-(--color-border-strong) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text-primary) outline-none transition focus:border-(--color-text-muted) aria-[invalid=true]:border-[color:var(--color-text-error)]"
    />
  );
}

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className="w-full rounded-xl border border-(--color-border-strong) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text-primary) outline-none transition focus:border-(--color-text-muted) aria-[invalid=true]:border-[color:var(--color-text-error)]"
    />
  );
}

export function Textarea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className="min-h-28 w-full rounded-xl border border-(--color-border-strong) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text-primary) outline-none transition focus:border-(--color-text-muted) aria-[invalid=true]:border-[color:var(--color-text-error)]"
    />
  );
}

export function Button(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      className="rounded-xl bg-(--color-action) px-4 py-2 text-sm font-medium text-(--color-text-inverse) transition hover:bg-(--color-action-hover) disabled:cursor-not-allowed disabled:bg-(--color-action-disabled)"
    />
  );
}

export function Message({
  children,
  tone = "muted",
}: PropsWithChildren<{ tone?: "muted" | "error" }>) {
  const className =
    tone === "error"
      ? "text-sm text-[color:var(--color-text-error)]"
      : "text-sm text-[color:var(--color-text-muted)]";

  return <p className={className}>{children}</p>;
}
