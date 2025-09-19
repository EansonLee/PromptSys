'use client'

import React, { useCallback, useEffect, useMemo, useDeferredValue } from 'react';
import type { PromptRequest, ProgressData } from '@/types';
import { useAPI } from '@/hooks/useAPI';
import { useTabs } from '@/hooks/useTabs';
import { API_ENDPOINTS } from '@/constants/themes';

import PromptForm from './PromptForm';
import TabContainer from './TabContainer';
import ContentViewer from './ContentViewer';
const AIAgentActions = React.lazy(() => import('./AIAgentActions'));
import { ProgressVisualization } from './ProgressVisualization';
import ErrorBoundary from './ErrorBoundary';

interface PromptGeneratorProps {
  className?: string;
}

const PromptGeneratorRefactored: React.FC<PromptGeneratorProps> = ({ className = '' }) => {
  // 从环境变量读取配置（memoized）
  const showAIAgentActions = useMemo(() =>
    process.env.NEXT_PUBLIC_SHOW_AI_AGENT_ACTIONS === 'true', []);
  
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

  // 简化的状态管理 - PromptForm组件现在完全使用react-hook-form
  // 检查是否隐藏变体和参考文件字段（memoized）
  const showVariantAndReferenceFields = useMemo(() =>
    process.env.NEXT_PUBLIC_SHOW_VARIANT_AND_REFERENCE_FIELDS === 'true', []);

  // 只保留默认值常量，不需要状态管理
  const defaultFormData = React.useMemo(() => ({
    app_name: '',
    theme: '',
    variant_folder: showVariantAndReferenceFields ? '' : 'variant_default',
    ui_color: '',
    reference_file: showVariantAndReferenceFields ? '' : 'MainActivity',
    tab_count: 3
  }), [showVariantAndReferenceFields]);

  // 存储最后提交的表单数据，用于重新生成
  const [lastSubmittedData, setLastSubmittedData] = React.useState<PromptRequest | null>(null);

  // Progress tracking
  const [showProgress, setShowProgress] = React.useState(false);
  const [progressData, setProgressData] = React.useState<ProgressData>({
    progress: 0,
    status: '准备开始...',
    step: '初始化'
  });

  // 清理错误状态
  useEffect(() => {
    if (error) {
      clearError();
    }
  }, [clearError, error]);

  // 简化的事件处理器 - 不再需要状态同步
  const handleThemeSelect = useCallback(() => {
    // 主题选择现在直接在PromptForm中处理
  }, []);

  const handleTabCountChange = useCallback(() => {
    // Tab数量变化现在直接在PromptForm中处理
  }, []);

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



  // Form submit handler
  const handleSubmit = useCallback(async (data: PromptRequest) => {
    // 确保隐藏字段有默认值
    const processedData: PromptRequest = {
      ...data,
      variant_folder: showVariantAndReferenceFields ? data.variant_folder : 'variant_default',
      reference_file: showVariantAndReferenceFields ? data.reference_file : 'MainActivity'
    };

    // 保存最后提交的数据用于重新生成
    setLastSubmittedData(processedData);

    // 直接使用处理后的数据执行生成
    const tabCount = processedData.tab_count || 1;

    setShowProgress(true);
    clearTabs();

    // Initialize tabs and get their IDs
    const initialTabs = initializeTabs(tabCount);

    try {
      // Generate documents sequentially
      for (let i = 0; i < tabCount; i++) {
        const result = await generateSinglePrompt(
          processedData,
          (progressData) => handleProgress(progressData, i, tabCount, false)
        );

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

      // Complete
      setProgressData({
        progress: 100,
        status: `成功生成 ${tabCount} 个版本的提示词文档`,
        step: '完成'
      });

    } catch (err) {
      console.error('Batch generation failed:', err);
      // Mark all loading tabs as failed
      initialTabs.forEach(tab => {
        updateTab(tab.id, { isLoading: false });
      });
      // Hide progress on error
      setShowProgress(false);
    }
  }, [clearTabs, initializeTabs, generateSinglePrompt, handleProgress, updateTab, showVariantAndReferenceFields]);

  // Tab regeneration handler
  const handleRegenerateTab = useCallback(async (tabId: string) => {
    setShowProgress(true);
    updateTab(tabId, { isLoading: true });

    try {
      // 使用最后提交的数据进行重新生成
      if (!lastSubmittedData) {
        console.error('No form data available for regeneration');
        return;
      }
      const processedFormData = lastSubmittedData;

      const result = await generateSinglePrompt(
        processedFormData,
        (progressData) => handleProgress(progressData, 0, 1, true)
      );

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
  }, [lastSubmittedData, generateSinglePrompt, handleProgress, updateTab]);

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
          formData={defaultFormData}
          isLoading={isLoading}
          error={error}
          onThemeSelect={handleThemeSelect}
          onSubmit={handleSubmit}
          onTabCountChange={handleTabCountChange}
        />

        {/* AI Agent Actions - 条件渲染与懒加载 */}
        {hasValidTabs && showAIAgentActions && (
          <React.Suspense fallback={<div className="animate-pulse bg-gray-200 rounded-lg h-20"></div>}>
            <AIAgentActions
              onOpenClaudePage={handleOpenClaudePage}
              onGetRepository={handleGetRepository}
              onGetTasks={handleGetTasks}
              onExecuteTasks={handleExecuteTasks}
              hasSelectedPrompt={hasSelectedPrompt}
              isLoading={isLoading}
            />
          </React.Suspense>
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