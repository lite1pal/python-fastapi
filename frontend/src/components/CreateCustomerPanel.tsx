import { useState } from "react";

import { useCreateCustomer } from "../hooks/useCustomers";
import type { CustomerStatus } from "../api/types";
import { Button, Field, Input, Message, Panel, Select, Textarea } from "./ui";

const initialForm = {
  name: "",
  email: "",
  company: "",
  status: "lead" as CustomerStatus,
  notes: "",
};

export function CreateCustomerPanel() {
  const [form, setForm] = useState(initialForm);
  const createCustomer = useCreateCustomer();

  return (
    <Panel title="Create customer">
      <form
        className="grid gap-3"
        onSubmit={(event) => {
          event.preventDefault();
          createCustomer.mutate(
            {
              ...form,
              company: form.company || null,
              notes: form.notes || null,
            },
            {
              onSuccess: () => setForm(initialForm),
            },
          );
        }}
      >
        <Field>
          <Input
            placeholder="Name"
            value={form.name}
            onChange={(event) =>
              setForm((current) => ({ ...current, name: event.target.value }))
            }
          />
        </Field>
        <Field>
          <Input
            placeholder="Email"
            type="email"
            value={form.email}
            onChange={(event) =>
              setForm((current) => ({ ...current, email: event.target.value }))
            }
          />
        </Field>
        <Field>
          <Input
            placeholder="Company"
            value={form.company}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                company: event.target.value,
              }))
            }
          />
        </Field>
        <Field>
          <Select
            value={form.status}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                status: event.target.value as CustomerStatus,
              }))
            }
          >
            <option value="lead">lead</option>
            <option value="active">active</option>
            <option value="archived">archived</option>
          </Select>
        </Field>
        <Field>
          <Textarea
            placeholder="Notes"
            value={form.notes}
            onChange={(event) =>
              setForm((current) => ({ ...current, notes: event.target.value }))
            }
          />
        </Field>
        <div className="flex items-center gap-3">
          <Button type="submit" disabled={createCustomer.isPending}>
            {createCustomer.isPending ? "Saving..." : "Create customer"}
          </Button>
          {createCustomer.error ? (
            <Message tone="error">{createCustomer.error.message}</Message>
          ) : null}
        </div>
      </form>
    </Panel>
  );
}
