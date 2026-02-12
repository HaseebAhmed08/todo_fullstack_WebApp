import React from 'react';
import Link from 'next/link';
import { CheckCircle2, Circle, Trash2, Eye, Calendar, Clock } from 'lucide-react';

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
  createdAt,
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

  // Format date
  const dateFormatted = new Date(createdAt).toLocaleDateString(undefined, {
    month: 'short',
    day: 'numeric'
  });

  return (
    <div
      className={`
        bg-white rounded-2xl border border-slate-200 p-5 transition-all duration-300 group
        hover:border-yellow-300 hover:shadow-xl hover:shadow-yellow-500/5 hover:-translate-y-1
        ${completed ? 'bg-slate-50/50' : ''}
      `}
    >
      <div className="flex justify-between items-start mb-4">
        <div className="flex items-start space-x-3">
          <button
            onClick={handleToggleComplete}
            className={`mt-1 flex-shrink-0 transition-all active:scale-90 ${completed ? 'text-green-500' : 'text-slate-300 hover:text-yellow-500'
              }`}
          >
            {completed ? <CheckCircle2 className="h-6 w-6" /> : <Circle className="h-6 w-6" />}
          </button>

          <div className="flex flex-col">
            <h3 className={`font-bold text-lg leading-tight transition-all ${completed ? 'text-slate-400 line-through' : 'text-slate-900 group-hover:text-yellow-600'
              }`}>
              {title}
            </h3>
            <div className="flex items-center space-x-3 mt-1.5">
              <span className="flex items-center text-[10px] font-bold uppercase tracking-wider text-slate-400">
                <Calendar className="h-3 w-3 mr-1" />
                {dateFormatted}
              </span>
              <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${completed ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                }`}>
                {completed ? 'Success' : 'Active'}
              </span>
            </div>
          </div>
        </div>

        <div className="opacity-0 group-hover:opacity-100 flex space-x-1 transition-opacity">
          <button
            onClick={handleDelete}
            className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
            title="Delete Task"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {description && (
        <p className={`text-sm mb-5 line-clamp-2 ${completed ? 'text-slate-400' : 'text-slate-600'}`}>
          {description}
        </p>
      )}

      <div className="pt-4 border-t border-slate-100 flex justify-between items-center">
        <Link
          href={`/tasks/${id}`}
          className="flex items-center space-x-1.5 text-xs font-bold text-slate-400 hover:text-yellow-600 transition-colors"
        >
          <Eye className="h-3.5 w-3.5" />
          <span>Details</span>
        </Link>

        <div className="flex -space-x-2">
          <div className="h-6 w-6 rounded-full border-2 border-white bg-slate-200 flex items-center justify-center text-[8px] font-bold text-slate-500">
            JD
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
