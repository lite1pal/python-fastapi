import type { PropsWithChildren } from "react";

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
