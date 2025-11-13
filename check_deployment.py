#!/usr/bin/env python3
"""
Quick Deployment Status Checker
Helps verify your deployments are working
"""

import requests
import time
import sys

def check_backend(url):
    """Check if backend is responding"""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            print(f"✅ Backend LIVE: {url}")
            return True
        else:
            print(f"❌ Backend responding but error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not responding: {e}")
        return False

def check_frontend(url):
    """Check if frontend is responding"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Frontend LIVE: {url}")
            return True
        else:
            print(f"❌ Frontend responding but error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend not responding: {e}")
        return False

def test_logo_generation(backend_url):
    """Test logo generation endpoint"""
    try:
        test_data = {
            "company_name": "TestCorp",
            "industry": "technology",
            "colors": ["#3B82F6", "#1E40AF"],
            "num_variations": 1
        }
        
        response = requests.post(
            f"{backend_url}/api/professional-logos",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                print("✅ Logo generation working!")
                return True
        
        print(f"❌ Logo generation failed: {response.status_code}")
        return False
    except Exception as e:
        print(f"❌ Logo generation error: {e}")
        return False

def main():
    print("🚀 DEPLOYMENT STATUS CHECKER")
    print("=" * 40)
    
    # Get URLs from user
    backend_url = input("Enter your Railway backend URL: ").strip()
    frontend_url = input("Enter your Vercel frontend URL: ").strip()
    
    # Remove trailing slashes
    backend_url = backend_url.rstrip('/')
    frontend_url = frontend_url.rstrip('/')
    
    print("\n🔍 Checking deployments...")
    
    # Check backend
    backend_ok = check_backend(backend_url)
    time.sleep(1)
    
    # Check frontend  
    frontend_ok = check_frontend(frontend_url)
    time.sleep(1)
    
    # Test logo generation if backend is working
    if backend_ok:
        print("\n🎨 Testing logo generation...")
        logo_ok = test_logo_generation(backend_url)
    else:
        logo_ok = False
    
    print("\n" + "="*40)
    print("📊 DEPLOYMENT STATUS SUMMARY")
    print("="*40)
    
    print(f"Backend:  {'✅ LIVE' if backend_ok else '❌ DOWN'}")
    print(f"Frontend: {'✅ LIVE' if frontend_ok else '❌ DOWN'}")
    print(f"Logo Gen: {'✅ WORKING' if logo_ok else '❌ FAILED'}")
    
    if backend_ok and frontend_ok and logo_ok:
        print("\n🎉 CONGRATULATIONS!")
        print("Your AI Logo Generator is LIVE!")
        print(f"🌐 Share this URL: {frontend_url}")
        print("\n🎯 Users can now:")
        print("- Generate professional logos")
        print("- Choose from 6 logo categories")
        print("- Get industry-specific designs")
        print("- Download high-quality PNG files")
    else:
        print("\n⚠️ Issues detected. Check:")
        print("1. URLs are correct")
        print("2. Deployments finished successfully")
        print("3. Environment variables are set")

if __name__ == "__main__":
    main()