import { z } from 'zod';

export const addNewWorkspaceSchema = z.object({
  name: z.string().min(1, 'name must be at least 1 character'),
});

export type AddNewWorkspaceFormData = z.infer<typeof addNewWorkspaceSchema>;
