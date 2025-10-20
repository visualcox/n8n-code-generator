@echo off
chcp 65001 > nul
echo ================================
echo 🎨 n8n JSON 코드 생성기 Frontend 시작
echo ================================
echo.

cd frontend

REM node_modules 확인
if not exist "node_modules" (
    echo ❌ node_modules가 없습니다. 먼저 install.bat을 실행해주세요.
    pause
    exit /b 1
)

echo ✅ 준비 완료!
echo.
echo 🌐 개발 서버를 시작합니다...
echo    - 주소: http://localhost:3000
echo.
echo ⚠️  종료하려면 Ctrl+C를 누르세요
echo.
echo ================================
echo.

call npm run dev
