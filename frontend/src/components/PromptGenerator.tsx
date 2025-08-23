'use client'

import React, { useState } from 'react'
import { PromptRequest, PromptResponse } from '../types'
import { FixedContentAppender } from './FixedContentAppender'

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
    reference_file: ''
  })

  const [response, setResponse] = useState<PromptResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleThemeSelect = (theme: ThemeOption) => {
    setFormData(prev => ({ ...prev, theme: theme.description }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      const res = await fetch(`${apiBaseUrl}/generate-prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`)
      }

      const data: PromptResponse = await res.json()
      setResponse(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : '生成失败')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-8">
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

      {/* 生成结果 */}
      {response && (
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