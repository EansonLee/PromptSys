export interface PromptRequest {
  app_name: string;
  theme: string;
  variant_folder: string;
  ui_color: string;
  reference_file?: string;
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