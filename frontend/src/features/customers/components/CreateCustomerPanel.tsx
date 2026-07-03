import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import {
  createCustomerSchema,
  initialCreateCustomerForm,
  toCreateCustomerPayload,
  type CreateCustomerFormValues,
} from "../forms/createCustomerForm";
import { useCreateCustomer } from "../../../hooks/useCustomers";
import {
  Button,
  FormField,
  Input,
  Message,
  Panel,
  Select,
  Textarea,
} from "../../../components/ui";

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
        <FormField
          error={errors.name?.message}
          id="create-customer-name"
          label="Name"
          required
        >
          <Input placeholder="Jane Doe" {...register("name")} />
        </FormField>
        <FormField
          error={errors.email?.message}
          id="create-customer-email"
          label="Email"
          required
        >
          <Input placeholder="jane@example.com" type="email" {...register("email")} />
        </FormField>
        <FormField id="create-customer-company" label="Company">
          <Input placeholder="Acme Inc." {...register("company")} />
        </FormField>
        <FormField id="create-customer-status" label="Status">
          <Select {...register("status")}>
            <option value="lead">lead</option>
            <option value="active">active</option>
            <option value="archived">archived</option>
          </Select>
        </FormField>
        <FormField id="create-customer-notes" label="Notes">
          <Textarea placeholder="Add context for the team" {...register("notes")} />
        </FormField>
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
