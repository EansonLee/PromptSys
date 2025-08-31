'use client'

import React, { memo } from 'react';
import type { ThemeOption } from '@/types';
import { BUILT_IN_THEMES } from '@/constants/themes';

interface ThemeSelectorProps {
  onThemeSelect: (theme: ThemeOption) => void;
  selectedTheme?: string;
  className?: string;
}

const ThemeSelector: React.FC<ThemeSelectorProps> = memo(({ 
  onThemeSelect, 
  selectedTheme,
  className = '' 
}) => {
  return (
    <div className={className}>
      <p className="text-xs text-gray-500 mb-3">选择内置主题：</p>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
        {BUILT_IN_THEMES.map((theme) => (
          <button
            key={theme.id}
            type="button"
            onClick={() => onThemeSelect(theme)}
            className={`
              flex flex-col items-center p-3 border-2 rounded-lg 
              transition-all duration-200 group
              hover:border-blue-400 hover:bg-blue-50 hover:scale-105
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
              ${selectedTheme === theme.description 
                ? 'border-blue-500 bg-blue-50 scale-105' 
                : 'border-gray-200'
              }
            `}
            title={theme.description}
            aria-label={`选择主题：${theme.name}`}
          >
            <span 
              className="text-2xl mb-1 group-hover:scale-110 transition-transform"
              role="img"
              aria-label={theme.icon}
            >
              {theme.icon}
            </span>
            <span className="text-xs font-medium text-gray-700 group-hover:text-blue-600 text-center">
              {theme.name}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
});

ThemeSelector.displayName = 'ThemeSelector';

export default ThemeSelector;