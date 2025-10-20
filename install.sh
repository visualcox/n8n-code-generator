#!/bin/bash

echo "========================================"
echo "📦 n8n JSON 코드 생성기 설치"
echo "========================================"
echo ""

# Python 확인
echo "1️⃣  Python 확인 중..."
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python이 설치되어 있지 않습니다."
    echo "   https://www.python.org/downloads/ 에서 설치해주세요."
    exit 1
fi

PYTHON_CMD="python"
if ! command -v python &> /dev/null; then
    PYTHON_CMD="python3"
fi

echo "✅ Python 발견: $($PYTHON_CMD --version)"
echo ""

# Node.js 확인
echo "2️⃣  Node.js 확인 중..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js가 설치되어 있지 않습니다."
    echo "   https://nodejs.org/ 에서 설치해주세요."
    exit 1
fi

echo "✅ Node.js 발견: $(node --version)"
echo "✅ npm 발견: $(npm --version)"
echo ""

# Backend 설치
echo "3️⃣  Backend 설치 중..."
cd backend

if [ ! -d "venv" ]; then
    echo "   가상환경 생성 중..."
    $PYTHON_CMD -m venv venv
fi

echo "   가상환경 활성화 중..."
source venv/bin/activate

echo "   Python 패키지 설치 중... (5-10분 소요)"
pip install --upgrade pip
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo ""
    echo "   ⚠️  .env 파일 생성 필요!"
    echo "   .env.example을 복사하여 .env 파일을 만들고"
    echo "   OpenAI API 키를 설정해주세요."
    echo ""
    cp .env.example .env
    echo "   ✅ .env 파일이 생성되었습니다."
    echo "   📝 이제 .env 파일을 편집하여 API 키를 입력하세요:"
    echo "      nano .env"
fi

cd ..
echo "✅ Backend 설치 완료!"
echo ""

# Frontend 설치
echo "4️⃣  Frontend 설치 중..."
cd frontend

echo "   npm 패키지 설치 중... (5-10분 소요)"
npm install

cd ..
echo "✅ Frontend 설치 완료!"
echo ""

# 실행 스크립트 실행 권한 부여
chmod +x start_backend.sh
chmod +x start_frontend.sh

echo "========================================"
echo "🎉 설치가 완료되었습니다!"
echo "========================================"
echo ""
echo "📝 다음 단계:"
echo ""
echo "1. OpenAI API 키 설정"
echo "   - backend/.env 파일을 열어서"
echo "   - OPENAI_API_KEY=여기에_API_키_입력"
echo "   - 저장하세요"
echo ""
echo "2. Backend 실행 (터미널 1)"
echo "   ./start_backend.sh"
echo ""
echo "3. Frontend 실행 (터미널 2)"
echo "   ./start_frontend.sh"
echo ""
echo "4. 브라우저에서 열기"
echo "   http://localhost:3000"
echo ""
echo "자세한 내용은 '비개발자를_위한_실행_가이드.md'를 참조하세요!"
echo ""
