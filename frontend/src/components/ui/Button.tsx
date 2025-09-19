'use client'

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium transition-all duration-300 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed rounded-xl glass-button relative overflow-hidden group';
  
  const variantClasses = {
    primary: 'text-glass-primary hover:text-white focus:ring-2 focus:ring-blue-400/50 focus:ring-offset-2 focus:ring-offset-transparent',
    secondary: 'text-glass-secondary hover:text-glass-primary focus:ring-2 focus:ring-purple-400/50 focus:ring-offset-2 focus:ring-offset-transparent',
    danger: 'text-red-200 hover:text-white focus:ring-2 focus:ring-red-400/50 focus:ring-offset-2 focus:ring-offset-transparent',
    success: 'text-green-200 hover:text-white focus:ring-2 focus:ring-green-400/50 focus:ring-offset-2 focus:ring-offset-transparent'
  };

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {/* Hover effect overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-400/0 via-purple-400/10 to-pink-400/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl"></div>
      
      {/* Button content */}
      <div className="relative z-10 flex items-center justify-center">
        {loading && (
          <div className="mr-2 w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
        )}
        {!loading && icon && (
          <span className="mr-2 group-hover:scale-110 transition-transform duration-200">{icon}</span>
        )}
        <span className="font-semibold">{children}</span>
      </div>
      
      {/* Shine effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out"></div>
    </button>
  );
};

export default Button;