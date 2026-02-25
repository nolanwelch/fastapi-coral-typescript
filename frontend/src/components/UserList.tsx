import { useUsers } from "../hooks/useUsers";

export function UserList() {
  const { data: users, isLoading, isError, error } = useUsers();

  if (isLoading) {
    return <p>Loading users...</p>;
  }

  if (isError) {
    return <p>Error loading users: {error.message}</p>;
  }

  if (!users || users.length === 0) {
    return <p>No users found.</p>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          <strong>{user.name}</strong> — {user.email}
          <br />
          <small>Created: {new Date(user.created_at).toLocaleString()}</small>
        </li>
      ))}
    </ul>
  );
}
