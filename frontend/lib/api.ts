import axios from 'axios';
import { FactCheckResult } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const factCheckText = async (text: string, context?: string): Promise<FactCheckResult> => {
  const response = await api.post<FactCheckResult>('/api/fact-check/text', {
    text,
    context,
  });
  return response.data;
};

export const factCheckURL = async (url: string): Promise<FactCheckResult> => {
  const response = await api.post<FactCheckResult>('/api/fact-check/url', {
    url,
  });
  return response.data;
};

export const factCheckImage = async (file: File): Promise<FactCheckResult> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post<FactCheckResult>('/api/fact-check/image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;

