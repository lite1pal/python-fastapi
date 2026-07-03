import { apiRequest } from "@/lib/http/apiClient";
import type {
  CreateCustomerRequest,
  CreateCustomerAvatarUploadRequest,
  CustomerAvatarUploadResponse,
  CustomerResponse,
  PatchCustomerRequest,
  QueuedResponse,
} from "./types";

export function listCustomers(params?: { limit?: number; search?: string }) {
  const searchParams = new URLSearchParams();

  if (params?.limit !== undefined) {
    searchParams.set("limit", String(params.limit));
  }

  if (params?.search) {
    searchParams.set("search", params.search);
  }

  const query = searchParams.size > 0 ? `?${searchParams.toString()}` : "";
  return apiRequest<CustomerResponse[]>(`/customers${query}`);
}

export function getCustomer(customerId: number) {
  return apiRequest<CustomerResponse>(`/customers/${customerId}`);
}

export function createCustomer(payload: CreateCustomerRequest) {
  return apiRequest<CustomerResponse>("/customers", {
    method: "POST",
    body: payload,
  });
}

export function patchCustomer(
  customerId: number,
  payload: PatchCustomerRequest,
) {
  return apiRequest<CustomerResponse>(`/customers/${customerId}`, {
    method: "PATCH",
    body: payload,
  });
}

export function deleteCustomer(customerId: number) {
  return apiRequest<CustomerResponse>(`/customers/${customerId}`, {
    method: "DELETE",
  });
}

export function summarizeCustomerNotes(customerId: number) {
  return apiRequest<QueuedResponse>(
    `/customers/${customerId}/summarize_notes`,
    {
      method: "POST",
    },
  );
}

export function createCustomerUploadUrl(
  customerId: number,
  payload: CreateCustomerAvatarUploadRequest,
) {
  return apiRequest<CustomerAvatarUploadResponse>(
    `/customers/${customerId}/upload_url`,
    {
      method: "POST",
      body: payload,
    },
  );
}
