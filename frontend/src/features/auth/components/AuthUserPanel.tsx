import { useAuthMe } from "../../../hooks/useAuth";
import { Panel, QueryState } from "../../../components/ui";

export function AuthUserPanel() {
  const auth = useAuthMe();

  return (
    <Panel title="Authenticated user">
      <QueryState
        error={auth.error}
        isEmpty={!auth.data}
        isLoading={auth.isLoading}
        loadingMessage="Loading user..."
      >
        <pre className="overflow-auto rounded-xl bg-(--color-surface-strong) p-4 text-sm text-(--color-text-inverse)">
          {JSON.stringify(auth.data, null, 2)}
        </pre>
      </QueryState>
    </Panel>
  );
}
