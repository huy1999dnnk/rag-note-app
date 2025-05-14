import { Button } from '@/components/ui/button';
import { useNavigate } from 'react-router';
import { useTitle } from '@/hooks/useTitle';
export default function NotFound() {
  const navigate = useNavigate();
  useTitle('Page Not Found');
  return (
    <div className="flex flex-col items-center justify-center h-screen text-center px-4">
      <h1 className="text-6xl font-bold mb-4">404</h1>
      <h2 className="text-2xl font-medium mb-6">Page Not Found</h2>
      <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-md">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div className="flex gap-4">
        <Button onClick={() => navigate(-1)}>Go Back</Button>
        <Button variant="outline" onClick={() => navigate('/')}>
          Go Home
        </Button>
      </div>
    </div>
  );
}
