'use client'

import React from 'react';

// Field icon mapping
const FIELD_ICONS = {
  app_name: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
    </svg>
  ),
  theme: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
    </svg>
  ),
  variant_folder: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
    </svg>
  ),
  ui_color: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM21 5a2 2 0 00-2-2h-4a2 2 0 00-2 2v12a4 4 0 004 4 4 4 0 004-4V5z" />
    </svg>
  ),
  reference_file: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  tab_count: (
    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
    </svg>
  )
} as const;

interface BaseFormFieldProps {
  label: string;
  name: string;
  error?: string;
  touched?: boolean;
  required?: boolean;
  helpText?: string;
  className?: string;
  children?: React.ReactNode; // 支持自定义内容，如颜色选择器
}

interface InputFormFieldProps extends BaseFormFieldProps {
  type?: 'text' | 'number' | 'email' | 'password';
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  min?: number;
  max?: number;
}

interface TextareaFormFieldProps extends BaseFormFieldProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  rows?: number;
}

type FormFieldProps = InputFormFieldProps | TextareaFormFieldProps;

function isTextareaProps(props: FormFieldProps): props is TextareaFormFieldProps {
  return 'rows' in props;
}

const FormFieldEnhanced: React.FC<FormFieldProps> = (props) => {
  const { 
    label, 
    name, 
    error, 
    touched, 
    required = false, 
    helpText, 
    className = '',
    children
  } = props;

  const inputClasses = `
    w-full pl-12 pr-4 py-3 rounded-xl glass-input-enhanced text-glass-primary placeholder:text-glass-muted/80
    transition-all duration-300 resize-none
    ${error && touched 
      ? 'border-red-400/50 focus:border-red-400 focus:ring-2 focus:ring-red-400/20' 
      : ''
    }
  `;

  const getFieldIcon = (fieldName: string) => {
    return FIELD_ICONS[fieldName as keyof typeof FIELD_ICONS] || FIELD_ICONS.app_name;
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
      
      {/* Input Container with Icon */}
      <div className="relative">
        <div className="absolute left-4 top-1/2 transform -translate-y-1/2 input-icon pointer-events-none z-10">
          {getFieldIcon(name)}
        </div>

        {isTextareaProps(props) ? (
          <textarea
            name={name}
            value={props.value}
            onChange={props.onChange}
            placeholder={props.placeholder || `请输入${label}...`}
            rows={props.rows || 3}
            className={inputClasses}
            aria-invalid={error && touched ? 'true' : 'false'}
            aria-describedby={
              error && touched ? `${name}-error` : 
              helpText ? `${name}-help` : undefined
            }
          />
        ) : (
          <input
            type={props.type || 'text'}
            name={name}
            value={props.value}
            onChange={props.onChange}
            placeholder={props.placeholder || `请输入${label}...`}
            min={props.min}
            max={props.max}
            className={inputClasses}
            aria-invalid={error && touched ? 'true' : 'false'}
            aria-describedby={
              error && touched ? `${name}-error` : 
              helpText ? `${name}-help` : undefined
            }
          />
        )}

        {/* Additional UI elements (like color picker) */}
        {children && (
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 z-10">
            {children}
          </div>
        )}
      </div>
      
      {error && touched && (
        <p id={`${name}-error`} className="mt-2 text-sm text-red-400 animate-fade-in" role="alert">
          <span className="flex items-center space-x-1">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <span>{error}</span>
          </span>
        </p>
      )}
      
      {helpText && !(error && touched) && (
        <p id={`${name}-help`} className="mt-2 text-sm text-glass-muted">
          {helpText}
        </p>
      )}
    </div>
  );
};

export default FormFieldEnhanced;