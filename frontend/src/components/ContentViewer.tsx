'use client'

import React, { memo, useState, useCallback } from 'react';
import type { PromptResponse } from '@/types';
import Button from './ui/Button';
import { FixedContentAppender } from './FixedContentAppender';

interface ContentViewerProps {
  response: PromptResponse;
}

// Moved from utils/index.ts since it's only used here
function extractFunctionModules(functionOutput: string): string {
  if (!functionOutput) return '';

  // Remove example content
  let content = functionOutput.replace(/\*\*示例展示[：:]\*\*[\s\S]*?(?=\n\n|$)/g, '');

  // Remove end markers
  const endMarkers = ['UI要求：', 'UI 要求：', '权限说明：', '数据采集逻辑：', '任务执行完'];

  for (const marker of endMarkers) {
    const markerIndex = content.indexOf(marker);
    if (markerIndex !== -1) {
      content = content.substring(0, markerIndex).trim();
      break;
    }
  }

  const lines = content.split('\n');
  const moduleStartIndexes: number[] = [];

  // Find module titles
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]?.trim() || '';
    const modulePatterns = [
      /###\s*🔹?\s*模块\s*\d+/i,
      /🔹\s*模块\s*\d+/i,
      /模块\s*\d+[：:]/i,
      /模块\s*\d+\s*[（(]/i
    ];

    const isModuleTitle = modulePatterns.some(pattern => pattern.test(line));

    if (isModuleTitle) {
      moduleStartIndexes.push(i);
    }
  }

  if (moduleStartIndexes.length === 0) {
    return content.trim();
  }

  const modules: string[] = [];

  for (let i = 0; i < moduleStartIndexes.length; i++) {
    const startLineIndex = moduleStartIndexes[i];
    const endLineIndex = i < moduleStartIndexes.length - 1 ? moduleStartIndexes[i + 1] : lines.length;

    const moduleLines = lines.slice(startLineIndex, endLineIndex);

    const filteredLines = moduleLines.filter(line => {
      const trimmed = (line || '').trim();
      return trimmed !== '' && trimmed !== '---' && trimmed !== '###' && trimmed !== '======';
    });

    const moduleContent = filteredLines.join('\n').trim();

    if (moduleContent && moduleContent.length > 10) {
      modules.push(moduleContent);
    }
  }

  return modules.length > 0 ? modules.join('\n\n---\n\n') : content.trim();
}

