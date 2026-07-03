import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  createCustomer,
  deleteCustomer,
  getCustomer,
  listCustomers,
  patchCustomer,
  summarizeCustomerNotes,
} from "@/api/customers";
import type {
  CreateCustomerRequest,
  PatchCustomerRequest,
} from "@/api/types";

export function useCustomers(params?: { limit?: number; search?: string }) {
  return useQuery({
    queryKey: ["customers", params],
    queryFn: () => listCustomers(params),
  });
}

export function useCustomer(customerId: number) {
  return useQuery({
    queryKey: ["customers", customerId],
    queryFn: () => getCustomer(customerId),
    enabled: Number.isFinite(customerId),
  });
}

export function useCreateCustomer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateCustomerRequest) => createCustomer(payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customers"] });
    },
  });
}

export function usePatchCustomer(customerId: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: PatchCustomerRequest) =>
      patchCustomer(customerId, payload),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customers"] });
      void queryClient.invalidateQueries({ queryKey: ["customers", customerId] });
    },
  });
}

export function useDeleteCustomer() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (customerId: number) => deleteCustomer(customerId),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["customers"] });
    },
  });
}

export function useSummarizeCustomerNotes(customerId: number) {
  return useMutation({
    mutationFn: () => summarizeCustomerNotes(customerId),
  });
}
