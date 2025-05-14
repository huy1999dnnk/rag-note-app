import { Button } from '@/components/ui/button';
import AddEditNote from '@/components/note/add-edit-note';
import ListItemNotes from './list-item-notes';
export type Note = {
  id: string;
  title: string;
};

interface ISidebarNote {
  data: Note[];
  isLoading: boolean;
}

export default function SidebarNote({ data, isLoading }: ISidebarNote) {
  return (
    <div className="flex flex-col h-full pb-4">
      <div className="flex w-full justify-center">
        <AddEditNote>
          <Button variant="outline" className="cursor-pointer">
            New note
          </Button>
        </AddEditNote>
      </div>
      <div className="mt-2 overflow-y-auto">
        <ListItemNotes data={data} isLoading={isLoading} />
      </div>
    </div>
  );
}
