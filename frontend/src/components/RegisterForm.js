import React, { useState } from "react";
import api from "../services/api";
import logo from "../logo.png";

const styles = {
  form: {
    backgroundColor: "#ffffff",
    padding: "30px",
    borderRadius: "8px",
    maxWidth: "500px",
    margin: "auto",
  },
  inputGroup: {
    marginBottom: "20px",
  },
  input: {
    flex: "1",
    marginRight: "10px",
    width: "100%",
    marginBottom: "10px",
  },
  button: {
    backgroundColor: "#007BFF",
    color: "#ffffff",
    padding: "8px 16px",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
  },
  logo: {
    width: "150px",
    height: "auto",
    display: "block",
    marginBottom: "20px",
    marginLeft: "auto",
    marginRight: "auto",
  },
};

const RegisterForm = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
      alert("Error registering user.");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <img src={logo} alt="Logo" style={styles.logo} />
      <h1>Register</h1>
      <div style={styles.inputGroup}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
      </div>
      <button type="submit" style={styles.button}>
        Register
      </button>
    </form>
  );
};

export default RegisterForm;
