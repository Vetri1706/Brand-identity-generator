#!/usr/bin/env python3
"""
GitHub Repository Setup Helper
Provides commands for connecting to GitHub
"""

def show_github_commands():
    """Show the exact commands needed for GitHub setup"""
    
    print("🎯 GITHUB SETUP COMMANDS")
    print("=" * 50)
    
    print("\n📋 STEP 1: Create GitHub Repository")
    print("1. Go to https://github.com")
    print("2. Click 'New repository' (green button)")
    print("3. Name: brand-identity-generator") 
    print("4. Description: 🎨 Revolutionary AI Logo Generator")
    print("5. Select 'Public'")
    print("6. Click 'Create repository'")
    
    print("\n📤 STEP 2: Connect Your Local Code to GitHub")
    print("After creating the repository, run these commands:")
    print("")
    
    print("# Add your GitHub repository as remote origin")
    print("git remote add origin https://github.com/YOUR_USERNAME/brand-identity-generator.git")
    print("")
    print("# Rename branch to main")
    print("git branch -M main")
    print("")
    print("# Push your code to GitHub") 
    print("git push -u origin main")
    print("")
    
    print("🔄 Replace 'YOUR_USERNAME' with your actual GitHub username!")
    
    print("\n🚀 STEP 3: Free Deployment")
    print("✅ Backend: Railway.app (connect GitHub repo)")
    print("✅ Frontend: Vercel.com (import GitHub repo, set root: 'frontend')")
    
    print("\n🎉 Your revolutionary logo generator will be LIVE!")
    print("📱 Accessible worldwide with professional URLs")
    print("⚡ Auto-updates when you push to GitHub")

def main():
    print("🎨 REVOLUTIONARY LOGO GENERATOR")
    print("GitHub Repository Setup Helper")
    print("-" * 40)
    
    show_github_commands()
    
    print("\n📚 For detailed step-by-step instructions:")
    print("📖 Read: GITHUB_DEPLOYMENT_GUIDE.md")
    
    print("\n🌟 Ready to share your revolutionary AI with the world!")

if __name__ == "__main__":
    main()