// axiosInstance.ts
import axios, { AxiosError, type AxiosRequestConfig } from 'axios';
const baseURL = import.meta.env.VITE_API_V1_URL;
console.log('baseURL', baseURL);
let isRefreshing = false;
let failedQueue: any[] = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

const api = axios.create({
  baseURL,
  withCredentials: false, // Needed if using HttpOnly cookies for refresh token
});

// Attach access token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle expired access token
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    if (
      (error.response?.data as { detail?: string })?.detail === 'Token has expired' &&
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes('/api/v1/auth/refresh')
    ) {
      originalRequest._retry = true;

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({
            resolve: (token: string) => {
              if (originalRequest.headers) {
                originalRequest.headers['Authorization'] = 'Bearer ' + token;
              }
              resolve(api(originalRequest));
            },
            reject: (err: AxiosError) => {
              reject(err);
            },
          });
        });
      }

      isRefreshing = true;

      try {
        const refresh_token = localStorage.getItem('refresh_token');
        const res = await axios.post(
          `${baseURL}/auth/refresh`,
          {
            refresh_token,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
            // Needed if using HttpOnly cookies for refresh token
          }
        );

        const newAccessToken = res.data.access_token;
        const newRefreshToken = res.data.refresh_token;
        localStorage.setItem('access_token', newAccessToken);
        localStorage.setItem('refresh_token', newRefreshToken);

        processQueue(null, newAccessToken);

        if (originalRequest.headers) {
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        }
        return api(originalRequest);
      } catch (err) {
        processQueue(err as AxiosError, null);
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        // optional: redirect to login
        window.location.href = '/auth/login';
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default api;
