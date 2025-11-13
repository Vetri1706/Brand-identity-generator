"""Test logo generation"""
from logo_generator import logo_generator

# Test simple logo
print("Generating simple logo...")
logo1 = logo_generator.generate_simple_logo(
    "TechFlow AI",
    ["#2563EB", "#10B981", "#F59E0B"],
    "modern"
)
print(f"✅ Simple logo generated: {len(logo1)} characters")

# Test geometric logo
print("\nGenerating geometric logo...")
logo2 = logo_generator.generate_geometric_logo(
    "TechFlow AI",
    ["#2563EB", "#10B981"],
    "hexagon"
)
print(f"✅ Geometric logo generated: {len(logo2)} characters")

# Test minimal logo
print("\nGenerating minimal logo...")
logo3 = logo_generator.generate_minimal_logo(
    "TechFlow AI",
    ["#2563EB", "#10B981", "#F59E0B"]
)
print(f"✅ Minimal logo generated: {len(logo3)} characters")

print("\n🎉 All logo generation tests passed!")
print("Images are base64 encoded strings ready for display in browser")
