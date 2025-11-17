#!/usr/bin/env python3
"""
Simple test script for the Wealthy Prime Checker API
Run this after starting the server to test all endpoints
"""

import urllib.request
import urllib.error
import json
import sys


def test_endpoint(method, url, data=None, description=""):
    """Test an API endpoint and print results"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Method: {method}")
    print(f"URL: {url}")
    
    try:
        if data:
            print(f"Data: {json.dumps(data)}")
            post_data = json.dumps(data).encode('utf-8')
            headers = {'Content-Type': 'application/json'}
            req = urllib.request.Request(url, data=post_data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, method=method)
        
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        
        print(f"\n✅ Status: {response.status} {response.reason}")
        print(f"Response:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except urllib.error.HTTPError as e:
        print(f"\n❌ Error: {e.code} {e.reason}")
        try:
            error_data = json.loads(e.read())
            print(json.dumps(error_data, indent=2))
        except:
            pass
        return None
    except urllib.error.URLError as e:
        print(f"\n❌ Connection Error: {e.reason}")
        print("\n💡 Make sure the server is running!")
        print("   Start it with: uvicorn app.main:app --reload")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return None


def main():
    """Run all API tests"""
    BASE_URL = "http://localhost:8000"
    
    print("\n" + "🚀 " * 20)
    print("WEALTHY PRIME CHECKER API - TEST SUITE")
    print("🚀 " * 20)
    
    # Test 1: Root endpoint
    test_endpoint(
        "GET",
        f"{BASE_URL}/",
        description="Test 1: Root Endpoint (Health Check)"
    )
    
    # Test 2: Health endpoint
    test_endpoint(
        "GET",
        f"{BASE_URL}/health",
        description="Test 2: Health Endpoint"
    )
    
    # Test 3: Check a small prime number
    result1 = test_endpoint(
        "POST",
        f"{BASE_URL}/api/v1/prime/check",
        data={"number": 17},
        description="Test 3: Check Prime Number (17)"
    )
    
    # Test 4: Check a non-prime number
    test_endpoint(
        "POST",
        f"{BASE_URL}/api/v1/prime/check",
        data={"number": 20},
        description="Test 4: Check Non-Prime Number (20)"
    )
    
    # Test 5: Check edge case (1 is not prime)
    test_endpoint(
        "POST",
        f"{BASE_URL}/api/v1/prime/check",
        data={"number": 1},
        description="Test 5: Edge Case (1 - not prime)"
    )
    
    # Test 6: Check edge case (2 is prime)
    test_endpoint(
        "POST",
        f"{BASE_URL}/api/v1/prime/check",
        data={"number": 2},
        description="Test 6: Edge Case (2 - the only even prime)"
    )
    
    # Test 7: Check a large prime
    result2 = test_endpoint(
        "POST",
        f"{BASE_URL}/api/v1/prime/check",
        data={"number": 7919},
        description="Test 7: Large Prime Number (7919)"
    )
    
    # Test 8: Retrieve by transaction ID (if we got a result earlier)
    if result1 and 'transaction_id' in result1:
        transaction_id = result1['transaction_id']
        test_endpoint(
            "GET",
            f"{BASE_URL}/api/v1/prime/check/{transaction_id}",
            description=f"Test 8: Retrieve by Transaction ID ({transaction_id})"
        )
    
    # Test 9: Try to retrieve non-existent transaction
    test_endpoint(
        "GET",
        f"{BASE_URL}/api/v1/prime/check/INVALID-TXN",
        description="Test 9: Retrieve Non-Existent Transaction (should fail)"
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ TEST SUITE COMPLETE!")
    print("=" * 60)
    print("\n📊 Check your database to see the records:")
    print("   PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \\")
    print("     -c \"SELECT transaction_id, number, is_prime, created_at FROM prime_check_requests;\"")
    print("\n📚 View API docs at: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)

