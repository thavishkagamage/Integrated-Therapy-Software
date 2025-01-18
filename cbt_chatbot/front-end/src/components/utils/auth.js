import axios from 'axios';

export const refreshToken = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken');
    const response = await axios.post('http://localhost:8000/api/users/tokenrefresh/', {
      refresh: refreshToken,
    });
    localStorage.setItem('accessToken', response.data.access);
    return response.data.access;
  } catch (error) {
    console.error('Error refreshing token:', error.response ? error.response.data : error.message);
    throw error;
  }
};