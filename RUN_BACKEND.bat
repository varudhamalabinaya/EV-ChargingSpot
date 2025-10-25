@echo off
REM Start Plug Spotter Pro Backend Server
REM This script installs dependencies and runs the FastAPI backend

echo.
echo ========================================
echo  PLUG SPOTTER PRO - Backend Server
echo ========================================
echo.

REM Change to project root
cd /d "%~dp0"

REM Install dependencies if not already installed
echo Installing Python dependencies...
python -m pip install -q fastapi uvicorn motor pymongo pydantic pydantic-settings python-jose passlib python-multipart python-dotenv cryptography

REM Change to backend directory
cd backend

REM Start backend server
echo.
echo ========================================
echo  Starting Backend on http://localhost:8000
echo ========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
