'use client'

import React, { useState, useCallback, memo } from 'react';
import { parseMultipleColors, colorsToDisplayString } from '@/utils/colorUtils';
import { ColorTags } from './ColorPreview';
import ColorPickerReactColorful from './ColorPickerReactColorful';

interface ColorInputProps {
  label: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  helpText?: string;
  className?: string;
}

const ColorInput: React.FC<ColorInputProps> = memo(({
  label,
  name,
  value,
  onChange,
  error,
  required = false,
  helpText,
  className = ''
}) => {
  const [isPickerOpen, setIsPickerOpen] = useState(false);

  // 解析颜色输入（简化为memoized计算）
  const parsedColors = React.useMemo(() => parseMultipleColors(value), [value]);

  // 添加颜色到输入框
  const handleColorAdd = useCallback((newColor: string) => {
    const currentColors = value.trim();
    const separator = '、';
    const newValue = currentColors
      ? `${currentColors}${separator}${newColor}`
      : newColor;

    // 创建一个模拟的事件对象
    const mockEvent = {
      target: {
        name,
        value: newValue,
        type: 'text'
      }
    } as React.ChangeEvent<HTMLInputElement>;

    onChange(mockEvent);
    setIsPickerOpen(false);
  }, [value, name, onChange]);

  // 移除特定颜色
  const handleColorRemove = useCallback((index: number) => {
    const validColors = parsedColors.colors.filter(c => c.isValid);
    if (index >= 0 && index < validColors.length) {
      validColors.splice(index, 1);
      const newValue = colorsToDisplayString(validColors);
      
      const mockEvent = {
        target: {
          name,
          value: newValue,
          type: 'text'
        }
      } as React.ChangeEvent<HTMLInputElement>;
      
      onChange(mockEvent);
    }
  }, [parsedColors.colors, name, onChange]);


  return (
    <div className={className}>
      {/* 简化的表单字段 */}
      <div className="relative group">
        <label className="block text-sm font-semibold text-glass-primary mb-3">
          {label}
          {required && <span className="text-pink-400 ml-1">*</span>}
        </label>

        <div className="relative">
          <input
            type="text"
            name={name}
            value={value}
            onChange={() => {}} // 禁用手动输入
            placeholder="请使用右侧取色按钮选择颜色"
            readOnly={true}
            className="w-full pl-4 pr-12 py-3 rounded-xl glass-input-enhanced text-black placeholder:text-gray-500 transition-all duration-300"
          />

          {/* 颜色选择器触发按钮 */}
          <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
            <button
              type="button"
              onClick={() => setIsPickerOpen(true)}
              className="w-8 h-8 rounded-lg border-2 border-white/30 shadow-md transition-all duration-200 hover:scale-110 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-1 relative overflow-hidden group cursor-pointer"
              style={{
                backgroundColor: parsedColors.hasValidColors ? parsedColors.colors.find(c => c.isValid)?.hex : '#0066CC'
              }}
              title="点击选择颜色"
              aria-label="打开颜色选择器"
            >
              {/* Icon overlay */}
              <div className="absolute inset-0 flex items-center justify-center bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
                </svg>
              </div>

              {/* Gradient overlay for visual enhancement */}
              <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/10 rounded-md"></div>
            </button>
          </div>
        </div>

        {/* 错误信息 */}
        {error && (
          <p className="mt-2 text-sm text-red-400 animate-fade-in" role="alert">
            {error}
          </p>
        )}

        {/* 帮助文本 */}
        {helpText && !error && (
          <p className="mt-2 text-sm text-glass-muted">
            {helpText}
          </p>
        )}
      </div>

      {/* 颜色选择器弹窗 */}
      <ColorPickerReactColorful
        isOpen={isPickerOpen}
        onClose={() => setIsPickerOpen(false)}
        onColorSelect={handleColorAdd}
        initialColor={parsedColors.hasValidColors ? parsedColors.colors.find(c => c.isValid)?.hex : undefined}
      />

      {/* 简化的颜色预览区域 - 只显示标签预览 */}
      {parsedColors.hasValidColors && (
        <div className="mt-3">
          <ColorTags
            colors={parsedColors.colors}
            onColorRemove={handleColorRemove}
            maxDisplay={8}
          />
        </div>
      )}

      {/* 简化的状态提示 */}
      {parsedColors.invalidInputs.length > 0 && (
        <p className="mt-2 text-sm text-orange-600">
          无法识别: {parsedColors.invalidInputs.join('、')} - 请使用取色按钮选择颜色
        </p>
      )}
    </div>
  );
});

ColorInput.displayName = 'ColorInput';

export default ColorInput;