import { useState, useCallback } from 'react';
import type { TabDocument } from '@/types';

export interface UseTabsReturn {
  tabs: readonly TabDocument[];
  activeTabId: string | null;
  selectedTabIds: readonly string[];
  setActiveTab: (id: string) => void;
  selectTab: (id: string, selected: boolean) => void;
  selectSingleTab: (id: string) => void;
  addTab: (tab: TabDocument) => void;
  updateTab: (id: string, updates: Partial<Omit<TabDocument, 'id'>>) => void;
  removeTab: (id: string) => void;
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

  const selectTab = useCallback((id: string, selected: boolean) => {
    setSelectedTabIds(prev => {
      if (selected) {
        return [...prev, id];
      } else {
        return prev.filter(tabId => tabId !== id);
      }
    });
  }, []);

  const selectSingleTab = useCallback((id: string) => {
    setSelectedTabIds([id]);
  }, []);

  const addTab = useCallback((tab: TabDocument) => {
    setTabs(prev => [...prev, tab]);
    if (activeTabId === null) {
      setActiveTabId(tab.id);
    }
  }, [activeTabId]);

  const updateTab = useCallback((id: string, updates: Partial<Omit<TabDocument, 'id'>>) => {
    setTabs(prev => prev.map(tab => 
      tab.id === id ? { ...tab, ...updates } : tab
    ));
  }, []);

  const removeTab = useCallback((id: string) => {
    setTabs(prev => {
      const newTabs = prev.filter(tab => tab.id !== id);
      // If removing the active tab, set a new active tab
      if (id === activeTabId && newTabs.length > 0) {
        setActiveTabId(newTabs[0]?.id || null);
      } else if (newTabs.length === 0) {
        setActiveTabId(null);
      }
      return newTabs;
    });
    
    // Remove from selected tabs
    setSelectedTabIds(prev => prev.filter(tabId => tabId !== id));
  }, [activeTabId]);

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
    selectTab,
    selectSingleTab,
    addTab,
    updateTab,
    removeTab,
    clearTabs,
    initializeTabs
  };
}