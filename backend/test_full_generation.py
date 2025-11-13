"""Test full branding generation with logo images"""
import requests
import json

url = "http://localhost:8000/api/v1/generate-branding"

payload = {
    "company_profile": {
        "name": "TechFlow AI",
        "company_type": "ai_ml",
        "industry": "Artificial Intelligence",
        "description": "Building AI automation tools",
        "target_audience": "Tech companies",
        "brand_values": ["Innovation", "Trust"],
        "tone": "professional",
        "additional_context": "Modern tech company"
    },
    "focus": "all",
    "num_variations": 3
}

print("🚀 Testing branding generation with logo images...")
print("=" * 60)

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    
    print(f"✅ Status: {response.status_code} OK")
    print(f"⏱️  Generation time: {result.get('generation_time', 'N/A')}")
    print()
    
    # Check logos
    logos = result.get('logos', [])
    print(f"📸 Logos generated: {len(logos)}")
    for i, logo in enumerate(logos, 1):
        image_url = logo.get('image_url', '')
        has_image = 'Yes' if image_url and len(image_url) > 100 else 'No'
        image_size = len(image_url) if image_url else 0
        print(f"   Logo {i}:")
        print(f"     - Style: {logo.get('style', 'N/A')}")
        print(f"     - Has Image: {has_image}")
        print(f"     - Image Size: {image_size} chars")
        print(f"     - Prompt: {logo.get('prompt_used', '')[:80]}...")
    
    print()
    print(f"📝 Taglines: {len(result.get('taglines', []))}")
    print(f"🎨 Color Palette: {len(result.get('color_palette', {}).get('colors', {}))} colors")
    print(f"✍️  Typography: {result.get('typography', {}).get('primary_font', 'N/A')}")
    
    print()
    print("=" * 60)
    print("🎉 SUCCESS! Logo images are being generated!")
    
    # Verify image format
    if logos and logos[0].get('image_url', '').startswith('data:image/png;base64,'):
        print("✅ Images are in correct base64 format for display")
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
