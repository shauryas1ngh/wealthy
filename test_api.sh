#!/bin/bash

echo "🧪 Testing Wealthy Prime Checker API"
echo "===================================="
echo ""

# Test root endpoint
echo "1️⃣  Testing root endpoint..."
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""
echo ""

# Test health check
echo "2️⃣  Testing health check..."
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test prime check endpoint
echo "3️⃣  Testing prime number check (17 - is prime)..."
curl -s -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}' | python3 -m json.tool
echo ""
echo ""

# Test non-prime number
echo "4️⃣  Testing non-prime number (20 - not prime)..."
curl -s -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 20}' | python3 -m json.tool
echo ""
echo ""

# Test large prime
echo "5️⃣  Testing large prime number (7919)..."
curl -s -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 7919}' | python3 -m json.tool
echo ""
echo ""

echo "✅ All tests complete!"
echo ""
echo "📚 View interactive API docs at: http://localhost:8000/docs"
echo "📊 View database records with:"
echo "   PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db -c 'SELECT * FROM prime_check_requests;'"

