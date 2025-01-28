import React from 'react';
import ReactDOM from 'react-dom/client';
import Register from './components/Register'; 
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter
import App from './App'; 

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

