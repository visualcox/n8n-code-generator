@echo off
chcp 65001 > nul
echo ================================
echo 🚀 n8n JSON 코드 생성기 Backend 시작
echo ================================
echo.

cd backend

REM 가상환경 확인
if not exist "venv" (
    echo ❌ 가상환경이 없습니다. 먼저 install.bat을 실행해주세요.
    pause
    exit /b 1
)

REM .env 파일 확인
if not exist ".env" (
    echo ⚠️  .env 파일이 없습니다!
    echo 📝 .env.example을 복사하여 .env 파일을 만들고 API 키를 설정해주세요.
    echo.
    echo 명령어:
    echo   copy .env.example .env
    echo   notepad .env
    pause
    exit /b 1
)

echo 📦 가상환경 활성화 중...
call venv\Scripts\activate.bat

echo ✅ 준비 완료!
echo.
echo 🌐 서버를 시작합니다...
echo    - 주소: http://localhost:8000
echo    - API 문서: http://localhost:8000/docs
echo.
echo ⚠️  종료하려면 Ctrl+C를 누르세요
echo.
echo ================================
echo.

python main.py
