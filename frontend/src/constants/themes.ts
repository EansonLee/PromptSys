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
};

export const API_ENDPOINTS = {
  GENERATE_PROMPT: '/generate-prompt-stream',
  OPEN_CLAUDE_CLI: '/open-claude-cli',
  GET_REPOSITORY: '/get-repository',
  GET_TASKS: '/get-tasks',
  EXECUTE_TASKS: '/execute-tasks'
} as const;