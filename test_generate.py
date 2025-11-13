import requests
import json

# Test data
data = {
    "company_id": "test123",
    "company_profile": {
        "name": "TestCompany",
        "company_type": "saas",
        "industry": "Software",
        "description": "A test software company building amazing products",
        "target_audience": "Developers and tech teams",
        "brand_values": ["Innovation", "Simplicity"],
        "tone": "professional"
    },
    "num_variations": 3,
    "focus": "all"
}

try:
    print("Testing backend at http://localhost:8000/api/v1/generate-branding")
    response = requests.post(
        "http://localhost:8000/api/v1/generate-branding",
        json=data,
        timeout=60
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse Headers: {response.headers}")
    print(f"\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
    
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"\nError Response:")
        print(e.response.text)
