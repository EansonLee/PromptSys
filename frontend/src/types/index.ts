export interface PromptRequest {
  app_name: string;
  theme: string;
  variant_folder: string;
  ui_color: string;
  reference_file?: string;
  tab_count?: number;
}

export interface PromptResponse {
  role: string;
  goal: string;
  function_output: string;
  ui_requirements: string;
  fixed_content: string;
  theme_type: string;
  raw_gpt_output: string;
  timestamp: string;
}

export interface BaseContent {
  role: string;
  goal: string;
  function_output: string;
  ui_requirements: string;
  fixed_content: string;
  theme_type: string;
}

export interface ProgressData {
  progress: number;
  status: string;
  step: string;
  result?: PromptResponse;
  error?: string;
}

export interface BatchPromptResponse {
  documents: PromptResponse[];
  total_count: number;
  generated_at: string;
}

export interface TabDocument {
  id: string;
  title: string;
  response: PromptResponse;
  isLoading?: boolean;
}