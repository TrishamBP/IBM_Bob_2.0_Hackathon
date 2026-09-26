'use client';

import { createContext, useContext } from 'react';
import type { SourceCitationData } from '@/types/chat';

/** Opens the source viewer for a citation; `null` outside a provider. */
export const SourceViewerContext = createContext<((source: SourceCitationData) => void) | null>(
  null
);

export function useOpenSource() {
  return useContext(SourceViewerContext);
}
