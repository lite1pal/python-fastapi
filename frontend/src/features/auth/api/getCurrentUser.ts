import type { AuthUserResponse } from "@/api/types";
import { apiRequest } from "@/lib/http/apiClient";

export function getCurrentUser() {
  return apiRequest<AuthUserResponse>("/auth/me");
}
