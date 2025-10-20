@echo off
chcp 65001 > nul
echo ========================================
echo 📦 n8n JSON 코드 생성기 설치
echo ========================================
echo.

REM Python 확인
echo 1️⃣  Python 확인 중...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되어 있지 않습니다.
    echo    https://www.python.org/downloads/ 에서 설치해주세요.
    echo    설치 시 "Add Python to PATH" 체크박스를 꼭 체크하세요!
    pause
    exit /b 1
)
python --version
echo.

REM Node.js 확인
echo 2️⃣  Node.js 확인 중...
node --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js가 설치되어 있지 않습니다.
    echo    https://nodejs.org/ 에서 설치해주세요.
    pause
    exit /b 1
)
node --version
npm --version
echo.

REM Backend 설치
echo 3️⃣  Backend 설치 중...
cd backend

if not exist "venv" (
    echo    가상환경 생성 중...
    python -m venv venv
)

echo    가상환경 활성화 중...
call venv\Scripts\activate.bat

echo    Python 패키지 설치 중... (5-10분 소요)
python -m pip install --upgrade pip
pip install -r requirements.txt

if not exist ".env" (
    echo.
    echo    ⚠️  .env 파일 생성 필요!
    echo    .env.example을 복사하여 .env 파일을 만듭니다...
    copy .env.example .env
    echo    ✅ .env 파일이 생성되었습니다.
    echo    📝 이제 backend\.env 파일을 열어서 API 키를 입력하세요!
    echo.
)

cd ..
echo ✅ Backend 설치 완료!
echo.

REM Frontend 설치
echo 4️⃣  Frontend 설치 중...
cd frontend

echo    npm 패키지 설치 중... (5-10분 소요)
call npm install

cd ..
echo ✅ Frontend 설치 완료!
echo.

echo ========================================
echo 🎉 설치가 완료되었습니다!
echo ========================================
echo.
echo 📝 다음 단계:
echo.
echo 1. OpenAI API 키 설정
echo    - backend\.env 파일을 메모장으로 열어서
echo    - OPENAI_API_KEY=여기에_실제_API_키_입력
echo    - 저장하세요
echo.
echo 2. Backend 실행 (명령 프롬프트 1)
echo    start_backend.bat
echo.
echo 3. Frontend 실행 (명령 프롬프트 2)
echo    start_frontend.bat
echo.
echo 4. 브라우저에서 열기
echo    http://localhost:3000
echo.
echo 자세한 내용은 '비개발자를_위한_실행_가이드.md'를 참조하세요!
echo.
pause
