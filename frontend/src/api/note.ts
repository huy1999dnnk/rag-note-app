import api from '@/lib/axios';
import { PartialBlock } from '@/types/blocknote';

export const getAllNotes = async ({ workspace_id }: { workspace_id: string }) => {
  const res = await api.get(`/notes/${workspace_id}`);
  return res.data;
};

export const createNote = async ({
  title,
  workspace_id,
}: {
  title: string;
  workspace_id: string;
}) => {
  const res = await api.post('/notes', {
    title,
    workspace_id,
  });
  return res.data;
};

export const deleteNote = async ({ node_id }: { node_id: string }) => {
  const res = await api.delete(`/notes/${node_id}`);
  return res.data;
};

export const updateNoteTitle = async ({ id, title }: { id: string; title: string }) => {
  const res = await api.put(`/notes/title`, {
    title,
    id,
  });
  return res.data;
};

export const updateNoteContent = async ({
  note_id,
  content,
}: {
  note_id: string;
  content: PartialBlock[];
}) => {
  const res = await api.put(`/notes/content`, {
    content,
    note_id,
  });
  return res.data;
};

export const getNoteContent = async ({ note_id }: { note_id: string }) => {
  const res = await api.get(`/notes/${note_id}/content`);
  return res.data;
};
