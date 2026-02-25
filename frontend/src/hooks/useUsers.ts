import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { UsersService } from "../api/services";
import type { UserCreate, UserUpdate } from "../api/types";

export function useUsers() {
  return useQuery({
    queryKey: ["users"],
    queryFn: UsersService.listUsers,
  });
}

export function useUser(id: string) {
  return useQuery({
    queryKey: ["users", id],
    queryFn: () => UsersService.getUser(id),
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UserCreate) => UsersService.createUser(data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UserUpdate }) =>
      UsersService.updateUser(id, data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

export function useDeleteUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => UsersService.deleteUser(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}
