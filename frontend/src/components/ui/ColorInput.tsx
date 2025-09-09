'use client'

import React, { useState, useEffect, useCallback, memo } from 'react';
import { parseMultipleColors, colorsToDisplayString } from '@/utils/colorUtils';
import type { ParsedColors } from '@/types';
import ColorPreview, { ColorTags } from './ColorPreview';
import ColorPickerTrigger from './ColorPickerTrigger';
import FormFieldEnhanced from './FormFieldEnhanced';

interface ColorInputProps {
  label: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  touched?: boolean;
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
  touched,
  required = false,
  placeholder,
  helpText,
  className = ''
}) => {
  const [parsedColors, setParsedColors] = useState<ParsedColors>({
    colors: [],
    hasValidColors: false,
    invalidInputs: []
  });

  // 解析颜色输入
  useEffect(() => {
    const parsed = parseMultipleColors(value);
    setParsedColors(parsed);
  }, [value]);

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
      {/* 使用增强的FormField，并添加颜色选择器按钮 */}
      <FormFieldEnhanced
        label={label}
        name={name}
        type="text"
        value={value}
        onChange={() => {}} // 禁用手动输入
        error={error}
        touched={touched}
        required={required}
        placeholder="请使用右侧取色按钮选择颜色"
        helpText="点击右侧取色按钮打开颜色选择器，支持多次选择，选中的颜色将自动添加到此处"
        readOnly={true}
      >
        {/* 颜色选择器触发按钮 */}
        <ColorPickerTrigger
          onColorSelect={handleColorAdd}
          currentColor={parsedColors.hasValidColors ? parsedColors.colors.find(c => c.isValid)?.hex : undefined}
          className="mr-2"
        />
      </FormFieldEnhanced>

      {/* 颜色预览区域 */}
      {parsedColors.hasValidColors && (
        <div className="mt-3 space-y-3">
          {/* 圆点预览 */}
          <div className="flex items-center space-x-3">
            <span className="text-sm font-medium text-black">颜色预览:</span>
            <ColorPreview
              colors={[...parsedColors.colors]}
              onColorRemove={handleColorRemove}
              size="md"
              showLabels={true}
            />
          </div>

          {/* 标签预览 */}
          <div className="space-y-2">
            <span className="text-sm font-medium text-black">颜色标签:</span>
            <ColorTags
              colors={[...parsedColors.colors]}
              onColorRemove={handleColorRemove}
              maxDisplay={8}
            />
          </div>
        </div>
      )}

      {/* 无效颜色提示 */}
      {parsedColors.invalidInputs.length > 0 && (
        <div className="mt-2 p-3 bg-orange-50/50 border border-orange-200/30 rounded-lg animate-fade-in">
          <div className="flex items-start space-x-2">
            <svg className="w-4 h-4 text-orange-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div className="flex-1">
              <p className="text-sm font-medium text-orange-700">无法识别的颜色格式：</p>
              <p className="text-sm text-orange-600 mt-1">
                {parsedColors.invalidInputs.join('、')}
              </p>
              <p className="text-xs text-orange-500 mt-1">
                请使用支持的颜色格式，或点击取色按钮选择颜色
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 颜色格式提示 */}
      {!parsedColors.hasValidColors && value.trim() && (
        <div className="mt-2 p-3 bg-blue-50/50 border border-blue-200/30 rounded-lg">
          <div className="flex items-start space-x-2">
            <svg className="w-4 h-4 text-blue-500 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            <div className="flex-1">
              <p className="text-sm font-medium text-blue-700">支持的颜色格式：</p>
              <ul className="text-sm text-blue-600 mt-1 space-y-1">
                <li>• 中文颜色名：红色、蓝色、绿色、紫色等</li>
                <li>• 十六进制：#FF0000、#0066CC、#32CD32</li>
                <li>• RGB格式：rgb(255,0,0)</li>
                <li>• 英文颜色名：red、blue、green</li>
                <li>• 特殊描述：绿色清新、紫色梦幻、橙色活力</li>
              </ul>
              <p className="text-xs text-blue-500 mt-2">
                多个颜色请用&ldquo;、&rdquo;、&ldquo;,&rdquo;或空格分隔
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
});

ColorInput.displayName = 'ColorInput';

export default ColorInput;