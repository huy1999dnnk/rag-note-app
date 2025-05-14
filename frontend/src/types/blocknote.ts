import { InlineContent, TableContent } from '@blocknote/core';

export type PartialBlock = {
  id?: string;
  type?: string;
  props?: Partial<Record<string, any>>; // exact type depends on "type"
  content?: string | InlineContent<any, any>[] | TableContent<any, any>;
  children?: PartialBlock[];
};
