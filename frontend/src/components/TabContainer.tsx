'use client'

import React, { memo, useCallback } from 'react';
import type { TabDocument } from '@/types';
import Button from './ui/Button';
import LoadingSpinner from './ui/LoadingSpinner';

interface TabContainerProps {
  tabs: readonly TabDocument[];
  activeTabId: string | null;
  selectedTabIds: readonly string[];
  onTabSelect: (id: string) => void;
  onTabPromptSelect: (id: string, selected: boolean) => void;
  onRegenerateTab: (id: string) => void;
  children: (tab: TabDocument) => React.ReactNode;
}

const TabContainer: React.FC<TabContainerProps> = memo(({
  tabs,
  activeTabId,
  selectedTabIds,
  onTabSelect,
  onTabPromptSelect,
  onRegenerateTab,
  children
}) => {
  const handlePromptSelection = useCallback((tabId: string, selected: boolean) => {
    onTabPromptSelect(tabId, selected);
  }, [onTabPromptSelect]);

  if (tabs.length === 0) {
    return null;
  }

  return (
    <div className="glass rounded-2xl overflow-hidden glass-hover transition-all duration-500 animate-fade-in">
      {/* Header */}
      <div className="border-b border-white/20 relative">
        <div className="glass-secondary rounded-t-2xl p-6 pb-4">
          <h2 className="text-2xl font-bold text-glass-primary flex items-center space-x-3">
            <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse-glow"></div>
            <span>生成结果</span>
          </h2>
        </div>
        
        {/* Tab Navigation */}
        <div className="flex overflow-x-auto scrollbar-hide bg-gradient-to-r from-transparent via-white/5 to-transparent" role="tablist">
          {tabs.map((tab, index) => (
            <button
              key={tab.id}
              onClick={() => onTabSelect(tab.id)}
              className={`
                flex-shrink-0 px-6 py-4 text-sm font-medium transition-all duration-300 relative group
                focus:outline-none focus:ring-2 focus:ring-blue-400/50 focus:ring-inset
                ${activeTabId === tab.id
                  ? 'text-glass-primary'
                  : 'text-glass-secondary hover:text-glass-primary'
                }
              `}
              role="tab"
              aria-selected={activeTabId === tab.id}
              aria-controls={`tabpanel-${tab.id}`}
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Tab active indicator */}
              {activeTabId === tab.id && (
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 rounded-full animate-shimmer"></div>
              )}
              
              <div className="flex items-center space-x-3 relative z-10">
                <div className="relative">
                  <input
                    type="radio"
                    name="selectedPrompt"
                    checked={selectedTabIds.includes(tab.id)}
                    onChange={(e) => handlePromptSelection(tab.id, e.target.checked)}
                    className="sr-only"
                    disabled={tab.isLoading || !tab.response.role}
                    aria-label={`选择 ${tab.title} 作为提示词`}
                  />
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-200 cursor-pointer ${
                    selectedTabIds.includes(tab.id)
                      ? 'border-green-400 bg-green-400/20'
                      : 'border-glass-border hover:border-blue-400'
                  }`}>
                    {selectedTabIds.includes(tab.id) && (
                      <svg className="w-3 h-3 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                </div>
                
                <span className="font-semibold">{tab.title}</span>
                
                {tab.isLoading && (
                  <LoadingSpinner size="sm" color="text-blue-400" />
                )}
                
                {selectedTabIds.includes(tab.id) && !tab.isLoading && (
                  <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse-glow"></div>
                )}
              </div>
              
              {/* Tab hover effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-blue-400/0 via-purple-400/5 to-pink-400/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg"></div>
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="relative">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            id={`tabpanel-${tab.id}`}
            className={`p-8 transition-all duration-500 ${
              activeTabId === tab.id 
                ? 'block opacity-100 transform translate-y-0' 
                : 'hidden opacity-0 transform translate-y-2'
            }`}
            role="tabpanel"
            aria-labelledby={`tab-${tab.id}`}
          >
            {tab.isLoading ? (
              <div className="flex items-center justify-center py-16">
                <div className="text-center glass-secondary rounded-2xl p-8">
                  <LoadingSpinner size="lg" className="mx-auto mb-6" />
                  <p className="text-glass-primary text-lg font-semibold mb-2">正在生成 {tab.title}</p>
                  <p className="text-glass-muted">请耐心等待，AI正在为您创建精彩内容...</p>
                  
                  {/* Loading animation particles */}
                  <div className="flex justify-center space-x-1 mt-4">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            ) : tab.response.role ? (
              <div className="space-y-8">
                {/* Action buttons */}
                <div className="flex justify-end items-center gap-4">
                  <div className="glass-tertiary rounded-xl p-3 flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse-glow"></div>
                    <span className="text-glass-secondary text-sm font-medium">生成完成</span>
                  </div>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => onRegenerateTab(tab.id)}
                    disabled={tab.isLoading}
                    icon={
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    }
                  >
                    重新生成
                  </Button>
                </div>

                {/* Tab content with glass container */}
                <div className="glass-secondary rounded-2xl p-6 animate-fade-in">
                  {children(tab)}
                </div>
              </div>
            ) : (
              <div className="text-center py-16">
                <div className="glass-secondary rounded-2xl p-8 max-w-md mx-auto">
                  <svg className="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.664-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <p className="text-glass-primary text-lg font-semibold mb-2">生成失败</p>
                  <p className="text-glass-muted mb-6">请尝试重新生成内容</p>
                  <Button
                    variant="primary"
                    onClick={() => onRegenerateTab(tab.id)}
                    icon={
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    }
                  >
                    重试
                  </Button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
});

TabContainer.displayName = 'TabContainer';

export default TabContainer;