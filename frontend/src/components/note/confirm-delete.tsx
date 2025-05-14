import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { useNotes } from '@/hooks/use-notes';
import React from 'react';
import { Button } from '@/components/ui/button';
import { useParams } from 'react-router';

interface IConfirmDeleteProps {
  children?: React.ReactNode;
  id: string;
}

export default function ConfirmDelete({ children, id }: IConfirmDeleteProps) {
  const { workspaceId } = useParams();
  const { deleteNoteFn } = useNotes(workspaceId);

  return (
    <Popover>
      <PopoverTrigger asChild>{children}</PopoverTrigger>
      <PopoverContent>
        <div className="flex flex-col">
          <p className="text-sm">Are you sure you want to delete this note?</p>
          <div className="flex justify-center mt-2">
            <Button
              variant="outline"
              className="mr-2"
              onClick={() => {
                deleteNoteFn(id);
              }}
            >
              Delete
            </Button>
          </div>
        </div>
      </PopoverContent>
    </Popover>
  );
}
