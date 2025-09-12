'use client'

import React, { memo, useCallback } from 'react';
import type { PromptRequest, FormErrors, FormTouched, ThemeOption } from '@/types';
import FormField from './ui/FormField';
import FormFieldEnhanced from './ui/FormFieldEnhanced';
import ColorInput from './ui/ColorInput';
import Button from './ui/Button';
import Card from './ui/Card';
import ThemeSelector from './ThemeSelector';

interface PromptFormProps {
  formData: PromptRequest;
  errors: FormErrors;
  touched: FormTouched;
  isValid: boolean;
  isLoading: boolean;
  error: string | null;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
  onThemeSelect: (theme: ThemeOption) => void;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  onTabCountChange: (count: number) => void;
}

const PromptForm: React.FC<PromptFormProps> = memo(({
  formData,
  errors,
  touched,
  isValid,
  isLoading,
  error,
  onInputChange,
  onThemeSelect,
  onSubmit,
  onTabCountChange
}) => {
  // 从环境变量读取隐藏配置
  const showVariantAndReferenceFields = process.env.NEXT_PUBLIC_SHOW_VARIANT_AND_REFERENCE_FIELDS === 'true';
  
  const handleTabCountChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = Math.max(1, Math.min(10, parseInt(e.target.value, 10) || 1));
    onTabCountChange(value);
  }, [onTabCountChange]);

  const handleThemeSelect = useCallback((theme: ThemeOption) => {
    onThemeSelect(theme);
  }, [onThemeSelect]);

  return (
    <Card className="animate-scale-in">
      <Card.Header>
        <div className="flex items-center space-x-3">
          <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse-glow"></div>
          <h2 className="text-2xl font-bold text-glass-primary">输入参数</h2>
        </div>
      </Card.Header>

      <Card.Content>
        <form onSubmit={onSubmit} className="space-y-6" noValidate>
          {/* App Name */}
          <FormFieldEnhanced
            label="APP 名称"
            name="app_name"
            type="text"
            value={formData.app_name}
            onChange={onInputChange}
            error={errors.app_name}
            touched={touched.app_name}
            placeholder="例如：免费流量直达"
            required
          />

          {/* Theme */}
          <div className="space-y-4">
            <FormFieldEnhanced
              label="主题"
              name="theme"
              value={formData.theme}
              onChange={onInputChange}
              error={errors.theme}
              touched={touched.theme}
              placeholder="例如：流量星球馆，通过读取真实流量数据，映射为星球能量值"
              rows={3}
              required
            />

            {/* Theme Selector */}
            <ThemeSelector
              onThemeSelect={handleThemeSelect}
              selectedTheme={formData.theme}
            />
          </div>

          {/* Variant Folder - 条件显示 */}
          {showVariantAndReferenceFields && (
            <FormFieldEnhanced
              label="变体文件夹"
              name="variant_folder"
              type="text"
              value={formData.variant_folder}
              onChange={onInputChange}
              error={errors.variant_folder}
              touched={touched.variant_folder}
              placeholder="例如：variant_traffic137630"
              required
              helpText="只能包含字母、数字和下划线"
            />
          )}

          {/* UI Color with Enhanced Input */}
          <ColorInput
            label="UI主色调"
            name="ui_color"
            value={formData.ui_color}
            onChange={onInputChange}
            error={errors.ui_color}
            touched={touched.ui_color}
            placeholder="例如：#FF0000、绿色、紫色梦幻"
            required
            helpText="支持中文颜色名、十六进制代码等多种格式，可选择多个颜色"
          />

          {/* Reference File - 条件显示 */}
          {showVariantAndReferenceFields && (
            <FormFieldEnhanced
              label="参考文件"
              name="reference_file"
              type="text"
              value={formData.reference_file || ''}
              onChange={onInputChange}
              placeholder="例如：HomeFragment（自动添加@前缀和.kt后缀）"
              helpText="输入文件名（如 HomeFragment），系统会自动格式化为 @HomeFragment.kt"
            />
          )}

          {/* Tab Count */}
          <FormFieldEnhanced
            label="生成Tab数量"
            name="tab_count"
            type="number"
            value={formData.tab_count || 3}
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