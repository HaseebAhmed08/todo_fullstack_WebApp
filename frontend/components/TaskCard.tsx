import React from 'react';
import Link from 'next/link';

interface TaskCardProps {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  onToggleComplete?: (id: string) => void;
  onDelete?: (id: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title,
  description,
  completed,
  onToggleComplete,
  onDelete
}) => {
  const handleToggleComplete = () => {
    if (onToggleComplete) {
      onToggleComplete(id);
    }
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete(id);
    }
  };

  return (
    <div
      className={`
        bg-white rounded-lg shadow-md p-6 mb-4 transition-all duration-300 ease-in-out transform
        hover:scale-[1.02] hover:shadow-lg
        border-l-4 ${completed ? 'border-green-500' : 'border-yellow-custom'}
      `}
    >
      <div className="flex justify-between items-start">
        <div>
          <h3 className={`text-lg font-semibold ${completed ? 'line-through text-gray-600' : 'text-gray-900'}`}>
            {title}
          </h3>
          {description && (
            <p className="mt-2 text-gray-700">
              {description}
            </p>
          )}
        </div>

        <div className="flex space-x-2">
          <button
            onClick={handleToggleComplete}
            className={`p-2 rounded-full ${
              completed
                ? 'bg-green-100 text-green-600 hover:bg-green-200'
                : 'bg-yellow-100 text-yellow-custom hover:bg-yellow-200'
            }`}
            title={completed ? 'Mark as incomplete' : 'Mark as complete'}
            aria-label={completed ? 'Mark task as incomplete' : 'Mark task as complete'}
          >
            {completed ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            )}
          </button>

          <button
            onClick={handleDelete}
            className="p-2 rounded-full bg-red-100 text-red-600 hover:bg-red-200"
            title="Delete task"
            aria-label="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <div className="mt-4 flex justify-between items-center">
        <span className={`text-xs px-2 py-1 rounded-full ${completed ? 'bg-green-100 text-green-900' : 'bg-yellow-100 text-yellow-900'}`}>
          {completed ? 'Completed' : 'Pending'}
        </span>

        <Link
          href={`/tasks/${id}`}
          className="text-sm text-yellow-600 hover:text-yellow-700 font-medium"
        >
          View details →
        </Link>
      </div>
    </div>
  );
};

export default TaskCard;