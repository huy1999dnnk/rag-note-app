import { createNote, deleteNote, getAllNotes, updateNoteTitle } from '@/api/note';
import { MUTATION_KEY, QUERY_KEY } from '@/constants/query-key';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router';
import { toast } from 'sonner';

export const useNotes = (workspaceId?: string) => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const {
    data: notesList,
    isLoading,
    isError: isErrorNoteList,
  } = useQuery({
    queryKey: [QUERY_KEY.NOTE_LIST, workspaceId],
    queryFn: () => getAllNotes({ workspace_id: workspaceId! }),
    enabled: !!workspaceId,
    retry: 0,
  });

  const { mutateAsync: createNoteFn, isPending: isPendingCreateNote } = useMutation({
    mutationKey: [MUTATION_KEY.CREATE_NOTE],
    mutationFn: createNote,
  });

  const { mutateAsync: updateNoteTitleFn } = useMutation({
    mutationKey: [MUTATION_KEY.UPDATE_NOTE_TITLE],
    mutationFn: updateNoteTitle,
  });

  const { mutate: deleteNoteFn } = useMutation({
    mutationKey: [MUTATION_KEY.DELETE_NOTE],
    mutationFn: (noteId: string) => deleteNote({ node_id: noteId }),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY.NOTE_LIST],
      });
      toast.success('Note deleted successfully');
      navigate(`/${workspaceId}`);
    },
  });

  return {
    notesList,
    isLoading,
    createNoteFn,
    updateNoteTitleFn,
    deleteNoteFn,
    isErrorNoteList,
    isPendingCreateNote,
  };
};
