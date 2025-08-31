'use client'

import React from 'react';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  className?: string;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  color = 'text-blue-400',
  className = ''
}) => {
  const sizeClasses = {
    sm: 'w-5 h-5',
    md: 'w-7 h-7', 
    lg: 'w-10 h-10'
  };

  return (
    <div
      className={`${sizeClasses[size]} relative ${className}`}
      role="status"
      aria-label="加载中"
    >
      {/* Outer ring with gradient */}
      <div className={`${sizeClasses[size]} rounded-full border-2 border-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 animate-spin`}>
        <div className={`${sizeClasses[size]} rounded-full bg-transparent border-2 border-transparent`} style={{
          background: 'conic-gradient(transparent, transparent, transparent, rgba(255,255,255,0.3))'
        }}></div>
      </div>
      
      {/* Inner glow effect */}
      <div className={`absolute inset-0 ${sizeClasses[size]} rounded-full bg-gradient-to-r from-blue-400/20 via-purple-400/20 to-pink-400/20 blur-sm animate-pulse-glow`}></div>
      
      <span className="sr-only">加载中...</span>
    </div>
  );
};

export default LoadingSpinner;