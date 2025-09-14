'use client'

import React from 'react';
import { UseFormRegisterReturn, FieldError } from 'react-hook-form';

const FIELD_ICONS = {
  theme: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
    </svg>
  )
} as const;

interface EnhancedTextareaProps {
  label: string;
  name: string;
  placeholder?: string;
  required?: boolean;
  helpText?: string;
  className?: string;
  registration: UseFormRegisterReturn;
  error?: FieldError;
  rows?: number;
}

const EnhancedTextarea: React.FC<EnhancedTextareaProps> = ({
  label,
  name,
  placeholder,
  required = false,
  helpText,
  className = '',
  registration,
  error,
  rows = 3
}) => {
  const textareaClasses = `
    w-full pl-12 pr-4 py-3 rounded-xl glass-input-enhanced text-black placeholder:text-gray-500
    transition-all duration-300 resize-none
    ${error
      ? 'border-red-400/50 focus:border-red-400 focus:ring-2 focus:ring-red-400/20'
      : ''
    }
  `;

  const getFieldIcon = (fieldName: string) => {
    return FIELD_ICONS[fieldName as keyof typeof FIELD_ICONS] || FIELD_ICONS.theme;
  };

  return (
    <div className={`relative group input-field-group ${className}`}>
      <label className="block text-sm font-semibold text-glass-primary mb-3 transition-colors duration-200 group-focus-within:text-blue-400">
        <span className="flex items-center space-x-2">
          <span className="input-icon">{getFieldIcon(name)}</span>
          <span>{label}</span>
          {required && <span className="text-pink-400 ml-1">*</span>}
        </span>
      </label>

      <div className="relative">
        <div className="absolute left-4 top-4 input-icon pointer-events-none z-10">
          {getFieldIcon(name)}
        </div>

        <textarea
          placeholder={placeholder || `请输入${label}...`}
          rows={rows}
          className={textareaClasses}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={
            error ? `${name}-error` :
            helpText ? `${name}-help` : undefined
          }
          {...registration}
        />
      </div>

      {error && (
        <p id={`${name}-error`} className="mt-2 text-sm text-red-400 animate-fade-in" role="alert">
          <span className="flex items-center space-x-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error.message}</span>
          </span>
        </p>
      )}

      {helpText && !error && (
        <p id={`${name}-help`} className="mt-2 text-sm text-glass-muted">
          {helpText}
        </p>
      )}
    </div>
  );
};

export default EnhancedTextarea;