#!/bin/bash

echo "================================"
echo "🚀 n8n JSON 코드 생성기 Backend 시작"
echo "================================"
echo ""

# 작업 디렉토리로 이동
cd "$(dirname "$0")/backend"

# 가상환경 활성화
echo "📦 가상환경 활성화 중..."
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ 가상환경이 없습니다. 먼저 설치를 진행해주세요."
    echo ""
    echo "설치 명령어:"
    echo "  cd backend"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다!"
    echo "📝 .env.example을 복사하여 .env 파일을 만들고 API 키를 설정해주세요."
    echo ""
    echo "명령어:"
    echo "  cp .env.example .env"
    echo "  nano .env  # 또는 원하는 에디터로 편집"
    exit 1
fi

echo "✅ 준비 완료!"
echo ""
echo "🌐 서버를 시작합니다..."
echo "   - 주소: http://localhost:8000"
echo "   - API 문서: http://localhost:8000/docs"
echo ""
echo "⚠️  종료하려면 Ctrl+C를 누르세요"
echo ""
echo "================================"
echo ""

# 서버 실행
python main.py
