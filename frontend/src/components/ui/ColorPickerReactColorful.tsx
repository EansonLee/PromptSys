'use client'

import React, { useState, useRef, useEffect, useCallback, memo } from 'react';
import { HexColorPicker, HexColorInput } from 'react-colorful';
import { getPresetColorGroups, generateRandomColor } from '@/utils/colorUtils';

interface ColorPickerReactColorfulProps {
  isOpen: boolean;
  onClose: () => void;
  onColorSelect: (color: string) => void;
  initialColor?: string;
  className?: string;
}

const ColorPickerReactColorful: React.FC<ColorPickerReactColorfulProps> = memo(({
  isOpen,
  onClose,
  onColorSelect,
  initialColor = '#0066CC',
  className = ''
}) => {
  const [selectedColor, setSelectedColor] = useState(initialColor);
  const [recentColors, setRecentColors] = useState<string[]>([]);
  const [activeTab, setActiveTab] = useState<'picker' | 'presets'>('picker');
  const pickerRef = useRef<HTMLDivElement>(null);

  // 初始化颜色
  useEffect(() => {
    if (initialColor && initialColor !== selectedColor) {
      setSelectedColor(initialColor);
    }
  }, [initialColor]);

  // 处理颜色变化
  const handleColorChange = useCallback((color: string) => {
    setSelectedColor(color);
  }, []);

  // 处理预设颜色选择
  const handlePresetColorSelect = useCallback((color: string) => {
    setSelectedColor(color);
  }, []);

  // 确认颜色选择
  const handleColorConfirm = useCallback(() => {
    onColorSelect(selectedColor);
    
    // 添加到最近使用的颜色
    setRecentColors(prev => {
      const newRecent = [selectedColor, ...prev.filter(c => c !== selectedColor)];
      return newRecent.slice(0, 8);
    });
    
    onClose();
  }, [selectedColor, onColorSelect, onClose]);

  // 生成随机颜色
  const handleRandomColor = useCallback(() => {
    const randomColor = generateRandomColor();
    setSelectedColor(randomColor);
  }, []);

  // 点击外部关闭
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (pickerRef.current && !pickerRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
    return;
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const presetColorGroups = getPresetColorGroups();

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div
        ref={pickerRef}
        className={`glass-premium-enhanced rounded-2xl w-full max-w-md mx-4 animate-scale-in shadow-2xl ${className}`}
        style={{ maxHeight: '85vh', minWidth: '320px' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-5 pb-0">
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-black" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
            </svg>
            <h3 className="text-lg font-semibold text-black">专业取色板</h3>
          </div>
          <button
            onClick={onClose}
            className="w-10 h-10 rounded-full glass-button flex items-center justify-center text-glass-secondary hover:text-red-400 transition-colors duration-200"
            aria-label="关闭颜色选择器"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* 标签切换 */}
        <div className="px-5 pt-4">
          <div className="flex space-x-1 glass-secondary rounded-lg p-1">
            <button
              onClick={() => setActiveTab('picker')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                activeTab === 'picker'
                  ? 'glass-button text-black shadow-sm'
                  : 'text-gray-600 hover:text-black'
              }`}
            >
              调色板
            </button>
            <button
              onClick={() => setActiveTab('presets')}
              className={`flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 ${
                activeTab === 'presets'
                  ? 'glass-button text-black shadow-sm'
                  : 'text-gray-600 hover:text-black'
              }`}
            >
              预设颜色
            </button>
          </div>
        </div>

        {/* 内容区域 */}
        <div className="p-5 overflow-y-auto" style={{ maxHeight: 'calc(85vh - 180px)' }}>
          {/* 颜色预览和输入 */}
          <div className="mb-6">
            <div className="flex items-center space-x-4 mb-4">
              <div
                className="w-14 h-14 sm:w-16 sm:h-16 rounded-xl border-2 border-white/30 shadow-lg relative overflow-hidden flex-shrink-0"
                style={{ backgroundColor: selectedColor }}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/10"></div>
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-black mb-2">当前颜色</div>
                <HexColorInput
                  color={selectedColor}
                  onChange={handleColorChange}
                  prefixed
                  placeholder="#0066CC"
                  className="w-full px-3 py-2 text-sm font-mono glass-input-enhanced rounded-lg text-black placeholder:text-gray-500 bg-white/50"
                />
              </div>
            </div>
          </div>

          {/* 标签内容 */}
          {activeTab === 'picker' && (
            <div className="mb-6">
              <div className="flex justify-center">
                <div className="react-colorful-wrapper w-full max-w-xs">
                  <HexColorPicker
                    color={selectedColor}
                    onChange={handleColorChange}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'presets' && (
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-sm font-medium text-black">预设颜色</h4>
                <button
                  onClick={handleRandomColor}
                  className="text-xs glass-button px-3 py-1 rounded-lg text-gray-600 hover:text-black transition-colors duration-200"
                >
                  随机色
                </button>
              </div>
              
              <div className="space-y-4">
                {presetColorGroups.map((group) => (
                  <div key={group.name}>
                    <div className="text-xs text-gray-600 mb-2">{group.name}</div>
                    <div className="grid grid-cols-6 sm:grid-cols-5 gap-2">
                      {group.colors.map((color) => (
                        <button
                          key={color}
                          onClick={() => handlePresetColorSelect(color)}
                          className={`aspect-square rounded-lg border-2 transition-all duration-200 hover:scale-105 ${
                            selectedColor === color 
                              ? 'border-white shadow-lg ring-2 ring-blue-400' 
                              : 'border-white/30 hover:border-white/50'
                          }`}
                          style={{ backgroundColor: color }}
                          title={color}
                          aria-label={`选择颜色 ${color}`}
                        >
                          <div className="w-full h-full rounded-md bg-gradient-to-br from-white/10 via-transparent to-black/10"></div>
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 最近使用的颜色 */}
          {recentColors.length > 0 && (
            <div className="mb-4">
              <h4 className="text-sm font-medium text-black mb-3">最近使用</h4>
              <div className="grid grid-cols-6 sm:grid-cols-8 gap-2">
                {recentColors.map((color, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedColor(color)}
                    className={`aspect-square rounded-lg border-2 transition-all duration-200 hover:scale-105 ${
                      selectedColor === color 
                        ? 'border-white shadow-lg ring-2 ring-blue-400' 
                        : 'border-white/30 hover:border-white/50'
                    }`}
                    style={{ backgroundColor: color }}
                    title={color}
                    aria-label={`选择最近使用的颜色 ${color}`}
                  >
                    <div className="w-full h-full rounded-md bg-gradient-to-br from-white/10 via-transparent to-black/10"></div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* 底部按钮 */}
        <div className="flex space-x-3 p-5 pt-0 border-t border-white/10">
          <button
            onClick={handleColorConfirm}
            className="flex-1 glass-button px-4 py-3 rounded-xl text-black hover:text-blue-600 font-medium transition-colors duration-200"
          >
            确定选择
          </button>
          <button
            onClick={onClose}
            className="px-4 py-3 rounded-xl text-gray-600 hover:text-black transition-colors duration-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  );
});

ColorPickerReactColorful.displayName = 'ColorPickerReactColorful';

export default ColorPickerReactColorful;