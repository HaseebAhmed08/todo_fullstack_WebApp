'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import Header from '@/components/Header';
import LoadingSpinner from '@/components/LoadingSpinner';
import ErrorAlert from '@/components/ErrorAlert';
import ProtectedRoute from '@/components/ProtectedRoute';
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

const TaskDetailPage: React.FC = () => {
  const params = useParams();
  const router = useRouter();
  const { session, loading: authLoading } = useAuth();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    completed: false,
  });

  // Get task ID from URL
  const taskId = params.id as string;

  // Fetch task details
  useEffect(() => {
    const fetchTask = async () => {
      // Check if user is authenticated before fetching task
      if (!taskId || !session?.user?.id || authLoading) {
        // Redirect to login if not authenticated
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        return;
      }

      try {
        setLoading(true);
        setError(null);

        // Fetch task from API
        const fetchedTask = await taskApi.getTask(taskId) as any;

        const normalizedTask: Task = {
          id: fetchedTask.id,
          title: fetchedTask.title,
          description: fetchedTask.description,
          completed: fetchedTask.completed,
          userId: fetchedTask.user_id,
          createdAt: new Date(fetchedTask.created_at),
          updatedAt: new Date(fetchedTask.updated_at)
        };

        setTask(normalizedTask);
        setFormData({
          title: normalizedTask.title,
          description: normalizedTask.description || '',
          completed: normalizedTask.completed,
        });
      } catch (err) {
        setError(handleApiError(err));
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId, session?.user?.id, authLoading]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim()) {
      setError('Task title is required');
      return;
    }

    if (!session?.user?.id || authLoading) {
      setError('User not authenticated or still loading');
      return;
    }

    setUpdating(true);
    setError(null);

    try {
      // Update task via API
      const updatedTask = await taskApi.updateTask(taskId, {
        title: formData.title,
        description: formData.description,
        completed: formData.completed,
      });

      setTask(updatedTask);
      setFormData({
        title: updatedTask.title,
        description: updatedTask.description || '',
        completed: updatedTask.completed,
      });
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    if (!session?.user?.id || authLoading) {
      setError('User not authenticated or still loading');
      return;
    }

    setDeleting(true);
    setError(null);

    try {
      // Delete task via API
      await taskApi.deleteTask(taskId);

      // Redirect back to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError(handleApiError(err));
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">Task not found</h2>
          <button
            onClick={() => router.push('/dashboard')}
            className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-yellow-500 hover:bg-yellow-600"
          >
            Back to Dashboard
          </button>
        </div>
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
              <button
                onClick={() => router.back()}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                ← Back
              </button>
              <h1 className="text-3xl font-bold text-gray-900 mt-4">Task Details</h1>
            </div>

            <div className="md:grid md:grid-cols-3 md:gap-6">
              <div className="md:col-span-1">
                <div className="px-4 sm:px-0">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Task Information</h3>
                  <p className="mt-1 text-sm text-gray-700">
                    View and edit the details of your task.
                  </p>
                </div>
              </div>
              <div className="mt-5 md:mt-0 md:col-span-2">
                <form onSubmit={handleUpdate}>
                  <div className="shadow sm:rounded-md sm:overflow-hidden">
                    <div className="px-4 py-5 bg-white sm:p-6">
                      <div className="grid grid-cols-6 gap-6">
                        <div className="col-span-6">
                          <label htmlFor="title" className="block text-sm font-medium text-gray-800">
                            Title *
                          </label>
                          <input
                            type="text"
                            name="title"
                            id="title"
                            value={formData.title}
                            onChange={handleChange}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
                          />
                        </div>

                        <div className="col-span-6">
                          <label htmlFor="description" className="block text-sm font-medium text-gray-800">
                            Description
                          </label>
                          <textarea
                            id="description"
                            name="description"
                            rows={4}
                            value={formData.description}
                            onChange={handleChange}
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
                          />
                        </div>

                        <div className="col-span-6">
                          <div className="flex items-center">
                            <input
                              id="completed"
                              name="completed"
                              type="checkbox"
                              checked={formData.completed}
                              onChange={handleChange}
                              className="h-4 w-4 text-yellow-500 focus:ring-yellow-500 border-gray-300 rounded"
                            />
                            <label htmlFor="completed" className="ml-2 block text-sm text-gray-800">
                              Mark as completed
                            </label>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="px-4 py-3 bg-gray-50 text-right sm:px-6 flex justify-between">
                      <button
                        type="button"
                        onClick={handleDelete}
                        disabled={deleting}
                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
                      >
                        {deleting ? 'Deleting...' : 'Delete Task'}
                      </button>
                      <button
                        type="submit"
                        disabled={updating}
                        className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-yellow-500 hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50"
                      >
                        {updating ? 'Updating...' : 'Save Changes'}
                      </button>
                    </div>
                  </div>
                </form>

                {error && <ErrorAlert message={error} className="mt-4" />}
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default TaskDetailPage;