import React, { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    minHeight: "100vh",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    width: "300px",
  },
  input: {
    marginBottom: "16px",
  },
  button: {
    marginBottom: "16px",
  },
  signInLink: {
    textDecoration: "none",
    color: "#0000ff",
    alignSelf: "center",
  },
};

const RegisterForm = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await api.post("users/", {
        username,
        email,
        password,
      });
      console.log(response.data);
      alert("User registered successfully!");
    } catch (error) {
      console.error(error);
      setError(error.response?.data?.message || "Error registering user.");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h1>Register</h1>
      <label>
        Username:
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
        />
      </label>
      <label>
        Email:
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
      </label>
      <button type="submit" style={styles.button}>
        Register
      </button>
      {error && <p className="error-message">{error}</p>}
      <p>
        Already have an account?{" "}
        <Link to="/signin" style={styles.signInLink}>
          Sign In
        </Link>
      </p>
    </form>
  );
};

export default RegisterForm;
