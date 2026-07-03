import type { CustomerResponse } from "../../../api/types";
import { Button } from "../../../components/ui";

type CustomerListItemProps = {
  customer: CustomerResponse;
  isArchiving: boolean;
  onArchive: (customerId: number) => void;
};

export function CustomerListItem({
  customer,
  isArchiving,
  onArchive,
}: CustomerListItemProps) {
  return (
    <li className="flex flex-col gap-4 rounded-2xl border border-(--color-border) bg-(--color-surface-muted) p-4 sm:flex-row sm:items-center sm:justify-between">
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
        onClick={() => onArchive(customer.id)}
        disabled={isArchiving}
      >
        Archive
      </Button>
    </li>
  );
}
