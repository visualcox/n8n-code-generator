#!/bin/bash

echo "================================================"
echo "🚀 n8n AI Workflow Generator - 원클릭 실행"
echo "================================================"
echo ""
echo "📦 Backend와 Frontend를 동시에 시작합니다..."
echo ""

# 현재 스크립트의 디렉토리로 이동
cd "$(dirname "$0")"

# Backend 실행 (백그라운드)
echo "🔧 Backend 시작 중..."
./start_backend.sh > /tmp/n8n-backend.log 2>&1 &
BACKEND_PID=$!
echo "   ✅ Backend 시작됨 (PID: $BACKEND_PID)"
echo "   📄 로그: /tmp/n8n-backend.log"

# Backend가 준비될 때까지 대기
echo ""
echo "⏳ Backend 초기화 대기 중..."
sleep 5

# Frontend 실행 (백그라운드)
echo ""
echo "🎨 Frontend 시작 중..."
cd frontend
npm run dev > /tmp/n8n-frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
echo "   ✅ Frontend 시작됨 (PID: $FRONTEND_PID)"
echo "   📄 로그: /tmp/n8n-frontend.log"

# 프로세스 ID 저장
echo "$BACKEND_PID" > /tmp/n8n-backend.pid
echo "$FRONTEND_PID" > /tmp/n8n-frontend.pid

echo ""
echo "================================================"
echo "✨ 실행 완료!"
echo "================================================"
echo ""
echo "🌐 브라우저에서 접속하세요:"
echo "   👉 http://localhost:3000"
echo ""
echo "📊 서버 상태:"
echo "   - Backend:  http://localhost:8000"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "📝 로그 확인:"
echo "   tail -f /tmp/n8n-backend.log"
echo "   tail -f /tmp/n8n-frontend.log"
echo ""
echo "🛑 종료 방법:"
echo "   ./stop.sh"
echo ""
echo "================================================"

# 브라우저 자동 열기 (5초 후)
sleep 5
if command -v open &> /dev/null; then
    echo "🌐 브라우저를 자동으로 엽니다..."
    open http://localhost:3000
fi

echo ""
echo "✅ 앱이 실행 중입니다!"
echo "   종료하려면: ./stop.sh"
echo ""
