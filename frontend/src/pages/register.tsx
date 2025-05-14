import { RegisterForm } from '@/components/auth/register-form';
import { useTitle } from '@/hooks/useTitle';
export default function Register() {
  useTitle('Register');
  return <RegisterForm />;
}
