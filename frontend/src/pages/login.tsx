import { LoginForm } from '@/components/auth/login-form';
import { useTitle } from '@/hooks/useTitle';

export default function LoginPage() {
  useTitle('Login');
  return <LoginForm />;
}
