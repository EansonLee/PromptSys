export interface PromptRequest {
  app_name: string;
  theme: string;
  variant_folder: string;
  ui_color: string;
}

export interface PromptResponse {
  role: string;
  goal: string;
  function_output: string;
  ui_requirements: string;
  raw_gpt_output: string;
  timestamp: string;
}

export interface BaseContent {
  role: string;
  goal: string;
  function_output: string;
  ui_requirements: string;
}