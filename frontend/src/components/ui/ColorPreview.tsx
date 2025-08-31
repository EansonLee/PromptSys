'use client'

import React, { memo } from 'react';
import type { ColorInfo } from '@/utils/colorUtils';
import { getColorStyle, isDarkColor } from '@/utils/colorUtils';

interface ColorPreviewProps {
  colors: ColorInfo[];
  className?: string;
  showLabels?: boolean;
  size?: 'sm' | 'md' | 'lg';
  onColorRemove?: (index: number) => void;
}

const ColorPreview: React.FC<ColorPreviewProps> = memo(({
  colors,
  className = '',
  showLabels = true,
  size = 'md',
  onColorRemove
}) => {
  const validColors = colors.filter(c => c.isValid);
  
  if (validColors.length === 0) {
    return null;
  }

  const sizeClasses = {
    sm: 'w-6 h-6 text-xs',
    md: 'w-8 h-8 text-sm',
    lg: 'w-10 h-10 text-base'
  };

  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {validColors.map((color, index) => (
        <div
          key={index}
          className="relative group"
          title={`${color.original} → ${color.hex}`}
        >
          {/* 颜色圆点 */}
          <div
            className={`${sizeClasses[size]} rounded-full border-2 border-white/30 shadow-lg cursor-pointer transition-all duration-200 hover:scale-110 hover:shadow-xl relative overflow-hidden`}
            style={getColorStyle(color.hex)}
          >
            {/* 光泽效果 */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/20 via-transparent to-black/10 rounded-full"></div>
            
            {/* 删除按钮 */}
            {onColorRemove && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onColorRemove(index);
                }}
                className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-center justify-center hover:bg-red-600"
                aria-label={`删除颜色 ${color.original}`}
              >
                ×
              </button>
            )}
          </div>

          {/* 颜色标签 */}
          {showLabels && (
            <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-1 bg-black/80 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-20">
              <div className="text-center">
                <div className="font-medium">{color.original}</div>
                <div className="text-gray-300">{color.hex}</div>
              </div>
              {/* 小三角箭头 */}
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-black/80"></div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
});

ColorPreview.displayName = 'ColorPreview';

interface ColorTagsProps {
  colors: ColorInfo[];
  className?: string;
  onColorRemove?: (index: number) => void;
  maxDisplay?: number;
}

export const ColorTags: React.FC<ColorTagsProps> = memo(({
  colors,
  className = '',
  onColorRemove,
  maxDisplay = 10
}) => {
  const validColors = colors.filter(c => c.isValid);
  const displayColors = validColors.slice(0, maxDisplay);
  const remainingCount = validColors.length - maxDisplay;

  if (validColors.length === 0) {
    return null;
  }

  return (
    <div className={`flex flex-wrap gap-1 ${className}`}>
      {displayColors.map((color, index) => (
        <div
          key={index}
          className="group relative flex items-center space-x-1 px-3 py-1 rounded-full text-sm font-medium transition-all duration-200 hover:scale-105 glass-secondary"
          style={{
            backgroundColor: `${color.hex}20`,
            borderColor: `${color.hex}40`,
            color: isDarkColor(color.hex) ? color.hex : '#374151'
          }}
        >
          {/* 颜色指示点 */}
          <div
            className="w-3 h-3 rounded-full border border-white/30 shadow-sm"
            style={{ backgroundColor: color.hex }}
          />
          
          {/* 颜色名称 */}
          <span className="select-none">
            {color.original.length > 8 ? `${color.original.slice(0, 8)}...` : color.original}
          </span>
          
          {/* 删除按钮 */}
          {onColorRemove && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onColorRemove(index);
              }}
              className="ml-1 w-4 h-4 rounded-full bg-red-500/20 text-red-600 text-xs opacity-0 group-hover:opacity-100 transition-all duration-200 hover:bg-red-500/30 flex items-center justify-center"
              aria-label={`删除颜色 ${color.original}`}
            >
              ×
            </button>
          )}
        </div>
      ))}
      
      {/* 剩余颜色数量提示 */}
      {remainingCount > 0 && (
        <div className="flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600 border border-gray-200">
          +{remainingCount} 更多
        </div>
      )}
    </div>
  );
});

ColorTags.displayName = 'ColorTags';

export default ColorPreview;