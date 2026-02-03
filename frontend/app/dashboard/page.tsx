'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import Header from '@/components/Header';
import TaskList from '@/components/TaskList';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';
import { taskApi, handleApiError } from '@/lib/api';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: Date;
  updatedAt: Date;
}

const DashboardPage: React.FC = () => {
  const { session, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [creating, setCreating] = useState(false);

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      // Don't fetch if not logged in
      if (!session) return;

      try {
        setLoading(true);
        setError(null);
        const fetchedTasks = await taskApi.getTasks() as any[];

        const normalizedTasks: Task[] = fetchedTasks.map((t: any) => ({
          id: t.id,
          title: t.title,
          description: t.description,
          completed: t.completed,
          userId: t.user_id,
          createdAt: new Date(t.created_at),
          updatedAt: new Date(t.updated_at)
        }));
        setTasks(normalizedTasks);
      } catch (err) {
        setError(handleApiError(err));
      } finally {
        setLoading(false);
      }
    };

    if (!authLoading) {
      fetchTasks();
    }
  }, [session, authLoading]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setError('Task title is required');
      return;
    }

    if (!session?.user?.id) {
      setError('User not authenticated');
      return;
    }

    setCreating(true);
    setError(null);

    try {
      const newTask = await taskApi.createTask({
        title: newTaskTitle,
        description: newTaskDescription,
        user_id: session.user.id
      }) as any;

      const normalizedTask: Task = {
        id: newTask.id,
        title: newTask.title,
        description: newTask.description,
        completed: newTask.completed,
        userId: newTask.user_id,
        createdAt: new Date(newTask.created_at),
        updatedAt: new Date(newTask.updated_at)
      };

      setTasks(prev => [...prev, normalizedTask]);
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setCreating(false);
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      const taskToUpdate = tasks.find(task => task.id === id);
      if (!taskToUpdate) return;

      const updatedTask = await taskApi.updateTask(id, {
        completed: !taskToUpdate.completed
      }) as any;

      setTasks(prev => prev.map(task =>
        task.id === id ? {
          ...task,
          completed: updatedTask.completed,
          updatedAt: new Date(updatedTask.updated_at)
        } : task
      ));
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await taskApi.deleteTask(id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Task Dashboard</h1>
            <p className="mt-2 text-gray-700">
              Manage your tasks and stay organized.
            </p>
          </div>

          <div className="mb-8 bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Task</h2>
            <form onSubmit={handleCreateTask}>
              <div className="grid grid-cols-1 gap-6">
                <div>
                  <label htmlFor="task-title" className="block text-sm font-medium text-gray-800 mb-1">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    id="task-title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Enter task title"
                  />
                </div>

                <div>
                  <label htmlFor="task-description" className="block text-sm font-medium text-gray-800 mb-1">
                    Description
                  </label>
                  <textarea
                    id="task-description"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
                    placeholder="Enter task description (optional)"
                  />
                </div>

                <div>
                  <button
                    type="submit"
                    disabled={creating}
                    className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-yellow-500 hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50"
                  >
                    {creating ? (
                      <>
                        <LoadingSpinner size="sm" className="mr-2" />
                        Creating...
                      </>
                    ) : 'Create Task'}
                  </button>
                </div>
              </div>
            </form>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Your Tasks</h2>

            {error && <ErrorAlert message={error} />}

            <TaskList
              tasks={tasks}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDeleteTask}
              loading={loading}
              emptyMessage="No tasks yet. Create your first task above!"
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;