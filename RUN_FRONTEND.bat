@echo off
REM Start Plug Spotter Pro Frontend Server
REM This script installs dependencies and runs the React/Vite dev server

echo.
echo ========================================
echo  PLUG SPOTTER PRO - Frontend Server
echo ========================================
echo.

REM Change to project root
cd /d "%~dp0"

REM Install dependencies if not already installed
echo Installing npm dependencies...
call npm install --legacy-peer-deps

REM Start frontend server
echo.
echo ========================================
echo  Starting Frontend on http://localhost:5173
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause
