import '@/styles/tree-node.css';
import { MoveHandler, NodeRendererProps, Tree } from 'react-arborist';
import { Skeleton } from '@/components/ui/skeleton';
import { ChevronDown, ChevronRight, Folder, MoreHorizontal, Plus } from 'lucide-react';
import { useWorkspace } from '@/hooks/use-workspace';
import AddNewWorkspace from './add-new-workspace';
import { forwardRef, useEffect, useImperativeHandle, useRef, useState } from 'react';
import { MoreActionDropdown } from './more-action';
import { useNavigate, useParams } from 'react-router';
import { cn } from '@/lib/utils';
import { useElementSize } from '@/hooks/use-element-size';
import { useSidebar } from '@/components/ui/sidebar';

interface NodeRef {
  toggleNode: (id: string) => void;
  toogleParent: (id: string) => void;
}

export default function WorkspaceTree() {
  const { workspaceId } = useParams();
  const { state } = useSidebar();
  const isCollapsed = state === 'collapsed';
  const childRef = useRef<NodeRef>(null);
  const navigate = useNavigate();
  const { ref, height, width } = useElementSize();
  const dataLoadedRef = useRef(false);
  const wasCollapsedRef = useRef(false);

  const { workspaces: data, isLoading, updateWorkspaceParentFn } = useWorkspace();
  const [currentId, setCurrentId] = useState<string | undefined>();
  const [name, setName] = useState<string | undefined>();
  const [open, setOpen] = useState(false);

  const onMove: MoveHandler<{ name: string; children: any[] }> = ({ dragIds, parentId }) => {
    updateWorkspaceParentFn({
      id: dragIds[0],
      parentId: parentId!,
    });
  };

  const onNavigate = (id: string) => {
    navigate(`/${id}`);
  };

  // Reset dataLoadedRef when sidebar collapses/expands
  useEffect(() => {
    if (isCollapsed) {
      // Sidebar just collapsed
      wasCollapsedRef.current = true;
    } else if (wasCollapsedRef.current) {
      // Sidebar just expanded after being collapsed
      dataLoadedRef.current = false; // Reset to trigger the expand effect
      wasCollapsedRef.current = false;
    }
  }, [isCollapsed]);

  // Effect to expand tree to current workspace when data is loaded
  useEffect(() => {
    // Only run when we have both a workspaceId and data is loaded
    if (workspaceId && data && data.length > 0 && childRef.current && !dataLoadedRef.current) {
      // Set flag to prevent running this again if component re-renders
      dataLoadedRef.current = true;

      // Small delay to ensure tree is fully rendered
      setTimeout(() => {
        childRef.current?.toogleParent(workspaceId);
      }, 100);
    }
  }, [workspaceId, data, isCollapsed]);

  if (isCollapsed) {
    return null;
  }

  if (isLoading) {
    return <LoaderTree />;
  }

  return (
    <>
      <AddNewWorkspace
        openModal={open}
        setOpenModal={setOpen}
        currentId={currentId}
        onAddSubSuccess={() => {
          childRef?.current?.toggleNode(currentId!);
        }}
        name={name}
        setName={setName}
      />

      <div ref={ref} className="h-[300px] w-full overflow-auto min-h-0">
        <Tree<{ name: string; children: any[] }>
          data={data}
          openByDefault={false}
          width={width}
          height={height}
          paddingTop={8}
          paddingBottom={8}
          onMove={onMove}
          indent={12}
          children={({ style, dragHandle, node, tree }) => (
            <Node
              node={node}
              style={style}
              dragHandle={dragHandle}
              tree={tree}
              setOpen={setOpen}
              setCurrentId={setCurrentId}
              ref={childRef}
              setName={setName}
              onNavigate={onNavigate}
            />
          )}
        />
      </div>
    </>
  );
}

const Node = forwardRef<
  NodeRef,
  NodeRendererProps<{ name: string; children: any[] }> & {
    setCurrentId: (id: string | undefined) => void;
    setOpen: (open: boolean) => void;
    setName: (name: string | undefined) => void;
    onNavigate: (id: string) => void;
  }
>(({ node, style, dragHandle, setCurrentId, setOpen, tree, setName, onNavigate }, ref) => {
  const { workspaceId } = useParams();
  const toggleNode = (id: string) => {
    tree.open(id);
  };

  const toogleParent = (id: string) => {
    tree.openParents(id);
  };

  // Expose methods via ref
  useImperativeHandle(ref, () => ({
    toggleNode,
    toogleParent,
  }));

  const isActive = workspaceId === node.id;
  return (
    <>
      <div
        style={{
          ...style,
          width: '100%',
        }}
        ref={dragHandle}
        className="cursor-pointer tree-node"
        key={node.id}
      >
        <div
          className={cn(
            'w-full flex items-center justify-between p-1 rounded-md',
            isActive
              ? 'bg-slate-200 dark:bg-slate-800'
              : 'hover:bg-slate-100 dark:hover:bg-slate-700'
          )}
        >
          <div className="flex items-center gap-2 min-w-0 flex-1 ">
            <div className="flex-shrink-0">
              {node.data.children.length == 0 ? (
                <Folder size={14} />
              ) : node.isOpen ? (
                <ChevronDown size={14} onClick={() => node.toggle()} />
              ) : (
                <ChevronRight size={14} onClick={() => node.toggle()} />
              )}
            </div>
            <div className="flex-1 truncate" onClick={() => onNavigate(node.id)}>
              {node.data.name}
            </div>
          </div>
          <div className="flex items-center justify-center tree-node-actions pr-1">
            <Plus
              className="hover:bg-accent"
              size={18}
              onClick={() => {
                setCurrentId(node.id);
                setOpen(true);
              }}
            />

            <button className="p-1 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-md ml-2 flex-shrink-0">
              <MoreActionDropdown
                name={node.data.name}
                id={node.id}
                setName={setName}
                setCurrentId={setCurrentId}
                setOpen={setOpen}
              >
                <MoreHorizontal size={14} className="text-slate-500" />
              </MoreActionDropdown>
            </button>
          </div>
        </div>
      </div>
    </>
  );
});

const LoaderTree = () => {
  return (
    <div className="flex flex-col gap-2">
      <Skeleton className="h-4 w-1/2" />
      <Skeleton className="h-4 w-1/2" />
      <Skeleton className="h-4 w-1/2" />
    </div>
  );
};
