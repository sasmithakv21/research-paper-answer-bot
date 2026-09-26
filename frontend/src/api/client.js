import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const askQuestion = async (question, apiKey = '') => {
  const response = await axios.post(`${API_BASE_URL}/chat`, {
    question,
    api_key: apiKey || undefined,
  });
  return response.data;
};

export const fetchPapers = async () => {
  const response = await axios.get(`${API_BASE_URL}/papers`);
  return response.data.papers;
};

export const uploadPaper = async (file, apiKey = '') => {
  const formData = new FormData();
  formData.append('file', file);
  if (apiKey) {
    formData.append('api_key', apiKey);
  }

  const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
