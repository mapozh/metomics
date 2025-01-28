import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/HomePage.css";

const Init = () => {
  const [projects, setProjects] = useState([]); // List of projects the user has created
  const [newProjectName, setNewProjectName] = useState(""); // Name for the new project
  const [isCreatingProject, setIsCreatingProject] = useState(false); // Flag to show the name input field
  const navigate = useNavigate();

  // Handle when the user clicks to create a new project
  const handleCreateProject = () => {
    setIsCreatingProject(true); // Show the input field for project name
  };

  // When the user enters the name and clicks 'Next'
  const handleProjectNameSubmit = () => {
    if (newProjectName.trim() === "") {
      alert("Please provide a name for the new project.");
      return;
    }

    // Add the new project to the list (simulate saving it)
    const newProject = { id: projects.length + 1, name: newProjectName };
    setProjects([...projects, newProject]);

    // Redirect to DynamicForm to fill the form for the new project
    navigate("/dynamicform");

    setIsCreatingProject(false); // Hide the project name input
    setNewProjectName(""); // Clear the project name input
  };

  return (
    <div className="init-container">
      <div className="projects-list">
        <h3>Your Projects</h3>
        <ul>
          {projects.map((project) => (
            <li key={project.id}>{project.name}</li>
          ))}
        </ul>
        <button className="refresh-button" onClick={() => {}}>
          Refresh Projects
        </button>
      </div>

      <div className="create-project">
        <h3>Create New Project</h3>
        {isCreatingProject ? (
          <>
            <input
              type="text"
              placeholder="Enter Project Name"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
            />
            <button className="create-button" onClick={handleProjectNameSubmit}>
              Next
            </button>
          </>
        ) : (
          <button className="create-button" onClick={handleCreateProject}>
            + Create Project
          </button>
        )}
      </div>
    </div>
  );
};

export default Init;
