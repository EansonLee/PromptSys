import type { ThemeOption } from '@/types';

export const BUILT_IN_THEMES: readonly ThemeOption[] = [
  {
    id: 'wifi_creative_checkin',
    name: 'WiFi-无功能',
    description: '无需WiFi实际功能、创意功能',
    icon: '🌟'
  },
  {
    id: 'wifi_real_scanning',
    name: 'WiFi真实扫描',
    description: '需要有WiFi实际功能、创意功能',
    icon: '📡'
  },
  {
    id: 'clean_creative_ball',
    name: '清理创意球',
    description: '清理、不需要真实的清理功能、创意',
    icon: '🧹'
  },
  {
    id: 'magnify_emotion',
    name: '放大创意',
    description: '无实际放大功能、创意',
    icon: '🔍'
  },
  {
    id: 'magnify_memory',
    name: '字体放大',
    description: '系统字体放大功能、创意',
    icon: '💭'
  },
  {
    id: 'traffic_real_monitor',
    name: '流量真实监控',
    description: '流量、需要真实流量数据、创意可视化',
    icon: '📊'
  },
  {
    id: 'traffic_creative_planet',
    name: '流量星球馆',
    description: '流量、不需要真实流量功能、创意',
    icon: '🌌'
  }
] as const;

export const DEFAULT_FORM_VALUES = {
  app_name: '',
  theme: '',
  variant_folder: '',
  ui_color: '',
  reference_file: '',
  tab_count: 3
} as const;

export const VALIDATION_RULES = {
  app_name: {
    required: 'APP 名称不能为空',
    minLength: { value: 2, message: 'APP 名称至少需要2个字符' },
    maxLength: { value: 50, message: 'APP 名称不能超过50个字符' }
  },
  theme: {
    required: '主题不能为空',
    minLength: { value: 5, message: '主题描述至少需要5个字符' },
    maxLength: { value: 500, message: '主题描述不能超过500个字符' }
  },
  variant_folder: {
    required: '变体文件夹不能为空',
    pattern: {
      value: /^[a-zA-Z0-9_]+$/,
      message: '变体文件夹只能包含字母、数字和下划线'
    }
  },
  ui_color: {
    required: 'UI主色调不能为空'
  },
  reference_file: {
    // Optional field, no validation rules needed but included for completeness
  },
  tab_count: {
    min: { value: 1, message: '最少生成1个版本' },
    max: { value: 10, message: '最多生成10个版本' }
  }
} as const;

export const API_ENDPOINTS = {
  GENERATE_PROMPT: '/generate-prompt-stream',
  OPEN_CLAUDE_CLI: '/open-claude-cli',
  GET_REPOSITORY: '/get-repository',
  GET_TASKS: '/get-tasks',
  EXECUTE_TASKS: '/execute-tasks'
} as const;