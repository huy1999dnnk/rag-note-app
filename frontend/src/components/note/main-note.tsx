import { useParams } from 'react-router';
import BlockNoteEditor from '@/components/ui/blocknote-editor';
import { useQuery } from '@tanstack/react-query';
import { getNoteContent } from '@/api/note';

export default function MainNote() {
  const { noteId } = useParams<{ noteId: string }>();

  const { data: initialContent, isLoading } = useQuery({
    queryKey: ['note', noteId],
    queryFn: () => getNoteContent({ note_id: noteId! }),
    enabled: !!noteId,
  });

  return (
    <div className="flex flex-col w-full h-full">
      <div className="flex-1 min-h-0 overflow-hidden">
        <BlockNoteEditor
          initialContent={initialContent?.content}
          isLoading={isLoading}
          noteId={noteId}
        />
      </div>
      <div className="py-2 border-t text-center">2025</div>
    </div>
  );
}
