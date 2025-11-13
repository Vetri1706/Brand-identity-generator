@echo off
echo ============================================
echo  Brand Identity Generator - FIXED VERSION
echo  (Uses Fast Built-in Generators)
echo ============================================
echo.
echo This version uses FAST built-in generators
echo No Ollama needed - works instantly!
echo.
pause

echo.
echo [Step 1/2] Starting Backend...
start "Backend Server" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo [Step 2/2] Starting Frontend...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Waiting for frontend to start...
timeout /t 10 /nobreak > nul

echo.
echo ============================================
echo  ✅ ALL DONE!
echo ============================================
echo.
echo Your app is running at:
echo   Frontend: http://localhost:3000
echo   Backend:  http://localhost:8000
echo.
echo Two windows opened:
echo   1. Backend Server (Python)
echo   2. Frontend Server (Node.js)
echo.
echo Keep both windows open!
echo.
echo Opening browser...
start http://localhost:3000
echo.
echo ============================================
echo  Ready to create amazing brands!
echo ============================================
echo.
pause
