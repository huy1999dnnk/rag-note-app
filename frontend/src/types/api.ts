import { AxiosError } from 'axios';

export interface ApiErrorResponse {
  detail: string;
  status_code: number;
  type?: string;
}

export type ApiError = AxiosError<ApiErrorResponse>;
