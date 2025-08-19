#!/bin/bash

echo "启动提示词生成系统..."

echo ""
echo "1. 启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!

echo ""
echo "2. 等待后端启动..."
sleep 5

echo ""
echo "3. 启动前端服务..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "系统启动完成！"
echo "前端地址: http://localhost:3000"
echo "后端地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait