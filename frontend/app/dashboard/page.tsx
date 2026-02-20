'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../../services/tasks';
import TaskList from '../../components/tasks/TaskList';
import TaskForm from '../../components/tasks/TaskForm';
import { Task } from '../../types';

const DashboardPage = () => {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  useEffect(() => {
    if (isAuthenticated) {
      loadTasks();
    }
  }, [isAuthenticated]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await fetchTasks();
      setTasks(tasksData);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load tasks';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description?: string) => {
    try {
      const newTask = await createTask({ title, description });
      setTasks([newTask, ...tasks]);
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create task';
      setError(errorMessage);
    }
  };

  const handleUpdateTask = async (id: string, updates: Partial<Task>) => {
    try {
      const updatedTask = await updateTask(id, updates);
      setTasks(tasks.map(task => (task.id === id ? updatedTask : task)));
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update task';
      setError(errorMessage);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete task';
      setError(errorMessage);
    }
  };

  const handleToggleCompletion = async (id: string) => {
    try {
      const currentTask = tasks.find(task => task.id === id);
      if (currentTask) {
        const updatedTask = await toggleTaskCompletion(id, !currentTask.completed);
        setTasks(tasks.map(task => (task.id === id ? updatedTask : task)));
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to toggle task completion';
      setError(errorMessage);
    }
  };

  if (isLoading || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950">
        <div className="text-center space-y-5">
          <div className="animate-spin rounded-full h-14 w-14 border-b-2 border-violet-400 mx-auto"></div>
          <p className="text-indigo-200/90 text-xl font-medium">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950 text-white antialiased relative overflow-x-hidden">
      {/* Subtle background overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_25%,rgba(139,92,246,0.08),transparent_50%),radial-gradient(circle_at_85%_75%,rgba(167,139,250,0.06),transparent_60%)] pointer-events-none" />

      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white/5 backdrop-blur-2xl border-b border-white/10 shadow-xl shadow-black/30">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between h-16 md:h-18">
            <div className="flex items-center gap-4">
              <h1 className="text-3xl md:text-4xl font-extrabold bg-gradient-to-r from-violet-300 via-purple-300 to-fuchsia-300 bg-clip-text text-transparent tracking-tight">
                Modern Todo
              </h1>
              <span className="text-sm md:text-base text-indigo-300/80 font-medium hidden sm:block">
                Tasks
              </span>
            </div>

            <button
              onClick={logout}
              className="px-6 py-2.5 rounded-xl text-base font-semibold
                       bg-gradient-to-r from-violet-600 to-purple-600
                       hover:from-violet-500 hover:to-purple-500
                       shadow-lg shadow-violet-900/40 hover:shadow-xl hover:shadow-violet-700/50
                       hover:-translate-y-0.5 active:scale-95 transition-all duration-300"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-10 md:py-12 relative z-10">
        <div className="space-y-10 md:space-y-12">
          {/* Task Input Card */}
          <div className="bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl shadow-black/40 p-8 md:p-10 transition-all duration-500">
            <h2 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-violet-300 via-purple-300 to-fuchsia-300 bg-clip-text text-transparent mb-8 tracking-tight">
              Your Tasks
            </h2>

            <TaskForm onCreateTask={handleCreateTask} />
          </div>

          {error && (
            <div className="bg-red-900/40 backdrop-blur-sm border border-red-500/30 rounded-2xl p-5 text-center">
              <p className="text-red-200 font-medium">{error}</p>
            </div>
          )}

          {/* Tasks List Card */}
          <div className="bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl shadow-black/40 overflow-hidden">
            <TaskList
              tasks={tasks}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
              onToggleCompletion={handleToggleCompletion}
            />
          </div>

          {/* Empty state */}
          {tasks.length === 0 && !loading && (
            <div className="text-center py-20 text-indigo-300/70">
              <p className="text-2xl font-medium">No tasks yet...</p>
              <p className="mt-3 text-lg">Add your first task above to get started!</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;