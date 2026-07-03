import { z } from "zod";

import type { CreateCustomerRequest, CustomerStatus } from "@/api/types";

const customerStatuses = ["lead", "active", "archived"] as const satisfies readonly CustomerStatus[];

export const createCustomerSchema = z.object({
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

export type CreateCustomerFormValues = z.infer<typeof createCustomerSchema>;

export const initialCreateCustomerForm: CreateCustomerFormValues = {
  name: "",
  email: "",
  company: "",
  status: "lead",
  notes: "",
};

export function toCreateCustomerPayload(
  values: CreateCustomerFormValues,
): CreateCustomerRequest {
  return {
    ...values,
    company: values.company || null,
    notes: values.notes || null,
  };
}
