import React, { useState } from "react"; // Import useState
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"; // Import Navigate
import HomePage from "./components/HomePage";
import Register from "./components/Register";
import Signin from "./components/Signin";
import DynamicForm from "./components/DynamicForm";
import Chatbot from "./components/Chatbot";
import Header from "./components/Header"; 
// import CreateProject from "./components/CreateProject"; 

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);

    const handleSignIn = (userData) => {
        setIsAuthenticated(true);
        setUser(userData);
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        setUser(null);
    };


    return (
            <div style={{ flex: 1 }}>
                {/* {isAuthenticated ? (
                    <Header handleLogout={handleLogout} /> // Pass handleLogout to Header2
                ) : (
                    <Header />
                )} */}
                
                    <Routes>
                        <Route path="/register" element={<Register />} />
                        <Route path="/signin" element={<Signin />} />
                        <Route path="/" element={<HomePage />} />
                        <Route path="/dynamicform" element={<DynamicForm />} />
                        <Route path="/chatbot" element={<Chatbot />} />
                        <Route
                            path="/create-project"
                            element={isAuthenticated ? <CreateProject /> : <Navigate to="/signin" />}
                        />
                    </Routes>
            </div>
    );
};


export default App;


