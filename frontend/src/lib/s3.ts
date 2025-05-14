import { FILE_BLOCK_TYPES } from '@/constants/s3';
import { PartialBlock } from '@/types/blocknote';

// Utility: Extract S3 object key from a presigned URL or return as-is if already a key
function extractObjectKey(urlOrKey: string): string {
  // If it's already a key (not a URL), return as is
  if (!urlOrKey.startsWith('http')) return urlOrKey;
  // Example: https://bucket.s3.amazonaws.com/uploads/userid/filename.ext?AWSAccessKeyId=...
  // Extract the path after the bucket domain, before the query string
  try {
    const url = new URL(urlOrKey);
    // Remove leading slash
    return url.pathname.startsWith('/') ? url.pathname.slice(1) : url.pathname;
  } catch {
    // If parsing fails, return as is
    return urlOrKey;
  }
}

// Utility: Recursively process blocks to replace file block URLs with object keys
export function normalizeFileBlocks(blocks: PartialBlock[]): PartialBlock[] {
  return blocks.map((block) => {
    if (
      block &&
      typeof block.type === 'string' &&
      FILE_BLOCK_TYPES.includes(block.type) &&
      block.props &&
      typeof block.props.url === 'string'
    ) {
      return {
        ...block,
        props: {
          ...block.props,
          url: extractObjectKey(block.props.url),
        },
      };
    }
    // If you have nested blocks, handle them here (e.g., block.children)
    return block;
  });
}
