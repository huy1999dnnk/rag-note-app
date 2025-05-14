import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import { Link } from 'react-router';
import { useForm } from 'react-hook-form';
import { LoginFormData, loginSchema } from '@/schema/auth-schema';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { useMutation } from '@tanstack/react-query';
import { login } from '@/api/auth';
import { ApiError } from '@/types/api';
import { useAuth } from '@/contexts/AuthContext';
import { GoogleLoginButton } from './google-login-button';
import { PasswordInput } from '@/components/ui/password-input';
export function LoginForm({ className, ...props }: React.ComponentPropsWithoutRef<'div'>) {
  const { fetchUser } = useAuth();
  const { mutate, isPending } = useMutation({
    mutationFn: login,
    onSuccess(data) {
      // Handle success
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      fetchUser();
      toast.success('Login successful');
    },
    onError(error: ApiError) {
      // Handle error
      toast.error(error.response?.data.detail || 'Login failed', {
        position: 'top-center',
      });
    },
  });

  const form = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  // 2. Define a submit handler.
  function onSubmit(values: LoginFormData) {
    mutate({
      email: values.email,
      password: values.password,
    });
  }

  return (
    <div className={cn('flex flex-col gap-6', className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Login</CardTitle>
          <CardDescription>Enter your email below to login to your account</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input disabled={isPending} placeholder="This is your email" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Password</FormLabel>
                    <FormControl>
                      <PasswordInput disabled={isPending} placeholder="" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button disabled={isPending} className="w-full" type="submit">
                {isPending ? 'Processing...' : 'Login'}
              </Button>
            </form>
          </Form>
          <div className="flex justify-center">
            <Link
              to={{
                pathname: '/auth/forgot-password',
              }}
              className="inline-block text-sm underline-offset-4 hover:underline"
            >
              Forgot your password?
            </Link>
          </div>

          <GoogleLoginButton />
          <p className="text-center text-sm">
            Don&apos;t have an account?{' '}
            <Link
              to={{
                pathname: '/auth/register',
              }}
              className="underline underline-offset-4"
            >
              Sign up
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
