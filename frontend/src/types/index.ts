// API Request/Response Types
export interface PromptRequest {
  readonly app_name: string;
  readonly theme: string;
  readonly variant_folder: string;
  readonly ui_color: string;
  readonly reference_file?: string;
  readonly tab_count?: number;
  readonly prompt_type?: 'android' | 'frontend';
}

export interface PromptResponse {
  readonly role: string;
  readonly goal: string;
  readonly function_output: string;
  readonly ui_requirements: string;
  readonly fixed_content: string;
  readonly theme_type: string;
  readonly raw_gpt_output: string;
  readonly timestamp: string;
}

export interface BaseContent {
  readonly role: string;
  readonly goal: string;
  readonly function_output: string;
  readonly ui_requirements: string;
  readonly fixed_content: string;
  readonly theme_type: string;
}

// Progress and State Types
export type ProgressStep = 
  | '初始化'
  | '参数验证'
  | 'GPT连接'
  | 'GPT处理'
  | '内容解析'
  | '结果封装'
  | '完成';

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface ProgressData {
  readonly progress: number;
  readonly status: string;
  readonly step: ProgressStep;
  readonly result?: PromptResponse;
  readonly error?: string;
}

export interface BatchPromptResponse {
  readonly documents: readonly PromptResponse[];
  readonly total_count: number;
  readonly generated_at: string;
}

// UI State Types
export interface TabDocument {
  readonly id: string;
  readonly title: string;
  readonly response: PromptResponse;
  readonly isLoading: boolean;
}

export interface ThemeOption {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly icon: string;
}

export type PromptType = 'android' | 'frontend';

export interface PromptTypeOption {
  readonly value: PromptType;
  readonly label: string;
  readonly description: string;
  readonly icon: string;
}

// Form validation types removed - using react-hook-form instead

// API Error Types
export interface APIError {
  readonly error: string;
  readonly details?: string;
  readonly code?: string;
}

// Hook return types moved to respective hook files for better locality

// Constants moved to constants/themes.ts for better organization

// Color-related Types
export interface ColorInfo {
  readonly original: string;    // 原始输入
  readonly hex: string;        // 十六进制格式
  readonly rgb: string;        // RGB格式
  readonly isValid: boolean;   // 是否是有效颜色
}

export interface ParsedColors {
  colors: ColorInfo[];
  hasValidColors: boolean;
  invalidInputs: string[];
}

export interface ColorPickerState {
  readonly isOpen: boolean;
  readonly selectedColor: string;
  readonly recentColors: readonly string[];
}

// Utility Types
export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};