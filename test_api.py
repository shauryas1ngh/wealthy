"""
Sample script to test the Wealthy Prime Checker API
Run this after starting the server with: python test_api.py
"""

import requests
import json
from typing import List

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"


def test_health_check():
    """Test if the API is running."""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    response = requests.get("http://localhost:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def check_prime(number: int) -> dict:
    """Check if a number is prime."""
    print("\n" + "="*50)
    print(f"Checking if {number} is prime")
    print("="*50)
    
    response = requests.post(
        f"{BASE_URL}/prime/check",
        json={"number": number}
    )
    
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    return result


def get_check_by_transaction_id(transaction_id: str):
    """Retrieve a check by transaction ID."""
    print("\n" + "="*50)
    print(f"Retrieving check for transaction: {transaction_id}")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/prime/check/{transaction_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        return result
    else:
        print(f"Error: {response.text}")
        return None


def get_history(skip: int = 0, limit: int = 10):
    """Get prime check history."""
    print("\n" + "="*50)
    print(f"Fetching history (skip={skip}, limit={limit})")
    print("="*50)
    
    response = requests.get(
        f"{BASE_URL}/prime/history",
        params={"skip": skip, "limit": limit}
    )
    
    print(f"Status Code: {response.status_code}")
    results = response.json()
    print(f"Found {len(results)} records")
    print(f"Response: {json.dumps(results, indent=2)}")
    
    return results


def main():
    """Run all tests."""
    print("\n" + "🚀 "*25)
    print("WEALTHY PRIME CHECKER API - TEST SCRIPT")
    print("🚀 "*25)
    
    try:
        # Test health check
        if not test_health_check():
            print("❌ API is not responding. Make sure it's running!")
            return
        
        # Test with various numbers
        test_numbers = [2, 3, 4, 17, 20, 97, 100, 1, 0, -5]
        
        transaction_ids = []
        
        for num in test_numbers:
            result = check_prime(num)
            transaction_ids.append(result["transaction_id"])
        
        # Test retrieving by transaction ID
        if transaction_ids:
            get_check_by_transaction_id(transaction_ids[0])
        
        # Test getting history
        get_history(skip=0, limit=5)
        
        print("\n" + "✅ "*25)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ "*25 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API.")
        print("Please make sure the server is running:")
        print("  uvicorn app.main:app --reload")
        print()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    main()

