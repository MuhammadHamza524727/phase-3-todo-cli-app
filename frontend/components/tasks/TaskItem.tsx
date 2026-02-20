import React, { useState } from 'react';
import { Task } from '../../types';

interface TaskItemProps {
  task: Task;
  onUpdate: (id: string, updates: Partial<Task>) => void;
  onDelete: (id: string) => void;
  onToggleCompletion: (id: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete, onToggleCompletion }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [isDeleting, setIsDeleting] = useState(false);

  const handleSave = () => {
    if (title.trim()) {
      onUpdate(task.id, { title, description: description.trim() || undefined });
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const handleDelete = () => {
    setIsDeleting(true);
    onDelete(task.id);
  };

  const handleToggleCompletion = () => {
    onToggleCompletion(task.id);
  };

  return (
    <li className={`px-4 py-4 sm:px-6 ${task.completed ? 'bg-surface' : 'bg-surface'}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="h-4 w-4 text-accent focus:ring-accent border-border rounded"
          />
          <div className="ml-3 min-w-0 flex-1">
            {isEditing ? (
              <div className="space-y-2">
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="block w-full px-3 py-2 border border-border bg-surface placeholder-text-secondary text-text-primary rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent sm:text-sm"
                  placeholder="Task title"
                />
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="block w-full px-3 py-2 border border-border bg-surface placeholder-text-secondary text-text-primary rounded-md shadow-sm focus:outline-none focus:ring-accent focus:border-accent sm:text-sm"
                  placeholder="Task description (optional)"
                  rows={2}
                />
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={handleSave}
                    className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-success bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-success"
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="inline-flex items-center px-3 py-1 border border-border text-xs font-medium rounded text-text-primary bg-surface hover:bg-surface focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <p className={`text-sm font-medium ${task.completed ? 'line-through text-text-secondary' : 'text-text-primary'}`}>
                  {task.title}
                </p>
                {task.description && (
                  <p className={`text-sm ${task.completed ? 'line-through text-text-secondary' : 'text-text-secondary'}`}>
                    {task.description}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {!isEditing && (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-2.5 py-0.5 border border-border text-xs font-medium rounded text-text-primary bg-surface hover:bg-surface focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent"
            >
              Edit
            </button>
          )}
          <button
            type="button"
            onClick={handleDelete}
            disabled={isDeleting}
            className="inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-surface bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
      <div className="mt-2 flex items-center justify-between">
        <div className="text-xs text-text-secondary">
          Created: {new Date(task.createdAt).toLocaleDateString()}
        </div>
        {task.updatedAt !== task.createdAt && (
          <div className="text-xs text-text-secondary">
            Updated: {new Date(task.updatedAt).toLocaleDateString()}
          </div>
        )}
      </div>
    </li>
  );
};

export default TaskItem;