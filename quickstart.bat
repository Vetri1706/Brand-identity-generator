@echo off
REM Quick start script for Brand Identity Generator MVP on Windows

echo.
echo ====================================
echo Brand Identity Generator MVP
echo Quick Start Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.10+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18.17+
    pause
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Create Python virtual environment
echo [1/4] Setting up backend environment...
cd backend
if not exist venv (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install backend dependencies
pip install -q -r requirements.txt
echo [OK] Backend dependencies installed

REM Create .env file if not exists
if not exist .env (
    copy .env.example .env
    echo [!] Created .env file - PLEASE ADD YOUR API KEYS
)

REM Setup frontend
echo.
echo [2/4] Setting up frontend environment...
cd ..\frontend
if not exist node_modules (
    call npm install -q
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] Frontend dependencies already installed
)

REM Create .env.local if not exists
if not exist .env.local (
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
    echo [OK] Frontend environment configured
) else (
    echo [OK] Frontend environment already configured
)

REM Setup training
echo.
echo [3/4] Setting up training environment...
cd ..\backend
REM Training uses same virtual environment

REM Create data directories
if not exist data\training (
    mkdir data\training
    echo [OK] Training data directories created
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo [NEXT STEPS]
echo.
echo 1. Add your API keys to backend\.env:
echo    - TOGETHER_API_KEY (get from https://www.together.ai)
echo    - COHERE_API_KEY (optional, from https://cohere.com)
echo.
echo 2. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
echo 3. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo [DOCUMENTATION]
echo - Setup Guide: SETUP_GUIDE.md
echo - README: README.md
echo - API Docs: http://localhost:8000/docs (when backend running)
echo.
pause
