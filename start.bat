@echo off
echo 启动提示词生成系统...

echo.
echo 1. 启动后端服务...
cd backend
start cmd /k "python main.py"

echo.
echo 2. 启动前端服务...
cd ../frontend
start cmd /k "npm run dev"

echo.
echo 系统启动完成！
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:8000
echo API文档: http://localhost:8000/docs

pause