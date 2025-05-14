import { useMutation } from '@tanstack/react-query';
import { resetPasswordSchema, ResetPasswordFormData } from '@/schema/auth-schema';
import { resetPassword } from '@/api/auth';
import { Link, useNavigate, useSearchParams } from 'react-router';
import { MUTATION_KEY } from '@/constants/query-key';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { PasswordInput } from '@/components/ui/password-input';
import { ApiError } from '@/types/api';
import { toast } from 'sonner';
export default function ResetPasswordForm() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const code = searchParams.get('code');
  const { mutate, isPending, isSuccess } = useMutation({
    mutationKey: [MUTATION_KEY.RESET_PASSWORD],
    mutationFn: resetPassword,
    onError: (error: ApiError) => {
      toast.error(error.response?.data.detail || 'An error occurred. Please try again later.');
    },
  });

  const form = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data: ResetPasswordFormData) => {
    if (!code) return;
    const { password } = data;
    mutate({ code, password });
  };

  const renderResetPasswordSuccess = () => {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Password Reset Successful</h1>
          <p>Your password has been reset successfully.</p>
          <Link to="/auth/login" className="text-foreground underline">
            Back to Login
          </Link>
        </div>
      </div>
    );
  };

  if (!code) {
    return (
      <div className="text-center">
        <h2 className="text-xl font-semibold mb-2">Invalid Reset Link</h2>
        <p className="mb-4">The password reset link is invalid or has expired.</p>
        <Button onClick={() => navigate('/auth/password-reset')}>Request New Reset Link</Button>
      </div>
    );
  }

  return (
    <>
      {isSuccess ? (
        renderResetPasswordSuccess()
      ) : (
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>New Password</FormLabel>
                  <FormControl>
                    <PasswordInput placeholder="******" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="confirmPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <PasswordInput placeholder="******" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="w-full" disabled={isPending}>
              {isPending ? 'Resetting...' : 'Reset Password'}
            </Button>
          </form>
          <div className="flex justify-center mt-4">
            <Link
              to="/auth/login"
              className="text-sm text-foreground underline hover:text-accent-foreground self-center"
            >
              Back to Login
            </Link>
          </div>
        </Form>
      )}
    </>
  );
}
