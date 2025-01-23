import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import '../LoginPage.css'; // Import the CSS file

const LoginPage = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            // Handle successful login
            const data = await response.json();
            console.log("Login successful!", data);
            // Redirect to the DynamicForm page after successful login
            navigate("/dynamicform");  // Redirect to /dynamicform page
        } else {
            const errorData = await response.json();
            setErrorMessage(errorData.message || "Invalid credentials");
        }
    };

    return (
        <div className="login-container">
            <h2 className="login-heading">Login</h2>
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <form className="login-form" onSubmit={handleSubmit}>
                <div className="input-group">
                    <label htmlFor="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="login-button">
                    Log In
                </button>
            </form>
        </div>
    );
};

export default LoginPage;
