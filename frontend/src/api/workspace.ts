import api from '@/lib/axios';

export const getWorkspaceList = async () => {
  const res = await api.get('/workspaces');
  return res.data;
};

export const createWorkspace = async ({
  name,
  parent_id,
}: {
  name: string;
  parent_id: string | null;
}) => {
  const res = await api.post('/workspaces', {
    name,
    parent_id,
  });
  return res.data;
};

export const deleteWorkspace = async (id: string) => {
  const res = await api.delete(`/workspaces/${id}`);
  return res.data;
};

export const updateWorkspaceName = async ({ name, id }: { name: string; id: string }) => {
  const res = await api.put(`/workspaces/name`, {
    name,
    id,
  });
  return res.data;
};

export const updateWorkspaceParent = async ({ id, parentId }: { id: string; parentId: string }) => {
  const res = await api.put(`/workspaces/parent`, {
    parent_id: parentId,
    id,
  });
  return res.data;
};
