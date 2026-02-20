import apiClient from './api-client';
import { Task } from '../types';

interface CreateTaskData {
  title: string;
  description?: string;
  completed?: boolean;
}

interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
}

/**
 * Fetch all tasks for the authenticated user
 */
export const fetchTasks = async (): Promise<Task[]> => {
  try {
    const response = await apiClient.get('/api/tasks');
    return Array.isArray(response.data) ? response.data : [];
  } catch (error: any) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Failed to fetch tasks');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred while fetching tasks.');
    }
  }
};

/**
 * Create a new task
 */
export const createTask = async (taskData: CreateTaskData): Promise<Task> => {
  try {
    const response = await apiClient.post('/api/tasks', taskData);
    return response.data; // Backend returns the task directly
  } catch (error: any) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Failed to create task');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred while creating task.');
    }
  }
};

/**
 * Update an existing task
 */
export const updateTask = async (id: string, taskData: UpdateTaskData): Promise<Task> => {
  try {
    const response = await apiClient.put(`/api/tasks/${id}`, taskData);
    return response.data; // Backend returns the task directly
  } catch (error: any) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Failed to update task');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred while updating task.');
    }
  }
};

/**
 * Delete a task
 */
export const deleteTask = async (id: string): Promise<void> => {
  try {
    await apiClient.delete(`/api/tasks/${id}`);
  } catch (error: any) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Failed to delete task');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred while deleting task.');
    }
  }
};

/**
 * Toggle task completion status
 */
export const toggleTaskCompletion = async (id: string, completed: boolean): Promise<Task> => {
  try {
    const response = await apiClient.patch(`/api/tasks/${id}/complete`, { completed });
    return response.data; // Backend returns the updated task directly
  } catch (error: any) {
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.error || 'Failed to update task completion');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error. Please check your connection.');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred while updating task completion.');
    }
  }
};