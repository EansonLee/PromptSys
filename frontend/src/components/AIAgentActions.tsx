'use client'

import React, { memo } from 'react';
import Button from './ui/Button';
import Card from './ui/Card';

interface AIAgentActionsProps {
  onOpenClaudePage: () => Promise<void>;
  onGetRepository: () => Promise<void>;
  onGetTasks: () => Promise<void>;
  onExecuteTasks: () => Promise<void>;
  hasSelectedPrompt: boolean;
  isLoading?: boolean;
}

const AIAgentActions: React.FC<AIAgentActionsProps> = memo(({
  onOpenClaudePage,
  onGetRepository,
  onGetTasks,
  onExecuteTasks,
  hasSelectedPrompt,
  isLoading = false
}) => {
  const actionButtons = [
    {
      id: 'open-page',
      label: '打开页面',
      onClick: onOpenClaudePage,
      icon: (
        <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
        </svg>
      ),
      bgColor: 'bg-green-100 group-hover:bg-green-200',
      borderColor: 'border-green-200 hover:border-green-400',
      hoverBg: 'hover:bg-green-50',
      textColor: 'text-green-700 group-hover:text-green-700'
    },
    {
      id: 'get-repository',
      label: '获取仓库',
      onClick: onGetRepository,
      icon: (
        <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 1v6M16 1v6" />
        </svg>
      ),
      bgColor: 'bg-blue-100 group-hover:bg-blue-200',
      borderColor: 'border-blue-200 hover:border-blue-400',
      hoverBg: 'hover:bg-blue-50',
      textColor: 'text-blue-700 group-hover:text-blue-700'
    },
    {
      id: 'get-tasks',
      label: '获取任务',
      onClick: onGetTasks,
      icon: (
        <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      ),
      bgColor: 'bg-orange-100 group-hover:bg-orange-200',
      borderColor: 'border-orange-200 hover:border-orange-400',
      hoverBg: 'hover:bg-orange-50',
      textColor: 'text-orange-700 group-hover:text-orange-700'
    },
    {
      id: 'execute-tasks',
      label: '执行任务',
      onClick: onExecuteTasks,
      icon: (
        <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H15M9 10V9a2 2 0 012-2h2a2 2 0 012 2v1m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v1m-6 0h6" />
        </svg>
      ),
      bgColor: 'bg-purple-100 group-hover:bg-purple-200',
      borderColor: 'border-purple-200 hover:border-purple-400',
      hoverBg: 'hover:bg-purple-50',
      textColor: 'text-purple-700 group-hover:text-purple-700'
    }
  ];

  return (
    <Card className="bg-gradient-to-r from-purple-50 to-blue-50">
      <Card.Header>
        <h2 className="text-2xl font-semibold text-gray-800 flex items-center">
          <svg className="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          AI Agent 自动化操作
        </h2>
      </Card.Header>

      <Card.Content>
        {/* Selection reminder */}
        <div className="mb-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <div className="flex items-center mb-2">
            <svg className="w-5 h-5 text-amber-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h4 className="text-amber-800 font-medium">操作提醒</h4>
          </div>
          <p className="text-amber-700 text-sm">
            {hasSelectedPrompt 
              ? '已选择提示词，可以进行 AI Agent 自动化操作'
              : '请在标签页中选择一个生成的提示词，然后使用以下按钮进行 AI Agent 自动化操作'
            }
          </p>
        </div>

        {/* Action buttons grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {actionButtons.map((action) => (
            <button
              key={action.id}
              onClick={action.onClick}
              disabled={isLoading}
              className={`
                flex flex-col items-center p-4 bg-white border-2 rounded-lg 
                transition-all duration-200 group
                ${action.borderColor} ${action.hoverBg}
                focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
                disabled:opacity-50 disabled:cursor-not-allowed
              `}
              aria-label={action.label}
            >
              <div className={`w-12 h-12 rounded-full flex items-center justify-center mb-3 transition-colors ${action.bgColor}`}>
                {action.icon}
              </div>
              <span className={`text-sm font-medium ${action.textColor}`}>
                {action.label}
              </span>
            </button>
          ))}
        </div>
      </Card.Content>
    </Card>
  );
});

AIAgentActions.displayName = 'AIAgentActions';

export default AIAgentActions;