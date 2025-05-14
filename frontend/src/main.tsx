import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router';
import App from './App';
import { ThemeProvider } from './contexts/ThemeContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from '@/components/ui/sonner';
import { AuthProvider } from './contexts/AuthContext';
export const queryClient = new QueryClient();

const root = document.getElementById('root');

if (!root) {
  throw new Error("Root element with id 'root' not found.");
}

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ThemeProvider>
          <App />
          <Toaster />
        </ThemeProvider>
      </AuthProvider>
    </QueryClientProvider>
  </BrowserRouter>
);
