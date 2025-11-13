#!/bin/bash

# Quick start script for Brand Identity Generator MVP on macOS/Linux

echo ""
echo "===================================="
echo "Brand Identity Generator MVP"
echo "Quick Start Script"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed. Please install Node.js 18.17+"
    exit 1
fi

echo "[OK] Python and Node.js are installed"
echo ""

# Create Python virtual environment
echo "[1/4] Setting up backend environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies
pip install -q -r requirements.txt
echo "[OK] Backend dependencies installed"

# Create .env file if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "[!] Created .env file - PLEASE ADD YOUR API KEYS"
fi

# Setup frontend
echo ""
echo "[2/4] Setting up frontend environment..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install -q
    echo "[OK] Frontend dependencies installed"
else
    echo "[OK] Frontend dependencies already installed"
fi

# Create .env.local if not exists
if [ ! -f ".env.local" ]; then
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
    echo "[OK] Frontend environment configured"
else
    echo "[OK] Frontend environment already configured"
fi

# Setup training
echo ""
echo "[3/4] Setting up training environment..."
cd ../backend
# Training uses same virtual environment

# Create data directories
mkdir -p data/training
echo "[OK] Training data directories created"

echo ""
echo "===================================="
echo "Setup Complete!"
echo "===================================="
echo ""
echo "[NEXT STEPS]"
echo ""
echo "1. Add your API keys to backend/.env:"
echo "   - TOGETHER_API_KEY (get from https://www.together.ai)"
echo "   - COHERE_API_KEY (optional, from https://cohere.com)"
echo ""
echo "2. Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Start Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "[DOCUMENTATION]"
echo "- Setup Guide: SETUP_GUIDE.md"
echo "- README: README.md"
echo "- API Docs: http://localhost:8000/docs (when backend running)"
echo ""
