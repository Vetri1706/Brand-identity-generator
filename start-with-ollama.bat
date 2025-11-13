@echo off
echo.
echo ============================================
echo   Brand Identity Generator - Quick Start
echo ============================================
echo.
echo This will guide you through running the app
echo with Ollama (free, local LLM)
echo.
pause

echo.
echo [1/6] Checking if Ollama is installed...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo   WARNING: Ollama not found!
    echo.
    echo   Option 1: Install Ollama for better AI results
    echo     Download: https://ollama.ai/download/windows
    echo     Then run this script again
    echo.
    echo   Option 2: Use built-in generators (simpler results)
    echo     Run: start-simple.bat instead
    echo.
    echo   Press any key to exit...
    pause >nul
    exit /b 1
)
echo   OK - Ollama is installed!

echo.
echo [2/6] Checking if Mistral model is downloaded...
ollama list | findstr mistral >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo   Mistral model not found. Downloading now...
    echo   This will take 2-5 minutes (4GB download)
    echo.
    ollama pull mistral
    if %errorlevel% neq 0 (
        echo   ERROR: Failed to download model
        pause
        exit /b 1
    )
)
echo   OK - Mistral model ready!

echo.
echo [3/6] Starting Ollama server in background...
start "Ollama Server" cmd /c "ollama serve"
timeout /t 3 /nobreak >nul
echo   OK - Ollama server started!

echo.
echo [4/6] Starting Backend API...
cd /d "%~dp0backend"
start "Backend API" cmd /k "echo Starting Backend... && python -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 5 /nobreak >nul
echo   OK - Backend starting (check the new window)

echo.
echo [5/6] Starting Frontend...
cd /d "%~dp0frontend"
start "Frontend Dev Server" cmd /k "echo Starting Frontend... && npm run dev"
echo   OK - Frontend starting (check the new window)

echo.
echo [6/6] Opening browser...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ============================================
echo   SUCCESS! Your app is starting up!
echo ============================================
echo.
echo Three windows have opened:
echo   1. Ollama Server (keep running)
echo   2. Backend API (keep running)
echo   3. Frontend (keep running)
echo.
echo Your browser will open to: http://localhost:3000
echo (If not, open it manually)
echo.
echo To stop: Close all three windows
echo.
pause
