import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { useCreateCustomer } from "../hooks/useCustomers";
import type { CustomerStatus } from "../api/types";
import { Button, Field, Input, Message, Panel, Select, Textarea } from "./ui";

const customerStatuses = ["lead", "active", "archived"] as const satisfies readonly CustomerStatus[];

const createCustomerSchema = z.object({
  name: z.string().trim().min(1, "Name is required."),
  email: z
    .string()
    .trim()
    .min(1, "Email is required.")
    .email("Enter a valid email address."),
  company: z.string(),
  status: z.enum(customerStatuses),
  notes: z.string(),
});

type CreateCustomerFormValues = z.infer<typeof createCustomerSchema>;

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
    resolver: zodResolver(createCustomerSchema),
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
            {...register("name")}
          />
          {errors.name ? <Message tone="error">{errors.name.message}</Message> : null}
        </Field>
        <Field>
          <Input
            placeholder="Email *"
            type="email"
            aria-invalid={errors.email ? "true" : "false"}
            {...register("email")}
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
