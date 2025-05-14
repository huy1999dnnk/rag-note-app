import { useAuth } from '@/contexts/AuthContext';
import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate, useParams } from 'react-router';
import { useMutation } from '@tanstack/react-query';
import { handleSocialCallback } from '@/api/auth';
import { MUTATION_KEY } from '@/constants/query-key';
import { toast } from 'sonner';

export default function SocialCallback() {
  const [searchParams] = useSearchParams();
  const { provider } = useParams();
  const code = searchParams.get('code');
  const navigate = useNavigate();
  const { fetchUser } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const { mutate } = useMutation({
    mutationFn: handleSocialCallback,
    mutationKey: [MUTATION_KEY.GET_SOCIAL_AUTH_TOKEN],
    onSuccess: async (data) => {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      await fetchUser();
    },
    onError: (err) => {
      toast.error(`Failed to authenticate. Please try again. ${err.message}`);
      navigate('/auth/login');
    },
    retry: false,
  });

  useEffect(() => {
    if (!code || !provider) {
      setError('Missing authentication data');
      return;
    }
    mutate({
      provider,
      code,
    });
  }, [provider, code]);

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-screen">
        <div className="text-red-500 mb-4">{error}</div>
        <button onClick={() => navigate('/auth/login')} className="text-blue-500 hover:underline">
          Back to login
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
        <p className="mt-4">Completing your sign in...</p>
      </div>
    </div>
  );
}
