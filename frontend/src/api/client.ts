/**
 * Axios client configuration for CodeOracle API
 */
import axios, { AxiosInstance, AxiosError } from 'axios';
import type { ErrorResponse } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT || '30000');

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError<ErrorResponse>) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with error status
      const errorData = error.response.data;
      console.error('API Error:', errorData);
      
      // You can add custom error handling here
      if (error.response.status === 401) {
        // Handle unauthorized
        console.error('Unauthorized access');
      } else if (error.response.status === 404) {
        // Handle not found
        console.error('Resource not found');
      } else if (error.response.status >= 500) {
        // Handle server errors
        console.error('Server error');
      }
      
      return Promise.reject(errorData);
    } else if (error.request) {
      // Request made but no response
      console.error('No response from server');
      return Promise.reject({
        error: 'Network Error',
        detail: 'Unable to connect to the server. Please check your connection.',
        code: 'NETWORK_ERROR',
      } as ErrorResponse);
    } else {
      // Something else happened
      console.error('Request error:', error.message);
      return Promise.reject({
        error: 'Request Error',
        detail: error.message,
        code: 'REQUEST_ERROR',
      } as ErrorResponse);
    }
  }
);

export default apiClient;

// Made with Bob
