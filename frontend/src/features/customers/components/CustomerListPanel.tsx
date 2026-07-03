import { useDeleteCustomer, useCustomers } from "../../../hooks/useCustomers";
import { Message, Panel, QueryState } from "../../../components/ui";
import { CustomerListItem } from "./CustomerListItem";

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
            <CustomerListItem
              key={customer.id}
              customer={customer}
              isArchiving={deleteCustomer.isPending}
              onArchive={deleteCustomer.mutate}
            />
          ))}
        </ul>
      </QueryState>
    </Panel>
  );
}
