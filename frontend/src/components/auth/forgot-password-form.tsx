import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { forgotPasswordSchema, ForgotPasswordFormData } from '@/schema/auth-schema';
import { toast } from 'sonner';
import { forgotPassword } from '@/api/auth';
import { useMutation } from '@tanstack/react-query';
import { MUTATION_KEY } from '@/constants/query-key';
import { ApiError } from '@/types/api';
import { CheckCircle } from 'lucide-react';
import { Link } from 'react-router';

const PasswordResetRequestForm = () => {
  const { mutate, isSuccess, isPending } = useMutation({
    mutationFn: forgotPassword,
    mutationKey: [MUTATION_KEY.FORGOT_PASSWORD],
    onError: (error: ApiError) => {
      if (error?.response?.data.detail) {
        form.setError('email', {
          type: 'server',
          message: error?.response?.data.detail,
        });
        toast.error('Invalid credentials', {
          position: 'top-center',
        });
      }
    },
  });

  const form = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: '',
    },
  });

  async function onSubmit(data: ForgotPasswordFormData) {
    mutate({
      email: data.email,
    });
  }

  const renderSuccessMessage = () => {
    return (
      <div>
        <div className="flex items-center justify-center p-4 border-2 border-accent-foreground rounded-md gap-3">
          <CheckCircle />
          <p className="text-sm font-medium text-foreground">
            Password reset email sent successfully!
          </p>
        </div>
        <div className="flex justify-center mt-4">
          <Link
            to="/auth/login"
            className="text-sm text-foreground underline hover:text-accent-foreground self-center"
          >
            Back to Login
          </Link>
        </div>
      </div>
    );
  };

  return (
    <>
      {isSuccess ? (
        renderSuccessMessage()
      ) : (
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="your.email@example.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="w-full" disabled={isPending}>
              {isPending ? 'Sending...' : 'Send Reset Link'}
            </Button>
            <div className="flex justify-center">
              <Link
                to="/auth/login"
                className="text-sm text-foreground underline hover:text-accent-foreground self-center"
              >
                Back to Login
              </Link>
            </div>
          </form>
        </Form>
      )}
    </>
  );
};

export default PasswordResetRequestForm;
