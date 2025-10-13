'use client';

import { useState, useRef, ChangeEvent } from 'react';
import { Upload, Link as LinkIcon, FileText, X } from 'lucide-react';
import { factCheckText, factCheckURL, factCheckImage } from '@/lib/api';
import { FactCheckResult, InputType } from '@/types';

interface FactCheckerProps {
  onFactCheckComplete: (result: FactCheckResult) => void;
  onFactCheckStart: () => void;
  isLoading: boolean;
}

export default function FactChecker({ onFactCheckComplete, onFactCheckStart, isLoading }: FactCheckerProps) {
  const [inputType, setInputType] = useState<InputType>('text');
  const [textInput, setTextInput] = useState('');
  const [urlInput, setUrlInput] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select an image file');
        return;
      }
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      setError(null);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async () => {
    setError(null);
    onFactCheckStart();

    try {
      let result: FactCheckResult;

      if (inputType === 'text') {
        if (!textInput.trim()) {
          setError('Please enter some text to fact-check');
          return;
        }
        result = await factCheckText(textInput);
      } else if (inputType === 'url') {
        if (!urlInput.trim()) {
          setError('Please enter a URL to fact-check');
          return;
        }
        result = await factCheckURL(urlInput);
      } else {
        if (!selectedFile) {
          setError('Please select an image to fact-check');
          return;
        }
        result = await factCheckImage(selectedFile);
      }

      onFactCheckComplete(result);
      setTextInput('');
      setUrlInput('');
      clearFile();
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fact-check. Please try again.');
      onFactCheckComplete({} as FactCheckResult);
    }
  };

  return (
    <div className="bg-mistral-gray rounded-2xl p-8 shadow-2xl border border-mistral-light-gray">
      {/* Input Type Tabs */}
      <div className="flex space-x-2 mb-6 bg-mistral-dark rounded-xl p-1">
        {[
          { type: 'text' as InputType, icon: FileText, label: 'Text' },
          { type: 'url' as InputType, icon: LinkIcon, label: 'URL' },
          { type: 'image' as InputType, icon: Upload, label: 'Image' },
        ].map(({ type, icon: Icon, label }) => (
          <button
            key={type}
            onClick={() => setInputType(type)}
            className={`flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg transition-all ${
              inputType === type
                ? 'bg-mistral-orange text-white shadow-lg'
                : 'text-mistral-text/70 hover:text-mistral-text hover:bg-mistral-light-gray'
            }`}
            disabled={isLoading}
          >
            <Icon size={20} />
            <span className="font-medium">{label}</span>
          </button>
        ))}
      </div>

      {/* Input Areas */}
      <div className="mb-6">
        {inputType === 'text' && (
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Enter text to fact-check... (e.g., claims, statements, or information)"
            className="w-full h-40 bg-mistral-dark text-mistral-text rounded-xl px-4 py-3 border border-mistral-light-gray focus:border-mistral-orange focus:ring-2 focus:ring-mistral-orange/20 outline-none transition-all resize-none"
            disabled={isLoading}
          />
        )}

        {inputType === 'url' && (
          <input
            type="url"
            value={urlInput}
            onChange={(e) => setUrlInput(e.target.value)}
            placeholder="Enter URL to fact-check... (e.g., https://example.com/article)"
            className="w-full bg-mistral-dark text-mistral-text rounded-xl px-4 py-3 border border-mistral-light-gray focus:border-mistral-orange focus:ring-2 focus:ring-mistral-orange/20 outline-none transition-all"
            disabled={isLoading}
          />
        )}

        {inputType === 'image' && (
          <div>
            {!selectedFile ? (
              <div
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-mistral-light-gray rounded-xl p-12 text-center hover:border-mistral-orange transition-all cursor-pointer bg-mistral-dark/50"
              >
                <Upload className="mx-auto mb-4 text-mistral-orange" size={48} />
                <p className="text-mistral-text font-medium mb-2">Click to upload image</p>
                <p className="text-mistral-text/60 text-sm">PNG, JPG, GIF up to 10MB</p>
              </div>
            ) : (
              <div className="relative rounded-xl overflow-hidden bg-mistral-dark p-4">
                <button
                  onClick={clearFile}
                  className="absolute top-6 right-6 bg-mistral-gray/90 hover:bg-red-600 text-white p-2 rounded-full transition-all z-10"
                >
                  <X size={20} />
                </button>
                <img
                  src={previewUrl!}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg"
                />
                <p className="text-mistral-text/70 text-sm mt-4 text-center">{selectedFile.name}</p>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
              disabled={isLoading}
            />
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-xl p-4 text-red-400">
          {error}
        </div>
      )}

      {/* Submit Button */}
      <button
        onClick={handleSubmit}
        disabled={isLoading}
        className="w-full bg-gradient-to-r from-mistral-orange to-mistral-accent text-white font-semibold py-4 rounded-xl hover:shadow-lg hover:shadow-mistral-orange/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
      >
        {isLoading ? (
          <>
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <span>Analyzing...</span>
          </>
        ) : (
          <span>Fact Check</span>
        )}
      </button>

      {/* Info */}
      <p className="text-mistral-text/50 text-xs text-center mt-4">
        Results are generated by AI and should be verified from multiple sources
      </p>
    </div>
  );
}

