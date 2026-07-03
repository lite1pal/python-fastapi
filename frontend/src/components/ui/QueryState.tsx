import type { PropsWithChildren, ReactNode } from "react";

import { Message } from "@/components/ui/Message";

type QueryStateProps = PropsWithChildren<{
  empty?: ReactNode;
  error?: Error | null;
  isEmpty?: boolean;
  isLoading?: boolean;
  loadingMessage?: string;
}>;

export function QueryState({
  children,
  empty = null,
  error,
  isEmpty = false,
  isLoading = false,
  loadingMessage = "Loading...",
}: QueryStateProps) {
  if (isLoading) {
    return <Message>{loadingMessage}</Message>;
  }

  if (error) {
    return <Message tone="error">{error.message}</Message>;
  }

  if (isEmpty) {
    return <>{empty}</>;
  }

  return <>{children}</>;
}
