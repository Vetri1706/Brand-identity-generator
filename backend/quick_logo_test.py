#!/usr/bin/env python3
"""
Quick Logo Generation Test
Tests individual logo generation to verify functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from professional_logo_generator import ProfessionalLogoGenerator
import base64

def test_logo_generation():
    """Test logo generation"""
    generator = ProfessionalLogoGenerator()
    
    # Test companies and industries
    test_cases = [
        {"company": "TechFlow AI", "industry": "technology", "colors": ["#3B82F6", "#1E40AF"]},
        {"company": "FinanceSecure", "industry": "finance", "colors": ["#059669", "#047857"]},
        {"company": "HealthCare Plus", "industry": "healthcare", "colors": ["#DC2626", "#B91C1C"]}
    ]
    
    for test_case in test_cases:
        try:
            print(f"🎨 Testing {test_case['company']} ({test_case['industry']})...")
            
            # Generate 3 diverse logos
            logos = generator.generate_diverse_professional_logos(
                company_name=test_case['company'],
                industry=test_case['industry'],
                colors=test_case['colors'],
                num_variations=3
            )
            
            print(f"   ✅ Generated {len(logos)} logos")
            
            # Check sizes for diversity
            sizes = []
            for i, logo_data in enumerate(logos):
                size = len(logo_data)
                sizes.append(size)
                print(f"   📏 Logo {i+1}: {size:,} characters")
                
                # Save for inspection
                filename = f"test_{test_case['company'].replace(' ', '_')}_logo_{i+1}.png"
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(logo_data))
                print(f"   💾 Saved as {filename}")
            
            # Calculate variation
            if len(sizes) > 1:
                variation = max(sizes) - min(sizes)
                avg_size = sum(sizes) / len(sizes)
                diversity_score = min(10, (variation / avg_size) * 10)
                print(f"   📊 Size variation: {variation:,} chars")
                print(f"   🎯 Diversity estimate: {diversity_score:.1f}/10")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n🎯 Logo generation test complete!")

if __name__ == "__main__":
    test_logo_generation()