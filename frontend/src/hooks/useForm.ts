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
  // 检查是否隐藏变体和参考文件字段
  const showVariantAndReferenceFields = process.env.NEXT_PUBLIC_SHOW_VARIANT_AND_REFERENCE_FIELDS === 'true';
  
  // 为隐藏字段提供默认值
  const getDefaultValues = useCallback((): PromptRequest => {
    const defaults = { ...DEFAULT_FORM_VALUES };
    
    if (!showVariantAndReferenceFields) {
      defaults.variant_folder = 'variant_default';
      defaults.reference_file = 'MainActivity';
    }
    
    return defaults;
  }, [showVariantAndReferenceFields]);

  const [formData, setFormData] = useState<PromptRequest>(() => ({
    ...getDefaultValues(),
    ...initialValues
  }));
  
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
    const hasErrors = Object.keys(errors).length === 0;
    const hasRequiredFields = formData.app_name.trim() !== '' && 
                               formData.theme.trim() !== '';
    
    // 如果显示变体文件夹字段，则需要验证
    const hasVariantFolder = showVariantAndReferenceFields 
      ? formData.variant_folder.trim() !== '' 
      : true; // 隐藏时不需要验证用户输入
    
    return hasErrors && hasRequiredFields && hasVariantFolder;
  }, [errors, formData, showVariantAndReferenceFields]);

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
    setFormData({ ...getDefaultValues(), ...initialValues });
    setTouched({});
  }, [initialValues, getDefaultValues]);

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