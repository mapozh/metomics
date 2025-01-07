import axios from 'axios';

const API_URL = 'http://localhost:8000/metadata';

// Add Sample API
export const addSample = async (sampleData) => {
  try {
    const response = await axios.post(`${API_URL}/add-sample`, null, {
      params: sampleData, // Send parameters in query string
    });
    return response.data; // Return response
  } catch (error) {
    console.error('Error adding sample:', error);
    throw error; // Handle error
  }
};

// Fetch Samples API
export const fetchSamples = async () => {
  try {
    const response = await axios.get(`${API_URL}/fetch-samples`);
    return response.data; // Return fetched data
  } catch (error) {
    console.error('Error fetching samples:', error);
    throw error; // Handle error
  }
};