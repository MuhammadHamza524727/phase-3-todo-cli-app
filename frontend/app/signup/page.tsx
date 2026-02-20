'use client';
import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../lib/auth-context';
import { isValidEmail, isValidPassword } from '../../lib/utils';

const SignupPage = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { signup, isAuthenticated, isLoading } = useAuth();

  // Redirect to dashboard if already authenticated
  React.useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace('/dashboard');
    }
  }, [isAuthenticated, isLoading, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!name.trim()) {
      setError('Please enter your name');
      return;
    }
    if (!isValidEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }
    if (!isValidPassword(password)) {
      setError('Password must be at least 8 characters with uppercase, lowercase, and number');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      await signup({ email, password, password_confirm: confirmPassword, name });
      router.replace('/dashboard');
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred during signup';
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
      {/* Optional subtle background texture/animation layer */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_30%,rgba(139,92,246,0.12),transparent_40%),radial-gradient(circle_at_80%_70%,rgba(167,139,250,0.10),transparent_50%)] pointer-events-none" />

      <div className="w-full max-w-lg relative z-10">
        <div className="bg-white/5 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl shadow-black/40 p-10 md:p-12 transition-all duration-500">
          {/* Header */}
          <div className="text-center mb-10">
            <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-violet-300 via-purple-300 to-fuchsia-300 bg-clip-text text-transparent tracking-tight">
              Create Account
            </h2>
            <p className="mt-3 text-lg text-indigo-200/80 font-medium">
              Start managing your tasks in style
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-7">
            {error && (
              <div className="bg-red-900/40 backdrop-blur-sm border border-red-500/30 rounded-2xl p-4 text-center">
                <p className="text-red-200 font-medium text-sm">{error}</p>
              </div>
            )}

            <div className="space-y-6">
              {/* Name */}
              <div>
                <input
                  id="name"
                  type="text"
                  autoComplete="name"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-6 py-5 rounded-2xl bg-white/10 border border-white/15 text-white placeholder-indigo-300/60
                           focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/40
                           transition-all duration-300 shadow-inner hover:shadow-lg hover:bg-white/15"
                  placeholder="Full Name"
                />
              </div>

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
                  autoComplete="new-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-6 py-5 rounded-2xl bg-white/10 border border-white/15 text-white placeholder-indigo-300/60
                           focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/40
                           transition-all duration-300 shadow-inner hover:shadow-lg hover:bg-white/15"
                  placeholder="Password"
                />
              </div>

              {/* Confirm Password */}
              <div>
                <input
                  id="confirm-password"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="w-full px-6 py-5 rounded-2xl bg-white/10 border border-white/15 text-white placeholder-indigo-300/60
                           focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500/40
                           transition-all duration-300 shadow-inner hover:shadow-lg hover:bg-white/15"
                  placeholder="Confirm Password"
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
                  Creating...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <p className="mt-10 text-center text-indigo-200/80 text-sm">
            Already have an account?{' '}
            <Link
              href="/login"
              className="font-semibold text-violet-300 hover:text-violet-200 underline underline-offset-4 transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;