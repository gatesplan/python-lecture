@echo off
echo ========================================
echo Python Exercise Problem Renderer
echo ========================================
echo.
echo Starting local server...
echo Server will run on: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"

REM 서버 시작 후 3초 대기 후 브라우저 열기
start "" cmd /c "timeout /t 3 >nul && start http://localhost:8000"

python -m http.server 8000

pause