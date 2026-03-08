'use client';

import { useState, useEffect, useCallback } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

interface ApiError {
  detail: string;
}

// Get token from localStorage
const getToken = () => {
  return localStorage.getItem('token');
};

// Generic API request function with JWT token
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();

  if (!token) {
    throw new Error('No authentication token available. Please log in.');
  }

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  };

  const response = await fetch(`${API_URL}${endpoint}`, config);

  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(errorData.detail || `API request failed: ${response.status}`);
  }

  // For responses with no content (like DELETE), return early
  if (response.status === 204) {
    return {} as T;
  }

  return response.json() as Promise<T>;
}

export const useTasks = (userId: string | null) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks from API on mount
  useEffect(() => {
    if (!userId) {
      setTasks([]);
      setLoading(false);
      return;
    }

    const fetchTasks = async () => {
      try {
        setLoading(true);
        setError(null);
        // Fetch todos from backend (using /api/todos/ endpoint)
        const fetchedTasks = await apiRequest<Task[]>('/api/todos/');
        
        // Transform backend format to frontend format
        const normalizedTasks: Task[] = fetchedTasks.map((t: any) => ({
          id: t.id,
          title: t.title,
          description: t.description || '',
          completed: t.completed,
          userId: t.user_id,
          createdAt: t.created_at,
          updatedAt: t.updated_at,
        }));
        
        setTasks(normalizedTasks);
      } catch (err: any) {
        console.error('Error fetching tasks:', err);
        setError(err.message || 'Failed to load tasks');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [userId]);

  // Add a new task
  const addTask = useCallback(async (title: string, description?: string) => {
    if (!userId) {
      setError('User not authenticated');
      return null;
    }

    try {
      // Create todo via backend API
      const newTask = await apiRequest<Task>('/api/todos/', {
        method: 'POST',
        body: JSON.stringify({
          title,
          description: description || '',
          completed: false,
          priority: 'medium',
        }),
      });

      const normalizedTask: Task = {
        id: newTask.id,
        title: newTask.title,
        description: newTask.description || '',
        completed: newTask.completed,
        userId: newTask.userId,
        createdAt: newTask.createdAt,
        updatedAt: newTask.updatedAt,
      };

      setTasks(prev => [...prev, normalizedTask]);
      return normalizedTask;
    } catch (err: any) {
      console.error('Error creating task:', err);
      setError(err.message || 'Failed to create task');
      return null;
    }
  }, [userId]);

  // Update a task
  const updateTask = useCallback(async (id: string, updates: Partial<Task>) => {
    try {
      const updatedTask = await apiRequest<Task>(`/api/todos/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          title: updates.title,
          description: updates.description,
          completed: updates.completed,
          priority: 'medium',
        }),
      });

      setTasks(prev => prev.map(task =>
        task.id === id
          ? {
              ...task,
              title: updatedTask.title,
              description: updatedTask.description || '',
              completed: updatedTask.completed,
              updatedAt: updatedTask.updatedAt,
            }
          : task
      ));
      
      return updatedTask;
    } catch (err: any) {
      console.error('Error updating task:', err);
      setError(err.message || 'Failed to update task');
      throw err;
    }
  }, []);

  // Delete a task
  const deleteTask = useCallback(async (id: string) => {
    try {
      await apiRequest(`/api/todos/${id}`, {
        method: 'DELETE',
      });
      
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err: any) {
      console.error('Error deleting task:', err);
      setError(err.message || 'Failed to delete task');
      throw err;
    }
  }, []);

  // Toggle task completion
  const toggleComplete = useCallback(async (id: string) => {
    try {
      const taskToUpdate = tasks.find(t => t.id === id);
      if (!taskToUpdate) return;

      const updatedTask = await apiRequest<Task>(`/api/todos/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          completed: !taskToUpdate.completed,
        }),
      });

      setTasks(prev => prev.map(task =>
        task.id === id
          ? {
              ...task,
              completed: updatedTask.completed,
              updatedAt: updatedTask.updatedAt,
            }
          : task
      ));
    } catch (err: any) {
      console.error('Error toggling task:', err);
      setError(err.message || 'Failed to update task');
    }
  }, [tasks]);

  return {
    tasks,
    loading,
    error,
    addTask,
    updateTask,
    deleteTask,
    toggleComplete,
  };
};
