import axios from 'axios';
import { User, Task } from '../types';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8080',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to all requests
apiClient.interceptors.request.use(
  (config) => {
    // Only use localStorage in browser environment
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    // Ensure we don't duplicate the /api prefix
    if (!config.url?.startsWith('/api')) {
      config.url = `/api${config.url}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Remove tokens and redirect to login if unauthorized
      // Only use localStorage and window in browser environment
      if (typeof window !== 'undefined') {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Authentication API functions
export const authAPI = {
  register: async (userData: { email: string; password: string; password_confirm: string; name: string }) => {
    const response = await apiClient.post('/api/register', userData);
    return response.data;
  },

  login: async (credentials: { email: string; password: string }) => {
    const response = await apiClient.post('/api/login', credentials);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
};

// Task API functions
export const taskAPI = {
  getTasks: async (): Promise<Task[]> => {
    const response = await apiClient.get('/api/tasks');
    return response.data;
  },

  createTask: async (taskData: { title: string; description?: string; completed?: boolean }) => {
    const response = await apiClient.post('/api/tasks', taskData);
    return response.data;
  },

  updateTask: async (id: string, taskData: { title?: string; description?: string; completed?: boolean }) => {
    const response = await apiClient.put(`/api/tasks/${id}`, taskData);
    return response.data;
  },

  deleteTask: async (id: string) => {
    await apiClient.delete(`/api/tasks/${id}`);
  },

  toggleTaskCompletion: async (id: string, completed: boolean) => {
    const response = await apiClient.patch(`/api/tasks/${id}/complete`, { completed });
    return response.data;
  }
};

export default apiClient;