import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DynamicForm from "./components/DynamicForm";
import Chatbot from "./components/Chatbot";
import LoginPage from "./components/LoginPage";

const App = () => {
    return (
        <Router>
            <div>
                {/* <h1>RNA-seq Metadata Management</h1> */}
                <Routes>
                    <Route path="/" element={<DynamicForm />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/login" element={<LoginPage />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;

