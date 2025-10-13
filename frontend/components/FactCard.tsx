'use client';

import { FactCheckResult } from '@/types';
import { Share2, CheckCircle, XCircle, AlertCircle, ExternalLink, RotateCcw } from 'lucide-react';

interface FactCardProps {
  result: FactCheckResult;
  onReset: () => void;
}

export default function FactCard({ result, onReset }: FactCardProps) {
  const getRatingColor = (rating: number) => {
    if (rating >= 8) return 'text-green-500';
    if (rating >= 5) return 'text-yellow-500';
    return 'text-red-500';
  };

  const getRatingLabel = (rating: number) => {
    if (rating >= 8) return 'Highly Accurate';
    if (rating >= 6) return 'Mostly Accurate';
    if (rating >= 4) return 'Mixed';
    return 'Inaccurate';
  };

  const handleShare = async () => {
    const shareText = `Fact Check Result: ${result.rating}/10 - ${result.explanation}`;
    
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Mistral Fact Check Result',
          text: shareText,
        });
      } catch (err) {
        console.log('Share cancelled');
      }
    } else {
      navigator.clipboard.writeText(shareText);
      alert('Result copied to clipboard!');
    }
  };

  return (
    <div className="bg-mistral-gray rounded-2xl p-8 shadow-2xl border border-mistral-light-gray">
      {/* Header */}
      <div className="flex justify-between items-start mb-8">
        <div>
          <h2 className="text-2xl font-bold text-white mb-2">Fact Check Result</h2>
          <p className="text-mistral-text/60 text-sm">
            Analyzed via {result.input_type} • {new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={handleShare}
            className="bg-mistral-light-gray hover:bg-mistral-orange text-white p-3 rounded-lg transition-all"
            title="Share result"
          >
            <Share2 size={20} />
          </button>
          <button
            onClick={onReset}
            className="bg-mistral-light-gray hover:bg-mistral-orange text-white p-3 rounded-lg transition-all"
            title="New fact check"
          >
            <RotateCcw size={20} />
          </button>
        </div>
      </div>

      {/* Rating Section */}
      <div className="bg-mistral-dark rounded-xl p-6 mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Rating Score */}
          <div>
            <h3 className="text-mistral-text/70 text-sm font-medium mb-3">Accuracy Rating</h3>
            <div className="flex items-baseline space-x-3">
              <span className={`text-6xl font-bold ${getRatingColor(result.rating)}`}>
                {result.rating.toFixed(1)}
              </span>
              <span className="text-2xl text-mistral-text/50">/10</span>
            </div>
            <p className={`mt-2 font-semibold ${getRatingColor(result.rating)}`}>
              {getRatingLabel(result.rating)}
            </p>
          </div>

          {/* Confidence */}
          <div>
            <h3 className="text-mistral-text/70 text-sm font-medium mb-3">AI Confidence</h3>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-mistral-text">{(result.confidence * 100).toFixed(0)}%</span>
                <span className="text-mistral-text/50">confidence</span>
              </div>
              <div className="w-full bg-mistral-light-gray rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-mistral-orange to-mistral-accent h-3 rounded-full transition-all"
                  style={{ width: `${result.confidence * 100}%` }}
                ></div>
              </div>
              <p className="text-xs text-mistral-text/60 mt-2">
                {result.confidence >= 0.8 ? 'High confidence' : result.confidence >= 0.5 ? 'Moderate confidence' : 'Low confidence'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Explanation */}
      <div className="bg-mistral-dark rounded-xl p-6 mb-6">
        <div className="flex items-start space-x-3">
          <AlertCircle className="text-mistral-orange mt-1 flex-shrink-0" size={20} />
          <div>
            <h3 className="text-white font-semibold mb-2">Explanation</h3>
            <p className="text-mistral-text leading-relaxed">{result.explanation}</p>
          </div>
        </div>
      </div>

      {/* Detailed Analysis */}
      <div className="bg-mistral-dark rounded-xl p-6 mb-6">
        <h3 className="text-white font-semibold mb-3">Detailed Analysis</h3>
        <p className="text-mistral-text leading-relaxed whitespace-pre-wrap">{result.analysis}</p>
      </div>

      {/* Correct & Incorrect Aspects */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Correct Aspects */}
        {result.correct_aspects && result.correct_aspects.length > 0 && (
          <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-6">
            <div className="flex items-center space-x-2 mb-4">
              <CheckCircle className="text-green-500" size={20} />
              <h3 className="text-white font-semibold">Correct Aspects</h3>
            </div>
            <ul className="space-y-2">
              {result.correct_aspects.map((aspect, index) => (
                <li key={index} className="text-green-300 text-sm flex items-start space-x-2">
                  <span className="text-green-500 mt-0.5">✓</span>
                  <span>{aspect}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Incorrect Aspects */}
        {result.incorrect_aspects && result.incorrect_aspects.length > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6">
            <div className="flex items-center space-x-2 mb-4">
              <XCircle className="text-red-500" size={20} />
              <h3 className="text-white font-semibold">Incorrect/Unverified</h3>
            </div>
            <ul className="space-y-2">
              {result.incorrect_aspects.map((aspect, index) => (
                <li key={index} className="text-red-300 text-sm flex items-start space-x-2">
                  <span className="text-red-500 mt-0.5">✗</span>
                  <span>{aspect}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Sources */}
      {result.sources && result.sources.length > 0 && (
        <div className="bg-mistral-dark rounded-xl p-6">
          <h3 className="text-white font-semibold mb-4">Sources</h3>
          <div className="space-y-3">
            {result.sources.map((source, index) => (
              <div
                key={index}
                className="bg-mistral-light-gray rounded-lg p-4 hover:bg-mistral-light-gray/80 transition-all"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="text-white font-medium mb-1">{source.title}</h4>
                    <p className="text-mistral-text/60 text-sm mb-2">{source.relevance}</p>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-mistral-orange hover:text-mistral-accent text-sm flex items-center space-x-1"
                    >
                      <span>View source</span>
                      <ExternalLink size={14} />
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

