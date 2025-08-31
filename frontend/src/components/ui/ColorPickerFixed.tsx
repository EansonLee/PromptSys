'use client'

import React, { useState, useRef, useEffect, useCallback, memo } from 'react';
import { getPresetColorGroups, generateRandomColor } from '@/utils/colorUtils';

interface ColorPickerFixedProps {
  isOpen: boolean;
  onClose: () => void;
  onColorSelect: (color: string) => void;
  initialColor?: string;
  className?: string;
}

const ColorPickerFixed: React.FC<ColorPickerFixedProps> = memo(({
  isOpen,
  onClose,
  onColorSelect,
  initialColor = '#0066CC',
  className = ''
}) => {
  const [selectedColor, setSelectedColor] = useState(initialColor);
  const [recentColors, setRecentColors] = useState<string[]>([]);
  const pickerRef = useRef<HTMLDivElement>(null);

  // 处理预设颜色选择
  const handleColorSelect = useCallback((color: string) => {
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
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const presetColorGroups = getPresetColorGroups();

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div
        ref={pickerRef}
        className={`glass-premium rounded-2xl w-full max-w-sm mx-4 animate-scale-in shadow-2xl ${className}`}
        style={{ maxHeight: '85vh' }}
      >
        {/* Header with proper spacing */}
        <div className="flex items-center justify-between p-5 pb-0">
          <div className="flex items-center space-x-2">
            <svg className="w-5 h-5 text-glass-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
            </svg>
            <h3 className="text-lg font-semibold text-glass-primary">选择颜色</h3>
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

        {/* Content area with scroll */}
        <div className="p-5 overflow-y-auto" style={{ maxHeight: 'calc(85vh - 80px)' }}>
          {/* Color Preview */}
          <div className="mb-6">
            <div className="flex items-center space-x-4 mb-4">
              <div
                className="w-16 h-16 rounded-xl border-2 border-white/30 shadow-lg relative overflow-hidden"
                style={{ backgroundColor: selectedColor }}
              >
                <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/10"></div>
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-glass-primary mb-2">当前颜色</div>
                <input
                  type="text"
                  value={selectedColor}
                  onChange={(e) => {
                    const value = e.target.value;
                    if (value.match(/^#[0-9A-Fa-f]{0,6}$/)) {
                      setSelectedColor(value);
                    }
                  }}
                  className="w-full px-3 py-2 text-sm font-mono glass-input-enhanced rounded-lg"
                  placeholder="#0066CC"
                />
              </div>
            </div>
          </div>

          {/* Preset Colors */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-sm font-medium text-glass-primary">预设颜色</h4>
              <button
                onClick={handleRandomColor}
                className="text-xs glass-button px-3 py-1 rounded-lg text-glass-secondary hover:text-glass-primary transition-colors duration-200"
              >
                随机色
              </button>
            </div>
            
            <div className="space-y-4">
              {presetColorGroups.map((group) => (
                <div key={group.name}>
                  <div className="text-xs text-glass-muted mb-2">{group.name}</div>
                  <div className="grid grid-cols-5 gap-2">
                    {group.colors.map((color) => (
                      <button
                        key={color}
                        onClick={() => handleColorSelect(color)}
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

          {/* Recent Colors */}
          {recentColors.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-medium text-glass-primary mb-3">最近使用</h4>
              <div className="grid grid-cols-8 gap-2">
                {recentColors.map((color, index) => (
                  <button
                    key={index}
                    onClick={() => handleColorSelect(color)}
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

        {/* Fixed bottom buttons */}
        <div className="flex space-x-3 p-5 pt-0 border-t border-white/10">
          <button
            onClick={handleColorConfirm}
            className="flex-1 glass-button px-4 py-3 rounded-xl text-glass-primary hover:text-white font-medium transition-colors duration-200"
          >
            确定选择
          </button>
          <button
            onClick={onClose}
            className="px-4 py-3 rounded-xl text-glass-secondary hover:text-glass-primary transition-colors duration-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  );
});

ColorPickerFixed.displayName = 'ColorPickerFixed';

export default ColorPickerFixed;