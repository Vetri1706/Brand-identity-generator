"""
Test script for VISUAL industry logos
Tests: Floral, Food, Beauty, Healthcare with visual symbols
"""
import sys
sys.path.insert(0, r"C:\Users\vetri\Miniproj\brand_identity_generator_mvp\backend")

from industry_logo_generator import industry_logo_generator
import base64

def test_logo(industry, company_name, colors):
    """Test logo generation"""
    print(f"\n🎨 Testing {industry.upper()} logo for '{company_name}'...")
    
    try:
        logo_data = industry_logo_generator.generate_industry_logo(
            company_name=company_name,
            industry=industry,
            colors=colors,
            style_preference="variation_1"
        )
        
        # Save to file
        filename = f"test_{industry}_{company_name.replace(' ', '_').lower()}.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(logo_data))
        
        print(f"✅ Logo saved: {filename}")
        print(f"   File size: {len(base64.b64decode(logo_data)) / 1024:.2f} KB")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Test different industries with VISUAL symbols
print("=" * 60)
print("TESTING VISUAL INDUSTRY LOGOS")
print("=" * 60)

# 1. FLORAL - Should show flowers, leaves, petals
test_logo(
    "floral bouquet shop",
    "Rose Garden",
    ["#EC4899", "#10B981", "#A855F7"]  # Pink, Green, Purple
)

# 2. FOOD/RESTAURANT - Should show chef hat, fork, spoon
test_logo(
    "restaurant food",
    "The Bistro",
    ["#EF4444", "#F97316", "#10B981"]  # Red, Orange, Green
)

# 3. BEAUTY/SPA - Should show lotus, butterfly, stones
test_logo(
    "beauty spa wellness",
    "Zen Spa",
    ["#A855F7", "#06B6D4", "#EC4899"]  # Purple, Cyan, Pink
)

# 4. HEALTHCARE - Should show STETHOSCOPE, not just letters!
test_logo(
    "healthcare medical",
    "HealthCare Plus",
    ["#0EA5E9", "#10B981", "#FFFFFF"]  # Blue, Green, White
)

# 5. TECH - For comparison
test_logo(
    "technology ai",
    "TechCorp",
    ["#2563EB", "#8B5CF6", "#10B981"]  # Blue, Purple, Green
)

print("\n" + "=" * 60)
print("✅ All tests complete! Check the .png files")
print("=" * 60)
print("\n📸 WHAT TO LOOK FOR:")
print("   🌹 Floral: Actual flowers, leaves, petals (NO TEXT!)")
print("   🍴 Food: Chef hat, fork, spoon symbols (NO TEXT!)")
print("   🦋 Beauty: Lotus flower, butterfly, spa stones (NO TEXT!)")
print("   🩺 Healthcare: STETHOSCOPE, heart, medical symbols (NO TEXT!)")
print("   🖥️  Tech: Neural networks, circuits")
print("\nIf you see just letters/text - the logos need more work!")
print("If you see ACTUAL VISUAL SYMBOLS - SUCCESS! 🎉")
