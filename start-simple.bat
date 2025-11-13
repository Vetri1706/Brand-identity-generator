@echo off
echo.
echo ============================================
echo   Brand Identity Generator - Quick Start
echo   (NO OLLAMA NEEDED - Uses Built-in AI)
echo ============================================
echo.
echo This version uses built-in fallback generators
echo (No external AI needed, works immediately!)
echo.
pause

echo.
echo [1/3] Starting Backend API...
cd /d "%~dp0backend"
start "Backend API" cmd /k "echo Starting Backend with built-in generators... && python -m uvicorn main:app --host 127.0.0.1 --port 8000"
timeout /t 8 /nobreak >nul
echo   OK - Backend starting (check the new window)

echo.
echo [2/3] Starting Frontend...
cd /d "%~dp0frontend"
start "Frontend Dev Server" cmd /k "echo Starting Frontend... && npm run dev"
echo   OK - Frontend starting (check the new window)

echo.
echo [3/3] Opening browser...
timeout /t 10 /nobreak >nul
start http://localhost:3000

echo.
echo ============================================
echo   SUCCESS! Your app is starting up!
echo ============================================
echo.
echo Two windows have opened:
echo   1. Backend API (keep running)
echo   2. Frontend (keep running)
echo.
echo Your browser will open to: http://localhost:3000
echo (If not, open it manually)
echo.
echo NOTE: This uses built-in generators (simpler results)
echo For BETTER results, install Ollama:
echo   1. Download: https://ollama.ai/download/windows
echo   2. Run: ollama pull mistral
echo   3. Use: start-with-ollama.bat instead
echo.
echo To stop: Close both terminal windows
echo.
pause
