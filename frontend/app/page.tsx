'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../lib/auth-context';

const HomePage = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950">
        <div className="text-center space-y-5">
          <div className="animate-spin rounded-full h-14 w-14 border-b-2 border-violet-400 mx-auto"></div>
          <p className="text-indigo-200/90 text-xl font-medium">Checking authentication...</p>
        </div>
      </div>
    );
  }

  return (
    <div className=" min-h-screen bg-gradient-to-br from-indigo-950 via-purple-950 to-violet-950 text-white antialiased relative overflow-hidden">
      {/* Subtle background overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_10%_20%,rgba(139,92,246,0.09),transparent_50%),radial-gradient(circle_at_90%_80%,rgba(167,139,250,0.07),transparent_60%)] pointer-events-none" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 pt-20 pb-24 lg:pt-32 lg:pb-40">
        <div className="lg:flex lg:items-center lg:justify-between gap-12">
          {/* Left - Content */}
          <div className="lg:max-w-2xl text-center lg:text-left">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight">
              <span className="block bg-gradient-to-r from-violet-300 via-purple-300 to-fuchsia-300 bg-clip-text text-transparent">
                Manage Tasks
              </span>
              <span className="block mt-2 text-indigo-200/90">with Elegance</span>
            </h1>

            <p className="mt-6 text-lg sm:text-xl text-indigo-200/80 max-w-xl mx-auto lg:mx-0 leading-relaxed">
              A clean, secure, and beautiful task manager built for focus and productivity.
              Start organizing your day in seconds.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-5">
              {isAuthenticated ? (
                <Link
                  href="/dashboard"
                  className="inline-flex items-center justify-center px-10 py-5 text-lg font-semibold rounded-2xl
                           bg-gradient-to-r from-violet-600 to-purple-600 text-white
                           hover:from-violet-500 hover:to-purple-500
                           shadow-xl shadow-violet-900/40 hover:shadow-2xl hover:shadow-violet-700/50
                           hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-300"
                >
                  Go to Dashboard
                </Link>
              ) : (
                <Link
                  href="/signup"
                  className="inline-flex items-center justify-center px-10 py-5 text-lg font-semibold rounded-2xl
                           bg-gradient-to-r from-violet-600 to-purple-600 text-white
                           hover:from-violet-500 hover:to-purple-500
                           shadow-xl shadow-violet-900/40 hover:shadow-2xl hover:shadow-violet-700/50
                           hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-300"
                >
                  Get Started
                </Link>
              )}

              {!isAuthenticated && (
                <Link
                  href="/login"
                  className="inline-flex items-center justify-center px-10 py-5 text-lg font-semibold rounded-2xl
                           border border-white/20 bg-white/5 backdrop-blur-xl text-indigo-200
                           hover:bg-white/10 hover:border-violet-500/40 hover:text-white
                           transition-all duration-300"
                >
                  Sign In
                </Link>
              )}
            </div>
          </div>

          {/* Right - Smaller Preview Card */}
          <div className="mt-16 lg:mt-0 lg:w-5/12 hidden lg:block">
            <div className="relative">
              {/* Glow effects */}
              <div className="absolute -inset-10 bg-gradient-to-br from-violet-600/20 to-purple-600/10 rounded-full blur-3xl opacity-40 animate-pulse-slow pointer-events-none" />

              {/* Glass preview card - smaller size */}
              <div className="relative rounded-3xl overflow-hidden border border-white/10 bg-white/5 backdrop-blur-2xl shadow-2xl shadow-black/50">
                <img
                  src="/images/image.png" // ← replace with your actual screenshot path
                  alt="Speckit dashboard preview - dark mode task manager"
                  className="w-full h-auto object-cover"
                  width={500}
                  height={320}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-indigo-950/70 via-transparent to-transparent pointer-events-none" />
                <div className="absolute bottom-4 left-4 right-4 flex items-center justify-between text-xs">
                  <span className="text-indigo-200/90 font-medium"> Inbuild Task Agent</span>
                  <span className="text-violet-300/80">Secure • Modern • Fast</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;