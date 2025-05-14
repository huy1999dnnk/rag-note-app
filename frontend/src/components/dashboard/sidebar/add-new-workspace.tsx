import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { AddNewWorkspaceFormData, addNewWorkspaceSchema } from '@/schema/workspace-schema';
import { useWorkspace } from '@/hooks/use-workspace';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Button } from '@/components/ui/button';
import React, { useEffect, useState } from 'react';
import { Input } from '@/components/ui/input';
import {
  DialogHeader,
  DialogContent,
  Dialog,
  DialogTrigger,
  DialogTitle,
} from '@/components/ui/dialog';
import { useQueryClient } from '@tanstack/react-query';

import { toast } from 'sonner';
import { QUERY_KEY } from '@/constants/query-key';
import { FORM_MODE } from '@/constants/enum-variable';
import { useNavigate } from 'react-router';

interface IAddNewNote {
  children?: React.ReactNode;
  currentId?: string;
  name?: string;
  openModal?: boolean;
  setOpenModal?: (open: boolean) => void;
  onAddSubSuccess?: () => void;
  setName?: (name: string) => void;
}

export default function AddNewWorkspace({
  children,
  currentId,
  name,
  openModal,
  setOpenModal,
  onAddSubSuccess,
  setName,
}: IAddNewNote): React.ReactElement {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState(false);
  const { createWorkspaceAsync, updateWorkspaceNameFn } = useWorkspace();

  const mode = !name ? FORM_MODE.CREATE : FORM_MODE.EDIT;

  const titleModal =
    mode === FORM_MODE.CREATE
      ? currentId
        ? `Create Sub Workspace`
        : 'Create Workspace'
      : 'Edit Workspace Name';

  const titleSubmit = mode === FORM_MODE.CREATE ? 'Create' : 'Edit';

  const form = useForm<AddNewWorkspaceFormData>({
    resolver: zodResolver(addNewWorkspaceSchema),
    defaultValues: {
      name: '',
    },
  });

  const onSubmit = (values: AddNewWorkspaceFormData) => {
    if (mode === FORM_MODE.CREATE) {
      createWorkspaceAsync({ name: values.name, parent_id: currentId ?? null })
        .then((data) => {
          // Handle success
          form.reset();
          toast.success('Workspace created successfully', {
            position: 'top-center',
          });
          if (onAddSubSuccess) {
            onAddSubSuccess();
          }

          if (setOpenModal) {
            setOpenModal(false);
          }
          setOpen(false);
          queryClient.invalidateQueries({
            queryKey: [QUERY_KEY.WORKSPACE_LIST],
          });
          navigate(`/${data.id}`);
        })
        .catch(() => {
          // Handle error
          setOpen(false);
          toast.error('Failed to create workspace', {
            position: 'top-center',
          });
        });
    } else {
      updateWorkspaceNameFn({
        id: currentId!,
        name: values.name,
      })
        .then(() => {
          // Handle success
          form.reset();
          toast.success('Workspace name updated successfully', {
            position: 'top-center',
          });
          if (setOpenModal) {
            setOpenModal(false);
          }
          setOpen(false);
          queryClient.invalidateQueries({
            queryKey: [QUERY_KEY.WORKSPACE_LIST],
          });
        })
        .catch(() => {
          // Handle error
          setOpen(false);
          toast.error('Failed to update workspace name', {
            position: 'top-center',
          });
        });
    }
  };

  const onCloseForm = () => {
    form.reset();
    if (setName) {
      setName('');
    }
  };

  useEffect(() => {
    if (name) {
      form.setValue('name', name);
    }
  }, [name]);

  return (
    <Dialog open={openModal ?? open} onOpenChange={setOpenModal ?? setOpen}>
      <DialogTrigger asChild>{children}</DialogTrigger>
      <DialogContent className="sm:max-w-[425px]" onCloseAutoFocus={onCloseForm}>
        <DialogHeader>
          <DialogTitle>{titleModal}</DialogTitle>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Workspace Name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Workspace Name" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="btn">
              {titleSubmit}
            </Button>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}
