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
    <li className="px-5 py-4 sm:px-6 bg-white/5 hover:bg-white/8 transition-colors duration-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center flex-1 min-w-0">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            className="h-4 w-4 text-violet-500 focus:ring-violet-400 border-white/20 rounded bg-white/10 cursor-pointer"
          />
          <div className="ml-3 min-w-0 flex-1">
            {isEditing ? (
              <div className="space-y-2">
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="block w-full px-3 py-2 border border-white/20 bg-white/10 placeholder-indigo-300/50 text-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-violet-400 focus:border-violet-400 sm:text-sm"
                  placeholder="Task title"
                />
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="block w-full px-3 py-2 border border-white/20 bg-white/10 placeholder-indigo-300/50 text-white rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-violet-400 focus:border-violet-400 sm:text-sm"
                  placeholder="Task description (optional)"
                  rows={2}
                />
                <div className="flex space-x-2">
                  <button
                    type="button"
                    onClick={handleSave}
                    className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-semibold rounded-lg text-white bg-emerald-600 hover:bg-emerald-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-400 transition-colors"
                  >
                    Save
                  </button>
                  <button
                    type="button"
                    onClick={handleCancel}
                    className="inline-flex items-center px-3 py-1.5 border border-white/20 text-xs font-semibold rounded-lg text-indigo-200 bg-white/10 hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-400 transition-colors"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div>
                <p className={`text-sm font-medium ${task.completed ? 'line-through text-indigo-300/50' : 'text-white'}`}>
                  {task.title}
                </p>
                {task.description && (
                  <p className={`text-sm mt-0.5 ${task.completed ? 'line-through text-indigo-300/40' : 'text-indigo-200/70'}`}>
                    {task.description}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2 ml-3">
          <button
            type="button"
            onClick={handleToggleCompletion}
            className={`inline-flex items-center px-3 py-1.5 text-xs font-semibold rounded-lg transition-all duration-200 ${
              task.completed
                ? 'text-amber-200 bg-amber-600/30 border border-amber-500/40 hover:bg-amber-600/40'
                : 'text-emerald-200 bg-emerald-600/30 border border-emerald-500/40 hover:bg-emerald-600/40'
            }`}
          >
            {task.completed ? 'Undo' : 'Done'}
          </button>
          {!isEditing && (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-3 py-1.5 border border-white/20 text-xs font-semibold rounded-lg text-indigo-200 bg-white/10 hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-violet-400 transition-colors"
            >
              Edit
            </button>
          )}
          <button
            type="button"
            onClick={handleDelete}
            disabled={isDeleting}
            className="inline-flex items-center px-3 py-1.5 border border-red-500/40 text-xs font-semibold rounded-lg text-red-200 bg-red-600/30 hover:bg-red-600/40 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 disabled:opacity-50 transition-colors"
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
      <div className="mt-2 flex items-center justify-between">
        <div className="text-xs text-indigo-300/50">
          Created: {new Date(task.createdAt).toLocaleDateString()}
        </div>
        {task.updatedAt !== task.createdAt && (
          <div className="text-xs text-indigo-300/50">
            Updated: {new Date(task.updatedAt).toLocaleDateString()}
          </div>
        )}
      </div>
    </li>
  );
};

export default TaskItem;