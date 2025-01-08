interface TranscriptionResponse {
    transcript: string;
    error?: string;
  }
  
  interface TranscriptionError {
    error: string;
  }
  
  // Type guard function that we'll use
  const isTranscriptionResponse = (data: unknown): data is TranscriptionResponse => {
    return typeof data === 'object' && 
           data !== null &&
           'transcript' in data &&
           typeof (data as TranscriptionResponse).transcript === 'string' &&
           ((data as TranscriptionResponse).error === undefined || 
            typeof (data as TranscriptionResponse).error === 'string');
  };
  
  export const transcribeAudio = async (url: string): Promise<TranscriptionResponse> => {
    if (!url) {
      return { transcript: '', error: 'URL is required' };
    }
  
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/transcribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
  
      if (!response.ok) {
        const errorData: TranscriptionError = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      
      // Use the type guard to validate the response
      if (isTranscriptionResponse(data)) {
        return data;
      } else {
        throw new Error('Invalid response format from server');
      }
      
    } catch (error) {
      if (error instanceof Error) {
        return { transcript: '', error: error.message };
      }
      return { transcript: '', error: 'An unknown error occurred' };
    }
  };