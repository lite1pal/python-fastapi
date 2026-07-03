import { useState } from "react";

import { useAuthMe } from "./hooks/useAuth";
import {
  useCreateCustomer,
  useCustomers,
  useDeleteCustomer,
} from "./hooks/useCustomers";
import type { CustomerStatus } from "./api/types";

const initialForm = {
  name: "",
  email: "",
  company: "",
  status: "lead" as CustomerStatus,
  notes: "",
};

export function App() {
  const [form, setForm] = useState(initialForm);
  const auth = useAuthMe();
  const customers = useCustomers();
  const createCustomer = useCreateCustomer();
  const deleteCustomer = useDeleteCustomer();

  return (
    <main className="page">
      <section className="panel">
        <p className="eyebrow">FastAPI + React</p>
        <h1>Customer dashboard scaffold</h1>
        <p className="lede">
          Typed hooks are wired for the customer API and bearer-authenticated
          user lookup.
        </p>
      </section>

      <section className="panel">
        <h2>Authenticated user</h2>
        {auth.isLoading ? <p>Loading user...</p> : null}
        {auth.error ? <p>{auth.error.message}</p> : null}
        {auth.data ? (
          <pre>{JSON.stringify(auth.data, null, 2)}</pre>
        ) : null}
      </section>

      <section className="panel">
        <h2>Create customer</h2>
        <form
          className="form"
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
          <input
            placeholder="Name"
            value={form.name}
            onChange={(event) =>
              setForm((current) => ({ ...current, name: event.target.value }))
            }
          />
          <input
            placeholder="Email"
            type="email"
            value={form.email}
            onChange={(event) =>
              setForm((current) => ({ ...current, email: event.target.value }))
            }
          />
          <input
            placeholder="Company"
            value={form.company}
            onChange={(event) =>
              setForm((current) => ({
                ...current,
                company: event.target.value,
              }))
            }
          />
          <select
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
          </select>
          <textarea
            placeholder="Notes"
            value={form.notes}
            onChange={(event) =>
              setForm((current) => ({ ...current, notes: event.target.value }))
            }
          />
          <button type="submit" disabled={createCustomer.isPending}>
            {createCustomer.isPending ? "Saving..." : "Create customer"}
          </button>
        </form>
        {createCustomer.error ? <p>{createCustomer.error.message}</p> : null}
      </section>

      <section className="panel">
        <h2>Customers</h2>
        {customers.isLoading ? <p>Loading customers...</p> : null}
        {customers.error ? <p>{customers.error.message}</p> : null}
        <ul className="list">
          {customers.data?.map((customer) => (
            <li key={customer.id} className="listItem">
              <div>
                <strong>{customer.name}</strong>
                <p>{customer.email}</p>
                <p>{customer.status}</p>
              </div>
              <button
                type="button"
                onClick={() => deleteCustomer.mutate(customer.id)}
                disabled={deleteCustomer.isPending}
              >
                Archive
              </button>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
