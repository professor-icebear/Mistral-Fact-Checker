export interface Source {
  title: string;
  url: string;
  relevance: string;
}

export interface FactCheckResult {
  rating: number;
  explanation: string;
  confidence: number;
  analysis: string;
  correct_aspects: string[];
  incorrect_aspects: string[];
  sources: Source[];
  timestamp: string;
  input_type: 'text' | 'url' | 'image';
}

export type InputType = 'text' | 'url' | 'image';

