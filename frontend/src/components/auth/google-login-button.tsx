import { Button } from '@/components/ui/button';
import { FaGoogle } from 'react-icons/fa';
import { useCallback } from 'react';

export function GoogleLoginButton() {
  const handleGoogleLogin = useCallback(() => {
    window.location.href = `${import.meta.env.VITE_API_BASE_URL}${import.meta.env.VITE_GOOGLE_AUTH_ENDPOINT}`;
  }, []);

  return (
    <Button
      variant="outline"
      className="w-full flex items-center justify-center gap-2"
      onClick={handleGoogleLogin}
      type="button"
    >
      <FaGoogle className="h-4 w-4" />
      <span>Sign in with Google</span>
    </Button>
  );
}
