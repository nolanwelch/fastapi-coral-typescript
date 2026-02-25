import apiClient from "../client";
import type { UserCreate, UserRead, UserUpdate } from "../types";

export const UsersService = {
  listUsers: async (): Promise<UserRead[]> => {
    const response = await apiClient.get<UserRead[]>("/users/");
    return response.data;
  },

  getUser: async (userId: string): Promise<UserRead> => {
    const response = await apiClient.get<UserRead>(`/users/${userId}`);
    return response.data;
  },

  createUser: async (data: UserCreate): Promise<UserRead> => {
    const response = await apiClient.post<UserRead>("/users/", data);
    return response.data;
  },

  updateUser: async (userId: string, data: UserUpdate): Promise<UserRead> => {
    const response = await apiClient.patch<UserRead>(`/users/${userId}`, data);
    return response.data;
  },

  deleteUser: async (userId: string): Promise<void> => {
    await apiClient.delete(`/users/${userId}`);
  },
};
