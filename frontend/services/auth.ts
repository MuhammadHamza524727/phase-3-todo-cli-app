import axios from 'axios';
import apiClient from './api-client';
import { User } from '../types';

interface LoginCredentials {
  email: string;
  password: string;
}

interface SignupData {
  email: string;
  password: string;
  password_confirm: string;
  name: string;
}

interface LoginResponse {
  user: User;
  token: string;
}

interface SignupResponse {
  user: User;
  token: string;
}

/**
 * User login function
 */
export const loginUser = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  try {
    const response = await apiClient.post('/api/login', credentials);
    const { user, token } = response.data;

    // Store token in localStorage (only in browser environment)
    if (typeof window !== 'undefined') {
      localStorage.setItem('accessToken', token);
    }

    return { user, token };
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      // Server responded with error status
      throw new Error((error.response.data as { error?: string }).error || 'Login failed');
    } else if (axios.isAxiosError(error) && error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred during login.');
    }
  }
};

/**
 * User signup function
 */
export const signupUser = async (userData: SignupData): Promise<SignupResponse> => {
  try {
    const response = await apiClient.post('/api/register', userData);
    const { user, token } = response.data;

    // Store token in localStorage (only in browser environment)
    if (typeof window !== 'undefined') {
      localStorage.setItem('accessToken', token);
    }

    return { user, token };
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      // Server responded with error status
      throw new Error((error.response.data as { error?: string }).error || 'Signup failed');
    } else if (axios.isAxiosError(error) && error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred during signup.');
    }
  }
};

/**
 * User logout function
 */
export const logoutUser = (): void => {
  // Remove tokens from localStorage (only in browser environment)
  if (typeof window !== 'undefined') {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
};

/**
 * Get current authenticated user
 */
export const getCurrentUser = (): User | null => {
  try {
    // Only access localStorage in browser environment
    if (typeof window === 'undefined') {
      return null;
    }

    const token = localStorage.getItem('accessToken');
    if (!token) {
      return null;
    }

    // In a real implementation, you'd decode the JWT to get user info
    // For now, we'll return null and rely on the backend to validate
    return null;
  } catch (error) {
    console.error('Error getting current user:', error);
    return null;
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = (): boolean => {
  // Only access localStorage in browser environment
  if (typeof window === 'undefined') {
    return false;
  }

  const token = localStorage.getItem('accessToken');
  return !!token;
};