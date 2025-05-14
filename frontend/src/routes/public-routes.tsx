import { Navigate, Outlet } from 'react-router';
import { useAuth } from '@/contexts/AuthContext';

const PublicRoute = () => {
  const { user, loading } = useAuth();

  if (loading) return null;

  return !user ? <Outlet /> : <Navigate to="/" replace={true} />;
};

export default PublicRoute;
