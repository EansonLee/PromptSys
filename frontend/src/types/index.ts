// API Request/Response Types
export interface PromptRequest {
  readonly app_name: string;
  readonly theme: string;
  readonly variant_folder: string;
  readonly ui_color: string;
  readonly reference_file?: string;
  readonly tab_count?: number;
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

// Form and Validation Types
export interface FormErrors {
  app_name?: string;
  theme?: string;
  variant_folder?: string;
  ui_color?: string;
  reference_file?: string;
  tab_count?: string;
}

export interface FormTouched {
  app_name?: boolean;
  theme?: boolean;
  variant_folder?: boolean;
  ui_color?: boolean;
  reference_file?: boolean;
  tab_count?: boolean;
}

// API Error Types
export interface APIError {
  readonly error: string;
  readonly details?: string;
  readonly code?: string;
}

// Hook Return Types
export interface UsePromptGeneratorReturn {
  readonly formData: PromptRequest;
  readonly setFormData: React.Dispatch<React.SetStateAction<PromptRequest>>;
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly generatePrompt: (data: PromptRequest) => Promise<void>;
  readonly generateBatch: (data: PromptRequest) => Promise<void>;
}

export interface UseTabsReturn {
  readonly tabs: readonly TabDocument[];
  readonly activeTab: string | null;
  readonly setActiveTab: (id: string) => void;
  readonly addTab: (tab: TabDocument) => void;
  readonly updateTab: (id: string, updates: Partial<TabDocument>) => void;
  readonly removeTab: (id: string) => void;
  readonly clearTabs: () => void;
}

// Event Handler Types
export type InputChangeHandler = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
export type ButtonClickHandler = (event: React.MouseEvent<HTMLButtonElement>) => void;
export type FormSubmitHandler = (event: React.FormEvent<HTMLFormElement>) => void;

// Constants and Enums
export const THEME_TYPES = {
  WIFI_CREATIVE: 'wifi_creative_checkin',
  WIFI_SCANNING: 'wifi_real_scanning',
  CLEAN_CREATIVE: 'clean_creative_ball',
  MAGNIFY_EMOTION: 'magnify_emotion',
  MAGNIFY_MEMORY: 'magnify_memory',
  TRAFFIC_MONITOR: 'traffic_real_monitor',
  TRAFFIC_PLANET: 'traffic_creative_planet',
  DEFAULT: 'default'
} as const;

export type ThemeType = typeof THEME_TYPES[keyof typeof THEME_TYPES];

// Color-related Types
export interface ColorInfo {
  readonly original: string;    // 原始输入
  readonly hex: string;        // 十六进制格式
  readonly rgb: string;        // RGB格式
  readonly isValid: boolean;   // 是否是有效颜色
}

export interface ParsedColors {
  readonly colors: readonly ColorInfo[];
  readonly hasValidColors: boolean;
  readonly invalidInputs: readonly string[];
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