const ContentViewer: React.FC<ContentViewerProps> = memo(({ response }) => {
  const [showFullContent, setShowFullContent] = useState(false);
  
  // 从环境变量读取配置
  const showFinalVersionButton = true;

  const toggleFullContent = useCallback(() => {
    setShowFullContent(prev => !prev);
  }, []);

  if (!response.role) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Toggle button - 条件渲染 */}
      {showFinalVersionButton && (
        <div className="flex justify-center">
          <Button
            onClick={toggleFullContent}
            variant="success"
            size="sm"
            className="glass-hover"
            icon={
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            }
          >
            {showFullContent ? '收起完整版' : '最终版本'}
          </Button>
        </div>
      )}

      {showFullContent ? (
        /* Full Content View */
        <div className="space-y-8 animate-fade-in">
          <div className="glass-tertiary border border-green-400/30 rounded-2xl p-6">
            <h4 className="text-green-400 font-bold mb-3 flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse-gentle"></div>
              <span>📋 最终版本 - 完整解析内容</span>
            </h4>
            <p className="text-glass-secondary text-sm leading-relaxed">以下是包含所有字段的完整提示词文档</p>
          </div>

          {/* Role */}
          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full"></div>
              <span>角色</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <p className="text-glass-primary leading-relaxed font-medium">
                {response.role}
              </p>
            </div>
          </section>

          {/* Goal */}
          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full"></div>
              <span>目标</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <p className="text-glass-primary leading-relaxed font-medium">
                {response.goal}
              </p>
            </div>
          </section>

          {/* Function Output */}
          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-pink-400 to-cyan-400 rounded-full"></div>
              <span>功能输出</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <pre className="text-glass-primary text-sm whitespace-pre-wrap overflow-x-auto font-mono leading-relaxed">
                {response.function_output}
              </pre>
            </div>
          </section>

          {/* UI Requirements */}
          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full"></div>
              <span>UI 要求</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <p className="text-glass-primary leading-relaxed font-medium">
                {response.ui_requirements}
              </p>
            </div>
          </section>

          {/* Theme Type */}
          <div className="glass-tertiary border border-blue-400/30 rounded-2xl p-6">
            <h4 className="text-blue-400 font-bold mb-3 flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse-gentle"></div>
              <span>检测到的主题类型</span>
            </h4>
            <div className="flex items-center space-x-3">
              <span className="text-glass-primary font-semibold text-lg">{response.theme_type}</span>
              {response.theme_type !== 'default' && (
                <span className="glass-secondary px-3 py-1 rounded-full text-xs font-medium text-blue-400 border border-blue-400/30">
                  已应用专用技术要求
                </span>
              )}
            </div>
          </div>

          {/* Fixed Content Appender */}
          <FixedContentAppender 
            baseContent={{
              role: response.role,
              goal: response.goal,
              function_output: response.function_output,
              ui_requirements: response.ui_requirements,
              fixed_content: response.fixed_content,
              theme_type: response.theme_type
            }}
          />
        </div>
      ) : showFinalVersionButton ? (
        /* Simplified Function Modules View - 当按钮可见时 */
        <div className="space-y-6 animate-fade-in">
          <div className="glass-tertiary border border-blue-400/30 rounded-2xl p-6">
            <h4 className="text-blue-400 font-bold mb-3 flex items-center space-x-2">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse-gentle"></div>
              <span>🔍 功能模块预览</span>
            </h4>
            <p className="text-glass-secondary text-sm leading-relaxed">仅显示核心功能模块，点击&quot;最终版本&quot;查看完整内容</p>
          </div>

          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full"></div>
              <span>📱 功能模块</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <pre className="text-glass-primary text-sm whitespace-pre-wrap font-mono leading-relaxed">
                {extractFunctionModules(response.function_output)}
              </pre>
            </div>
          </section>
          
          <div className="text-center py-6 glass-tertiary rounded-2xl">
            <p className="text-glass-secondary text-sm mb-4">👆 这里只显示核心功能模块</p>
            <button
              onClick={toggleFullContent}
              className="glass-button px-6 py-3 rounded-xl font-semibold text-glass-primary hover:text-white transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-400/50 focus:ring-offset-2 focus:ring-offset-transparent group"
            >
              <span className="flex items-center space-x-2">
                <span>点击&quot;最终版本&quot;查看角色、目标、UI要求等完整内容</span>
                <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </span>
            </button>
          </div>
        </div>
      ) : (
        /* Function Output Only View - 当按钮隐藏时只显示功能输出 */
        <div className="space-y-6 animate-fade-in">
          <div className="glass-tertiary border border-green-400/30 rounded-2xl p-6">
            <h4 className="text-green-400 font-bold mb-3 flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse-gentle"></div>
              <span>📱 功能输出</span>
            </h4>
            <p className="text-glass-secondary text-sm leading-relaxed">显示核心功能模块内容</p>
          </div>

          <section className="glass-tertiary rounded-2xl p-6 hover:glass-secondary transition-all duration-300">
            <h3 className="text-xl font-bold text-glass-primary mb-4 flex items-center space-x-3">
              <div className="w-3 h-3 bg-gradient-to-r from-pink-400 to-cyan-400 rounded-full"></div>
              <span>功能输出</span>
            </h3>
            <div className="glass-secondary rounded-xl p-5">
              <pre className="text-glass-primary text-sm whitespace-pre-wrap overflow-x-auto font-mono leading-relaxed">
                {response.function_output}
              </pre>
            </div>
          </section>
        </div>
      )}
    </div>
  );
});

ContentViewer.displayName = 'ContentViewer';

export default ContentViewer;