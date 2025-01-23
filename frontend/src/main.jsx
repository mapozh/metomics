import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Import App component

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App /> {/* Render the App component which is inside BrowserRouter */}
  </React.StrictMode>
);
