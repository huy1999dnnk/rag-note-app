import React from 'react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useWorkspace } from '@/hooks/use-workspace';

interface IMoreActionDropdown {
  children: React.ReactNode;
  id: string;
  name: string;
  setName: (name: string) => void;
  setOpen: (open: boolean) => void;
  setCurrentId: (parentId: string) => void;
}

export function MoreActionDropdown({
  children,
  id,
  name,
  setName,
  setOpen,
  setCurrentId,
}: IMoreActionDropdown) {
  const { deleteWorkspaceFn } = useWorkspace();
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>{children}</DropdownMenuTrigger>
      <DropdownMenuContent className="w-56">
        <DropdownMenuGroup>
          <DropdownMenuItem
            onClick={() => {
              setOpen(true);
              setCurrentId(id);
              setName(name);
            }}
          >
            Edit workspace name
          </DropdownMenuItem>
          <DropdownMenuItem onClick={() => deleteWorkspaceFn(id)}>
            Delete workspace
          </DropdownMenuItem>
        </DropdownMenuGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
