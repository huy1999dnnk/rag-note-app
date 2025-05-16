import api from '@/lib/axios';
import { IUpdateUserProfile } from '@/types/user';
export const getProfile = async () => {
  console.log('getProfile', api);
  const res = await api.post('/user/profile');
  return res.data;
};

export const updateProfile = async ({ data }: { data: IUpdateUserProfile }) => {
  const res = await api.put('/user/profile', data);
  return res.data;
};

export const updateAvatar = async ({
  userId,
  objectKey,
}: {
  userId: number;
  objectKey: string;
}) => {
  const res = await api.post(`/user/update-avatar-user`, {
    object_key_s3: objectKey,
    user_id: userId,
  });
  return res.data;
};
