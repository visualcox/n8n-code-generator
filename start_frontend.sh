#!/bin/bash

echo "================================"
echo "🎨 n8n JSON 코드 생성기 Frontend 시작"
echo "================================"
echo ""

# 작업 디렉토리로 이동
cd "$(dirname "$0")/frontend"

# node_modules 확인
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules가 없습니다. 먼저 설치를 진행해주세요."
    echo ""
    echo "설치 명령어:"
    echo "  cd frontend"
    echo "  npm install"
    exit 1
fi

echo "✅ 준비 완료!"
echo ""
echo "🌐 개발 서버를 시작합니다..."
echo "   - 주소: http://localhost:3000"
echo ""
echo "⚠️  종료하려면 Ctrl+C를 누르세요"
echo ""
echo "================================"
echo ""

# 개발 서버 실행
npm run dev
