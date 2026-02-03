// API client for handling all CRUD operations with JWT token handling
import { authClient } from './auth-client';

// Base API URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Generic API request function with JWT token handling
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Use Better Auth's getSession to retrieve the JWT token
  const { data: session } = await authClient.getSession();

  // Note: Better Auth provides a token in the session or we can use the cookie.
  // For cross-origin FastAPI, we'll use the Authorization header.
  const token = session?.session.token || (typeof window !== 'undefined' ? localStorage.getItem('better-auth.session-token') : null);

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
      // Handle unauthorized (session expired)
      console.warn('Session expired or unauthorized');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API request failed: ${response.status} ${response.statusText}`);
    }

    // For responses with no content (like DELETE), return early
    if (response.status === 204) {
      return {} as T;
    }

    return response.json() as Promise<T>;
  } catch (error) {
    console.error(`API request failed: ${endpoint}.`, error);
    throw error;
  }
}

// TASK API METHODS
export const taskApi = {
  // Get all user tasks
  getTasks: () =>
    apiRequest('/api/tasks/'),

  // Create a new task
  createTask: (taskData: { title: string; description?: string; completed?: boolean; user_id: string }) =>
    apiRequest('/api/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    }),

  // Update a task
  updateTask: (id: string, taskData: { title?: string; description?: string; completed?: boolean }) =>
    apiRequest(`/api/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }),

  // Delete a task
  deleteTask: (id: string) =>
    apiRequest(`/api/tasks/${id}`, {
      method: 'DELETE',
    }),

  // Get a specific task
  getTask: (id: string) =>
    apiRequest(`/api/tasks/${id}`),
};

// GENERIC ERROR HANDLING
export const handleApiError = (error: any): string => {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return 'Network error. Please check your connection.';
  }
  return error.message || 'An unexpected error occurred.';
};