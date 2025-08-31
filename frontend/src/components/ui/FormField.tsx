'use client'

import React from 'react';

interface BaseFormFieldProps {
  label: string;
  name: string;
  error?: string;
  touched?: boolean;
  required?: boolean;
  helpText?: string;
  className?: string;
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

const FormField: React.FC<FormFieldProps> = (props) => {
  const { 
    label, 
    name, 
    error, 
    touched, 
    required = false, 
    helpText, 
    className = '' 
  } = props;

  const inputClasses = `
    w-full px-4 py-3 rounded-xl glass-input text-glass-primary placeholder:text-glass-muted
    transition-all duration-300 resize-none
    ${error && touched 
      ? 'border-red-400/50 focus:border-red-400 focus:ring-2 focus:ring-red-400/20' 
      : 'focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/20'
    }
  `;

  return (
    <div className={`relative group ${className}`}>
      <label className="block text-sm font-semibold text-glass-primary mb-3 transition-colors duration-200 group-focus-within:text-blue-400">
        {label}
        {required && <span className="text-pink-400 ml-1">*</span>}
      </label>
      
      {isTextareaProps(props) ? (
        <textarea
          name={name}
          value={props.value}
          onChange={props.onChange}
          placeholder={props.placeholder}
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
          placeholder={props.placeholder}
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

export default FormField;