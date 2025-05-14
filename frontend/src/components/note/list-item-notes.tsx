import { Note } from '@/components/note/sidebar-note';
import { Trash, Edit, FileText } from 'lucide-react';
import AddEditNote from './add-edit-note';
import ConfirmDelete from '@/components/note/confirm-delete';
import { Link, useParams } from 'react-router';
import { useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';
interface INodeSidebarItemProps {
  data: Note[];
  isLoading: boolean;
}

export default function ListItemNotes({ data, isLoading }: INodeSidebarItemProps) {
  const { workspaceId, noteId } = useParams();
  const newNoteRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (noteId && newNoteRef.current) {
      newNoteRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [data, noteId]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center h-32">
        <FileText size={32} className="text-slate-300 mb-2" />
        <p className="text-sm text-slate-500">Loading notes...</p>
      </div>
    );
  }

  if (data?.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-8 text-center h-32">
        <FileText size={32} className="text-slate-300 mb-2" />
        <p className="text-sm text-slate-500">No notes in this workspace</p>
        <p className="text-xs text-slate-400 mt-1">Create a new note to get started</p>
      </div>
    );
  }

  return (
    <div>
      {data.map((note) => {
        const isActive = note.id === noteId;
        return (
          <div
            key={note.id}
            ref={isActive ? newNoteRef : null}
            className={cn(
              'flex items-center p-2 border-b hover:bg-accent cursor-pointer group',
              isActive ? 'bg-slate-100 dark:bg-slate-800' : ''
            )}
          >
            <div className="w-full flex justify-between items-center">
              <Link
                to={{
                  pathname: `/${workspaceId}/${note.id}`,
                }}
                className={cn('text-sm flex-1', isActive ? 'font-medium' : '')}
              >
                {note.title}
              </Link>
              <div className="invisible items-center flex group-hover:visible">
                <AddEditNote noteData={note}>
                  <Edit size={16} className="mr-2" />
                </AddEditNote>
                <ConfirmDelete id={note.id}>
                  <Trash size={16} />
                </ConfirmDelete>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
