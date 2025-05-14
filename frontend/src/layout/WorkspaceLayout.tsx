import { Outlet, useParams } from 'react-router';
import { useNotes } from '@/hooks/use-notes';
import SidebarNote from '@/components/note/sidebar-note';

export default function WorkspaceLayout() {
  const { workspaceId, noteId } = useParams();
  const { notesList, isLoading, isErrorNoteList } = useNotes(workspaceId!);

  if (isErrorNoteList) {
    return (
      <div className="flex h-full items-center justify-center flex-col">
        <div className="text-2xl font-medium text-red-500">Error loading notes</div>
        <p className="text-slate-400 mt-2">Please try again later</p>
      </div>
    );
  }

  return (
    <div className="flex flex-row h-full min-h-0">
      <div className="min-w-64 h-full border-slate-200 dark:border-slate-800 flex flex-col min-h-0">
        <div className="w-full flex-1 overflow-hidden min-h-0">
          <SidebarNote isLoading={isLoading} data={notesList} />
        </div>
      </div>
      <div className="flex-1 h-full flex w-full flex-col min-h-0">
        <div className="flex-1 min-h-0">
          {noteId ? (
            <Outlet />
          ) : (
            <div className="flex h-full items-center justify-center flex-col">
              <div className="text-2xl font-medium text-slate-500">Select a note</div>
              <p className="text-slate-400 mt-2">
                Choose a note from the sidebar or create a new one
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
