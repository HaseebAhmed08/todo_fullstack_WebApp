'use client';

import React, { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useTasks } from '@/hooks/useTasks';
import Header from '@/components/Header';
import TaskList from '@/components/TaskList';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';
import ProtectedRoute from '@/components/ProtectedRoute';

const DashboardPage: React.FC = () => {
  const { session, loading: authLoading } = useAuth();
  const { tasks, loading, error, addTask, deleteTask, toggleComplete } = useTasks(session?.user?.id || null);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [creating, setCreating] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) {
      setFormError('Task title is required');
      return;
    }

    if (!session?.user?.id || authLoading) {
      setFormError('User not authenticated or still loading');
      return;
    }

    setCreating(true);
    setFormError(null);

    try {
      await addTask(newTaskTitle, newTaskDescription);
      setNewTaskTitle('');
      setNewTaskDescription('');
    } catch (err: any) {
      console.error('Error creating task:', err);
      setFormError(err.message || 'Failed to create task');
    } finally {
      setCreating(false);
    }
  };

  const handleToggleComplete = async (id: string) => {
    try {
      await toggleComplete(id);
    } catch (err: any) {
      console.error('Error toggling task:', err);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await deleteTask(id);
    } catch (err: any) {
      console.error('Error deleting task:', err);
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
    <ProtectedRoute>
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

              {(error || formError) && <ErrorAlert message={formError || error || ''} />}

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
    </ProtectedRoute>
  );
};

export default DashboardPage;
