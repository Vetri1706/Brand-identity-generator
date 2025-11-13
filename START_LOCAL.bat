@echo off
REM Brand Identity Generator - Local Startup Script
REM Start this script, then run the commands in separate terminals

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║   🎨 Brand Identity Generator - Local Setup with Ollama      ║
echo ║   Starting services...                                        ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo ✅ Prerequisites Check:
echo.

REM Check if Ollama is installed
echo 1. Checking Ollama...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ Ollama not found. Download from https://ollama.ai
    pause
    exit /b 1
) else (
    echo   ✅ Ollama found
)

REM Check if Python is installed
echo 2. Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ❌ Python not found. Install Python 3.8+
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo   ✅ %PYTHON_VERSION%
)

REM Check if Node.js is installed
echo 3. Checking Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ⚠️  Node.js not found. Install from https://nodejs.org
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
    echo   ✅ Node.js !NODE_VERSION!
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                 📋 Next Steps (3 Terminals)                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo Terminal 1 - Start Ollama:
echo   C:\Users\%USERNAME%^> ollama serve
echo.

echo Terminal 2 - Start Backend:
echo   C:\Users\%USERNAME%^> cd "%CD%\backend"
echo   C:\Users\%USERNAME%\...\backend^> python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.

echo Terminal 3 - Start Frontend:
echo   C:\Users\%USERNAME%^> cd "%CD%\frontend"
echo   C:\Users\%USERNAME%\...\frontend^> npm install ^(first time only^)
echo   C:\Users\%USERNAME%\...\frontend^> npm run dev
echo.

echo Then open: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.

pause
