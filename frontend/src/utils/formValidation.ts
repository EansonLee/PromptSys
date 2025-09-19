import type { PromptRequest } from '@/types';

export interface ValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
}

export const validateForm = (data: PromptRequest): ValidationResult => {
  const errors: Record<string, string> = {};

  // App name validation
  if (!data.app_name || data.app_name.trim().length === 0) {
    errors.app_name = 'APP名称不能为空';
  } else if (data.app_name.trim().length < 2) {
    errors.app_name = 'APP名称至少需要2个字符';
  } else if (data.app_name.trim().length > 50) {
    errors.app_name = 'APP名称不能超过50个字符';
  }

  // Theme validation
  if (!data.theme || data.theme.trim().length === 0) {
    errors.theme = '主题不能为空';
  } else if (data.theme.trim().length < 5) {
    errors.theme = '主题描述至少需要5个字符';
  } else if (data.theme.trim().length > 500) {
    errors.theme = '主题描述不能超过500个字符';
  }

  // Variant folder validation
  if (!data.variant_folder || data.variant_folder.trim().length === 0) {
    errors.variant_folder = '变体文件夹不能为空';
  } else {
    const folderPattern = /^[a-zA-Z0-9_]+$/;
    if (!folderPattern.test(data.variant_folder.trim())) {
      errors.variant_folder = '变体文件夹只能包含字母、数字和下划线';
    } else if (data.variant_folder.trim().length < 3) {
      errors.variant_folder = '变体文件夹至少需要3个字符';
    } else if (data.variant_folder.trim().length > 50) {
      errors.variant_folder = '变体文件夹不能超过50个字符';
    }
  }

  // UI color validation
  if (!data.ui_color || data.ui_color.trim().length === 0) {
    errors.ui_color = 'UI主色调不能为空';
  } else if (data.ui_color.trim().length > 200) {
    errors.ui_color = 'UI主色调描述不能超过200个字符';
  }

  // Reference file validation (optional)
  if (data.reference_file && data.reference_file.trim().length > 0) {
    if (data.reference_file.trim().length > 100) {
      errors.reference_file = '参考文件名不能超过100个字符';
    }
  }

  // Tab count validation (optional, handled elsewhere with specific logic)
  if (data.tab_count !== undefined) {
    if (data.tab_count < 1 || data.tab_count > 10) {
      errors.tab_count = 'Tab数量必须在1-10之间';
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

// Unified validation rules for React Hook Form - consolidated from themes.ts
export const validationRules = {
  app_name: {
    required: 'APP名称不能为空',
    minLength: {
      value: 2,
      message: 'APP名称至少需要2个字符'
    },
    maxLength: {
      value: 50,
      message: 'APP名称不能超过50个字符'
    }
  },
  theme: {
    required: '主题不能为空',
    minLength: {
      value: 5,
      message: '主题描述至少需要5个字符'
    },
    maxLength: {
      value: 500,
      message: '主题描述不能超过500个字符'
    }
  },
  variant_folder: {
    required: '变体文件夹不能为空',
    pattern: {
      value: /^[a-zA-Z0-9_]+$/,
      message: '变体文件夹只能包含字母、数字和下划线'
    },
    minLength: {
      value: 3,
      message: '变体文件夹至少需要3个字符'
    },
    maxLength: {
      value: 50,
      message: '变体文件夹不能超过50个字符'
    }
  },
  ui_color: {
    required: 'UI主色调不能为空',
    maxLength: {
      value: 200,
      message: 'UI主色调描述不能超过200个字符'
    }
  },
  reference_file: {
    maxLength: {
      value: 100,
      message: '参考文件名不能超过100个字符'
    }
  },
  tab_count: {
    min: {
      value: 1,
      message: 'Tab数量最少为1'
    },
    max: {
      value: 10,
      message: 'Tab数量最多为10'
    }
  }
};