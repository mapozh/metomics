import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import '../styles.css';

const DynamicForm = () => {
    const [formMetadata, setFormMetadata] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Initialize useNavigate for navigation

    // Log out function to navigate to the login page
    const handleLogout = () => {
        navigate("/login"); // Redirect to the login page
    };

    // Build hierarchy from metadata
    const buildHierarchy = (metadata) => {
        const map = {};
        metadata.forEach((item) => {
            map[item.name] = { ...item, children: [] };
        });

        const hierarchy = [];
        metadata.forEach((item) => {
            if (item.superclass) {
                if (map[item.superclass]) {
                    map[item.superclass].children.push(map[item.name]);
                }
            } else {
                hierarchy.push(map[item.name]);
            }
        });

        return hierarchy;
    };

    // Fetch metadata from backend
    useEffect(() => {
        fetch("http://127.0.0.1:8000/metadata/form-metadata")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to fetch metadata");
                }
                return response.json();
            })
            .then((data) => {
                const parsedData = buildHierarchy(data.metadata);
                setFormMetadata(parsedData);
                setLoading(false);
            })
            .catch((error) => {
                setError(error.message);
                setLoading(false);
            });
    }, []);

    // Render form recursively
    const renderForm = (items) => {
        return items.map((item) => (
            <div key={item.name} className="inputGroup">
                <label className="label">
                    {item.label || item.name.split("#").pop()}
                </label>
                <input
                    type="text"
                    name={item.name}
                    placeholder={item.comment || `Enter ${item.label || item.name.split("#").pop()}`}
                    className="input"
                />
                {item.children && renderForm(item.children)}
            </div>
        ));
    };

    if (loading) {
        return <div className="loadingText">Loading form...</div>;
    }

    if (error) {
        return <div className="errorText">Error: {error}</div>;
    }

    return (
        <div className="container">
            <h1 className="heading">Dynamic Form Generator</h1>
            <button className="logout-button" onClick={handleLogout}>Log Out</button>
            <form className="form">
                {renderForm(formMetadata)}
                <button type="submit" className="button">Submit</button>
            </form>
        </div>
    );
};

export default DynamicForm;
