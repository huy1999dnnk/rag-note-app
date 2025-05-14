import ResetPasswordForm from '@/components/auth/reset-password-form';
import { useTitle } from '@/hooks/useTitle';
export default function PasswordReset() {
  useTitle('Password Reset');
  return <ResetPasswordForm />;
}
