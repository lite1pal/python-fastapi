import { useDeleteCustomer, useCustomers } from "../../../hooks/useCustomers";
import { Button, Message, Panel, QueryState } from "../../../components/ui";

export function CustomerListPanel() {
  const customers = useCustomers();
  const deleteCustomer = useDeleteCustomer();

  return (
    <Panel title="Customers">
      <QueryState
        empty={<Message>No customers yet.</Message>}
        error={customers.error}
        isEmpty={customers.data?.length === 0}
        isLoading={customers.isLoading}
        loadingMessage="Loading customers..."
      >
        <ul className="grid list-none gap-3 p-0">
          {customers.data?.map((customer) => (
            <li
              key={customer.id}
              className="flex flex-col gap-4 rounded-2xl border border-(--color-border) bg-(--color-surface-muted) p-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <div>
                <strong className="text-sm font-semibold text-(--color-text-primary)">
                  {customer.name}
                </strong>
                <p className="mt-1 text-sm text-(--color-text-secondary)">
                  {customer.email}
                </p>
                <p className="mt-1 text-xs uppercase tracking-wide text-(--color-text-muted)">
                  {customer.status}
                </p>
              </div>
              <Button
                type="button"
                onClick={() => deleteCustomer.mutate(customer.id)}
                disabled={deleteCustomer.isPending}
              >
                Archive
              </Button>
            </li>
          ))}
        </ul>
      </QueryState>
    </Panel>
  );
}
