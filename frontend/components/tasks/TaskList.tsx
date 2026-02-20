import React from 'react';
import TaskItem from './TaskItem';
import { Task } from '../../types';

interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (id: string, updates: Partial<Task>) => void;
  onDeleteTask: (id: string) => void;
  onToggleCompletion: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onUpdateTask, onDeleteTask, onToggleCompletion }) => {
  // Check if there are no tasks
  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-accent"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-text-primary">No tasks</h3>
        <p className="mt-1 text-sm text-text-secondary">Get started by creating a new task.</p>
      </div>
    );
  }

  return (
    <div className="bg-surface shadow overflow-hidden sm:rounded-md">
      <ul className="divide-y divide-border">
        {tasks
          .filter((task): task is Task => Boolean(task && task.id))
          .map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={onUpdateTask}
              onDelete={onDeleteTask}
              onToggleCompletion={onToggleCompletion}
            />
          ))}
      </ul>
    </div>
  );
};

export default TaskList;