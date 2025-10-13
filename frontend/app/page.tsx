'use client';

import { useState } from 'react';
import FactChecker from '@/components/FactChecker';
import FactCard from '@/components/FactCard';
import PasswordGate from '@/components/PasswordGate';
import { FactCheckResult } from '@/types';

export default function Home() {
  const [result, setResult] = useState<FactCheckResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFactCheckComplete = (data: FactCheckResult) => {
    setResult(data);
    setIsLoading(false);
  };

  const handleFactCheckStart = () => {
    setIsLoading(true);
    setResult(null);
  };

  const handleReset = () => {
    setResult(null);
    setIsLoading(false);
  };

  return (
    <PasswordGate>
    <main className="min-h-screen bg-gradient-to-br from-mistral-dark via-mistral-gray to-mistral-dark">
      {/* Header */}
      <header className="border-b border-mistral-light-gray bg-mistral-dark/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-mistral-orange to-mistral-accent rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Mistral Fact Checker</h1>
              <p className="text-sm text-mistral-text/70">AI-powered fact verification</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Description */}
          {!result && !isLoading && (
            <div className="text-center space-y-4 animate-fade-in">
              <h2 className="text-4xl font-bold text-white">
                Verify Information with <span className="text-mistral-orange">AI</span>
              </h2>
              <p className="text-lg text-mistral-text/80 max-w-2xl mx-auto">
                Upload an image, paste a link, or enter text to get instant fact-checking powered by Mistral AI.
                Get detailed analysis with sources and confidence ratings.
              </p>
            </div>
          )}

          {/* Fact Checker Input */}
          {!result && (
            <FactChecker
              onFactCheckComplete={handleFactCheckComplete}
              onFactCheckStart={handleFactCheckStart}
              isLoading={isLoading}
            />
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="flex flex-col items-center justify-center py-20 space-y-4">
              <div className="relative">
                <div className="w-20 h-20 border-4 border-mistral-light-gray rounded-full"></div>
                <div className="w-20 h-20 border-4 border-mistral-orange border-t-transparent rounded-full animate-spin absolute top-0 left-0"></div>
              </div>
              <p className="text-mistral-text text-lg">Analyzing with Mistral AI...</p>
              <p className="text-mistral-text/60 text-sm">This may take a few moments</p>
            </div>
          )}

          {/* Fact Card Result */}
          {result && !isLoading && (
            <div className="animate-slide-up">
              <FactCard result={result} onReset={handleReset} />
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-20 border-t border-mistral-light-gray bg-mistral-dark/50 backdrop-blur-sm py-8">
        <div className="container mx-auto px-4 text-center text-mistral-text/60">
          <p>Powered by Mistral AI • Built with Next.js & FastAPI</p>
          <p className="mt-2 text-sm">Always verify important information from multiple sources</p>
        </div>
      </footer>
    </main>
    </PasswordGate>
  );
}
