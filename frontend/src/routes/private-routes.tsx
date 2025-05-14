import { Navigate, Outlet } from 'react-router';
import { useAuth } from '@/contexts/AuthContext';

const PrivateRoute = () => {
  const { user, loading } = useAuth();

  if (loading) return <Outlet />;

  return user ? <Outlet /> : <Navigate to="/auth/login" replace={true} />;
};

export default PrivateRoute;
