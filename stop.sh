#!/bin/bash

echo "================================================"
echo "🛑 n8n AI Workflow Generator - 종료"
echo "================================================"
echo ""

# PID 파일에서 프로세스 ID 읽기
if [ -f /tmp/n8n-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/n8n-backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        echo "🔧 Backend 종료 중... (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
        echo "   ✅ Backend 종료됨"
    else
        echo "⚠️  Backend가 이미 종료되었습니다"
    fi
    rm -f /tmp/n8n-backend.pid
else
    echo "⚠️  Backend PID 파일을 찾을 수 없습니다"
fi

echo ""

if [ -f /tmp/n8n-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/n8n-frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "🎨 Frontend 종료 중... (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
        echo "   ✅ Frontend 종료됨"
    else
        echo "⚠️  Frontend가 이미 종료되었습니다"
    fi
    rm -f /tmp/n8n-frontend.pid
else
    echo "⚠️  Frontend PID 파일을 찾을 수 없습니다"
fi

# 추가로 포트를 사용하는 프로세스 정리
echo ""
echo "🔍 포트 8000, 3000 사용 프로세스 확인 중..."

# 포트 8000 (Backend)
PID_8000=$(lsof -ti:8000 2>/dev/null)
if [ ! -z "$PID_8000" ]; then
    echo "   🔧 포트 8000 정리 중..."
    kill -9 $PID_8000 2>/dev/null
    echo "   ✅ 포트 8000 정리됨"
fi

# 포트 3000 (Frontend)
PID_3000=$(lsof -ti:3000 2>/dev/null)
if [ ! -z "$PID_3000" ]; then
    echo "   🎨 포트 3000 정리 중..."
    kill -9 $PID_3000 2>/dev/null
    echo "   ✅ 포트 3000 정리됨"
fi

# 로그 파일 정리 (선택사항)
if [ "$1" == "--clean" ]; then
    echo ""
    echo "🧹 로그 파일 정리 중..."
    rm -f /tmp/n8n-backend.log
    rm -f /tmp/n8n-frontend.log
    echo "   ✅ 로그 파일 정리됨"
fi

echo ""
echo "================================================"
echo "✅ 모든 프로세스가 종료되었습니다!"
echo "================================================"
echo ""
