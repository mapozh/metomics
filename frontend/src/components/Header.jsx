import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Header.css";

const Header = ({ handleLogout }) => {
  const navigate = useNavigate();

  const onLogout = () => {
    handleLogout(); // Call the logout handler passed as a prop
    navigate("/"); // Redirect to homepage
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light fixed-top">
      <div className="container-fluid">
        {/* Logo and Brand */}
        <Link className="navbar-brand" to="/dashboard">
          <span className="brand-text">OMIXS</span>
        </Link>

        {/* Toggler button for mobile view */}
        {/* <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button> */}

        {/* Navbar links */}
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <Link className="nav-link" to="/chatbot">
                ChatBot
              </Link>
            </li>
            <li className="nav-item">
              <button
                className="btn btn-danger logout-btn"
                onClick={onLogout}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;