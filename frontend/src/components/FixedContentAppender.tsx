'use client'

import React, { useState } from 'react'
import { BaseContent } from '../types'

interface Props {
  baseContent: BaseContent
}

export const FixedContentAppender: React.FC<Props> = ({ baseContent }) => {
  const [finalContent, setFinalContent] = useState<string>('')
  const [showFinal, setShowFinal] = useState(false)
  const [showEditor, setShowEditor] = useState(false)
  const [customFixedContent, setCustomFixedContent] = useState<string>(`### 5. 数据采集逻辑：
- 使用 @/module-wifi 中的工具类，参考 中获取WiFi列表的方式来获取周围网络列表
如需要跳转Dialog参考 
- 参考 @/module-wifi  中的工具类获取WiFi、信号等信息;
- 图表使用MpChart，参考 @FreeRankFragment.kt@free_fragment_rank.xml 中图表、流量获取的用法;
- 参考 @/module_fake 中使用数据库的方法进行数据库存储，在本变体中进行编写数据库文件即可

6. 权限说明：
参考 @/variant 中其他变体以及 @PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

- 参考 @FreeRankFragment.kt 中申请应用使用权限的方法;
7. 参考 @SpeedFragment.kt 中Fragment的可见性逻辑，对 进行修改，不需要马上进行扫描，只有进入Fragment点击按钮，给了权限后才进行扫描;
8. 新建的 Fragment逻辑也跟第 7.一样;
9. 参考 @BabyAppAdapter.kt 新建"RecycleView"的"Adapter";
10. 参考 @BabyChangeDialog.kt 新建Dialog;
11. 参考 @BabyFlowChangeActivity.kt 新建Activity;
12. 参考 @StatisticsFragment.kt 中流量的获取、使用方法;
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据`)

  const generateFinalContent = () => {
    const content = `角色：
${baseContent.role}

目标：
${baseContent.goal}

功能输出：
${baseContent.function_output}

${customFixedContent}

UI 要求：
${baseContent.ui_requirements}`

    setFinalContent(content)
    setShowFinal(true)
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(finalContent)
    alert('内容已复制到剪贴板')
  }

  return (
    <div className="mt-8 border-t pt-6">
      <div className="flex gap-4 mb-4">
        <button
          onClick={() => setShowEditor(!showEditor)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
        >
          {showEditor ? '隐藏' : '编辑'}固定内容
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
          <h3 className="text-lg font-medium text-gray-800 mb-4">编辑固定内容（第5-13条技术要求）</h3>
          <textarea
            value={customFixedContent}
            onChange={(e) => setCustomFixedContent(e.target.value)}
            className="w-full h-64 p-4 border rounded-md text-sm font-mono"
            placeholder="请输入固定内容..."
          />
          <p className="text-sm text-gray-600 mt-2">
            这部分内容将在"功能输出"后、"UI要求"前插入到最终模板中
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