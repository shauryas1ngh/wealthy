# API Examples

This document provides practical examples of using the Wealthy Prime Checker API.

## Table of Contents
- [cURL Examples](#curl-examples)
- [Python Examples](#python-examples)
- [JavaScript/Node.js Examples](#javascriptnodejs-examples)
- [Postman Collection](#postman-collection)

---

## cURL Examples

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Check Prime Numbers

```bash
# Check if 17 is prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'

# Check if 100 is prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 100}'

# Check edge cases
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 2}'  # Smallest prime

curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 1}'  # Not prime

curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 0}'  # Not prime
```

### 3. Get Check by Transaction ID

```bash
# Replace with actual transaction ID from previous response
curl http://localhost:8000/api/v1/prime/check/TXN-1700150400000-A1B2C3D4
```

### 4. Get History

```bash
# Get last 10 checks
curl http://localhost:8000/api/v1/prime/history?limit=10

# Get checks with pagination
curl http://localhost:8000/api/v1/prime/history?skip=0&limit=5
curl http://localhost:8000/api/v1/prime/history?skip=5&limit=5
```

---

## Python Examples

### Using `requests` Library

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Check if a number is prime
def check_prime(number):
    response = requests.post(
        f"{BASE_URL}/prime/check",
        json={"number": number}
    )
    return response.json()

# Test with multiple numbers
numbers = [2, 17, 20, 97, 100]
for num in numbers:
    result = check_prime(num)
    print(f"Number: {num}")
    print(f"Transaction ID: {result['transaction_id']}")
    print(f"Is Prime: {result['is_prime']}")
    print(f"Message: {result['message']}")
    print("-" * 50)

# 2. Retrieve by transaction ID
transaction_id = "TXN-1700150400000-A1B2C3D4"
response = requests.get(f"{BASE_URL}/prime/check/{transaction_id}")
print(json.dumps(response.json(), indent=2))

# 3. Get history
response = requests.get(f"{BASE_URL}/prime/history", params={"limit": 10})
history = response.json()
print(f"Total records: {len(history)}")
for record in history:
    print(f"{record['number']} -> Prime: {record['is_prime']}")
```

### Using `httpx` (Async)

```python
import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

async def check_prime_async(number):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/prime/check",
            json={"number": number}
        )
        return response.json()

async def main():
    # Check multiple numbers concurrently
    numbers = [2, 17, 97, 541, 1000]
    tasks = [check_prime_async(num) for num in numbers]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(f"{result['number']}: {result['message']}")

# Run the async function
asyncio.run(main())
```

---

## JavaScript/Node.js Examples

### Using Fetch API (Browser)

```javascript
// 1. Check if a number is prime
async function checkPrime(number) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/prime/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ number: number })
    });
    
    const data = await response.json();
    console.log(`Number: ${data.number}`);
    console.log(`Transaction ID: ${data.transaction_id}`);
    console.log(`Is Prime: ${data.is_prime}`);
    console.log(`Message: ${data.message}`);
    
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Test multiple numbers
const numbers = [2, 17, 20, 97, 100];
numbers.forEach(num => checkPrime(num));

// 2. Get check by transaction ID
async function getCheckByTransactionId(transactionId) {
  const response = await fetch(
    `http://localhost:8000/api/v1/prime/check/${transactionId}`
  );
  const data = await response.json();
  console.log(data);
}

// 3. Get history
async function getHistory(skip = 0, limit = 10) {
  const response = await fetch(
    `http://localhost:8000/api/v1/prime/history?skip=${skip}&limit=${limit}`
  );
  const data = await response.json();
  console.log(`Found ${data.length} records`);
  data.forEach(record => {
    console.log(`${record.number} -> Prime: ${record.is_prime}`);
  });
}

getHistory();
```

### Using Axios (Node.js)

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000/api/v1';

// 1. Check if a number is prime
async function checkPrime(number) {
  try {
    const response = await axios.post(`${BASE_URL}/prime/check`, {
      number: number
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// 2. Get check by transaction ID
async function getCheckByTransactionId(transactionId) {
  try {
    const response = await axios.get(
      `${BASE_URL}/prime/check/${transactionId}`
    );
    console.log(response.data);
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// 3. Get history
async function getHistory(skip = 0, limit = 10) {
  try {
    const response = await axios.get(`${BASE_URL}/prime/history`, {
      params: { skip, limit }
    });
    console.log(`Found ${response.data.length} records`);
    response.data.forEach(record => {
      console.log(`${record.number} -> Prime: ${record.is_prime}`);
    });
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

// Example usage
(async () => {
  await checkPrime(17);
  await checkPrime(100);
  await getHistory(0, 5);
})();
```

---

## Postman Collection

### Creating a Postman Collection

1. **Health Check**
   - Method: GET
   - URL: `http://localhost:8000/health`

2. **Check Prime**
   - Method: POST
   - URL: `http://localhost:8000/api/v1/prime/check`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
     ```json
     {
       "number": 17
     }
     ```

3. **Get by Transaction ID**
   - Method: GET
   - URL: `http://localhost:8000/api/v1/prime/check/{{transaction_id}}`
   - Use environment variable for `transaction_id`

4. **Get History**
   - Method: GET
   - URL: `http://localhost:8000/api/v1/prime/history`
   - Params:
     - `skip`: 0
     - `limit`: 10

---

## Response Examples

### Successful Prime Check (Prime Number)

```json
{
  "transaction_id": "TXN-1700150400000-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-16T12:00:00.000000"
}
```

### Successful Prime Check (Not Prime)

```json
{
  "transaction_id": "TXN-1700150500000-E5F6G7H8",
  "number": 100,
  "is_prime": false,
  "message": "100 is not a prime number",
  "created_at": "2025-11-16T12:01:40.000000"
}
```

### Error Response (Transaction Not Found)

```json
{
  "detail": "Transaction ID 'TXN-INVALID-ID' not found"
}
```

---

## Testing Tips

1. **Start the server**: `uvicorn app.main:app --reload`
2. **Use the interactive docs**: Navigate to http://localhost:8000/docs
3. **Run the test script**: `python test_api.py`
4. **Check database**: Connect to PostgreSQL to verify data persistence
   ```bash
   psql -U postgres -d wealthy_db
   SELECT * FROM prime_check_requests;
   ```

---

**Happy Testing! 🚀**

