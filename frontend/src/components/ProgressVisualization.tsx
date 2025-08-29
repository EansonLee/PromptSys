'use client'

import React, { useEffect, useState } from 'react'

interface ProgressData {
  progress: number
  status: string
  step: string
  result?: unknown
  error?: string
}

interface ProgressVisualizationProps {
  isVisible: boolean
  progressData?: ProgressData
  onComplete?: (result: unknown) => void
  onError?: (error: string) => void
}

const ProgressVisualization: React.FC<ProgressVisualizationProps> = ({
  isVisible,
  progressData: externalProgressData
}) => {
  const [internalProgressData] = useState<ProgressData>({
    progress: 0,
    status: '准备开始...',
    step: '初始化'
  })

  // 使用外部传入的 progressData 或内部状态
  const progressData = externalProgressData || internalProgressData

  const [animatedProgress, setAnimatedProgress] = useState(0)
  
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

  const getStepColor = (step: string) => {
    switch (step) {
      case '参数验证':
        return 'bg-blue-500'
      case 'GPT连接':
        return 'bg-green-500'
      case 'GPT处理':
        return 'bg-purple-500'
      case '内容解析':
        return 'bg-orange-500'
      case '结果封装':
        return 'bg-cyan-500'
      case '完成':
        return 'bg-emerald-500'
      default:
        return 'bg-blue-500'
    }
  }

  const getProgressRingColor = () => {
    if (progressData.progress >= 100) return 'text-emerald-500'
    if (progressData.progress >= 80) return 'text-cyan-500'
    if (progressData.progress >= 60) return 'text-orange-500'
    if (progressData.progress >= 40) return 'text-purple-500'
    if (progressData.progress >= 20) return 'text-green-500'
    return 'text-blue-500'
  }

  if (!isVisible) {
    return null
  }

  return (
    <div className="fixed inset-0 backdrop-blur-sm bg-white/30 flex items-center justify-center z-50">
      <div className="bg-white/95 backdrop-blur-md rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl border border-white/20">
        {/* 标题 */}
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-2">正在生成提示词</h3>
          <p className="text-gray-600">请稍等，这可能需要几秒钟...</p>
        </div>

        {/* 圆形进度环 */}
        <div className="flex justify-center mb-6">
          <div className="relative w-32 h-32">
            {/* 背景环 */}
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="6"
              />
              {/* 进度环 */}
              <circle
                cx="50"
                cy="50"
                r="45"
                fill="none"
                stroke="currentColor"
                strokeWidth="6"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 45}`}
                strokeDashoffset={`${2 * Math.PI * 45 * (1 - animatedProgress / 100)}`}
                className={`transition-all duration-500 ${getProgressRingColor()}`}
              />
            </svg>
            {/* 中央百分比显示 */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className={`text-2xl font-bold ${getProgressRingColor()}`}>
                {Math.round(animatedProgress)}%
              </span>
            </div>
          </div>
        </div>

        {/* 进度条 */}
        <div className="mb-6">
          <div className="bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className={`h-full transition-all duration-500 ease-out ${getStepColor(progressData.step)}`}
              style={{ width: `${animatedProgress}%` }}
            >
              <div className="h-full bg-white opacity-30 animate-pulse"></div>
            </div>
          </div>
        </div>

        {/* 状态信息 */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center space-x-2">
            <div className={`w-3 h-3 rounded-full animate-pulse ${getStepColor(progressData.step)}`}></div>
            <span className="text-sm font-medium text-gray-600">{progressData.step}</span>
          </div>
          <p className="text-gray-800 font-medium">{progressData.status}</p>
        </div>

        {/* 步骤指示器 */}
        <div className="mt-6 flex justify-between items-center text-xs">
          <div className={`flex flex-col items-center ${progressData.progress >= 10 ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${progressData.progress >= 10 ? 'bg-blue-500' : 'bg-gray-300'}`}></div>
            <span>验证</span>
          </div>
          <div className="flex-1 h-0.5 bg-gray-200 mx-2">
            <div 
              className="h-full bg-blue-500 transition-all duration-500"
              style={{ width: progressData.progress >= 20 ? '100%' : '0%' }}
            ></div>
          </div>
          <div className={`flex flex-col items-center ${progressData.progress >= 30 ? 'text-purple-600' : 'text-gray-400'}`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${progressData.progress >= 30 ? 'bg-purple-500' : 'bg-gray-300'}`}></div>
            <span>生成</span>
          </div>
          <div className="flex-1 h-0.5 bg-gray-200 mx-2">
            <div 
              className="h-full bg-purple-500 transition-all duration-500"
              style={{ width: progressData.progress >= 85 ? '100%' : '0%' }}
            ></div>
          </div>
          <div className={`flex flex-col items-center ${progressData.progress >= 85 ? 'text-orange-600' : 'text-gray-400'}`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${progressData.progress >= 85 ? 'bg-orange-500' : 'bg-gray-300'}`}></div>
            <span>解析</span>
          </div>
          <div className="flex-1 h-0.5 bg-gray-200 mx-2">
            <div 
              className="h-full bg-orange-500 transition-all duration-500"
              style={{ width: progressData.progress >= 100 ? '100%' : '0%' }}
            ></div>
          </div>
          <div className={`flex flex-col items-center ${progressData.progress >= 100 ? 'text-emerald-600' : 'text-gray-400'}`}>
            <div className={`w-2 h-2 rounded-full mb-1 ${progressData.progress >= 100 ? 'bg-emerald-500' : 'bg-gray-300'}`}></div>
            <span>完成</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export { ProgressVisualization }
export type { ProgressData }