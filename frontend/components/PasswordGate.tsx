'use client';

import { useState, useEffect, FormEvent } from 'react';
import { Lock, Eye, EyeOff } from 'lucide-react';

interface PasswordGateProps {
  children: React.ReactNode;
}

export default function PasswordGate({ children }: PasswordGateProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if already authenticated in session storage
    const authenticated = sessionStorage.getItem('fact_checker_authenticated');
    if (authenticated === 'true') {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // The password is "mistral2024" - you can change this
    const correctPassword = process.env.NEXT_PUBLIC_APP_PASSWORD || 'mistral2025';

    if (password === correctPassword) {
      sessionStorage.setItem('fact_checker_authenticated', 'true');
      setIsAuthenticated(true);
    } else {
      setError('Incorrect password. Please try again.');
      setPassword('');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-mistral-dark via-mistral-gray to-mistral-dark flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-mistral-light-gray border-t-mistral-orange rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-mistral-dark via-mistral-gray to-mistral-dark flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          {/* Lock Icon */}
          <div className="text-center mb-8 animate-fade-in">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-mistral-orange to-mistral-accent rounded-2xl mb-4 shadow-lg">
              <Lock className="w-10 h-10 text-white" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">Protected Access</h1>
            <p className="text-mistral-text/70">Enter password to access the Fact Checker</p>
          </div>

          {/* Password Form */}
          <form onSubmit={handleSubmit} className="bg-mistral-gray rounded-2xl p-8 shadow-2xl border border-mistral-light-gray animate-slide-up">
            <div className="mb-6">
              <label htmlFor="password" className="block text-mistral-text font-medium mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                  className="w-full bg-mistral-dark text-mistral-text rounded-xl px-4 py-3 pr-12 border border-mistral-light-gray focus:border-mistral-orange focus:ring-2 focus:ring-mistral-orange/20 outline-none transition-all"
                  autoFocus
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-mistral-text/50 hover:text-mistral-text transition-colors"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {error && (
              <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-xl p-4 text-red-400 text-sm animate-fade-in">
                {error}
              </div>
            )}

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-mistral-orange to-mistral-accent text-white font-semibold py-4 rounded-xl hover:shadow-lg hover:shadow-mistral-orange/30 transition-all flex items-center justify-center space-x-2"
            >
              <Lock size={20} />
              <span>Unlock Access</span>
            </button>

            <p className="text-mistral-text/50 text-xs text-center mt-4">
              Contact the administrator if you need access
            </p>
          </form>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}

