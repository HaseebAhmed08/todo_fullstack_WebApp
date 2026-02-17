import React from 'react';
import TaskCard from './TaskCard';

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}

interface TaskListProps {
  tasks: Task[];
  onToggleComplete?: (id: string) => void;
  onDelete?: (id: string) => void;
  loading?: boolean;
  emptyMessage?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleComplete,
  onDelete,
  loading = false,
  emptyMessage = 'No tasks found. Create your first task!'
}) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-10">
        <div className="text-center">
          <p>Loading tasks...</p>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="text-gray-700">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          id={task.id}
          title={task.title}
          description={task.description}
          completed={task.completed}
          createdAt={task.createdAt}
          updatedAt={task.updatedAt}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default TaskList;
