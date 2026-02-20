'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { isValidEmail } from '../../lib/utils';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { login, isAuthenticated, isLoading } = useAuth();

  // Redirect to dashboard if already authenticated
  React.useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!isValidEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    if (!password.trim()) {
      setError('Please enter your password');
      return;
    }

    setLoading(true);

    try {
      await login(email, password);
      router.replace('/dashboard');
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Invalid credentials or server error';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (isLoading || isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950">
        <div className="animate-spin rounded-full h-14 w-14 border-b-2 border-violet-400"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950 p-6 relative overflow-hidden">
      {/* Subtle background texture layer */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_30%,rgba(139,92,246,0.12),transparent_40%),radial-gradient(circle_at_80%_70%,rgba(167,139,250,0.10),transparent_50%)] pointer-events-none" />

      <div className="w-full max-w-lg relative z-10">
        <div className="bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl shadow-black/40 p-10 md:p-12 transition-all duration-500">
          {/* Header */}
          <div className="text-center mb-10">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-violet-300 via-purple-300 to-fuchsia-300 bg-clip-text text-transparent tracking-tight">
              Welcome Back
            </h2>
            <p className="mt-3 text-lg text-indigo-200/80 font-medium">
              Sign in to continue managing your tasks
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-7">
            {error && (
              <div className="bg-red-900/40 backdrop-blur-sm border border-red-500/30 rounded-2xl p-4 text-center">
                <p className="text-red-200 font-medium text-sm">{error}</p>
              </div>
            )}

            <div className="space-y-6">
              {/* Email */}
              <div>
                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-6 py-5 rounded-2xl bg-white/10 border border-white/15 text-white placeholder-indigo-300/60
                           focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/40
                           transition-all duration-300 shadow-inner hover:shadow-lg hover:bg-white/15"
                  placeholder="Email Address"
                />
              </div>

              {/* Password */}
              <div>
                <input
                  id="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-6 py-5 rounded-2xl bg-white/10 border border-white/15 text-white placeholder-indigo-300/60
                           focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/40
                           transition-all duration-300 shadow-inner hover:shadow-lg hover:bg-white/15"
                  placeholder="Password"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="relative w-full py-5 px-8 text-lg font-semibold rounded-2xl
                       bg-gradient-to-r from-violet-600 to-purple-600 text-white
                       hover:from-violet-500 hover:to-purple-500
                       focus:outline-none focus:ring-2 focus:ring-violet-400 focus:ring-offset-2 focus:ring-offset-indigo-950
                       disabled:opacity-50 shadow-xl shadow-violet-900/40 hover:shadow-2xl hover:shadow-violet-700/50
                       active:scale-[0.98] transition-all duration-300"
            >
              {loading ? (
                <div className="flex items-center justify-center gap-3">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                  Signing in...
                </div>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <p className="mt-10 text-center text-indigo-200/80 text-sm">
            Don{'\''}t have an account?{' '}
            <Link
              href="/signup"
              className="font-semibold text-violet-300 hover:text-violet-200 underline underline-offset-4 transition-colors"
            >
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;