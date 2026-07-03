import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import {
  createCustomerSchema,
  initialCreateCustomerForm,
  toCreateCustomerPayload,
  type CreateCustomerFormValues,
} from "../forms/createCustomerForm";
import { useCreateCustomer } from "../hooks/useCustomers";
import { Button, Field, Input, Message, Panel, Select, Textarea } from "./ui";

export function CreateCustomerPanel() {
  const createCustomer = useCreateCustomer();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateCustomerFormValues>({
    defaultValues: initialCreateCustomerForm,
    resolver: zodResolver(createCustomerSchema),
  });

  function onSubmit(values: CreateCustomerFormValues) {
    createCustomer.mutate(toCreateCustomerPayload(values), {
      onSuccess: () => reset(initialCreateCustomerForm),
    });
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
