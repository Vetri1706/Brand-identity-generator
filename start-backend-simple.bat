@echo off
echo ====================================
echo  Starting Backend (Fallback Mode)
echo ====================================
echo.

cd /d "%~dp0backend"

echo Starting FastAPI backend on http://localhost:8000
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause
