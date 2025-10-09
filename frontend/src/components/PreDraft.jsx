import { useState, useContext } from "react";
import { AuthContext } from "./AuthContext";

export default function PreDraft() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const { user, login, logout } = useContext(AuthContext);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;

    setLoading(true);

    try {
      // Send username to backend via proxy
      const response = await fetch("/addUser", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email }), // match backend key
      });

      const data = await response.json();

      if (response.ok && data.status === "success") {
        // Update AuthContext
        login(username);
        console.log("User logged in and added to backend:", data);
      } else {
        console.error("Backend error:", data.message);
        alert(data.message || "Login failed");
      }
    } catch (err) {
      console.error("Network or server error:", err);
      alert("Something went wrong. Please try again.");
    }

    setUsername(""); // clear input
    setLoading(false);
  };

  if (user) {
    return (
      <div style={{ textAlign: "center" }}>
        <h1>Welcome, {user.name} 🎉</h1>
        <button onClick={logout}>Logout</button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} style={{ textAlign: "center" }}>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Enter username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        disabled={loading}
      />
      <input
        type="text"
        placeholder="Enter Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
}
