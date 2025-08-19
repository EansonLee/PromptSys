# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack prompt generation system (提示词生成系统) built with FastAPI backend and Next.js frontend. The system generates creative prompts for Android app development using OpenAI's GPT-4 API through LangChain integration.

## Architecture

- **Backend** (`backend/`): FastAPI service with LangChain integration
  - `main.py`: FastAPI app with CORS middleware and endpoints
  - `services/prompt_generator.py`: Core prompt generation logic using OpenAI GPT-4
- **Frontend** (`frontend/`): Next.js 15 app with TypeScript and Tailwind CSS
  - React 19 components for user input and prompt display
  - Two main components: `PromptGenerator.tsx` and `FixedContentAppender.tsx`

## Common Commands

### Backend Development
```bash
cd backend
pip install -r requirements.txt
python main.py  # Starts FastAPI server on http://localhost:8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev     # Starts Next.js dev server on http://localhost:3000
npm run build   # Build for production
npm run start   # Start production server
npm run lint    # Run ESLint
```

### Quick Start
- Windows: Run `start.bat` (opens both backend and frontend in separate terminals)
- Linux/Mac: Run `./start.sh`

## Environment Configuration

### Backend Requirements
- Create `backend/.env` with required environment variables:
  ```
  OPENAI_API_KEY=your_openai_api_key
  OPENAI_BASE_URL=https://api.openai.com/v1  # Optional, defaults to OpenAI
  SILICONFLOW_API_KEY=your_siliconflow_api_key  # Fallback API key
  BACKEND_HOST=0.0.0.0  # Server host, defaults to localhost
  BACKEND_PORT=8000     # Server port
  CORS_ORIGINS=http://localhost:3000,http://192.168.38.226:3000  # Allowed CORS origins
  ```
- Python 3.9+ required
- Dependencies: FastAPI, uvicorn, langchain, langchain-openai, pydantic, python-dotenv, openai

### Frontend Requirements
- Create `frontend/.env.local` with:
  ```
  NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # Backend API URL
  ```
- Node.js 18+ required
- Uses Next.js 15, React 19, TypeScript 5, Tailwind CSS 4, ESLint 9

## API Endpoints

### POST /generate-prompt
Generates creative prompts based on:
- `app_name`: Android app name
- `theme`: Creative theme description
- `variant_folder`: Variant folder name for code generation

Returns structured response with role, goal, function_output, ui_requirements, and raw GPT output.

### GET /health
Health check endpoint returning status and timestamp.

## Key Technical Details

- **CORS**: Backend configured for multiple origins, supports both local and remote deployment
- **Dual LLM Strategy**: Primary GPT-4 API with SiliconFlow Qwen fallback for rate limiting
- **Environment Variables**: Centralized configuration in `.env` files for easy deployment
- **Logging**: Comprehensive logging throughout backend request flow with API source identification  
- **Error Handling**: Graceful fallback parsing if GPT returns non-JSON format
- **Template System**: GPT output formatted into structured template with role, goal, functions, and UI requirements
- **Real-time Generation**: No database - pure generation service with timestamp responses
- **Enhanced Creativity**: Detailed prompt templates with bullet points, emojis, and technical specifications

## Development Notes

- Backend uses GPT-4 model with SiliconFlow Qwen fallback (configurable in `.env`)
- Frontend includes editable fixed content section for customization
- System generates detailed creative output with specific data examples and UI specifications
- Chinese language support throughout the application
- Frontend includes clipboard copy functionality for generated templates
- Supports deployment to remote servers with configurable CORS origins

## Deployment Notes

### Remote Server Deployment
- Update `CORS_ORIGINS` in backend `.env` to include your server IP addresses
- Set `NEXT_PUBLIC_API_BASE_URL` in frontend `.env.local` to point to backend server
- Ensure backend listens on `0.0.0.0` (not localhost) for remote access