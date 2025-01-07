import React, { useState } from 'react';
import { addSample } from '../services/api';

const AddSampleForm = () => {
  const [formData, setFormData] = useState({
    sample_id: '',
    name: '',
    organism: '',
    library_type: '',
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await addSample(formData); // API call
      setMessage(response.message); // Success message
    } catch (error) {
      setMessage('Failed to add sample.'); // Error message
    }
  };

  return (
    <div>
      <h2>Add Sample</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="sample_id"
          placeholder="Sample ID"
          value={formData.sample_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="organism"
          placeholder="Organism"
          value={formData.organism}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="library_type"
          placeholder="Library Type"
          value={formData.library_type}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Sample</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddSampleForm;
