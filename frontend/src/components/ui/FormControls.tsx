import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  PropsWithChildren,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";

const baseControlClassName =
  "w-full rounded-xl border border-(--color-border-strong) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text-primary) outline-none transition focus:border-(--color-text-muted) aria-[invalid=true]:border-[color:var(--color-text-error)]";

export function Field({ children }: PropsWithChildren) {
  return <div className="grid gap-2">{children}</div>;
}

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={baseControlClassName} />;
}

export function Select(props: SelectHTMLAttributes<HTMLSelectElement>) {
  return <select {...props} className={baseControlClassName} />;
}

export function Textarea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={`min-h-28 ${baseControlClassName}`}
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
