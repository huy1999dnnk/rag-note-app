import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { AddNewNoteFormData, addNewNoteSchema } from '@/schema/note-schema';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Dialog, DialogTrigger, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import React from 'react';
import { Input } from '@/components/ui/input';
import { useNotes } from '@/hooks/use-notes';
import { useParams, useNavigate } from 'react-router';
import { useQueryClient } from '@tanstack/react-query';
import { QUERY_KEY } from '@/constants/query-key';
import { toast } from 'sonner';
import { useEffect } from 'react';

interface IAddEditNoteProps {
  children?: React.ReactNode;
  noteData?: {
    id: string;
    title: string;
  };
}

export default function AddEditNote({ children, noteData }: IAddEditNoteProps) {
  const navigate = useNavigate();
  const [open, setOpen] = React.useState(false);
  const queryClient = useQueryClient();
  const { workspaceId } = useParams();
  const { createNoteFn, isPendingCreateNote, updateNoteTitleFn } = useNotes();

  const isEditMode = noteData !== undefined;

  const title = isEditMode ? 'Edit note' : 'Create a new note';

  const form = useForm<AddNewNoteFormData>({
    resolver: zodResolver(addNewNoteSchema),
    defaultValues: {
      title: '',
    },
  });

  const onSubmit = (data: AddNewNoteFormData) => {
    if (!isEditMode) {
      createNoteFn({
        title: data.title,
        workspace_id: workspaceId!,
      })
        .then((data) => {
          form.reset();
          queryClient.invalidateQueries({
            queryKey: [QUERY_KEY.NOTE_LIST],
          });
          setOpen(false);
          toast.success('Note created successfully');
          navigate(`/${workspaceId}/${data.id}`);
        })
        .catch(() => {
          setOpen(false);
          toast.error('Failed to create note');
        });
    } else {
      updateNoteTitleFn({
        id: noteData!.id,
        title: data.title,
      })
        .then(() => {
          form.reset();
          queryClient.invalidateQueries({
            queryKey: [QUERY_KEY.NOTE_LIST],
          });
          setOpen(false);
          toast.success('Note updated successfully');
        })
        .catch(() => {
          setOpen(false);
          toast.error('Failed to update note');
        });
    }
  };

  const onReset = () => {
    if (isEditMode) {
      form.setValue('title', noteData?.title);
    } else {
      form.reset();
    }
  };

  useEffect(() => {
    if (noteData) {
      form.setValue('title', noteData.title);
    }
  }, [noteData]);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent onCloseAutoFocus={onReset}>
        <DialogTitle className="text-center text-lg font-semibold">{title}</DialogTitle>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-4">
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Title</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Enter note title" className="input" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button disabled={isPendingCreateNote} type="submit" className="btn cursor-pointer">
              Submit
            </Button>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
