'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../../services/tasks';
import TaskList from '../../components/tasks/TaskList';
import TaskForm from '../../components/tasks/TaskForm';
import ChatInterface from '../../components/chat/ChatInterface';
import { Task, ToolCall } from '../../types';

const DashboardPage = () => {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace('/login');
    }
  }, [isAuthenticated, isLoading, router]);

  const loadTasks = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      loadTasks();
    }
  }, [isAuthenticated, loadTasks]);

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

  // Refresh task list when chatbot performs task operations (T034)
  const handleToolCall = useCallback((toolCalls: ToolCall[]) => {
    const taskMutationTools = ['add_task', 'complete_task', 'update_task', 'delete_task'];
    const hasMutation = toolCalls.some(tc => taskMutationTools.includes(tc.tool));
    if (hasMutation) {
      loadTasks();
    }
  }, [loadTasks]);

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

            <div className="flex items-center gap-3">
              {/* Chat toggle button */}
              <button
                onClick={() => setChatOpen(!chatOpen)}
                className={`px-4 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center gap-2 ${
                  chatOpen
                    ? 'bg-violet-500/30 border border-violet-400/40 text-violet-200'
                    : 'bg-white/10 border border-white/10 text-indigo-200 hover:bg-white/15'
                }`}
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                  <path fillRule="evenodd" d="M10 2c-2.236 0-4.43.18-6.57.524C1.993 2.755 1 4.014 1 5.426v5.148c0 1.413.993 2.67 2.43 2.902.848.137 1.705.248 2.57.331v3.443a.75.75 0 0 0 1.28.53l3.58-3.579a.78.78 0 0 1 .527-.224 41.202 41.202 0 0 0 5.183-.5c1.437-.232 2.43-1.49 2.43-2.903V5.426c0-1.413-.993-2.67-2.43-2.902A41.289 41.289 0 0 0 10 2Z" clipRule="evenodd" />
                </svg>
                <span className="hidden sm:inline">AI Chat</span>
              </button>

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
        </div>
      </nav>

      <div className="flex relative z-10">
        {/* Main content */}
        <main className={`flex-1 max-w-7xl mx-auto px-6 py-10 md:py-12 transition-all duration-300 ${chatOpen ? 'mr-[400px] lg:mr-[420px]' : ''}`}>
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
                <p className="mt-3 text-lg">Add your first task above or ask the AI chat to help!</p>
              </div>
            )}
          </div>
        </main>

        {/* Chat panel — slide-out from right */}
        {chatOpen && (
          <>
            {/* Mobile overlay backdrop */}
            <div
              className="fixed inset-0 bg-black/50 z-30 lg:hidden"
              onClick={() => setChatOpen(false)}
            />

            {/* Chat panel */}
            <div className="fixed top-[64px] right-0 bottom-0 w-full sm:w-[400px] lg:w-[420px] z-40 bg-indigo-950/95 backdrop-blur-2xl border-l border-white/10 shadow-2xl shadow-black/50 flex flex-col">
              {/* Close button for mobile */}
              <button
                onClick={() => setChatOpen(false)}
                className="absolute top-3 right-3 z-50 lg:hidden p-1 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4 text-indigo-200">
                  <path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
                </svg>
              </button>

              <ChatInterface onToolCall={handleToolCall} />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
