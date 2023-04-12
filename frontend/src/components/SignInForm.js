import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
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
  registerLink: {
    textDecoration: "none",
    color: "#0000ff",
    alignSelf: "center",
  },
};

const SignInForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await api.post("/auth/login/", {
        username: username,
        password: password,
      });

      if (response.status === 200) {
        localStorage.setItem("access_token", response.data.access);
        navigate("/feed");
      } else {
        setError("Error signing in.");
      }
    } catch (error) {
      console.error(error);
      setError(error.response?.data?.message || "Error signing in.");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h1>Sign In</h1>
      <label>
        Username:
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
      </label>
      <button type="submit" style={styles.button}>
        Sign In
      </button>
      {error && <p className="error-message">{error}</p>}
      <p>
        Don't have an account?{" "}
        <Link to="/register" style={styles.registerLink}>
          Register
        </Link>
      </p>
    </form>
  );
};

export default SignInForm;
