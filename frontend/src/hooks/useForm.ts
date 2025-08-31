import { useState, useCallback, useMemo } from 'react';
import type { PromptRequest, FormErrors, FormTouched, InputChangeHandler } from '@/types';
import { DEFAULT_FORM_VALUES, VALIDATION_RULES } from '@/constants/themes';

export interface UseFormReturn {
  formData: PromptRequest;
  errors: FormErrors;
  touched: FormTouched;
  isValid: boolean;
  handleInputChange: InputChangeHandler;
  setFormData: React.Dispatch<React.SetStateAction<PromptRequest>>;
  setFieldValue: (field: keyof PromptRequest, value: any) => void;
  validateField: (field: keyof PromptRequest) => string | undefined;
  validateForm: () => boolean;
  resetForm: () => void;
  touchField: (field: keyof PromptRequest) => void;
}

function validateField(field: keyof PromptRequest, value: any): string | undefined {
  const rules = VALIDATION_RULES[field];
  
  if (!rules) return undefined;

  // Required validation
  if ('required' in rules && (!value || (typeof value === 'string' && value.trim() === ''))) {
    return rules.required;
  }

  if (typeof value === 'string') {
    // MinLength validation
    if ('minLength' in rules && value.length < rules.minLength.value) {
      return rules.minLength.message;
    }

    // MaxLength validation
    if ('maxLength' in rules && value.length > rules.maxLength.value) {
      return rules.maxLength.message;
    }

    // Pattern validation
    if ('pattern' in rules && !rules.pattern.value.test(value)) {
      return rules.pattern.message;
    }
  }

  if (typeof value === 'number') {
    // Min validation
    if ('min' in rules && value < rules.min.value) {
      return rules.min.message;
    }

    // Max validation
    if ('max' in rules && value > rules.max.value) {
      return rules.max.message;
    }
  }

  return undefined;
}

export function useForm(initialValues: Partial<PromptRequest> = {}): UseFormReturn {
  const [formData, setFormData] = useState<PromptRequest>({
    ...DEFAULT_FORM_VALUES,
    ...initialValues
  });
  
  const [touched, setTouched] = useState<FormTouched>({});

  const errors = useMemo(() => {
    const validationErrors: FormErrors = {};
    
    (Object.keys(formData) as Array<keyof PromptRequest>).forEach(field => {
      if (touched[field]) {
        const error = validateField(field, formData[field]);
        if (error) {
          validationErrors[field] = error;
        }
      }
    });

    return validationErrors;
  }, [formData, touched]);

  const isValid = useMemo(() => {
    return Object.keys(errors).length === 0 && 
           formData.app_name.trim() !== '' && 
           formData.theme.trim() !== '' && 
           formData.variant_folder.trim() !== '';
  }, [errors, formData]);

  const handleInputChange = useCallback<InputChangeHandler>((event) => {
    const { name, value, type } = event.target;
    const fieldName = name as keyof PromptRequest;
    
    let processedValue: any = value;
    
    if (type === 'number') {
      processedValue = parseInt(value, 10) || 0;
      if (fieldName === 'tab_count') {
        processedValue = Math.max(1, Math.min(10, processedValue));
      }
    }

    setFormData(prev => ({ ...prev, [fieldName]: processedValue }));
    
    // Mark field as touched
    setTouched(prev => ({ ...prev, [fieldName]: true }));
  }, []);

  const setFieldValue = useCallback((field: keyof PromptRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setTouched(prev => ({ ...prev, [field]: true }));
  }, []);

  const validateFieldCallback = useCallback((field: keyof PromptRequest) => {
    return validateField(field, formData[field]);
  }, [formData]);

  const validateForm = useCallback(() => {
    // Touch all fields
    const allTouched: FormTouched = {};
    (Object.keys(formData) as Array<keyof PromptRequest>).forEach(field => {
      allTouched[field] = true;
    });
    setTouched(allTouched);

    // Validate all fields
    const hasErrors = (Object.keys(formData) as Array<keyof PromptRequest>).some(field => {
      return validateField(field, formData[field]) !== undefined;
    });

    return !hasErrors && isValid;
  }, [formData, isValid]);

  const resetForm = useCallback(() => {
    setFormData({ ...DEFAULT_FORM_VALUES, ...initialValues });
    setTouched({});
  }, [initialValues]);

  const touchField = useCallback((field: keyof PromptRequest) => {
    setTouched(prev => ({ ...prev, [field]: true }));
  }, []);

  return {
    formData,
    errors,
    touched,
    isValid,
    handleInputChange,
    setFormData,
    setFieldValue,
    validateField: validateFieldCallback,
    validateForm,
    resetForm,
    touchField
  };
}