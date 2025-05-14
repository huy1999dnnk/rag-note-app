import '@blocknote/core/fonts/inter.css';
import '@/styles/blocknote.css';
import { BlockNoteView } from '@blocknote/shadcn';
import '@blocknote/shadcn/style.css';
import { useTheme } from '@/contexts/ThemeContext';
import {
  BlockNoteEditor,
  BlockSchemaFromSpecs,
  BlockSpecs,
  PartialBlock as PartialBlockType,
} from '@blocknote/core';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { debounce } from 'lodash';
import { useMutation } from '@tanstack/react-query';
import { updateNoteContent } from '@/api/note';
import { MUTATION_KEY } from '@/constants/query-key';
import { FILE_BLOCK_TYPES } from '@/constants/s3';
import { PartialBlock } from '@/types/blocknote';
import { normalizeFileBlocks } from '@/lib/s3';

import { resolveImageUrl, uploadFile } from '@/api/s3-upload';

interface IBlockNoteEditorProps {
  initialContent: PartialBlock[];
  isLoading: boolean;
  noteId: string | undefined;
}

export default function BlockNoteEditorComponent({
  initialContent,
  isLoading,
  noteId,
}: IBlockNoteEditorProps) {
  const noteIdRef = useRef<string | undefined>(noteId);
  const [resolvedContent, setResolvedContent] = useState<PartialBlock[] | undefined>(undefined);

  const { mutate } = useMutation({
    mutationKey: [MUTATION_KEY.UPDATE_NOTE_CONTENT, noteId],
    mutationFn: updateNoteContent,
    onError: (error) => {
      console.error('Error updating note content:', error);
    },
  });

  const saveContent = useCallback(
    debounce(async (content: any) => {
      const normalizedContent = normalizeFileBlocks(content);
      mutate({
        note_id: noteIdRef.current!,
        content: normalizedContent,
      });
    }, 700),
    []
  );

  const handleUpload = useCallback(
    async (file: File) => {
      return uploadFile(file, noteId as string);
    },
    [noteId]
  );

  const editor = useMemo(() => {
    if (isLoading || !resolvedContent) {
      return undefined;
    }
    return BlockNoteEditor.create({
      initialContent: resolvedContent as PartialBlockType<BlockSchemaFromSpecs<BlockSpecs>>[],
      uploadFile: handleUpload,
    });
  }, [isLoading, resolvedContent]);

  useEffect(() => {
    let isMounted = true;
    const processContent = async () => {
      if (!initialContent) {
        return;
      }
      const blocks = await Promise.all(
        initialContent.map(async (block) => {
          if (
            FILE_BLOCK_TYPES.includes(block?.type!) &&
            block.props?.url &&
            !block.props.url.startsWith('http')
          ) {
            try {
              const url = await resolveImageUrl(block.props.url);
              return {
                ...block,
                props: {
                  ...block.props,
                  url,
                },
              };
            } catch {
              return block;
            }
          }
          return block;
        })
      );
      if (isMounted) setResolvedContent(blocks as PartialBlock[]);
    };
    processContent();
    return () => {
      isMounted = false;
    };
  }, [initialContent]);

  useEffect(() => {
    if (!editor) return;
    const unsubscribe = editor.onChange((editor) => {
      saveContent(editor.document);
    });
    return () => {
      unsubscribe?.();
    };
  }, [editor, saveContent]);

  // Always keep the latest noteId in a ref
  useEffect(() => {
    noteIdRef.current = noteId;
  }, [noteId]);

  // Cancel debounce when noteId changes (or on unmount)
  useEffect(() => {
    return () => {
      saveContent.cancel();
    };
  }, [noteId, saveContent]);

  if (editor === undefined) {
    return 'Loading content...';
  }
  const { theme } = useTheme();

  return (
    <div className="h-full flex flex-col min-h-0">
      <div className="flex-1 overflow-y-auto blocknote-full-height">
        <BlockNoteView slashMenu={true} editor={editor} theme={theme} />
      </div>
    </div>
  );
}
