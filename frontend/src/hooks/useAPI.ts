import { useState, useCallback } from 'react';
import type { PromptRequest, PromptResponse, ProgressData, APIError } from '@/types';

export interface UseAPIReturn {
  isLoading: boolean;
  error: string | null;
  clearError: () => void;
  generateSinglePrompt: (
    request: PromptRequest,
    onProgress?: (data: ProgressData) => void
  ) => Promise<PromptResponse | null>;
  callAgentAction: (
    endpoint: string,
    data?: Record<string, unknown>
  ) => Promise<{ success: boolean; message: string; data?: unknown }>;
}

export function useAPI(): UseAPIReturn {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const getApiUrl = useCallback(() => {
    return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  }, []);

  const generateSinglePrompt = useCallback(async (
    request: PromptRequest,
    onProgress?: (data: ProgressData) => void
  ): Promise<PromptResponse | null> => {
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}/generate-prompt-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('无法读取响应流');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        
        if (done) break;
        
        buffer += decoder.decode(value, { stream: true });
        
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.error) {
                throw new Error(data.error);
              }
              
              if (onProgress) {
                onProgress({
                  progress: data.progress || 0,
                  status: data.status || '',
                  step: data.step || '处理中',
                });
              }
              
              if (data.result) {
                // Ensure final progress update before returning result
                if (onProgress && data.progress >= 100) {
                  onProgress({
                    progress: 100,
                    status: data.status || '生成完成！',
                    step: '完成',
                  });
                }
                return data.result as PromptResponse;
              }
            } catch (parseError) {
              console.warn('解析SSE数据失败:', parseError);
            }
          }
        }
      }

      throw new Error('未收到完整响应');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '生成失败';
      setError(errorMessage);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [getApiUrl]);

  const callAgentAction = useCallback(async (
    endpoint: string,
    data?: Record<string, unknown>
  ) => {
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: data ? JSON.stringify(data) : undefined,
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error || '操作失败');
      }

      return {
        success: true,
        message: result.message || '操作成功',
        data: result
      };
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '操作失败';
      setError(errorMessage);
      return {
        success: false,
        message: errorMessage
      };
    } finally {
      setIsLoading(false);
    }
  }, [getApiUrl]);

  return {
    isLoading,
    error,
    clearError,
    generateSinglePrompt,
    callAgentAction
  };
}