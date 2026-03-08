'use client';

import { useState, useEffect, useCallback } from 'react';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

const STORAGE_KEY = 'todo_tasks';

export const useTasks = (userId: string | null) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks from localStorage on mount
  useEffect(() => {
    if (!userId) {
      setTasks([]);
      setLoading(false);
      return;
    }

    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const allTasks = JSON.parse(stored);
        // Filter tasks for this user
        const userTasks = allTasks.filter((t: Task) => t.userId === userId);
        setTasks(userTasks);
      }
    } catch (err) {
      console.error('Error loading tasks from localStorage:', err);
      setError('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  }, [userId]);

  // Save tasks to localStorage
  const saveToStorage = useCallback((newTasks: Task[]) => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      const allTasks: Task[] = stored ? JSON.parse(stored) : [];
      
      if (!userId) return;
      
      // Remove old tasks for this user
      const otherUserTasks = allTasks.filter((t: Task) => t.userId !== userId);
      // Add new tasks for this user
      const updatedTasks = [...otherUserTasks, ...newTasks];
      
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedTasks));
    } catch (err) {
      console.error('Error saving tasks to localStorage:', err);
    }
  }, [userId]);

  // Add a new task
  const addTask = useCallback((title: string, description?: string) => {
    if (!userId) {
      setError('User not authenticated');
      return null;
    }

    const newTask: Task = {
      id: crypto.randomUUID(),
      title,
      description: description || '',
      completed: false,
      userId,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    setTasks(prev => {
      const updated = [...prev, newTask];
      saveToStorage(updated);
      return updated;
    });

    return newTask;
  }, [userId, saveToStorage]);

  // Update a task
  const updateTask = useCallback((id: string, updates: Partial<Task>) => {
    setTasks(prev => {
      const updated = prev.map(task => 
        task.id === id 
          ? { ...task, ...updates, updatedAt: new Date().toISOString() }
          : task
      );
      saveToStorage(updated);
      return updated;
    });
  }, [saveToStorage]);

  // Delete a task
  const deleteTask = useCallback((id: string) => {
    setTasks(prev => {
      const updated = prev.filter(task => task.id !== id);
      saveToStorage(updated);
      return updated;
    });
  }, [saveToStorage]);

  // Toggle task completion
  const toggleComplete = useCallback((id: string) => {
    setTasks(prev => {
      const updated = prev.map(task =>
        task.id === id
          ? { ...task, completed: !task.completed, updatedAt: new Date().toISOString() }
          : task
      );
      saveToStorage(updated);
      return updated;
    });
  }, [saveToStorage]);

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
