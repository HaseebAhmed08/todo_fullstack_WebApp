// API client for handling all CRUD operations with JWT token handling
import { authClient } from './auth-client';

// Base API URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Generic API request function with proper authentication handling for Better Auth
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Check if user is authenticated by getting session
  const sessionResult = await authClient.getSession();
  if (!sessionResult?.data?.user) {
    throw new Error('Authentication required. Please log in.');
  }

    // Get JWT token reliably using Better Auth's getToken() method
    const tokenResult = await authClient.getToken();
    let token: string | null = null;

    if (typeof tokenResult === 'string') {
      token = tokenResult;
    } else if (typeof tokenResult === 'object' && tokenResult !== null) {
      token = tokenResult.accessToken || tokenResult.token || tokenResult?.user?.accessToken;
    }

    // Fallback: if still no token, try getting session directly and log for debugging
    if (!token) {
      const session = await authClient.getSession();
      console.warn('🔍 Token extraction failed. Debug info:', {
        tokenResult,
        session,
        'session.data.accessToken': session?.data?.accessToken,
        'session.session.accessToken': session?.session?.accessToken,
        'session.session.token': session?.session?.token,
        'session.user.accessToken': session?.user?.accessToken,
      });
      token = session?.data?.accessToken ||
              session?.session?.accessToken ||
              session?.session?.token ||
              session?.user?.accessToken;
    }

    if (!token) {
      throw new Error('Authentication required. Please log in.');
    }

    if (typeof token === 'string') {
      console.log(`✅ JWT token acquired (length: ${token.length}, prefix: ${token.substring(0, Math.min(10, token.length))}...)`);
    } else {
      console.warn(`⚠️ Token is not a string after extraction! Type: ${typeof token}, Value:`, token);
      throw new Error('Authentication failed: invalid token type');
    }

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      // Add Authorization header if we have a token
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
    // Include credentials to send authentication cookies with the request
    credentials: 'include',
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
      console.error('Token validation failed. The backend rejected the token.');
      throw new Error('Could not validate credentials. Please log in again.');
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: `API request failed: ${response.status} ${response.statusText}` }));
      throw new Error(errorData.detail);
    }

    // For responses with no content (like DELETE), return an empty object.
    if (response.status === 204) {
      return {} as T;
    }

    return response.json() as Promise<T>;
  } catch (error) {
    console.error(`API request failed for endpoint: ${endpoint}. Error:`, error);
    // Re-throw the error to be handled by the calling function/component.
    throw error;
  }
}

// TASK API METHODS
export const taskApi = {
  getTasks: (userId: string) =>
    apiRequest(`/api/${userId}/tasks/`),

  createTask: (userId: string, taskData: { title: string; description?: string; completed?: boolean }) =>
    apiRequest(`/api/${userId}/tasks/`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    }),

  updateTask: (userId: string, id: string, taskData: { title?: string; description?: string; completed?: boolean }) =>
    apiRequest(`/api/${userId}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    }),

  deleteTask: (userId: string, id: string) =>
    apiRequest(`/api/${userId}/tasks/${id}`, {
      method: 'DELETE',
    }),

  getTask: (userId: string, id: string) =>
    apiRequest(`/api/${userId}/tasks/${id}`),
};

// USER PROFILE API METHODS
export const userApi = {
  getProfile: () =>
    apiRequest('/api/auth/me'),

  updateProfile: (userData: { name?: string; email?: string }) =>
    apiRequest('/api/users/me', {
      method: 'PUT',
      body: JSON.stringify(userData),
    }),
};

// GENERIC ERROR HANDLING
export const handleApiError = (error: any): string => {
  if (error.message && (error.message.includes('Authentication required') || error.message.includes('Could not validate credentials'))) {
    return error.message;
  }
  if (error instanceof TypeError && error.message.includes('fetch')) {
    return 'Network error. Please check your connection or if the server is running.';
  }
  return error.message || 'An unexpected error occurred.';
};