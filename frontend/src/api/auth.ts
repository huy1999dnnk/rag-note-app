import api from '@/lib/axios';
import axios from 'axios';
export const login = async ({ email, password }: { email: string; password: string }) => {
  const res = await api.post('/auth/login', {
    email,
    password,
  });
  return res.data;
};
export const register = async ({ email, password }: { email: string; password: string }) => {
  const res = await api.post('/auth/register', {
    email,
    password,
  });
  return res.data;
};
export const logout = async ({ refresh_token }: { refresh_token: string }) => {
  const res = await api.post('/auth/logout', {
    refresh_token,
  });
  return res.data;
};
export const handleSocialCallback = async ({
  provider,
  code,
}: {
  provider: string;
  code: string;
}) => {
  const res = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/auth/${provider}/token`, {
    code,
  });
  return res.data;
};

export const forgotPassword = async ({ email }: { email: string }) => {
  const res = await api.post('/auth/password-reset/request', {
    email,
  });
  return res.data;
};

export const resetPassword = async ({ password, code }: { password: string; code: string }) => {
  const res = await api.post('/auth/password-reset/verify', {
    password,
    code,
  });
  return res.data;
};
