import type {
  ButtonHTMLAttributes,
  InputHTMLAttributes,
  ReactElement,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from "react";
import { cloneElement, isValidElement } from "react";

import { Message } from "@/components/ui/Message";

const baseControlClassName =
  "w-full rounded-xl border border-(--color-border-strong) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text-primary) outline-none transition focus:border-(--color-text-muted) aria-[invalid=true]:border-[color:var(--color-text-error)]";

type FormControlElementProps = {
  "aria-describedby"?: string;
  "aria-invalid"?: "false" | "true";
  id?: string;
};

type FormFieldProps = {
  children: ReactElement<FormControlElementProps>;
  error?: string;
  id: string;
  label: string;
  required?: boolean;
};

export function FormField({
  children,
  error,
  id,
  label,
  required = false,
}: FormFieldProps) {
  const errorId = `${id}-error`;

  if (!isValidElement(children)) {
    return null;
  }

  const control = cloneElement(children, {
    "aria-describedby": error ? errorId : undefined,
    "aria-invalid": error ? "true" : "false",
    id,
  });

  return (
    <div className="grid gap-2">
      <label
        className="text-sm font-medium text-(--color-text-primary)"
        htmlFor={id}
      >
        {label}
        {required ? <span className="text-[color:var(--color-text-error)]"> *</span> : null}
      </label>
      {control}
      {error ? (
        <Message tone="error">
          <span id={errorId}>{error}</span>
        </Message>
      ) : null}
    </div>
  );
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
