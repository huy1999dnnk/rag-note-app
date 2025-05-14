import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useMutation } from '@tanstack/react-query';
import { logout } from '@/api/auth';
import { getProfile } from '@/api/user';
type User = {
  id: number;
  email: string;
  username: string | undefined;
  created_at: string;
  updated_at: string | undefined;
  image: string | undefined;
  type_auth: 'local' | 'social';
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  fetchUser: () => void;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const { mutate: logOutFn } = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      setUser(null);
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },
  });

  const fetchUser = async () => {
    setLoading(true);
    try {
      const user = await getProfile();
      setUser(user);
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const signOut = () => {
    const refresh_token = localStorage.getItem('refresh_token');
    if (refresh_token) {
      logOutFn({ refresh_token });
    } else {
      setUser(null);
    }
  };

  // Initialize auth state on app load
  useEffect(() => {
    fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, fetchUser, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for consuming context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
