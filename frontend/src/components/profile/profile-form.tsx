import { getObjectKeyFileUpload } from '@/api/s3-upload';
import { updateAvatar, updateProfile } from '@/api/user';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { PasswordInput } from '@/components/ui/password-input';
import { useAuth } from '@/contexts/AuthContext';
import { ChangeEvent, useState, useRef, useEffect } from 'react';
import { toast } from 'sonner';
import { ProfileSchema, profileSchema } from '@/schema/user-schema';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation } from '@tanstack/react-query';
import { MUTATION_KEY } from '@/constants/query-key';
import { ApiError } from '@/types/api';

export default function ProfileForm() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { user, fetchUser } = useAuth();
  const [isUploading, setIsUploading] = useState(false);
  const form = useForm<ProfileSchema>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      username: '',
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
      email: '',
    },
  });

  const { mutate, isPending } = useMutation({
    mutationFn: updateProfile,
    mutationKey: [MUTATION_KEY.UPDATE_USER_PROFILE],
    onSuccess: async () => {
      toast.success('Profile updated successfully');
      await fetchUser();
      form.setValue('currentPassword', '');
      form.setValue('newPassword', '');
      form.setValue('confirmPassword', '');
    },
    onError: (error: ApiError) => {
      if (error.response?.data.detail === 'Current password is incorrect') {
        form.setError('currentPassword', {
          type: 'server',
          message: 'Current password is incorrect',
        });
      } else if (error.response?.data.detail === 'Username already exists') {
        form.setError('username', {
          type: 'server',
          message: 'Username already exists, please choose another one',
        });
      } else {
        toast.error('Failed to update profile. Please try again.');
      }
    },
  });

  const handleAvatarUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setIsUploading(true);
    try {
      // Simulate an upload
      const objectKey = await getObjectKeyFileUpload(file);
      // Update user profile with new avatar URL
      await updateAvatar({ userId: user?.id!, objectKey });
      await fetchUser();
      toast.success('Avatar uploaded successfully!');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      toast.error(`Failed to upload avatar. Please try again. ${errorMessage}`);
    } finally {
      setIsUploading(false);
    }
  };

  useEffect(() => {
    if (user) {
      form.reset({
        username: user.username || '',
        email: user.email || '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
      });
    }
  }, [user, form]);

  function onSubmit(data: ProfileSchema) {
    mutate({
      data: {
        username: data.username ?? null,
        current_password: data.currentPassword ?? '',
        new_password: data.newPassword ?? null,
        type_auth: user?.type_auth as 'local' | 'social',
      },
    });
  }

  const handleButtonUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 py-6">
      <Card>
        <CardHeader>
          <CardTitle>Profile Settings</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center space-x-4">
            <Avatar className="h-20 w-20">
              <AvatarImage src={user?.image} alt={user?.username || user?.email} />
              <AvatarFallback>
                {user?.username?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase()}
              </AvatarFallback>
            </Avatar>
            <div className="space-y-2">
              <h3 className="font-medium">Profile Picture</h3>
              <div className="flex items-center">
                <label className="cursor-pointer">
                  <Input
                    type="file"
                    className="hidden"
                    onChange={handleAvatarUpload}
                    accept="image/*"
                    disabled={isUploading}
                    ref={fileInputRef}
                  />
                  <Button
                    variant="outline"
                    size="sm"
                    disabled={isUploading}
                    onClick={handleButtonUploadClick}
                  >
                    {isUploading ? 'Uploading...' : 'Change'}
                  </Button>
                </label>
              </div>
            </div>
          </div>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Username</FormLabel>
                    <FormControl>
                      <Input {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input {...field} disabled />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="space-y-4">
                <h3 className="font-medium">Change Password</h3>

                <FormField
                  control={form.control}
                  name="currentPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Current Password</FormLabel>
                      <FormControl>
                        <PasswordInput {...field} disabled={user?.type_auth === 'social'} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="newPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>New Password</FormLabel>
                      <FormControl>
                        <PasswordInput {...field} />
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
                        <PasswordInput {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button type="submit" className="w-full" disabled={isPending}>
                {isPending ? 'Updating...' : 'Save Changes'}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
