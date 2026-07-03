import { useAuthMe } from "../../../hooks/useAuth";
import { Message, Panel } from "../../../components/ui";

export function AuthUserPanel() {
  const auth = useAuthMe();

  return (
    <Panel title="Authenticated user">
      {auth.isLoading ? <Message>Loading user...</Message> : null}
      {auth.error ? <Message tone="error">{auth.error.message}</Message> : null}
      {auth.data ? (
        <pre className="overflow-auto rounded-xl bg-(--color-surface-strong) p-4 text-sm text-(--color-text-inverse)">
          {JSON.stringify(auth.data, null, 2)}
        </pre>
      ) : null}
    </Panel>
  );
}
