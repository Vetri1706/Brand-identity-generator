#!/usr/bin/env python3
"""
Simple Deployment Checker
Tests your deployed logo generator without external dependencies
"""

import urllib.request
import urllib.parse
import json
import sys

def test_url(url, description):
    """Test if a URL is accessible"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.getcode() == 200:
                print(f"✅ {description}: {url}")
                return True
            else:
                print(f"❌ {description} error: {response.getcode()}")
                return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def test_logo_api(backend_url):
    """Test logo generation API"""
    try:
        # Prepare test data
        test_data = {
            "company_name": "TestCorp",
            "industry": "technology", 
            "colors": ["#3B82F6"],
            "num_variations": 1
        }
        
        # Convert to JSON
        json_data = json.dumps(test_data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            f"{backend_url}/api/professional-logos",
            data=json_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # Send request
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.getcode() == 200:
                result = json.loads(response.read().decode())
                if result and len(result) > 0:
                    print("✅ Logo generation API working!")
                    return True
            
        print(f"❌ API returned: {response.getcode()}")
        return False
        
    except Exception as e:
        print(f"❌ Logo API test failed: {e}")
        return False

def main():
    print("🚀 QUICK DEPLOYMENT TEST")
    print("=" * 30)
    
    print("Enter your deployment URLs:")
    backend = input("Railway Backend URL: ").strip().rstrip('/')
    frontend = input("Vercel Frontend URL: ").strip().rstrip('/')
    
    if not backend or not frontend:
        print("❌ Please provide both URLs")
        return
    
    print("\n🔍 Testing deployments...")
    
    # Test backend health
    backend_ok = test_url(f"{backend}/health", "Backend Health")
    
    # Test frontend
    frontend_ok = test_url(frontend, "Frontend")
    
    # Test logo generation
    if backend_ok:
        logo_ok = test_logo_api(backend)
    else:
        logo_ok = False
        print("⏭️ Skipping logo test (backend down)")
    
    print("\n📊 RESULTS:")
    print(f"Backend:  {'✅' if backend_ok else '❌'}")
    print(f"Frontend: {'✅' if frontend_ok else '❌'}")
    print(f"Logo API: {'✅' if logo_ok else '❌'}")
    
    if backend_ok and frontend_ok and logo_ok:
        print("\n🎉 ALL SYSTEMS GO!")
        print(f"🌐 Your logo generator is live: {frontend}")
        print("\n🎯 Users can now generate professional logos!")
    else:
        print("\n⚠️ Some issues found. Check deployment guides.")

if __name__ == "__main__":
    main()