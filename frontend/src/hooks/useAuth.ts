import { getCurrentUser } from "@/features/auth/api/getCurrentUser";
import { useQuery } from "@tanstack/react-query";

export function useAuthMe() {
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: getCurrentUser,
  });
}
