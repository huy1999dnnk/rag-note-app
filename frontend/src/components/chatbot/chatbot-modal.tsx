import { useState, useRef, useEffect, useCallback } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Bot, Send, Loader2, MessageSquare, AlertTriangle, RefreshCw } from 'lucide-react';
import { sendMessageChatbot } from '@/api/chatbot';
import { cn } from '@/lib/utils';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { motion, AnimatePresence } from 'framer-motion';
import { useParams } from 'react-router';
import { toast } from 'sonner';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean; // Indicates if this message is currently streaming
}

export default function ChatbotModal() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [historyLimitExceeded, setHistoryLimitExceeded] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { noteId } = useParams<{ noteId: string }>();

  // Effect for auto-scrolling and auto-focusing
  useEffect(() => {
    if (open) {
      const timer = setTimeout(() => {
        if (scrollRef.current) {
          scrollRef.current.scrollIntoView({ behavior: 'smooth' });
        }
        if (inputRef.current) {
          inputRef.current.focus();
        }
      }, 100);

      return () => clearTimeout(timer);
    }
  }, [messages, open]);

  const resetChat = useCallback(() => {
    setMessages([]);
    setHistoryLimitExceeded(false);
    toast('Chat history reset');
  }, [toast]);

  const sendMessage = async () => {
    if (!input.trim() || isStreaming) return;

    const userMsg = { role: 'user' as const, content: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput('');

    // Add an empty assistant message that will be streamed
    setMessages((msgs) => [
      ...msgs,
      {
        role: 'assistant',
        content: '',
        isStreaming: true,
      },
    ]);

    setIsStreaming(true);

    try {
      await sendMessageChatbot(
        {
          message: input,
          note_ids: noteId ? [noteId] : [],
          chat_history: messages,
        },
        // This callback gets called with each chunk
        (chunk, isDone, responseObj) => {
          if (responseObj?.error_type === 'HISTORY_TOO_LONG') {
            setHistoryLimitExceeded(true);

            // Add system message about the limit
            setMessages((prev) => [
              ...prev,
              {
                role: 'assistant',
                content: responseObj.answer,
              },
            ]);
            setIsStreaming(false);
            return;
          }
          setMessages((currentMessages) => {
            // Get the current messages
            const messages = [...currentMessages];
            // Find the last message (which should be the streaming assistant message)
            const lastIndex = messages.length - 1;
            if (lastIndex >= 0 && messages[lastIndex].role === 'assistant') {
              // Update its content with the latest chunk
              messages[lastIndex] = {
                ...messages[lastIndex],
                content: chunk,
                isStreaming: !isDone,
              };
            }
            return messages;
          });

          if (isDone) {
            setIsStreaming(false);
          }
        }
      );
    } catch (error) {
      console.error('Chatbot error:', error);
      setMessages((msgs) => {
        const messages = [...msgs];
        const lastIndex = messages.length - 1;
        if (lastIndex >= 0 && messages[lastIndex].role === 'assistant') {
          messages[lastIndex] = {
            role: 'assistant',
            content: 'Sorry, something went wrong.',
            isStreaming: false,
          };
        }
        return messages;
      });
      setIsStreaming(false);
    }
  };

  return (
    <>
      {/* Floating Button with Pulse Animation */}
      <AnimatePresence>
        {!open && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            className="fixed bottom-6 right-6 z-50"
          >
            <Button
              onClick={() => setOpen(true)}
              size="icon"
              className="h-14 w-14 rounded-full shadow-lg bg-primary hover:bg-primary/90 relative"
            >
              <MessageSquare className="h-6 w-6 text-primary-foreground" />
              {/* Pulse effect */}
              <span className="absolute w-full h-full rounded-full animate-ping bg-primary/30" />
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Dialog */}
      <Dialog
        open={open}
        onOpenChange={(newOpen) => {
          // Don't allow closing while streaming
          if (isStreaming && !newOpen) return;
          setOpen(newOpen);
        }}
      >
        <DialogContent
          className="p-0 gap-0 sm:rounded-xl border shadow-xl max-w-[400px] data-[state=open]:animate-in data-[state=open]:slide-in-from-bottom-full"
          style={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            margin: 0,
            width: '90vw',
            maxHeight: '70vh',
          }}
        >
          <DialogHeader className="border-b px-4 py-3 flex flex-row items-center justify-between bg-card rounded-t-xl">
            <DialogTitle className="flex items-center gap-2 text-lg font-semibold">
              <Bot className="h-5 w-5 text-primary" />
              AI Assistant
              <Button
                variant="ghost"
                size="sm"
                className="h-8 text-xs flex items-center gap-1 hover:bg-primary/10 cursor-pointer"
                onClick={resetChat}
                disabled={messages.length === 0}
              >
                <span className="text-primary font-medium">+</span> New Chat
              </Button>
            </DialogTitle>
          </DialogHeader>

          <ScrollArea
            className="flex-grow overflow-auto bg-gradient-to-br from-muted/50 to-muted p-4"
            style={{ height: '350px' }}
          >
            <div className="space-y-4 pb-1">
              {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full py-8 text-center">
                  <div className="rounded-full bg-primary/10 p-3 mb-2">
                    <Bot className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="font-medium text-lg mb-1">AI Assistant</h3>
                  <p className="text-sm text-muted-foreground max-w-[250px]">
                    Search anything in your notes
                  </p>
                </div>
              )}

              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={cn(
                    'flex gap-2',
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  )}
                >
                  {msg.role === 'assistant' && (
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-primary/10 text-primary">
                        <Bot className="h-4 w-4" />
                      </AvatarFallback>
                    </Avatar>
                  )}

                  <div
                    className={cn(
                      'rounded-xl px-3 py-2 max-w-[80%] text-sm whitespace-pre-wrap',
                      msg.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : historyLimitExceeded && i === messages.length - 1
                          ? 'bg-amber-50 border border-amber-300 text-amber-800'
                          : 'bg-muted border'
                    )}
                  >
                    {msg.content ||
                      (msg.isStreaming && (
                        <Loader2 className="animate-spin h-4 w-4 inline-block" />
                      ))}
                    {msg.isStreaming && <span className="ml-1 animate-pulse">▌</span>}
                  </div>

                  {msg.role === 'user' && (
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-muted">U</AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
              {historyLimitExceeded && (
                <Alert className="my-4 border-amber-500 bg-amber-50 text-amber-900">
                  <AlertTriangle className="h-5 w-5 text-amber-500" />
                  <AlertTitle className="font-medium">Conversation Limit Reached</AlertTitle>
                  <AlertDescription className="mt-2">
                    <p className="mb-2">
                      The conversation history is too long for the AI to process effectively.
                    </p>
                    <Button
                      variant="outline"
                      className="border-amber-500 text-amber-700 hover:bg-amber-100 hover:text-amber-900 flex items-center gap-2"
                      onClick={resetChat}
                    >
                      <RefreshCw className="h-4 w-4" /> Clear Chat History
                    </Button>
                  </AlertDescription>
                </Alert>
              )}

              {/* This is the key for scrolling - a dummy div that is always at the bottom */}
              <div ref={scrollRef} aria-hidden="true" />
            </div>
          </ScrollArea>

          <form
            className="flex items-center gap-2 px-4 py-3 border-t bg-card rounded-b-xl"
            onSubmit={(e) => {
              e.preventDefault();
              if (!historyLimitExceeded) sendMessage();
            }}
          >
            <Input
              ref={inputRef}
              className="flex-1 bg-muted"
              placeholder={
                historyLimitExceeded
                  ? 'Please clear chat history to continue...'
                  : 'Type your message...'
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isStreaming || historyLimitExceeded}
            />
            <Button
              type="submit"
              size="icon"
              disabled={isStreaming || !input.trim() || historyLimitExceeded}
              className={cn(
                'rounded-full',
                isStreaming || !input.trim() || historyLimitExceeded ? 'opacity-50' : 'opacity-100'
              )}
            >
              {isStreaming ? (
                <Loader2 className="animate-spin h-4 w-4" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </Button>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
}
