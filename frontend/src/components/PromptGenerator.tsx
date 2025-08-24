'use client'

import React, { useState } from 'react'
import { PromptRequest, PromptResponse, ProgressData, TabDocument } from '../types'
import { FixedContentAppender } from './FixedContentAppender'
import { ProgressVisualization } from './ProgressVisualization'

interface ThemeOption {
  id: string
  name: string
  description: string
  icon: string
}

const BUILT_IN_THEMES: ThemeOption[] = [
  {
    id: 'wifi_creative_checkin',
    name: 'WiFi创意签到',
    description: '无需WiFi实际功能、创意、结合签到功能',
    icon: '🌟'
  },
  {
    id: 'wifi_real_scanning',
    name: 'WiFi真实扫描',
    description: '需要有WiFi实际功能、创意、不需要有签到功能',
    icon: '📡'
  },
  {
    id: 'clean_creative_ball',
    name: '清理创意球',
    description: '清理、不需要真实的清理功能、创意',
    icon: '🧹'
  },
  {
    id: 'clean_creative_dream',
    name: '清理梦境室',
    description: '清理、不需要真实的清理功能、创意',
    icon: '🌙'
  },
  {
    id: 'magnify_emotion',
    name: '放大情绪镜',
    description: '放大、无放大功能、创意',
    icon: '🔍'
  },
  {
    id: 'magnify_memory',
    name: '放大回忆器',
    description: '放大、无放大功能、创意',
    icon: '💭'
  },
  {
    id: 'traffic_real_monitor',
    name: '流量真实监控',
    description: '流量、需要真实流量数据、创意可视化',
    icon: '📊'
  },
  {
    id: 'traffic_creative_planet',
    name: '流量星球馆',
    description: '流量、不需要真实流量功能、创意星球主题',
    icon: '🌌'
  }
]

