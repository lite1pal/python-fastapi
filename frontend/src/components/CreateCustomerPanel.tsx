import { useForm } from "react-hook-form";

import { useCreateCustomer } from "../hooks/useCustomers";
import type { CustomerStatus } from "../api/types";
import { Button, Field, Input, Message, Panel, Select, Textarea } from "./ui";

type CreateCustomerFormValues = {
  name: string;
  email: string;
  company: string;
  status: CustomerStatus;
  notes: string;
};

const initialForm: CreateCustomerFormValues = {
  name: "",
  email: "",
  company: "",
  status: "lead",
  notes: "",
};

export function CreateCustomerPanel() {
  const createCustomer = useCreateCustomer();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateCustomerFormValues>({
    defaultValues: initialForm,
  });

  function onSubmit(values: CreateCustomerFormValues) {
    createCustomer.mutate(
      {
        ...values,
        company: values.company || null,
        notes: values.notes || null,
      },
      {
        onSuccess: () => reset(initialForm),
      },
    );
  }

  return (
    <Panel title="Create customer">
      <form className="grid gap-3" onSubmit={handleSubmit(onSubmit)}>
        <Field>
          <Input
            placeholder="Name *"
            aria-invalid={errors.name ? "true" : "false"}
            {...register("name", {
              required: "Name is required.",
              validate: (value) =>
                value.trim().length > 0 || "Name is required.",
            })}
          />
          {errors.name ? <Message tone="error">{errors.name.message}</Message> : null}
        </Field>
        <Field>
          <Input
            placeholder="Email *"
            type="email"
            aria-invalid={errors.email ? "true" : "false"}
            {...register("email", {
              required: "Email is required.",
              pattern: {
                value: /\S+@\S+\.\S+/,
                message: "Enter a valid email address.",
              },
            })}
          />
          {errors.email ? (
            <Message tone="error">{errors.email.message}</Message>
          ) : null}
        </Field>
        <Field>
          <Input placeholder="Company" {...register("company")} />
        </Field>
        <Field>
          <Select {...register("status")}>
            <option value="lead">lead</option>
            <option value="active">active</option>
            <option value="archived">archived</option>
          </Select>
        </Field>
        <Field>
          <Textarea placeholder="Notes" {...register("notes")} />
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
