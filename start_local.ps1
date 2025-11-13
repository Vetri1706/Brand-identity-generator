# Brand Identity Generator - PowerShell Startup Script
# Usage: .\start_local.ps1

param(
    [switch]$SkipOllama = $false,
    [string]$Model = "mistral"
)

function Write-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  $Text" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step {
    param([string]$Text, [string]$Status = "")
    if ($Status -eq "OK") {
        Write-Host "✅ $Text" -ForegroundColor Green
    } elseif ($Status -eq "WARN") {
        Write-Host "⚠️  $Text" -ForegroundColor Yellow
    } elseif ($Status -eq "ERROR") {
        Write-Host "❌ $Text" -ForegroundColor Red
    } else {
        Write-Host "▶️  $Text" -ForegroundColor Cyan
    }
}

Write-Header "🎨 Brand Identity Generator - Local Setup"

# Check prerequisites
Write-Host "📋 Checking Prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version
    Write-Step "Python: $pythonVersion" "OK"
} catch {
    Write-Step "Python not found. Install from https://python.org" "ERROR"
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Step "Node.js: $nodeVersion" "OK"
} catch {
    Write-Step "Node.js not found. Install from https://nodejs.org" "WARN"
}

# Check npm
try {
    $npmVersion = npm --version
    Write-Step "npm: $npmVersion" "OK"
} catch {
    Write-Step "npm not found" "ERROR"
    exit 1
}

# Check Ollama
if (-not $SkipOllama) {
    try {
        $ollamaVersion = ollama --version
        Write-Step "Ollama: $ollamaVersion" "OK"
    } catch {
        Write-Step "Ollama not found. Install from https://ollama.ai" "ERROR"
        exit 1
    }
}

Write-Host ""
Write-Header "🚀 Starting Services"
Write-Host ""

# Get project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Step "Backend path: $projectRoot\backend"
Write-Step "Frontend path: $projectRoot\frontend"
Write-Host ""

# Instructions
Write-Header "📋 FOLLOW THESE STEPS IN 3 SEPARATE TERMINALS"

Write-Host "TERMINAL 1 - Start Ollama:" -ForegroundColor Yellow
Write-Host @"
  PS> ollama serve

  This will be the "AI Brain" running at http://localhost:11434
  Keep this running!
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "TERMINAL 2 - Start Backend:" -ForegroundColor Yellow
Write-Host @"
  PS> cd "$projectRoot\backend"
  PS> python -m uvicorn main:app --reload

  Backend API runs at http://localhost:8000
  Keep this running!
"@ -ForegroundColor Gray

Write-Host ""
Write-Host "TERMINAL 3 - Start Frontend:" -ForegroundColor Yellow
Write-Host @"
  PS> cd "$projectRoot\frontend"
  PS> npm run dev

  Frontend runs at http://localhost:3000
  Keep this running!
"@ -ForegroundColor Gray

Write-Host ""
Write-Header "✅ THEN OPEN IN BROWSER"
Write-Host "🌐 http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "📚 Check these:" -ForegroundColor Yellow
Write-Host "  • API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "  • Health Check: http://localhost:8000/health" -ForegroundColor Gray
Write-Host "  • Ollama Status: http://localhost:11434/api/tags" -ForegroundColor Gray
Write-Host ""

# Quick setup commands
Write-Header "🛠️ QUICK SETUP COMMANDS"

Write-Host "Install backend dependencies:" -ForegroundColor Yellow
Write-Host "  cd `"$projectRoot\backend`"" -ForegroundColor Gray
Write-Host "  pip install -r requirements.txt" -ForegroundColor Gray
Write-Host ""

Write-Host "Install frontend dependencies:" -ForegroundColor Yellow
Write-Host "  cd `"$projectRoot\frontend`"" -ForegroundColor Gray
Write-Host "  npm install" -ForegroundColor Gray
Write-Host ""

Write-Host "Pull Ollama model (first time only):" -ForegroundColor Yellow
Write-Host "  ollama pull $Model" -ForegroundColor Gray
Write-Host ""

Write-Header "💡 HELPFUL COMMANDS"

Write-Host "List Ollama models:" -ForegroundColor Gray
Write-Host "  ollama list" -ForegroundColor Cyan
Write-Host ""

Write-Host "Remove Ollama model:" -ForegroundColor Gray
Write-Host "  ollama rm mistral" -ForegroundColor Cyan
Write-Host ""

Write-Host "Test backend health:" -ForegroundColor Gray
Write-Host "  curl http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""

Write-Host "View available models at:" -ForegroundColor Yellow
Write-Host "  https://ollama.ai/library" -ForegroundColor Cyan
Write-Host ""

Write-Header "✨ YOU'RE READY!"

Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Open 3 terminals" -ForegroundColor Gray
Write-Host "  2. Follow the TERMINAL instructions above" -ForegroundColor Gray
Write-Host "  3. Open http://localhost:3000 in browser" -ForegroundColor Gray
Write-Host "  4. Generate your first brand! 🎨" -ForegroundColor Gray
Write-Host ""
