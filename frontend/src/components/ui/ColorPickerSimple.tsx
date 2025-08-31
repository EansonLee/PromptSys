'use client'

import React, { useState, useRef, useEffect, useCallback, memo } from 'react';
import { getPresetColorGroups, generateRandomColor } from '@/utils/colorUtils';

interface ColorPickerSimpleProps {
  isOpen: boolean;
  onClose: () => void;
  onColorSelect: (color: string) => void;
  initialColor?: string;
  className?: string;
}

const ColorPickerSimple: React.FC<ColorPickerSimpleProps> = memo(({
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
        className={`glass-premium rounded-2xl p-4 sm:p-6 max-w-md w-full max-h-[85vh] overflow-y-auto animate-scale-in shadow-2xl ${className}`}
        style={{ minWidth: '300px', maxWidth: '400px' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6 w-full">
          <div className="flex items-center space-x-2 flex-1 min-w-0">
            <svg className="w-5 h-5 text-glass-primary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
            </svg>
            <h3 className="text-lg font-semibold text-glass-primary truncate">
              选择颜色
            </h3>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg glass-button flex items-center justify-center text-glass-secondary hover:text-glass-primary transition-colors duration-200 flex-shrink-0 ml-4"
            aria-label="关闭颜色选择器"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Color Preview */}
        <div className="mb-6">
          <div className="flex items-center space-x-4 mb-4">
            <div
              className="w-16 h-16 rounded-xl border-2 border-white/30 shadow-lg relative overflow-hidden"
              style={{ backgroundColor: selectedColor }}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/10"></div>
            </div>
            <div>
              <div className="text-sm font-medium text-glass-primary mb-1">当前颜色</div>
              <div className="text-xs text-glass-secondary font-mono bg-black/20 px-2 py-1 rounded">
                {selectedColor}
              </div>
            </div>
          </div>
        </div>

        {/* Hex Color Input */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-glass-primary mb-2">
            十六进制颜色码
          </label>
          <input
            type="text"
            value={selectedColor}
            onChange={(e) => {
              const value = e.target.value;
              if (value.match(/^#[0-9A-Fa-f]{0,6}$/)) {
                setSelectedColor(value);
              }
            }}
            className="w-full px-3 py-2 glass-input-enhanced text-glass-primary placeholder:text-glass-muted/80 rounded-lg"
            placeholder="#0066CC"
          />
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
                      className={`aspect-square rounded-lg border-2 transition-all duration-200 hover:scale-110 ${
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
                  className={`aspect-square rounded-lg border-2 transition-all duration-200 hover:scale-110 ${
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

        {/* Action Buttons */}
        <div className="flex space-x-3">
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

ColorPickerSimple.displayName = 'ColorPickerSimple';

export default ColorPickerSimple;