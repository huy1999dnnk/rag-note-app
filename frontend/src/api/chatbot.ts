import api from '@/lib/axios';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;
}

export interface ChatbotRequest {
  message: string;
  note_ids?: string[] | null;
  chat_history?: ChatMessage[];
}

// Streaming API call
export const sendMessageChatbot = async (
  request: ChatbotRequest,
  onChunk: (chunk: string, isDone: boolean, responseObj?: any) => void
): Promise<void> => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    const response = await fetch(`${api.defaults.baseURL}/chatbot/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Use the ReadableStream API for streaming
    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();

      if (done) {
        break;
      }

      // Decode the chunk and add to buffer
      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      // Process complete SSE messages that end with \n\n
      const messages = buffer.split('\n\n');
      buffer = messages.pop() || ''; // Keep the last incomplete message in the buffer

      for (const message of messages) {
        if (message.startsWith('data: ')) {
          const jsonData = message.slice(6); // Remove 'data: ' prefix
          try {
            const data = JSON.parse(jsonData);
            onChunk(data.answer, data.done, data);
          } catch (e) {
            console.error('Error parsing message:', message, e);
          }
        }
      }
    }
  } catch (error) {
    console.error('Streaming error:', error);
    onChunk('Sorry, something went wrong.', true);
    throw error;
  }
};
