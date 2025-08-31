'use client'

import React, { useEffect, useState, memo } from 'react';
import type { ProgressData, ProgressStep } from '@/types';

interface ProgressVisualizationProps {
  isVisible: boolean;
  progressData?: ProgressData;
  onComplete?: (result: unknown) => void;
  onError?: (error: string) => void;
}

const ProgressVisualization: React.FC<ProgressVisualizationProps> = memo(({
  isVisible,
  progressData: externalProgressData,
  onComplete
}) => {
  const [internalProgressData] = useState<ProgressData>({
    progress: 0,
    status: '准备开始...',
    step: '初始化'
  })

  // 使用外部传入的 progressData 或内部状态
  const progressData = externalProgressData || internalProgressData

  const [animatedProgress, setAnimatedProgress] = useState(0)
  
  // 当进度达到100%时触发完成回调
  useEffect(() => {
    if (progressData.progress >= 100 && progressData.step === '完成' && onComplete) {
      const timer = setTimeout(() => {
        onComplete(null);
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [progressData.progress, progressData.step, onComplete])
  
  // 动画效果：让进度条平滑过渡
  useEffect(() => {
    const timer = setInterval(() => {
      setAnimatedProgress(prev => {
        const diff = progressData.progress - prev
        if (Math.abs(diff) < 1) {
          return progressData.progress
        }
        return prev + diff * 0.1
      })
    }, 50)
    
    return () => clearInterval(timer)
  }, [progressData.progress])

  const getStepColor = (step: ProgressStep) => {
    switch (step) {
      case '参数验证':
        return 'bg-gradient-to-r from-blue-400 to-blue-500'
      case 'GPT连接':
        return 'bg-gradient-to-r from-green-400 to-green-500'
      case 'GPT处理':
        return 'bg-gradient-to-r from-purple-400 to-purple-500'
      case '内容解析':
        return 'bg-gradient-to-r from-orange-400 to-orange-500'
      case '结果封装':
        return 'bg-gradient-to-r from-cyan-400 to-cyan-500'
      case '完成':
        return 'bg-gradient-to-r from-emerald-400 to-emerald-500'
      default:
        return 'bg-gradient-to-r from-blue-400 to-blue-500'
    }
  }

  const getProgressRingColor = () => {
    if (progressData.progress >= 100) return 'text-emerald-400'
    if (progressData.progress >= 80) return 'text-cyan-400'
    if (progressData.progress >= 60) return 'text-orange-400'
    if (progressData.progress >= 40) return 'text-purple-400'
    if (progressData.progress >= 20) return 'text-green-400'
    return 'text-blue-400'
  }

  if (!isVisible) {
    return null
  }

  return (
    <div className="fixed inset-0 progress-modal flex items-center justify-center z-50 animate-fade-in">
      <div className="progress-modal-glass rounded-3xl p-10 max-w-lg w-full mx-4 animate-scale-in">
        {/* 标题 */}
        <div className="text-center mb-10">
          <h3 className="text-3xl font-bold progress-modal-text mb-4 flex items-center justify-center space-x-3">
            <div className="w-4 h-4 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse-glow"></div>
            <span>正在生成提示词</span>
          </h3>
          <p className="progress-modal-text-secondary text-lg">请稍等，AI正在为您创建精彩内容...</p>
        </div>

        {/* 圆形进度环 */}
        <div className="flex justify-center mb-8">
          <div className="relative w-40 h-40">
            {/* 背景环 */}
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="rgba(255, 255, 255, 0.1)"
                strokeWidth="4"
              />
              {/* 进度环 */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="url(#progressGradient)"
                strokeWidth="4"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 45}`}
                strokeDashoffset={`${2 * Math.PI * 45 * (1 - animatedProgress / 100)}`}
                className="transition-all duration-500 filter drop-shadow-lg"
              />
              {/* SVG Gradient Definition */}
              <defs>
                <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#60a5fa" />
                  <stop offset="50%" stopColor="#a855f7" />
                  <stop offset="100%" stopColor="#ec4899" />
                </linearGradient>
              </defs>
            </svg>
            
            {/* 中央百分比显示 */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <span className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  {Math.round(animatedProgress)}%
                </span>
                <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mx-auto mt-2 animate-pulse-glow"></div>
              </div>
            </div>
            
            {/* Rotating glow effect */}
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-400/20 via-purple-400/20 to-pink-400/20 blur-xl animate-spin opacity-50" style={{ animationDuration: '3s' }}></div>
          </div>
        </div>

        {/* 进度条 */}
        <div className="mb-8">
          <div className="bg-white/10 rounded-full h-4 overflow-hidden border border-white/20">
            <div
              className={`h-full transition-all duration-500 ease-out ${getStepColor(progressData.step)} relative overflow-hidden`}
              style={{ width: `${animatedProgress}%` }}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
            </div>
          </div>
        </div>

        {/* 状态信息 */}
        <div className="text-center space-y-4 mb-8">
          <div className="flex items-center justify-center space-x-3">
            <div className={`w-4 h-4 rounded-full animate-pulse-glow ${getStepColor(progressData.step).replace('bg-gradient-to-r', 'bg-gradient-to-br')}`}></div>
            <span className="text-lg font-bold progress-modal-text">{progressData.step}</span>
          </div>
          <p className="progress-modal-text-secondary font-medium text-lg">{progressData.status}</p>
        </div>

        {/* 步骤指示器 */}
        <div className="bg-white/10 rounded-2xl p-4 backdrop-blur-sm">
          <div className="flex justify-between items-center text-sm">
            <div className={`flex flex-col items-center transition-all duration-300 ${progressData.progress >= 10 ? 'text-blue-400' : 'progress-modal-text-secondary'}`}>
              <div className={`w-3 h-3 rounded-full mb-2 transition-all duration-300 ${progressData.progress >= 10 ? 'bg-blue-400 animate-pulse-glow' : 'bg-white/20'}`}></div>
              <span className="font-medium">验证</span>
            </div>
            
            <div className="flex-1 h-1 bg-white/20 rounded-full mx-3 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-500"
                style={{ width: progressData.progress >= 20 ? '100%' : '0%' }}
              ></div>
            </div>
            
            <div className={`flex flex-col items-center transition-all duration-300 ${progressData.progress >= 30 ? 'text-purple-400' : 'progress-modal-text-secondary'}`}>
              <div className={`w-3 h-3 rounded-full mb-2 transition-all duration-300 ${progressData.progress >= 30 ? 'bg-purple-400 animate-pulse-glow' : 'bg-white/20'}`}></div>
              <span className="font-medium">生成</span>
            </div>
            
            <div className="flex-1 h-1 bg-white/20 rounded-full mx-3 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-purple-400 to-orange-400 transition-all duration-500"
                style={{ width: progressData.progress >= 85 ? '100%' : '0%' }}
              ></div>
            </div>
            
            <div className={`flex flex-col items-center transition-all duration-300 ${progressData.progress >= 85 ? 'text-orange-400' : 'progress-modal-text-secondary'}`}>
              <div className={`w-3 h-3 rounded-full mb-2 transition-all duration-300 ${progressData.progress >= 85 ? 'bg-orange-400 animate-pulse-glow' : 'bg-white/20'}`}></div>
              <span className="font-medium">解析</span>
            </div>
            
            <div className="flex-1 h-1 bg-white/20 rounded-full mx-3 overflow-hidden">
              <div 
                className="h-full bg-gradient-to-r from-orange-400 to-emerald-400 transition-all duration-500"
                style={{ width: progressData.progress >= 100 ? '100%' : '0%' }}
              ></div>
            </div>
            
            <div className={`flex flex-col items-center transition-all duration-300 ${progressData.progress >= 100 ? 'text-emerald-400' : 'progress-modal-text-secondary'}`}>
              <div className={`w-3 h-3 rounded-full mb-2 transition-all duration-300 ${progressData.progress >= 100 ? 'bg-emerald-400 animate-pulse-glow' : 'bg-white/20'}`}></div>
              <span className="font-medium">完成</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
});

ProgressVisualization.displayName = 'ProgressVisualization';

export { ProgressVisualization }