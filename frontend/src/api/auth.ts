import { apiRequest } from "@/api/http";
import type { AuthUserResponse } from "@/api/types";

export function getCurrentUser() {
  return apiRequest<AuthUserResponse>("/auth/me");
}
