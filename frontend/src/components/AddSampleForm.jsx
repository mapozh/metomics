import React, { useState } from 'react';
import { addSample } from '../services/api';
import formMetadata from '../data/form_metadata.json';

const AddSampleForm = () => {
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState('');

  // Load metadata for the "Sample" class
  const sampleMetadata = formMetadata.Sample || { properties: [] };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await addSample(formData);
      setMessage(response.message || 'Sample added successfully!');
    } catch (error) {
      setMessage('Failed to add sample. Please try again.');
    }
  };

  return (
    <div>
      <h2>Add Sample</h2>
      <form onSubmit={handleSubmit}>
        {sampleMetadata.properties.map((prop) => (
          <div key={prop.name} style={{ marginBottom: '10px' }}>
            <label>
              {prop.label}:
              <input
                type={prop.type}
                name={prop.name}
                placeholder={prop.label}
                value={formData[prop.name] || ''}
                onChange={handleChange}
                required
              />
            </label>
          </div>
        ))}
        <button type="submit">Add Sample</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default AddSampleForm;

