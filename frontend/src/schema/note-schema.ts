import { z } from 'zod';

export const addNewNoteSchema = z.object({
  title: z.string().min(1, 'title must be at least 1 character'),
});

export type AddNewNoteFormData = z.infer<typeof addNewNoteSchema>;
