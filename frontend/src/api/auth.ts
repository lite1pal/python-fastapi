import type { AuthUserResponse } from "./types";
import { apiRequest } from "./http";

export function getCurrentUser() {
  return apiRequest<AuthUserResponse>("/auth/me");
}
