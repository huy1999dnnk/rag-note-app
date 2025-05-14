import z from 'zod';

const hasLetterAndNumber = (val: string) => /[A-Za-z]/.test(val) && /\d/.test(val);

const optionalString = z
  .string()
  .transform((val) => (val.trim() === '' ? undefined : val))
  .optional();

export const profileSchema = z
  .object({
    email: z.string().email('Invalid email address'),
    username: optionalString.refine((val) => !val || val.length >= 3, {
      message: 'Username must be at least 3 characters',
    }),
    currentPassword: optionalString,
    newPassword: optionalString
      .refine((val) => !val || val.length >= 6, {
        message: 'Password must be at least 6 characters',
      })
      .refine((val) => !val || hasLetterAndNumber(val), {
        message: 'Password must contain at least one letter and one number',
      }),
    confirmPassword: optionalString,
  })
  .refine(
    (data) => {
      if (data.newPassword && data.newPassword !== data.confirmPassword) {
        return false;
      }
      return true;
    },
    {
      message: "Passwords don't match",
      path: ['confirmPassword'],
    }
  )
  .refine(
    (data) => {
      if (data.confirmPassword && !data.newPassword) {
        return false;
      }
      return true;
    },
    {
      message: 'New password is required to confirm',
      path: ['newPassword'],
    }
  )
  .refine(
    (data) => {
      if (data.currentPassword && !data.newPassword) {
        return false;
      }
      return true;
    },
    {
      message: 'New password is required to confirm',
      path: ['newPassword'],
    }
  );

export type ProfileSchema = z.infer<typeof profileSchema>;