const PromptGenerator: React.FC = () => {
  const [formData, setFormData] = useState<PromptRequest>({
    app_name: '',
    theme: '',
    variant_folder: '',
    ui_color: '蓝色科技感',
    reference_file: '',
    tab_count: 3
  })

  const [response, setResponse] = useState<PromptResponse | null>(null)
  const [tabDocuments, setTabDocuments] = useState<TabDocument[]>([])
  const [activeTabId, setActiveTabId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showProgress, setShowProgress] = useState(false)
  const [progressData, setProgressData] = useState<ProgressData>({
    progress: 0,
    status: '准备开始...',
    step: '初始化'
  })
  const [currentGeneratingIndex, setCurrentGeneratingIndex] = useState(0)
  const [totalToGenerate, setTotalToGenerate] = useState(0)
  const [showFullContent, setShowFullContent] = useState<{[tabId: string]: boolean}>({})
  const [activeFullViewTab, setActiveFullViewTab] = useState<string | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleThemeSelect = (theme: ThemeOption) => {
    setFormData(prev => ({ ...prev, theme: theme.description }))
  }

  const generateSingleDocument = async (documentIndex: number, total: number = 1, isRegeneration: boolean = false): Promise<PromptResponse> => {
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    
    return new Promise(async (resolve, reject) => {
      try {
        const res = await fetch(`${apiBaseUrl}/generate-prompt-stream`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        })

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }

        const reader = res.body?.getReader()
        if (!reader) {
          throw new Error('无法读取响应流')
        }

        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
          const { done, value } = await reader.read()
          
          if (done) break
          
          buffer += decoder.decode(value, { stream: true })
          
          // 处理服务器发送的事件
          const lines = buffer.split('\n')
          buffer = lines.pop() || '' // 保留未完成的行
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6))
                
                if (data.error) {
                  throw new Error(data.error)
                }
                
                // 修复进度计算逻辑
                let totalProgress: number
                let statusMessage: string
                
                if (isRegeneration) {
                  // 重新生成时显示单独进度
                  totalProgress = data.progress || 0
                  statusMessage = `重新生成: ${data.status || ''}`
                } else {
                  // 批量生成时计算总体进度
                  if (total <= 0) total = 1 // 防止除以0
                  const baseProgress = (documentIndex / total) * 100
                  const docProgressPortion = (data.progress || 0) / total
                  totalProgress = baseProgress + docProgressPortion
                  statusMessage = `文档 ${documentIndex + 1}/${total}: ${data.status || ''}`
                }
                
                // 确保进度值在有效范围内
                totalProgress = Math.max(0, Math.min(100, totalProgress))
                
                setProgressData({
                  progress: isNaN(totalProgress) ? 0 : totalProgress,
                  status: statusMessage,
                  step: data.step || ''
                })
                
                // 如果收到最终结果
                if (data.result) {
                  resolve(data.result)
                  return
                }
              } catch (parseError) {
                console.warn('解析SSE数据失败:', parseError)
              }
            }
          }
        }
      } catch (err) {
        reject(err)
      }
    })
  }

  const handleBatchGeneration = async () => {
    const tabCount = formData.tab_count || 1
    
    setShowProgress(true)
    setIsLoading(true)
    setError(null)
    setResponse(null)
    setTabDocuments([])
    setCurrentGeneratingIndex(0)
    setTotalToGenerate(tabCount)
    
    // 初始化标签页
    const initialTabs: TabDocument[] = Array.from({ length: tabCount }, (_, index) => ({
      id: `tab-${Date.now()}-${index}`,
      title: `页面 ${index + 1}`,
      response: {} as PromptResponse,
      isLoading: true
    }))
    
    setTabDocuments(initialTabs)
    setActiveTabId(initialTabs[0]?.id || null)
    
    try {
      // 逐个生成文档
      for (let i = 0; i < tabCount; i++) {
        setCurrentGeneratingIndex(i)
        
        const result = await generateSingleDocument(i, tabCount, false)
        
        // 更新对应标签页的结果
        setTabDocuments(prev => 
          prev.map(tab => 
            tab.id === initialTabs[i].id 
              ? { ...tab, response: result, isLoading: false }
              : tab
          )
        )
      }
      
      // 所有文档生成完成
      setProgressData({
        progress: 100,
        status: `成功生成 ${tabCount} 个版本的提示词文档`,
        step: '完成'
      })
      
      setTimeout(() => {
        setShowProgress(false)
      }, 1500)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : '批量生成失败')
      setShowProgress(false)
      
      // 标记失败的文档
      setTabDocuments(prev => 
        prev.map(tab => 
          tab.isLoading ? { ...tab, isLoading: false } : tab
        )
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await handleBatchGeneration()
  }

  const extractFunctionModules = (functionOutput: string): string => {
    if (!functionOutput) return ''
    
    console.log('=== 开始提取功能模块（防止错误分割）===')
    console.log('原始功能输出长度:', functionOutput.length)
    
    // 第一步：移除示例展示内容
    let content = functionOutput.replace(/\*\*示例展示[：:]\*\*[\s\S]*?(?=\n\n|$)/g, '')
    console.log('移除示例展示后长度:', content.length)
    
    // 第二步：移除明确的结束内容（UI要求、权限等）
    const endMarkers = [
      'UI要求：',
      'UI 要求：', 
      '权限说明：',
      '数据采集逻辑：',
      '任务执行完'
    ]
    
    for (const marker of endMarkers) {
      const markerIndex = content.indexOf(marker)
      if (markerIndex !== -1) {
        content = content.substring(0, markerIndex).trim()
        console.log(`在位置 ${markerIndex} 截断内容，因为发现: ${marker}`)
        break
      }
    }
    
    // 第三步：使用灵活的模块识别，确保找到所有模块
    const lines = content.split('\n')
    const moduleStartIndexes = []
    
    // 识别模块标题的多种格式
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim()
      const modulePatterns = [
        /###\s*🔹?\s*模块\s*\d+/i,  // ### 🔹 模块 1
        /🔹\s*模块\s*\d+/i,        // 🔹 模块 1
        /模块\s*\d+[：:]/i,        // 模块 1：
        /模块\s*\d+\s*[（(]/i      // 模块 1（
      ]
      
      let isModuleTitle = false
      for (const pattern of modulePatterns) {
        if (pattern.test(line)) {
          isModuleTitle = true
          break
        }
      }
      
      if (isModuleTitle) {
        moduleStartIndexes.push(i)
        console.log(`找到模块标题在第 ${i} 行: ${line}`)
      }
    }
    
    console.log(`找到 ${moduleStartIndexes.length} 个真正的模块标题`)
    
    if (moduleStartIndexes.length === 0) {
      // 如果没有找到标准模块标题，尝试更宽松的匹配
      console.log('没有找到标准模块标题，尝试宽松匹配')
      for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim()
        if (line.includes('模块') && /\d+/.test(line)) {
          moduleStartIndexes.push(i)
          console.log(`宽松匹配找到模块在第 ${i} 行: ${line}`)
        }
      }
    }
    
    if (moduleStartIndexes.length === 0) {
      // 最后兜底：返回清理过的全部内容
      console.log('仍然没有找到模块标题，返回全部清理后的内容')
      return content.trim()
    }
    
    // 第四步：提取每个模块的完整内容（不进行任何内部分割）
    const modules = []
    
    for (let i = 0; i < moduleStartIndexes.length; i++) {
      const startLineIndex = moduleStartIndexes[i]
      const endLineIndex = i < moduleStartIndexes.length - 1 ? moduleStartIndexes[i + 1] : lines.length
      
      // 提取从模块标题到下一个模块标题的所有内容
      const moduleLines = lines.slice(startLineIndex, endLineIndex)
      
      // 保守的过滤：只移除明确的分隔符，保留所有实际内容
      const filteredLines = moduleLines.filter(line => {
        const trimmed = line.trim()
        // 只移除完全空行和单独的分隔符行
        return trimmed !== '' && trimmed !== '---' && trimmed !== '###' && trimmed !== '======'
      })
      
      const moduleContent = filteredLines.join('\n').trim()
      
      console.log(`模块 ${i + 1} 内容长度: ${moduleContent.length}`)
      console.log(`模块 ${i + 1} 开头: ${moduleContent.substring(0, 80).replace(/\n/g, '\\n')}...`)
      
      if (moduleContent && moduleContent.length > 10) {
        modules.push(moduleContent)
        
        // 特别输出模块2的完整内容用于调试
        if (i === 1) {
          console.log('=== 模块2完整内容 ===')
          console.log(moduleContent.substring(0, 200))
        }
      }
    }
    
    if (modules.length > 0) {
      const result = modules.join('\n\n---\n\n')
      console.log(`=== 成功提取 ${modules.length} 个完整模块，总长度: ${result.length} ===`)
      
      // 确保不会有内容被意外分离
      console.log('检查是否有内容被意外分离...')
      const resultLines = result.split('\n')
      const separateContentLines = resultLines.filter(line => {
        const trimmed = line.trim()
        return trimmed.includes('联动') || trimmed.includes('长期') || trimmed.includes('价值') || trimmed.includes('粘性')
      })
      console.log(`发现潜在分离内容行数: ${separateContentLines.length}`)
      
      return result
    }
    
    // 最终fallback
    console.log('使用最终fallback')
    return content.trim() || functionOutput.substring(0, 1000) + '...'
  }

  const toggleFullContent = (tabId: string) => {
    if (showFullContent[tabId]) {
      // 如果当前是展开状态，收起
      setShowFullContent(prev => ({ ...prev, [tabId]: false }))
      setActiveFullViewTab(null)
    } else {
      // 展开完整内容
      setShowFullContent(prev => ({ ...prev, [tabId]: true }))
      setActiveFullViewTab(tabId)
    }
  }

  const regenerateTab = async (tabId: string) => {
    // 显示进度窗口
    setShowProgress(true)
    setError(null)
    
    // 设置该标签页为加载状态
    setTabDocuments(prev => 
      prev.map(tab => 
        tab.id === tabId ? { ...tab, isLoading: true } : tab
      )
    )
    
    try {
      const result = await generateSingleDocument(0, 1, true) // 重新生成单个文档，标记为重新生成
      
      // 更新标签页结果
      setTabDocuments(prev => 
        prev.map(tab => 
          tab.id === tabId 
            ? { ...tab, response: result, isLoading: false }
            : tab
        )
      )
      
      // 显示完成状态
      setProgressData({
        progress: 100,
        status: '重新生成完成！',
        step: '完成'
      })
      
      setTimeout(() => {
        setShowProgress(false)
      }, 1000)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : '重新生成失败')
      setShowProgress(false)
      
      // 取消加载状态
      setTabDocuments(prev => 
        prev.map(tab => 
          tab.id === tabId ? { ...tab, isLoading: false } : tab
        )
      )
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* 进度可视化组件 */}
      <ProgressVisualization 
        isVisible={showProgress}
        progressData={progressData}
        onComplete={(result) => {
          setResponse(result)
          setShowProgress(false)
        }}
        onError={(error) => {
          setError(error)
          setShowProgress(false)
        }}
      />
      {/* 输入表单 */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6">输入参数</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              APP 名称
            </label>
            <input
              type="text"
              name="app_name"
              value={formData.app_name}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：免费流量直达"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              主题
            </label>
            
            {/* 内置主题按钮 */}
            <div className="mb-4">
              <p className="text-xs text-gray-500 mb-3">选择内置主题：</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
                {BUILT_IN_THEMES.map((theme) => (
                  <button
                    key={theme.id}
                    type="button"
                    onClick={() => handleThemeSelect(theme)}
                    className="flex flex-col items-center p-3 border-2 border-gray-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all duration-200 group"
                    title={theme.description}
                  >
                    <span className="text-2xl mb-1 group-hover:scale-110 transition-transform">
                      {theme.icon}
                    </span>
                    <span className="text-xs font-medium text-gray-700 group-hover:text-blue-600 text-center">
                      {theme.name}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            <textarea
              name="theme"
              value={formData.theme}
              onChange={handleInputChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：流量星球馆，通过读取真实流量数据，映射为星球能量值"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              变体文件夹
            </label>
            <input
              type="text"
              name="variant_folder"
              value={formData.variant_folder}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：variant_traffic137630"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              UI主色调
            </label>
            <input
              type="text"
              name="ui_color"
              value={formData.ui_color}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：蓝色科技感、绿色清新、紫色梦幻"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              参考文件 <span className="text-gray-500 text-xs">(可选)</span>
            </label>
            <input
              type="text"
              name="reference_file"
              value={formData.reference_file || ''}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="例如：HomeFragment（自动添加@前缀和.kt后缀）"
            />
            <p className="text-xs text-gray-500 mt-1">
              输入文件名（如"HomeFragment"），系统会自动格式化为"@HomeFragment.kt"
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              生成Tab数量
            </label>
            <input
              type="number"
              name="tab_count"
              value={formData.tab_count || 3}
              onChange={(e) => setFormData(prev => ({ ...prev, tab_count: Math.max(1, Math.min(10, parseInt(e.target.value) || 3)) }))}
              min="1"
              max="10"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="3"
            />
            <p className="text-xs text-gray-500 mt-1">
              一次生成多个不同版本的提示词文档（1-10个）
            </p>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? '生成中...' : '生成提示词'}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-600">{error}</p>
          </div>
        )}
      </div>

      {/* 多标签页生成结果 */}
      {tabDocuments.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="border-b border-gray-200">
            <h2 className="text-2xl font-semibold text-gray-800 p-6 pb-4">生成结果</h2>
            
            {/* 标签页导航 */}
            <div className="flex overflow-x-auto">
              {tabDocuments.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTabId(tab.id)}
                  className={`flex-shrink-0 px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                    activeTabId === tab.id
                      ? 'border-blue-500 text-blue-600 bg-blue-50'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <span>{tab.title}</span>
                    {tab.isLoading && (
                      <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* 标签页内容 */}
          {tabDocuments.map((tab) => (
            <div
              key={tab.id}
              className={`p-6 ${activeTabId === tab.id ? 'block' : 'hidden'}`}
            >
              {tab.isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">正在生成 {tab.title}...</p>
                  </div>
                </div>
              ) : tab.response.role ? (
                <div className="space-y-6">
                  {/* 操作按钮区域 */}
                  <div className="flex justify-between items-center mb-4">
                    <button
                      onClick={() => toggleFullContent(tab.id)}
                      className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-green-600 bg-green-50 border border-green-200 rounded-md hover:bg-green-100 transition-colors"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <span>{showFullContent[tab.id] ? '收起完整版' : '最终版本'}</span>
                    </button>
                    
                    <button
                      onClick={() => regenerateTab(tab.id)}
                      disabled={tab.isLoading}
                      className="flex items-center space-x-2 px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors disabled:opacity-50"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      <span>重新生成</span>
                    </button>
                  </div>

                  {showFullContent[tab.id] ? (
                    /* 完整内容视图 */
                    <div className="space-y-6">
                      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                        <h4 className="text-green-800 font-medium mb-2">📋 最终版本 - 完整解析内容</h4>
                        <p className="text-green-700 text-sm">以下是包含所有字段的完整提示词文档</p>
                      </div>

                      <div>
                        <h3 className="text-lg font-medium text-gray-800 mb-2">角色：</h3>
                        <p className="text-gray-700 leading-relaxed">{tab.response.role}</p>
                      </div>

                      <div>
                        <h3 className="text-lg font-medium text-gray-800 mb-2">目标：</h3>
                        <p className="text-gray-700 leading-relaxed">{tab.response.goal}</p>
                      </div>

                      <div>
                        <h3 className="text-lg font-medium text-gray-800 mb-2">功能输出：</h3>
                        <pre className="bg-gray-50 p-4 rounded-md text-sm text-gray-700 whitespace-pre-wrap">
                          {tab.response.function_output}
                        </pre>
                      </div>

                      <div>
                        <h3 className="text-lg font-medium text-gray-800 mb-2">UI 要求：</h3>
                        <p className="text-gray-700 leading-relaxed">{tab.response.ui_requirements}</p>
                      </div>

                      {/* 主题类型显示 */}
                      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
                        <h4 className="text-sm font-medium text-blue-800 mb-2">检测到的主题类型</h4>
                        <p className="text-blue-700 text-sm">
                          <span className="font-semibold">{tab.response.theme_type}</span> 
                          {tab.response.theme_type !== 'default' && (
                            <span className="ml-2 text-xs bg-blue-100 px-2 py-1 rounded">已应用专用技术要求</span>
                          )}
                        </p>
                      </div>

                      {/* 固定内容拼接组件 */}
                      <FixedContentAppender 
                        baseContent={{
                          role: tab.response.role,
                          goal: tab.response.goal,
                          function_output: tab.response.function_output,
                          ui_requirements: tab.response.ui_requirements,
                          fixed_content: tab.response.fixed_content,
                          theme_type: tab.response.theme_type
                        }}
                      />
                    </div>
                  ) : (
                    /* 简化的功能模块视图 */
                    <div className="space-y-4">
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                        <h4 className="text-blue-800 font-medium mb-2">🔍 功能模块预览</h4>
                        <p className="text-blue-700 text-sm">仅显示核心功能模块，点击"最终版本"查看完整内容</p>
                      </div>

                      <div>
                        <h3 className="text-lg font-medium text-gray-800 mb-3">📱 功能模块：</h3>
                        <div className="bg-gray-50 p-4 rounded-md">
                          <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                            {extractFunctionModules(tab.response.function_output)}
                          </pre>
                        </div>
                      </div>
                      
                      <div className="text-center py-4 border-t border-gray-200">
                        <p className="text-gray-500 text-sm mb-2">👆 这里只显示核心功能模块</p>
                        <button
                          onClick={() => toggleFullContent(tab.id)}
                          className="text-green-600 hover:text-green-700 font-medium text-sm underline"
                        >
                          点击"最终版本"查看角色、目标、UI要求等完整内容 →
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <p>生成失败，请尝试重新生成</p>
                  <button
                    onClick={() => regenerateTab(tab.id)}
                    className="mt-4 px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
                  >
                    重试
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* 保留单个结果显示以支持向后兼容 */}
      {response && tabDocuments.length === 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">生成结果</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">角色：</h3>
              <p className="text-gray-700 leading-relaxed">{response.role}</p>
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">目标：</h3>
              <p className="text-gray-700 leading-relaxed">{response.goal}</p>
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">功能输出：</h3>
              <pre className="bg-gray-50 p-4 rounded-md text-sm text-gray-700 whitespace-pre-wrap">
                {response.function_output}
              </pre>
            </div>

            <div>
              <h3 className="text-lg font-medium text-gray-800 mb-2">UI 要求：</h3>
              <p className="text-gray-700 leading-relaxed">{response.ui_requirements}</p>
            </div>
          </div>

          {/* 主题类型显示 */}
          <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <h4 className="text-sm font-medium text-blue-800 mb-2">检测到的主题类型</h4>
            <p className="text-blue-700 text-sm">
              <span className="font-semibold">{response.theme_type}</span> 
              {response.theme_type !== 'default' && (
                <span className="ml-2 text-xs bg-blue-100 px-2 py-1 rounded">已应用专用技术要求</span>
              )}
            </p>
          </div>

          {/* 固定内容拼接组件 */}
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
      )}
    </div>
  )
}

export default PromptGenerator