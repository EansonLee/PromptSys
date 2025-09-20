import { useState, useCallback } from 'react';
import type { TabDocument } from '@/types';

export interface UseTabsReturn {
  tabs: readonly TabDocument[];
  activeTabId: string | null;
  selectedTabIds: readonly string[];
  setActiveTab: (id: string) => void;
  selectSingleTab: (id: string) => void;
  updateTab: (id: string, updates: Partial<Omit<TabDocument, 'id'>>) => void;
  clearTabs: () => void;
  initializeTabs: (count: number) => TabDocument[];
}

export function useTabs(): UseTabsReturn {
  const [tabs, setTabs] = useState<TabDocument[]>([]);
  const [activeTabId, setActiveTabId] = useState<string | null>(null);
  const [selectedTabIds, setSelectedTabIds] = useState<string[]>([]);

  const setActiveTab = useCallback((id: string) => {
    setActiveTabId(id);
  }, []);

  const selectSingleTab = useCallback((id: string) => {
    setSelectedTabIds([id]);
  }, []);

  const updateTab = useCallback((id: string, updates: Partial<Omit<TabDocument, 'id'>>) => {
    setTabs(prev => prev.map(tab => 
      tab.id === id ? { ...tab, ...updates } : tab
    ));
  }, []);


  const clearTabs = useCallback(() => {
    setTabs([]);
    setActiveTabId(null);
    setSelectedTabIds([]);
  }, []);

  const initializeTabs = useCallback((count: number) => {
    const initialTabs: TabDocument[] = Array.from({ length: count }, (_, index) => ({
      id: `tab-${Date.now()}-${index}`,
      title: `页面 ${index + 1}`,
      response: {} as any, // Will be populated later
      isLoading: true
    }));
    
    setTabs(initialTabs);
    setActiveTabId(initialTabs[0]?.id || null);
    setSelectedTabIds([]);
    
    return initialTabs; // Return the created tabs for immediate use
  }, []);

  return {
    tabs,
    activeTabId,
    selectedTabIds,
    setActiveTab,
    selectSingleTab,
    updateTab,
    clearTabs,
    initializeTabs
  };
}