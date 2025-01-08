import { useState } from 'react';
import { transcribeAudio } from '../services/api';

interface TranscriptionHook {
  transcript: string;
  error: string;
  loading: boolean;
  transcribe: (url: string) => Promise<void>;
}

export const useTranscription = (): TranscriptionHook => {
  const [transcript, setTranscript] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const transcribe = async (url: string): Promise<void> => {
    if (!url) {
      setError('Please provide a valid URL');
      return;
    }

    setLoading(true);
    setError('');
    setTranscript('');

    try {
      const response = await transcribeAudio(url);
      
      if (response.error) {
        setError(response.error);
      } else {
        setTranscript(response.transcript);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return {
    transcript,
    error,
    loading,
    transcribe,
  };
};