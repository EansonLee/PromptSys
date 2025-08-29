'use client'

import React, { useState, useEffect } from 'react'
import { BaseContent } from '../types'

interface Props {
  baseContent: BaseContent
}

export const FixedContentAppender: React.FC<Props> = ({ baseContent }) => {
  const [finalContent, setFinalContent] = useState<string>('')
  const [showFinal, setShowFinal] = useState(false)
  const [showEditor, setShowEditor] = useState(false)
  const [customFixedContent, setCustomFixedContent] = useState<string>(baseContent.fixed_content || '')

  // 当baseContent变化时更新固定内容
  useEffect(() => {
    setCustomFixedContent(baseContent.fixed_content || '')
  }, [baseContent.fixed_content])

  const generateFinalContent = () => {
    const content = `角色：
${baseContent.role}

目标：
${baseContent.goal}

功能输出：
${baseContent.function_output}

UI 要求：
${baseContent.ui_requirements}

${customFixedContent}`

    setFinalContent(content)
    setShowFinal(true)
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(finalContent)
    alert('内容已复制到剪贴板')
  }

  return (
    <div className="mt-8 border-t pt-6">
      <div className="mb-4">
        <h3 className="text-lg font-medium text-gray-800 mb-2">主题专用固定内容</h3>
        <p className="text-sm text-gray-600 mb-4">
          系统已根据主题类型 <span className="font-semibold text-blue-600">{baseContent.theme_type}</span> 自动选择了相应的技术要求和参考文档
        </p>
      </div>
      
      <div className="flex gap-4 mb-4">
        <button
          onClick={() => setShowEditor(!showEditor)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          {showEditor ? '隐藏' : '查看/编辑'}固定内容
        </button>
        
        <button
          onClick={generateFinalContent}
          className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
        >
          生成最终模板
        </button>
        
        {showFinal && (
          <button
            onClick={copyToClipboard}
            className="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 transition-colors"
          >
            复制到剪贴板
          </button>
        )}
      </div>

      {showEditor && (
        <div className="bg-gray-50 border rounded-lg p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-medium text-gray-800">
              主题专用固定内容 ({baseContent.theme_type})
            </h3>
            <div className="text-sm text-gray-500">
              {baseContent.theme_type !== 'default' ? '已应用主题专用要求' : '使用通用要求'}
            </div>
          </div>
          <textarea
            value={customFixedContent}
            onChange={(e) => setCustomFixedContent(e.target.value)}
            className="w-full h-64 p-4 border rounded-md text-sm font-mono"
            placeholder="请输入固定内容..."
          />
          <p className="text-sm text-gray-600 mt-2">
            系统已根据主题 &quot;<strong>{baseContent.theme_type}</strong>&quot; 自动选择了相应的技术要求。
            这部分内容将在&quot;功能输出&quot;后、&quot;UI要求&quot;前插入到最终模板中。
          </p>
        </div>
      )}

      {showFinal && (
        <div className="bg-gray-50 border rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-800 mb-4">最终模板（包含固定内容）</h3>
          <pre className="bg-white p-4 rounded border text-sm text-gray-700 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {finalContent}
          </pre>
        </div>
      )}
    </div>
  )
}