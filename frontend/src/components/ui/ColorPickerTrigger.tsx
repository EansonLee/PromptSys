'use client'

import React, { useState, memo } from 'react';
import ColorPickerReactColorful from './ColorPickerReactColorful';

interface ColorPickerTriggerProps {
  onColorSelect: (color: string) => void;
  currentColor?: string;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const ColorPickerTrigger: React.FC<ColorPickerTriggerProps> = memo(({
  onColorSelect,
  currentColor,
  className = '',
  size = 'md',
  disabled = false
}) => {
  const [isPickerOpen, setIsPickerOpen] = useState(false);

  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-8 h-8', 
    lg: 'w-10 h-10'
  };

  const handleColorSelect = (color: string) => {
    onColorSelect(color);
    setIsPickerOpen(false);
  };

  return (
    <>
      <button
        type="button"
        onClick={() => !disabled && setIsPickerOpen(true)}
        disabled={disabled}
        className={`${sizeClasses[size]} rounded-lg border-2 border-white/30 shadow-md transition-all duration-200 hover:scale-110 hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-1 relative overflow-hidden group ${
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        } ${className}`}
        style={{
          backgroundColor: currentColor || '#0066CC'
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

      <ColorPickerReactColorful
        isOpen={isPickerOpen}
        onClose={() => setIsPickerOpen(false)}
        onColorSelect={handleColorSelect}
        initialColor={currentColor}
      />
    </>
  );
});

ColorPickerTrigger.displayName = 'ColorPickerTrigger';

export default ColorPickerTrigger;