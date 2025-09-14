'use client'

import React, { memo, useCallback } from 'react';
import { useForm } from 'react-hook-form';
import type { PromptRequest, ThemeOption } from '@/types';
import { validationRules } from '@/utils/formValidation';
import EnhancedTextInput from './ui/EnhancedTextInput';
import EnhancedTextarea from './ui/EnhancedTextarea';
import FormFieldEnhanced from './ui/FormFieldEnhanced';
import ColorInput from './ui/ColorInput';
import Button from './ui/Button';
import Card from './ui/Card';
import ThemeSelector from './ThemeSelector';

interface PromptFormProps {
  formData: PromptRequest;
  isLoading: boolean;
  error: string | null;
  onThemeSelect: (theme: ThemeOption) => void;
  onSubmit: (data: PromptRequest) => void;
  onTabCountChange: (count: number) => void;
}

const PromptForm: React.FC<PromptFormProps> = memo(({
  formData,
  isLoading,
  error,
  onThemeSelect,
  onSubmit,
  onTabCountChange
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setValue,
    watch
  } = useForm<PromptRequest>({
    mode: 'onChange',
    defaultValues: formData
  });
  const handleTabCountChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Math.max(1, Math.min(10, parseInt(e.target.value, 10) || 1));
    setValue('tab_count', value);
    onTabCountChange(value);
  }, [onTabCountChange, setValue]);

  const handleThemeSelect = useCallback((theme: ThemeOption) => {
    setValue('theme', theme.description);
    onThemeSelect(theme);
  }, [onThemeSelect, setValue]);

  const handleColorChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setValue('ui_color', e.target.value, { shouldValidate: true });
  }, [setValue]);

  // Register ui_color field with validation
  React.useEffect(() => {
    register('ui_color', validationRules.ui_color);
  }, [register]);

  const handleFormSubmit = handleSubmit((data) => {
    onSubmit(data);
  });

  return (
    <Card className="animate-scale-in">
      <Card.Header>
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse-glow"></div>
          <h2 className="text-2xl font-bold text-glass-primary">输入参数</h2>
        </div>
      </Card.Header>

      <Card.Content>
        <form onSubmit={handleFormSubmit} className="space-y-6" noValidate>
          {/* App Name */}
          <EnhancedTextInput
            label="APP 名称"
            name="app_name"
            placeholder="例如：免费流量直达"
            required
            registration={register('app_name', validationRules.app_name)}
            error={errors.app_name}
          />

          {/* Theme */}
          <div className="space-y-4">
            <EnhancedTextarea
              label="主题"
              name="theme"
              placeholder="例如：流量星球馆，通过读取真实流量数据，映射为星球能量值"
              rows={3}
              required
              registration={register('theme', validationRules.theme)}
              error={errors.theme}
            />

            {/* Theme Selector */}
            <ThemeSelector
              onThemeSelect={handleThemeSelect}
              selectedTheme={watch('theme')}
            />
          </div>

          {/* Variant Folder */}
          <EnhancedTextInput
            label="变体文件夹"
            name="variant_folder"
            placeholder="例如：variant_traffic137630"
            required
            helpText="只能包含字母、数字和下划线"
            registration={register('variant_folder', validationRules.variant_folder)}
            error={errors.variant_folder}
          />

          {/* UI Color with Enhanced Input - Keep unchanged as requested */}
          <ColorInput
            label="UI主色调"
            name="ui_color"
            value={watch('ui_color') || ''}
            onChange={handleColorChange}
            error={errors.ui_color?.message}
            required
            helpText="支持中文颜色名、十六进制代码等多种格式，可选择多个颜色"
          />

          {/* Reference File */}
          <EnhancedTextInput
            label="参考文件"
            name="reference_file"
            placeholder="例如：HomeFragment（自动添加@前缀和.kt后缀）"
            helpText="输入文件名（如 HomeFragment），系统会自动格式化为 @HomeFragment.kt"
            registration={register('reference_file', validationRules.reference_file)}
            error={errors.reference_file}
          />

          {/* Tab Count - Keep unchanged as requested */}
          <FormFieldEnhanced
            label="生成Tab数量"
            name="tab_count"
            type="number"
            value={watch('tab_count') || 3}
            onChange={handleTabCountChange}
            min={1}
            max={10}
            placeholder="3"
            helpText="一次生成多个不同版本的提示词文档（1-10个）"
          />

          {/* Submit Button */}
          <Button
            type="submit"
            variant="primary"
            size="lg"
            loading={isLoading}
            disabled={!isValid || isLoading}
            className="w-full"
          >
            {isLoading ? '生成中...' : '生成提示词'}
          </Button>

          {/* Error Display */}
          {error && (
            <div 
              className="p-6 glass-secondary rounded-xl border border-red-400/30 animate-fade-in" 
              role="alert"
              aria-live="polite"
            >
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <p className="text-red-400 font-semibold text-lg">发生错误</p>
                  <p className="text-glass-secondary mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}
        </form>
      </Card.Content>
    </Card>
  );
});

PromptForm.displayName = 'PromptForm';

export default PromptForm;