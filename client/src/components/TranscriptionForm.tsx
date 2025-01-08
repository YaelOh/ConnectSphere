import React from 'react';
import { Card, CardHeader, CardContent } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Loader2 } from "lucide-react"
import { useTranscription } from '../hooks/useTranscription';

export const TranscriptionForm: React.FC = () => {
  const { transcript, error, loading, transcribe } = useTranscription();
  const [url, setUrl] = React.useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await transcribe(url);
  };

  return (
    <div className="container mx-auto p-4 max-w-2xl">
      <Card>
        <CardHeader>
          <h1 className="text-2xl font-bold text-center">
            Podcast Transcription Tool
          </h1>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter Spotify podcast episode URL"
                required
                className="w-full"
              />
            </div>
            <Button 
              type="submit" 
              disabled={loading}
              className="w-full"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Transcribing...
                </>
              ) : (
                'Transcribe'
              )}
            </Button>
          </form>

          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-500 rounded">
              {error}
            </div>
          )}

          {transcript && (
            <div className="mt-4 p-4 bg-gray-50 rounded">
              <h2 className="text-xl font-semibold mb-2">Transcript:</h2>
              <div className="whitespace-pre-wrap">{transcript}</div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};