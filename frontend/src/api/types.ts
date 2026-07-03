import type { components } from "./generated";

export type AuthUserResponse = components["schemas"]["AuthUserResponse"];
export type CreateCustomerAvatarUploadRequest =
  components["schemas"]["CreateCustomerAvatarUploadRequest"];
export type CreateCustomerRequest =
  components["schemas"]["CreateCustomerRequest"];
export type CustomerAvatarUploadResponse =
  components["schemas"]["CustomerAvatarUploadResponse"];
export type CustomerResponse = components["schemas"]["CustomerResponse"];
export type PatchCustomerRequest =
  components["schemas"]["PatchCustomerRequest"];
export type QueuedResponse = components["schemas"]["QueuedResponse"];
export type CustomerStatus = CustomerResponse["status"];
