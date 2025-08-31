'use client'

import React, { useState, useRef, useEffect, useCallback, memo } from 'react';
import { getPresetColorGroups, generateRandomColor, hexToRgb, rgbToHex, getColorStyle } from '@/utils/colorUtils';

interface ColorPickerProps {
  isOpen: boolean;
  onClose: () => void;
  onColorSelect: (color: string) => void;
  initialColor?: string;
  className?: string;
}

const ColorPicker: React.FC<ColorPickerProps> = memo(({
  isOpen,
  onClose,
  onColorSelect,
  initialColor = '#0066CC',
  className = ''
}) => {
  const [selectedColor, setSelectedColor] = useState(initialColor);
  const [hue, setHue] = useState(0);
  const [saturation, setSaturation] = useState(100);
  const [lightness, setLightness] = useState(50);
  const [recentColors, setRecentColors] = useState<string[]>([]);

  const pickerRef = useRef<HTMLDivElement>(null);

  // 从十六进制颜色计算HSL
  const hexToHsl = useCallback((hex: string) => {
    const rgb = hexToRgb(hex);
    if (!rgb) return { h: 0, s: 100, l: 50 };

    const r = rgb.r / 255;
    const g = rgb.g / 255;
    const b = rgb.b / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h = 0;
    let s = 0;
    const l = (max + min) / 2;

    if (max !== min) {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
      h /= 6;
    }

    return {
      h: Math.round(h * 360),
      s: Math.round(s * 100),
      l: Math.round(l * 100)
    };
  }, []);

  // 从HSL计算十六进制颜色
  const hslToHex = useCallback((h: number, s: number, l: number) => {
    h /= 360;
    s /= 100;
    l /= 100;

    const hue2rgb = (p: number, q: number, t: number) => {
      if (t < 0) t += 1;
      if (t > 1) t -= 1;
      if (t < 1/6) return p + (q - p) * 6 * t;
      if (t < 1/2) return q;
      if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
      return p;
    };

    let r, g, b;

    if (s === 0) {
      r = g = b = l; // achromatic
    } else {
      const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
      const p = 2 * l - q;
      r = hue2rgb(p, q, h + 1/3);
      g = hue2rgb(p, q, h);
      b = hue2rgb(p, q, h - 1/3);
    }

    return rgbToHex(
      Math.round(r * 255),
      Math.round(g * 255),
      Math.round(b * 255)
    );
  }, []);

  // 初始化颜色值
  useEffect(() => {
    if (initialColor && initialColor !== selectedColor) {
      setSelectedColor(initialColor);
      const hsl = hexToHsl(initialColor);
      setHue(hsl.h);
      setSaturation(hsl.s);
      setLightness(hsl.l);
    }
  }, [initialColor, selectedColor, hexToHsl]);

  // 更新选中颜色
  useEffect(() => {
    const newColor = hslToHex(hue, saturation, lightness);
    setSelectedColor(newColor);
  }, [hue, saturation, lightness, hslToHex]);

  // 处理预设颜色选择
  const handlePresetColorSelect = useCallback((color: string) => {
    setSelectedColor(color);
    const hsl = hexToHsl(color);
    setHue(hsl.h);
    setSaturation(hsl.s);
    setLightness(hsl.l);
  }, [hexToHsl]);

  // 确认颜色选择
  const handleColorConfirm = useCallback(() => {
    onColorSelect(selectedColor);
    
    // 添加到最近使用的颜色
    setRecentColors(prev => {
      const newRecent = [selectedColor, ...prev.filter(c => c !== selectedColor)];
      return newRecent.slice(0, 12); // 最多保存12个最近使用的颜色
    });
    
    onClose();
  }, [selectedColor, onColorSelect, onClose]);

  // 生成随机颜色
  const handleRandomColor = useCallback(() => {
    const randomColor = generateRandomColor();
    handlePresetColorSelect(randomColor);
  }, [handlePresetColorSelect]);

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
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-hidden">
      <div
        ref={pickerRef}
        className={`glass-premium rounded-2xl p-6 max-w-lg w-full max-h-[85vh] overflow-y-auto animate-scale-in shadow-2xl ${className}`}
        style={{ minWidth: '320px' }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-glass-primary flex items-center space-x-2">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
            </svg>
            <span>选择颜色</span>
          </h3>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-lg glass-button flex items-center justify-center text-glass-secondary hover:text-glass-primary transition-colors duration-200"
            aria-label="关闭颜色选择器"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Color Preview */}
        <div className="mb-6">
          <div className="flex items-center space-x-4 mb-4">
            <div
              className="w-16 h-16 rounded-xl border-2 border-white/30 shadow-lg"
              style={getColorStyle(selectedColor)}
            />
            <div>
              <div className="text-sm font-medium text-glass-primary mb-1">当前颜色</div>
              <div className="text-xs text-glass-secondary font-mono bg-black/20 px-2 py-1 rounded">
                {selectedColor}
              </div>
            </div>
          </div>
        </div>

        {/* HSL Controls */}
        <div className="space-y-6 mb-6">
          {/* Hue */}
          <div>
            <label className="block text-sm font-medium text-glass-primary mb-3">
              色相 (Hue): {hue}°
            </label>
            <div className="relative">
              <input
                type="range"
                min="0"
                max="360"
                value={hue}
                onChange={(e) => setHue(parseInt(e.target.value))}
                className="w-full h-3 rounded-lg appearance-none cursor-pointer slider-hue"
              />
            </div>
          </div>

          {/* Saturation */}
          <div>
            <label className="block text-sm font-medium text-glass-primary mb-3">
              饱和度 (Saturation): {saturation}%
            </label>
            <div className="relative">
              <input
                type="range"
                min="0"
                max="100"
                value={saturation}
                onChange={(e) => setSaturation(parseInt(e.target.value))}
                className="w-full h-3 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, hsl(${hue}, 0%, ${lightness}%), hsl(${hue}, 100%, ${lightness}%))`
                }}
              />
            </div>
          </div>

          {/* Lightness */}
          <div>
            <label className="block text-sm font-medium text-glass-primary mb-3">
              亮度 (Lightness): {lightness}%
            </label>
            <div className="relative">
              <input
                type="range"
                min="0"
                max="100"
                value={lightness}
                onChange={(e) => setLightness(parseInt(e.target.value))}
                className="w-full h-3 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, hsl(${hue}, ${saturation}%, 0%), hsl(${hue}, ${saturation}%, 50%), hsl(${hue}, ${saturation}%, 100%))`
                }}
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
              className="text-xs glass-button px-3 py-1 rounded-lg text-glass-secondary hover:text-glass-primary"
            >
              随机色
            </button>
          </div>
          
          <div className="space-y-4">
            {presetColorGroups.map((group) => (
              <div key={group.name}>
                <div className="text-xs text-glass-muted mb-2">{group.name}</div>
                <div className="flex flex-wrap gap-2">
                  {group.colors.map((color) => (
                    <button
                      key={color}
                      onClick={() => handlePresetColorSelect(color)}
                      className={`w-8 h-8 rounded-lg border-2 transition-all duration-200 hover:scale-110 ${
                        selectedColor === color 
                          ? 'border-white shadow-lg ring-2 ring-blue-400' 
                          : 'border-white/30 hover:border-white/50'
                      }`}
                      style={{ backgroundColor: color }}
                      title={color}
                      aria-label={`选择颜色 ${color}`}
                    />
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
            <div className="flex flex-wrap gap-2">
              {recentColors.map((color, index) => (
                <button
                  key={index}
                  onClick={() => handlePresetColorSelect(color)}
                  className={`w-8 h-8 rounded-lg border-2 transition-all duration-200 hover:scale-110 ${
                    selectedColor === color 
                      ? 'border-white shadow-lg ring-2 ring-blue-400' 
                      : 'border-white/30 hover:border-white/50'
                  }`}
                  style={{ backgroundColor: color }}
                  title={color}
                  aria-label={`选择最近使用的颜色 ${color}`}
                />
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-3">
          <button
            onClick={handleColorConfirm}
            className="flex-1 glass-button px-4 py-2 rounded-xl text-glass-primary hover:text-white font-medium transition-colors duration-200"
          >
            确定选择
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-glass-secondary hover:text-glass-primary transition-colors duration-200"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  );
});

ColorPicker.displayName = 'ColorPicker';

export default ColorPicker;