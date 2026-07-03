import { useQuery } from "@tanstack/react-query";

import { getCurrentUser } from "../api/auth";

export function useAuthMe() {
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: getCurrentUser,
  });
}
