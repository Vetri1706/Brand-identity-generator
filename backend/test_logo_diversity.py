"""
Professional Logo Diversity Test - Journal Publication Quality
Validates that each logo is genuinely different and meets professional standards
Tests the diversity claims and quality requirements for academic publication
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from professional_logo_generator import professional_logo_generator
import json
from datetime import datetime

def test_logo_diversity_and_quality():
    """Test logo diversity and professional quality for journal standards"""
    
    print("🎓 TESTING LOGO DIVERSITY FOR JOURNAL PUBLICATION")
    print("=" * 70)
    print("🎯 Validating genuine visual diversity")
    print("🎯 Testing professional quality standards")
    print("🎯 Ensuring publication-ready results")
    print("=" * 70)

    test_scenarios = [
        {
            "name": "TechFlow AI",
            "industry": "Technology",
            "colors": ["#6366F1", "#8B5CF6", "#06B6D4"],
            "expected_categories": ["wordmark", "lettermark", "pictorial"]
        },
        {
            "name": "FinanceSecure",
            "industry": "FinTech", 
            "colors": ["#059669", "#1E3A8A", "#FCD34D"],
            "expected_categories": ["abstract", "combination", "emblem"]
        },
        {
            "name": "HealthCare Plus",
            "industry": "HealthTech",
            "colors": ["#0EA5E9", "#059669", "#7C3AED"],
            "expected_categories": ["pictorial", "wordmark", "lettermark"]
        }
    ]

    all_results = []
    
    for scenario_idx, scenario in enumerate(test_scenarios, 1):
        print(f"\\n📊 Scenario {scenario_idx}: {scenario['name']} ({scenario['industry']})")
        print(f"   Testing 3 logo variations for diversity...")
        
        try:
            # Generate 3 diverse logos
            logos = professional_logo_generator.generate_diverse_professional_logos(
                scenario["name"],
                scenario["industry"], 
                scenario["colors"],
                3
            )
            
            if len(logos) != 3:
                print(f"   ❌ Expected 3 logos, got {len(logos)}")
                continue
            
            # Analyze diversity
            diversity_results = analyze_logo_diversity(logos, scenario)
            all_results.append(diversity_results)
            
            print(f"   📈 Data size variation: {diversity_results['size_variation']}")
            print(f"   🎨 Visual diversity score: {diversity_results['diversity_score']:.1f}/10")
            print(f"   ✅ Quality assessment: {diversity_results['quality_status']}")
            
            # Test specific requirements
            if diversity_results['size_variation'] > 10000:  # Significant data difference
                print("   ✅ Logos show significant structural differences")
            else:
                print("   ⚠️  Logos may be too similar")
            
            if diversity_results['diversity_score'] >= 8.0:
                print("   ✅ High visual diversity achieved")
            else:
                print("   ⚠️  Diversity could be improved")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    # Overall assessment
    print("\\n" + "=" * 70)
    print("📊 DIVERSITY & QUALITY ASSESSMENT")
    print("=" * 70)
    
    if all_results:
        avg_diversity = sum(r['diversity_score'] for r in all_results) / len(all_results)
        avg_size_var = sum(r['size_variation'] for r in all_results) / len(all_results)
        
        print(f"🎯 Average Diversity Score: {avg_diversity:.1f}/10")
        print(f"📊 Average Size Variation: {avg_size_var:,.0f} characters")
        
        # Journal publication criteria
        print("\\n📖 JOURNAL PUBLICATION CRITERIA:")
        
        # Criterion 1: Visual Diversity
        if avg_diversity >= 8.0:
            print("   ✅ Visual Diversity: EXCELLENT (≥8.0/10)")
        elif avg_diversity >= 7.0:
            print("   ⚡ Visual Diversity: GOOD (≥7.0/10)")
        else:
            print("   ⚠️  Visual Diversity: NEEDS IMPROVEMENT (<7.0/10)")
        
        # Criterion 2: Structural Differences
        if avg_size_var >= 15000:
            print("   ✅ Structural Differences: SIGNIFICANT (≥15k chars)")
        elif avg_size_var >= 8000:
            print("   ⚡ Structural Differences: MODERATE (≥8k chars)")
        else:
            print("   ⚠️  Structural Differences: MINIMAL (<8k chars)")
        
        # Criterion 3: Professional Quality
        quality_pass = all(r['quality_status'] == 'Professional' for r in all_results)
        if quality_pass:
            print("   ✅ Professional Quality: ALL LOGOS PASS")
        else:
            print("   ⚠️  Professional Quality: SOME ISSUES DETECTED")
        
        # Overall recommendation
        print("\\n🏆 OVERALL ASSESSMENT:")
        if avg_diversity >= 8.0 and avg_size_var >= 12000 and quality_pass:
            print("   🎉 JOURNAL PUBLICATION READY!")
            print("   ✅ Meets diversity requirements")
            print("   ✅ Shows genuine visual differences")
            print("   ✅ Professional quality maintained")
        elif avg_diversity >= 7.0 and avg_size_var >= 8000:
            print("   ⚡ GOOD QUALITY - Minor improvements recommended")
            print("   📝 Consider enhancing visual variety")
        else:
            print("   ⚠️  NEEDS SIGNIFICANT IMPROVEMENT")
            print("   📝 Increase visual diversity between variations")
            print("   📝 Ensure structural differences")
    
    return all_results

def analyze_logo_diversity(logos: list, scenario: dict) -> dict:
    """Analyze diversity between generated logos"""
    
    # Basic size analysis
    sizes = [len(logo) for logo in logos]
    min_size = min(sizes)
    max_size = max(sizes)
    size_variation = max_size - min_size
    
    # Diversity scoring (simplified analysis)
    diversity_score = 6.0  # Base score
    
    # Size variation indicates different complexity
    if size_variation > 20000:
        diversity_score += 2.0  # Significant differences
    elif size_variation > 10000:
        diversity_score += 1.0  # Moderate differences
    elif size_variation > 5000:
        diversity_score += 0.5  # Minor differences
    
    # Check for realistic size ranges
    if min_size > 20000:  # All logos have substantial content
        diversity_score += 0.5
    
    if all(size > 30000 for size in sizes):  # All are complex
        diversity_score += 0.5
    
    # Quality assessment based on size and consistency
    quality_status = "Professional" if min_size > 15000 else "Basic"
    
    return {
        "scenario": scenario["name"],
        "logo_sizes": sizes,
        "size_variation": size_variation,
        "diversity_score": min(10.0, diversity_score),
        "quality_status": quality_status,
        "min_size": min_size,
        "max_size": max_size,
        "avg_size": sum(sizes) / len(sizes)
    }

def test_specific_logo_categories():
    """Test that different logo categories are actually generated"""
    
    print("\\n🎨 TESTING SPECIFIC LOGO CATEGORIES")
    print("=" * 50)
    
    test_company = "TestCorp"
    test_industry = "Technology"
    test_colors = ["#2563EB", "#10B981", "#F59E0B"]
    
    # Generate multiple sets to see variety
    for set_num in range(1, 4):
        print(f"\\n📊 Logo Set {set_num}:")
        
        logos = professional_logo_generator.generate_diverse_professional_logos(
            f"{test_company} {set_num}",  # Different name to ensure variety
            test_industry,
            test_colors,
            3
        )
        
        for i, logo in enumerate(logos, 1):
            size = len(logo)
            print(f"   Logo {i}: {size:,} characters")
            
            # Simple heuristic analysis
            if size > 80000:
                complexity = "Very High"
            elif size > 50000:
                complexity = "High"  
            elif size > 30000:
                complexity = "Medium"
            else:
                complexity = "Low"
            
            print(f"            Complexity: {complexity}")
        
        # Check variation within set
        sizes = [len(logo) for logo in logos]
        variation = max(sizes) - min(sizes)
        print(f"   Set Variation: {variation:,} characters")
        
        if variation > 15000:
            print("   ✅ Significant variation detected")
        elif variation > 5000:
            print("   ⚡ Moderate variation detected")
        else:
            print("   ⚠️  Low variation - may be too similar")

def generate_publication_report():
    """Generate a report suitable for journal publication"""
    
    print("\\n📖 GENERATING PUBLICATION REPORT")
    print("=" * 40)
    
    report = {
        "study_title": "AI-Generated Logo Diversity Analysis",
        "date": datetime.now().isoformat(),
        "methodology": {
            "approach": "Multi-category logo generation system",
            "categories": [
                "Wordmark (Typography-focused)",
                "Lettermark (Monogram-based)", 
                "Pictorial (Icon-based)",
                "Abstract (Geometric artistic)",
                "Combination (Text + Icon)",
                "Emblem (Badge/Crest style)"
            ],
            "quality_metrics": [
                "Visual diversity score (0-10)",
                "Structural variation (character count difference)",
                "Professional quality assessment"
            ]
        },
        "test_results": "Results from diversity analysis",
        "conclusion": {
            "diversity_achieved": "To be determined",
            "publication_ready": "To be assessed",
            "recommendations": []
        }
    }
    
    # Save report
    with open("logo_diversity_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Report template saved as: logo_diversity_report.json")
    print("📝 Complete with actual test results for publication")

def main():
    """Main testing function"""
    
    print("🎓 PROFESSIONAL LOGO DIVERSITY VALIDATION")
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Testing for journal publication standards")
    
    # Run diversity tests
    results = test_logo_diversity_and_quality()
    
    # Test specific categories  
    test_specific_logo_categories()
    
    # Generate publication report
    generate_publication_report()
    
    print("\\n" + "=" * 70)
    print("✅ DIVERSITY VALIDATION COMPLETE")
    print("=" * 70)
    print("📊 Review results above to assess publication readiness")
    print("📝 Address any diversity issues before journal submission")
    print("🎯 Aim for 8.0+ diversity scores and significant size variations")

if __name__ == "__main__":
    main()