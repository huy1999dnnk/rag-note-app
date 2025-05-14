import { Routes, Route } from 'react-router';
import AuthLayout from '@/layout/AuthLayout';
import Login from '@/pages/login';
import Register from '@/pages/register';
import DashboardLayout from '@/layout/DashboardLayout';
import Setting from '@/pages/setting';
import './App.css';
import PrivateRoute from './routes/private-routes';
import PublicRoute from './routes/public-routes';
import { useRouteProgress } from '@/hooks/useRouteProgress';
import WorkspaceLayout from '@/layout/WorkspaceLayout';
import Note from '@/pages/note';
import SocialCallback from '@/pages/social-callback';
import PasswordResetRquest from '@/pages/password-reset-request';
import PasswordReset from '@/pages/password-reset';
import Profile from '@/pages/profile';
import NotFound from '@/pages/not-found';

function App() {
  useRouteProgress();

  return (
    <Routes>
      <Route element={<PrivateRoute />}>
        <Route path="/" element={<DashboardLayout />}>
          <Route path=":workspaceId/" element={<WorkspaceLayout />}>
            <Route path=":noteId" element={<Note />} />
          </Route>
          <Route path="setting" element={<Setting />} />
          <Route path="profile" element={<Profile />} />
        </Route>
      </Route>
      <Route element={<PublicRoute />}>
        <Route path="auth" element={<AuthLayout />}>
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Register />} />
          <Route path="forgot-password" element={<PasswordResetRquest />} />
          <Route path="reset-password" element={<PasswordReset />} />
        </Route>
        <Route path="auth/callback/:provider" element={<SocialCallback />} />
      </Route>
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default App;
