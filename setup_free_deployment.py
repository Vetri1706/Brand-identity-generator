#!/usr/bin/env python3
"""
FREE DEPLOYMENT SETUP SCRIPT
Prepares your logo generator for free deployment
"""

import os
import json
import subprocess
import sys

def create_deployment_files():
    """Create all necessary deployment configuration files"""
    
    print("🚀 Setting up FREE deployment configuration...")
    
    # Create Procfile for Heroku (backup option)
    procfile_content = "web: cd backend && python main.py"
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    print("✅ Created Procfile")
    
    # Create requirements.txt for backend
    requirements_content = """fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pillow>=10.0.1
pydantic>=2.5.0
python-multipart>=0.0.6
starlette>=0.27.0
"""
    
    backend_req_path = os.path.join("backend", "requirements.txt")
    if not os.path.exists(backend_req_path):
        with open(backend_req_path, "w") as f:
            f.write(requirements_content)
        print("✅ Created backend/requirements.txt")
    
    # Create package.json for frontend if not exists
    frontend_pkg_path = os.path.join("frontend", "package.json")
    if not os.path.exists(frontend_pkg_path):
        package_json = {
            "name": "logo-generator-frontend",
            "version": "1.0.0",
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "14.0.3",
                "react": "18.2.0",
                "react-dom": "18.2.0"
            },
            "engines": {
                "node": ">=18.0.0"
            }
        }
        with open(frontend_pkg_path, "w") as f:
            json.dump(package_json, f, indent=2)
        print("✅ Created frontend/package.json")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
*.log

# Node.js
node_modules/
.next/
npm-debug.log*

# Environment variables
.env
.env.local
.env.production.local

# IDEs
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Generated logos (for testing)
test_*.png
logo_diversity_report.json
"""
    
    if not os.path.exists(".gitignore"):
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print("✅ Created .gitignore")
    
    print("\n🎯 FREE DEPLOYMENT OPTIONS:")
    print("1. 🚂 Railway.app - Best for Python backend (Recommended)")
    print("2. 🎨 Render.com - Alternative Python hosting")
    print("3. ⚡ Vercel - Best for Next.js frontend")
    print("4. 🆓 Netlify - Alternative frontend hosting")
    
    print("\n📋 QUICK DEPLOYMENT STEPS:")
    print("1. Push code to GitHub:")
    print("   git init")
    print("   git add .")
    print('   git commit -m "Professional Logo Generator"')
    print("   git push origin main")
    print("")
    print("2. Deploy backend on Railway.app:")
    print("   - Sign up at railway.app")
    print("   - Import from GitHub")
    print("   - Auto-deployed! 🎉")
    print("")
    print("3. Deploy frontend on Vercel:")
    print("   - Sign up at vercel.com")
    print("   - Import from GitHub")
    print("   - Set root directory to 'frontend'")
    print("   - Auto-deployed! 🎉")

def check_git_setup():
    """Check if git is set up"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository detected")
            return True
        else:
            print("⚠️ No git repository found")
            print("Run: git init")
            return False
    except FileNotFoundError:
        print("❌ Git not installed")
        return False

def main():
    print("🎨 REVOLUTIONARY LOGO GENERATOR - FREE DEPLOYMENT SETUP")
    print("=" * 60)
    
    create_deployment_files()
    
    print("\n🔍 Checking git setup...")
    check_git_setup()
    
    print("\n🎉 DEPLOYMENT SETUP COMPLETE!")
    print("\n📚 Check these guides for detailed instructions:")
    print("- RAILWAY_DEPLOY_GUIDE.md")
    print("- RENDER_DEPLOY_GUIDE.md") 
    print("- VERCEL_FRONTEND_GUIDE.md")
    
    print("\n🚀 Your revolutionary logo generator is ready for the world!")

if __name__ == "__main__":
    main()