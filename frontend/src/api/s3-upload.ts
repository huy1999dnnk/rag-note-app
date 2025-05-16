import axios from 'axios';
import api from '@/lib/axios';
import { toast } from 'sonner';
import { ALLOWED_TYPES } from '@/constants/s3';
// Resolves an S3 object key to a presigned URL for display
export const resolveImageUrl = async (imageKey: string): Promise<string> => {
  const response = await api.get(`/upload/get-image-url?key=${encodeURIComponent(imageKey)}`);
  return response.data.url;
};

// Uploads a file to S3 and returns a presigned URL for immediate display
export const uploadFile = async (file: File, noteId: string): Promise<string> => {
  if (file.size > 10 * 1024 * 1024) {
    toast.error('File must be under 10MB.');
    throw new Error('File must be under 10MB.');
  }

  if (!ALLOWED_TYPES.includes(file.type)) {
    toast.error(
      'File type not supported. Please upload an image, video, PDF, Word, Excel, or PowerPoint file.'
    );
    throw new Error('File type not supported.');
  }

  // Step 1: Get presigned upload URL and object key from backend
  const { data } = await api.post('/upload/generate-upload-url', {
    filename: file.name,
    contentType: file.type,
    fileSize: file.size,
  });

  const { uploadUrl, objectKey } = data;
  if (!uploadUrl || !objectKey) {
    throw new Error('Failed to get upload URL or object key');
  }

  // Step 2: Upload the file directly to S3 using the presigned URL
  const uploadRes = await axios.put(uploadUrl, file, {
    headers: {
      'Content-Type': file.type,
    },
  });

  if (uploadRes.status !== 200) {
    throw new Error('File upload failed');
  }

  // Step 3: Get a presigned URL for immediate display in the editor
  const url = await resolveImageUrl(objectKey);

  if (file.type === 'application/pdf' && noteId) {
    try {
      // Fire and forget - don't wait for the response
      api
        .post('/chatbot/upload/process-pdf', {
          objectKey,
          noteId,
        })
        .catch((err) => console.log('PDF processing request failed', err));
    } catch (error) {
      // Just log the error but don't interrupt the flow
      console.error('Error requesting PDF processing:', error);
    }
  }

  return url;
};

export const getObjectKeyFileUpload = async (file: File): Promise<string> => {
  if (file.size > 10 * 1024 * 1024) {
    toast.error('File must be under 10MB.');
    throw new Error('File must be under 10MB.');
  }

  if (!ALLOWED_TYPES.includes(file.type)) {
    toast.error(
      'File type not supported. Please upload an image, video, PDF, Word, Excel, or PowerPoint file.'
    );
    throw new Error('File type not supported.');
  }

  // Step 1: Get presigned upload URL and object key from backend
  const { data } = await api.post('/upload/generate-upload-url', {
    filename: file.name,
    contentType: file.type,
    fileSize: file.size,
  });

  const { uploadUrl, objectKey } = data;
  if (!uploadUrl || !objectKey) {
    throw new Error('Failed to get upload URL or object key');
  }

  // Step 2: Upload the file directly to S3 using the presigned URL
  const uploadRes = await axios.put(uploadUrl, file, {
    headers: {
      'Content-Type': file.type,
    },
  });

  if (uploadRes.status !== 200) {
    throw new Error('File upload failed');
  }

  return objectKey;
};
