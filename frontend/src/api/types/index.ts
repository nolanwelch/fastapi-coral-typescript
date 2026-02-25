export interface UserCreate {
  name: string;
  email: string;
}

export interface UserRead {
  id: string;
  name: string;
  email: string;
  created_at: string;
}

export interface UserUpdate {
  name?: string;
  email?: string;
}
