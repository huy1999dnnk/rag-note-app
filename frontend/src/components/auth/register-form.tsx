import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { PasswordInput } from '@/components/ui/password-input';
import { Link } from 'react-router';
import { useForm } from 'react-hook-form';
import { RegisterFormData, registerSchema } from '@/schema/auth-schema';
import { zodResolver } from '@hookform/resolvers/zod';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { toast } from 'sonner';
import { useMutation } from '@tanstack/react-query';
import { register } from '@/api/auth';
import { ApiError } from '@/types/api';
import { useAuth } from '@/contexts/AuthContext';
export function RegisterForm({ className, ...props }: React.ComponentPropsWithoutRef<'div'>) {
  const { fetchUser } = useAuth();
  const { mutate, isPending } = useMutation({
    mutationFn: register,
    onSuccess(data) {
      // Handle success
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      fetchUser();
      toast.success('Registration successful');
    },
    onError(error: ApiError) {
      // Handle error
      if (error.response?.data.detail === 'Email already registered') {
        form.setError('email', {
          type: 'server',
          message: 'Email already registereds',
        });
      } else {
        toast.error(error.response?.data.detail || 'Registration failed');
      }
    },
  });

  const form = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  function onSubmit(values: RegisterFormData) {
    mutate({
      email: values.email,
      password: values.password,
    });
  }

  return (
    <div className={cn('flex flex-col gap-6', className)} {...props}>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Register</CardTitle>
          <CardDescription>Enter your email and password below</CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input {...field} disabled={isPending} />
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
                      <PasswordInput {...field} disabled={isPending} />
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
                      <PasswordInput {...field} disabled={isPending} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button type="submit" className="w-full" disabled={isPending}>
                {isPending ? 'Registering...' : 'Register'}
              </Button>
              <div className="mt-4 text-center text-sm">
                Already have an account?{' '}
                <Link to="/auth/login" className="underline underline-offset-4 hover:text-primary">
                  Login
                </Link>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
