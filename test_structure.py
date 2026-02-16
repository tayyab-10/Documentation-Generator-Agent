# Quick Test: Check if Python agent structure endpoint works

import requests

# Test the structure endpoint
url = "http://localhost:8003/api/documentation/types/SRS/structure"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
