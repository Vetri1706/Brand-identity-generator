#!/usr/bin/env python3
"""
Quick setup script for local development with Ollama
Installs dependencies and provides setup instructions
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a command and print output"""
    if description:
        print(f"\n📦 {description}")
    print(f"   Running: {cmd}")
    result = os.system(cmd)
    if result != 0:
        print(f"   ❌ Command failed!")
        return False
    print(f"   ✅ Done")
    return True

def main():
    print("""
╔═══════════════════════════════════════════════════════════════╗
║   🎨 Brand Identity Generator - Local Setup with Ollama      ║
║   Free, No API Keys Required!                                ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    # Check if Ollama is installed
    print("🔍 Checking for Ollama installation...")
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        print("   ✅ Ollama found!")
    except:
        print("""
   ❌ Ollama not found!
   
   Please install Ollama first:
   1. Go to https://ollama.ai
   2. Download and install for your OS
   3. Run this script again
        """)
        sys.exit(1)

    # Check if model is available
    print("\n🤖 Checking for Mistral model...")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        if "mistral" not in result.stdout:
            print("   Model not found. Pulling mistral...")
            os.system("ollama pull mistral")
        else:
            print("   ✅ Mistral model ready!")
    except:
        print("   ⚠️  Could not verify model. You may need to run: ollama pull mistral")

    # Install backend dependencies
    print("\n📦 Setting up backend...")
    backend_path = "backend"
    if os.path.exists(backend_path):
        os.chdir(backend_path)
        if platform.system() == "Windows":
            run_command("pip install -r requirements.txt", "Installing Python dependencies")
        else:
            run_command("pip3 install -r requirements.txt", "Installing Python dependencies")
        os.chdir("..")
    else:
        print(f"   ❌ Backend directory not found at {backend_path}")

    # Install frontend dependencies
    print("\n📦 Setting up frontend...")
    frontend_path = "frontend"
    if os.path.exists(frontend_path):
        os.chdir(frontend_path)
        if os.path.exists("package.json"):
            run_command("npm install", "Installing Node.js dependencies")
        else:
            print(f"   ❌ package.json not found in {frontend_path}")
        os.chdir("..")
    else:
        print(f"   ❌ Frontend directory not found at {frontend_path}")

    # Print instructions
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    ✅ Setup Complete!                        ║
╚═══════════════════════════════════════════════════════════════╝

🚀 Next Steps:

1. Start Ollama (Terminal 1):
   ollama serve

2. Start Backend (Terminal 2):
   cd backend
   python -m uvicorn main:app --reload

3. Start Frontend (Terminal 3):
   cd frontend
   npm run dev

4. Open browser:
   http://localhost:3000

📚 For more info, see: LOCAL_SETUP_OLLAMA.md
    """)

if __name__ == "__main__":
    main()
