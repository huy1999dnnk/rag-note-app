import {
  createWorkspace,
  deleteWorkspace,
  getWorkspaceList,
  updateWorkspaceName,
  updateWorkspaceParent,
} from '@/api/workspace';
import { QUERY_KEY, MUTATION_KEY } from '@/constants/query-key';
import { useQuery, useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router';

export const useWorkspace = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { data: workspaces, isLoading } = useQuery({
    queryKey: [QUERY_KEY.WORKSPACE_LIST],
    queryFn: getWorkspaceList,
  });

  const { mutateAsync: createWorkspaceAsync } = useMutation({
    mutationKey: [MUTATION_KEY.CREATE_WORKSPACE],
    mutationFn: createWorkspace,
  });

  const { mutate: deleteWorkspaceFn } = useMutation({
    mutationFn: deleteWorkspace,
    mutationKey: [MUTATION_KEY.DELETE_WORKSPACE],
    onSuccess: () => {
      toast.success('Delete workspace successfully');
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY.WORKSPACE_LIST],
      });
      navigate('/');
    },
  });

  const { mutate: updateWorkspaceParentFn } = useMutation({
    mutationFn: updateWorkspaceParent,
    mutationKey: [MUTATION_KEY.UPDATE_WORKSPACE_PARENT],
    onSuccess: () => {
      toast.success('Update workspace parent successfully');
      queryClient.invalidateQueries({
        queryKey: [QUERY_KEY.WORKSPACE_LIST],
      });
    },
  });

  const { mutateAsync: updateWorkspaceNameFn } = useMutation({
    mutationFn: updateWorkspaceName,
    mutationKey: [MUTATION_KEY.UPDATE_WORKSPACE_NAME],
  });

  return {
    workspaces,
    createWorkspaceAsync,
    isLoading,
    deleteWorkspaceFn,
    updateWorkspaceParentFn,
    updateWorkspaceNameFn,
  };
};
