'use client'

import React from 'react';
import { UseFormRegisterReturn, FieldError } from 'react-hook-form';

interface FormFieldSimpleProps {
  label: string;
  name: string;
  type?: 'text' | 'number' | 'email' | 'password';
  placeholder?: string;
  required?: boolean;
  helpText?: string;
  className?: string;
  registration: UseFormRegisterReturn;
  error?: FieldError;
  rows?: number;
}

const FormFieldSimple: React.FC<FormFieldSimpleProps> = ({
  label,
  type = 'text',
  placeholder,
  required = false,
  helpText,
  className = '',
  registration,
  error,
  rows
}) => {
  const inputClasses = `
    w-full px-4 py-3 rounded-xl glass-input-enhanced text-black placeholder:text-gray-500
    transition-all duration-300 resize-none
    ${error
      ? 'border-red-400/50 focus:border-red-400 focus:ring-2 focus:ring-red-400/20'
      : ''
    }
  `;

  return (
    <div className={`relative group ${className}`}>
      <label className="block text-sm font-semibold text-glass-primary mb-3">
        {label}
        {required && <span className="text-pink-400 ml-1">*</span>}
      </label>

      {rows ? (
        <textarea
          placeholder={placeholder || `请输入${label}...`}
          rows={rows}
          className={inputClasses}
          {...registration}
        />
      ) : (
        <input
          type={type}
          placeholder={placeholder || `请输入${label}...`}
          className={inputClasses}
          {...registration}
        />
      )}

      {error && (
        <p className="mt-2 text-sm text-red-400 animate-fade-in" role="alert">
          {error.message}
        </p>
      )}

      {helpText && !error && (
        <p className="mt-2 text-sm text-glass-muted">
          {helpText}
        </p>
      )}
    </div>
  );
};

export default FormFieldSimple;