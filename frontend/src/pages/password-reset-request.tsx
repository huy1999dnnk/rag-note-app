import PasswordResetRequestForm from '@/components/auth/forgot-password-form';
import { useTitle } from '@/hooks/useTitle';
export default function PasswordResetRquest() {
  useTitle('Password Reset Request');
  return <PasswordResetRequestForm />;
}
