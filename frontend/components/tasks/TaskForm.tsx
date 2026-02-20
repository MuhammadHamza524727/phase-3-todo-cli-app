import React, { useState } from 'react';

interface TaskFormProps {
  onCreateTask: (title: string, description?: string) => void;
}

const TaskForm: React.FC<TaskFormProps> = ({ onCreateTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    if (title.trim().length > 200) {
      setError('Title is too long (max 200 characters)');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      await onCreateTask(title.trim(), description.trim() || undefined);
      setTitle('');
      setDescription('');
    } catch (err) {
      setError('Failed to create task. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-surface shadow sm:rounded-lg p-6">
      <h2 className="text-lg font-medium text-text-primary mb-4">Create New Task</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}
        <div>
          <label htmlFor="task-title" className="block text-sm font-medium text-text-secondary mb-1">
            Title *
          </label>
          <input
            type="text"
            id="task-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="shadow-sm focus:ring-accent focus:border-accent block w-full sm:text-sm border-border bg-surface text-text-primary rounded-md p-2"
            placeholder="What needs to be done?"
            maxLength={200}
          />
          <p className="mt-1 text-xs text-text-secondary">Max 200 characters</p>
        </div>
        <div>
          <label htmlFor="task-description" className="block text-sm font-medium text-text-secondary mb-1">
            Description (optional)
          </label>
          <textarea
            id="task-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="shadow-sm focus:ring-accent focus:border-accent block w-full sm:text-sm border-border bg-surface text-text-primary rounded-md p-2"
            placeholder="Add details about the task..."
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting || !title.trim()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-surface bg-accent hover:bg-accent-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent disabled:opacity-50"
          >
            {isSubmitting ? 'Creating...' : 'Create Task'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;