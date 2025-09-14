'use client'

import React, { useCallback, useEffect, useMemo, startTransition, useDeferredValue } from 'react';
import type { PromptRequest, PromptResponse, ThemeOption, ProgressData } from '@/types';
import { useAPI } from '@/hooks/useAPI';
import { useTabs } from '@/hooks/useTabs';
import { useForm } from '@/hooks/useForm';
import { API_ENDPOINTS } from '@/constants/themes';

import PromptForm from './PromptForm';
import TabContainer from './TabContainer';
import ContentViewer from './ContentViewer';
import AIAgentActions from './AIAgentActions';
import { ProgressVisualization } from './ProgressVisualization';
import ErrorBoundary from './ErrorBoundary';

interface PromptGeneratorProps {
  className?: string;
}

const PromptGeneratorRefactored: React.FC<PromptGeneratorProps> = ({ className = '' }) => {
  // 从环境变量读取配置
  const showAIAgentActions = process.env.NEXT_PUBLIC_SHOW_AI_AGENT_ACTIONS === 'true';
  
  const { isLoading, error, clearError, generateSinglePrompt, callAgentAction } = useAPI();
  const { 
    tabs, 
    activeTabId, 
    selectedTabIds, 
    setActiveTab, 
    selectSingleTab, 
    updateTab, 
    clearTabs, 
    initializeTabs 
  } = useTabs();
  const {
    formData,
    errors,
    touched,
    isValid,
    handleInputChange,
    setFieldValue,
    validateForm
  } = useForm();

  // Progress tracking
  const [showProgress, setShowProgress] = React.useState(false);
  const [progressData, setProgressData] = React.useState<ProgressData>({
    progress: 0,
    status: '准备开始...',
    step: '初始化'
  });

  // Clear error when form data changes
  useEffect(() => {
    if (error) {
      clearError();
    }
  }, [formData, clearError, error]);

  // Theme selection handler
  const handleThemeSelect = useCallback((theme: ThemeOption) => {
    startTransition(() => {
      setFieldValue('theme', theme.description);
    });
  }, [setFieldValue]);

  // Tab count change handler
  const handleTabCountChange = useCallback((count: number) => {
    startTransition(() => {
      setFieldValue('tab_count', count);
    });
  }, [setFieldValue]);

  // Progress handler
  const handleProgress = useCallback((data: ProgressData, documentIndex: number, total: number, isRegeneration: boolean) => {
    let totalProgress: number;
    let statusMessage: string;
    
    if (isRegeneration) {
      totalProgress = data.progress;
      statusMessage = `重新生成: ${data.status}`;
    } else {
      if (total <= 0) total = 1;
      const baseProgress = (documentIndex / total) * 100;
      const docProgressPortion = data.progress / total;
      totalProgress = baseProgress + docProgressPortion;
      statusMessage = `文档 ${documentIndex + 1}/${total}: ${data.status}`;
    }
    
    totalProgress = Math.max(0, Math.min(100, totalProgress));
    
    setProgressData({
      progress: isNaN(totalProgress) ? 0 : totalProgress,
      status: statusMessage,
      step: data.step
    });
  }, []);

  // Generate single document
  const generateDocument = useCallback(async (
    documentIndex: number, 
    total: number = 1, 
    isRegeneration: boolean = false
  ): Promise<PromptResponse | null> => {
    return generateSinglePrompt(
      formData,
      (data) => handleProgress(data, documentIndex, total, isRegeneration)
    );
  }, [formData, generateSinglePrompt, handleProgress]);

  // Batch generation handler
  const handleBatchGeneration = useCallback(async () => {
    if (!validateForm()) {
      return;
    }

    const tabCount = formData.tab_count || 1;
    
    setShowProgress(true);
    clearTabs();
    
    // Initialize tabs and get their IDs
    const initialTabs = initializeTabs(tabCount);
    
    try {
      // Generate documents sequentially
      for (let i = 0; i < tabCount; i++) {
        const result = await generateDocument(i, tabCount, false);
        
        if (result) {
          const targetTabId = initialTabs[i]?.id;
          if (targetTabId) {
            updateTab(targetTabId, {
              response: result,
              isLoading: false
            });
          }
        }
      }
      
      // Complete - don't set timeout here as handleProgress will handle it
      setProgressData({
        progress: 100,
        status: `成功生成 ${tabCount} 个版本的提示词文档`,
        step: '完成'
      });
      
    } catch (err) {
      console.error('Batch generation failed:', err);
      // Mark all loading tabs as failed using the initial tabs reference
      initialTabs.forEach(tab => {
        updateTab(tab.id, { isLoading: false });
      });
      // Hide progress on error
      setShowProgress(false);
    }
  }, [validateForm, formData.tab_count, clearTabs, initializeTabs, generateDocument, updateTab]);

  // Form submit handler
  const handleSubmit = useCallback(async (data: PromptRequest) => {
    // Update form data with validated data from React Hook Form
    Object.entries(data).forEach(([key, value]) => {
      setFieldValue(key as keyof PromptRequest, value);
    });
    await handleBatchGeneration();
  }, [handleBatchGeneration, setFieldValue]);

  // Tab regeneration handler
  const handleRegenerateTab = useCallback(async (tabId: string) => {
    setShowProgress(true);
    updateTab(tabId, { isLoading: true });
    
    try {
      const result = await generateDocument(0, 1, true);
      
      if (result) {
        updateTab(tabId, {
          response: result,
          isLoading: false
        });
      }
      
      setProgressData({
        progress: 100,
        status: '重新生成完成！',
        step: '完成'
      });
      
    } catch (err) {
      console.error('Tab regeneration failed:', err);
      updateTab(tabId, { isLoading: false });
      // Hide progress on error
      setShowProgress(false);
    }
  }, [generateDocument, updateTab]);

  // AI Agent action handlers
  const handleOpenClaudePage = useCallback(async () => {
    const result = await callAgentAction(API_ENDPOINTS.OPEN_CLAUDE_CLI);
    if (result.success) {
      alert('Claude CLI 已成功打开');
    }
  }, [callAgentAction]);

  const handleGetRepository = useCallback(async () => {
    const result = await callAgentAction(API_ENDPOINTS.GET_REPOSITORY, {
      repository_url: 'https://gitlab.example.com/your-repo'
    });
    if (result.success && result.data) {
      alert(`仓库信息获取成功: ${(result.data as { repository_name?: string })?.repository_name || '未知'}`);
    }
  }, [callAgentAction]);

  const handleGetTasks = useCallback(async () => {
    if (selectedTabIds.length === 0) {
      alert('请至少选择一个提示词');
      return;
    }

    const selectedTab = tabs.find(tab => selectedTabIds.includes(tab.id));
    if (!selectedTab || !selectedTab.response.role) {
      alert('所选提示词内容无效');
      return;
    }

    const result = await callAgentAction(API_ENDPOINTS.GET_TASKS, {
      selected_prompt: {
        role: selectedTab.response.role,
        goal: selectedTab.response.goal,
        function_output: selectedTab.response.function_output,
        ui_requirements: selectedTab.response.ui_requirements
      }
    });
    
    if (result.success) {
      alert('任务已成功传递给 Claude CLI');
    }
  }, [selectedTabIds, tabs, callAgentAction]);

  const handleExecuteTasks = useCallback(async () => {
    const result = await callAgentAction(API_ENDPOINTS.EXECUTE_TASKS);
    if (result.success && result.data) {
      alert(`任务执行完成: ${(result.data as { status?: string })?.status || '成功'}`);
    }
  }, [callAgentAction]);

  // Deferred values for better performance
  const deferredTabs = useDeferredValue(tabs);
  const deferredFormData = useDeferredValue(formData);

  // Memoized values
  const hasSelectedPrompt = useMemo(() => selectedTabIds.length > 0, [selectedTabIds]);
  const hasValidTabs = useMemo(() => deferredTabs.length > 0, [deferredTabs]);

  return (
    <ErrorBoundary>
      <div className={`max-w-4xl mx-auto space-y-8 ${className}`}>
        {/* Progress Visualization */}
        <ProgressVisualization 
          isVisible={showProgress}
          progressData={progressData}
          onComplete={() => setShowProgress(false)}
        />

        {/* Input Form */}
        <PromptForm
          formData={deferredFormData}
          isLoading={isLoading}
          error={error}
          onThemeSelect={handleThemeSelect}
          onSubmit={handleSubmit}
          onTabCountChange={handleTabCountChange}
        />

        {/* AI Agent Actions - 条件渲染 */}
        {hasValidTabs && showAIAgentActions && (
          <AIAgentActions
            onOpenClaudePage={handleOpenClaudePage}
            onGetRepository={handleGetRepository}
            onGetTasks={handleGetTasks}
            onExecuteTasks={handleExecuteTasks}
            hasSelectedPrompt={hasSelectedPrompt}
            isLoading={isLoading}
          />
        )}

        {/* Tab Results */}
        {hasValidTabs && (
          <TabContainer
            tabs={deferredTabs}
            activeTabId={activeTabId}
            selectedTabIds={selectedTabIds}
            onTabSelect={setActiveTab}
            onTabPromptSelect={selectSingleTab}
            onRegenerateTab={handleRegenerateTab}
          >
            {(tab) => <ContentViewer response={tab.response} />}
          </TabContainer>
        )}
      </div>
    </ErrorBoundary>
  );
};

export default PromptGeneratorRefactored;