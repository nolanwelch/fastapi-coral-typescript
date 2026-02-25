import { type FormEvent, useState } from "react";
import { UserList } from "../components/UserList";
import { useCreateUser } from "../hooks/useUsers";

export function UsersPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const createUser = useCreateUser();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !email.trim()) return;
    createUser.mutate(
      { name: name.trim(), email: email.trim() },
      {
        onSuccess: () => {
          setName("");
          setEmail("");
        },
      },
    );
  };

  return (
    <div>
      <h1>Users</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name: </label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email: </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={createUser.isPending}>
          {createUser.isPending ? "Creating..." : "Add User"}
        </button>
        {createUser.isError && (
          <p style={{ color: "red" }}>
            Error: {createUser.error.message}
          </p>
        )}
      </form>

      <hr />

      <UserList />
    </div>
  );
}
