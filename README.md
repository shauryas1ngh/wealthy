# 🚀 Wealthy Prime Checker API

A REST API service built with FastAPI that checks if numbers are prime, assigns unique transaction IDs, and persists the data to PostgreSQL.

## ✅ Setup Complete!

Your database is connected and ready to go! Here's what we set up:

### 🗄️ Database Configuration

- **Database**: PostgreSQL 18.1
- **Host**: localhost:5432
- **Database Name**: `wealthy_db`
- **Table**: `prime_check_requests`
- **User**: postgres
- **Password**: *(three spaces)* - configured in `.env`

### 📊 Database Schema

```sql
Table: prime_check_requests
├── id (integer, primary key, auto-increment)
├── transaction_id (varchar, unique, indexed)
├── number (integer, indexed)
├── is_prime (boolean)
└── created_at (timestamp with timezone)
```

## 🎯 Quick Start

### 1. Start the API Server

The server is already running! If you need to restart it:

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
source venv/bin/activate
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 2. Test the API

Run the test script:

```bash
./test_api.sh
```

Or test manually with curl:

```bash
# Check if 17 is prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'
```

### 3. View Interactive Documentation

Open your browser and visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try out the API directly from the browser!

## 📡 API Endpoints

### Health Check

```bash
GET /
GET /health
```

### Check Prime Number

```bash
POST /api/v1/prime/check
Content-Type: application/json

{
  "number": 17
}
```

**Response:**
```json
{
  "transaction_id": "TXN-1700123456789-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-17T12:34:56.789Z"
}
```

### Get Result by Transaction ID

```bash
GET /api/v1/prime/check/{transaction_id}
```

## 🗃️ Working with the Database

### View all records

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT * FROM prime_check_requests;"
```

### Count total checks

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT COUNT(*) FROM prime_check_requests;"
```

### View only prime numbers

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT number, transaction_id, created_at FROM prime_check_requests WHERE is_prime = true;"
```

### Clear all records

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "TRUNCATE TABLE prime_check_requests;"
```

## 📁 Project Structure

```
/Users/shaurya/.cursor/worktrees/wealthy/YRZCT/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   └── routes/
│   │       └── prime.py        # Prime number API routes
│   ├── core/
│   │   ├── config.py           # Settings & environment variables
│   │   └── database.py         # Database connection & session
│   ├── models/
│   │   └── prime_check.py      # SQLAlchemy database models
│   ├── schemas/
│   │   └── prime.py            # Pydantic request/response schemas
│   └── services/
│       └── prime_service.py    # Business logic
├── .env                         # Environment variables
├── test_api.sh                  # API test script
└── README.md                    # This file
```

## 🧪 Example Usage

### Test different numbers:

```bash
# Small prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 2}'

# Large prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 7919}'

# Not prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 100}'

# Edge case
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 1}'
```

### Retrieve a specific check:

```bash
# First, make a check and note the transaction_id
TXID=$(curl -s -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}' | python3 -c "import sys, json; print(json.load(sys.stdin)['transaction_id'])")

# Then retrieve it
curl http://localhost:8000/api/v1/prime/check/$TXID
```

## 🔧 Configuration

All configuration is in `.env`:

```env
# Application Configuration
APP_NAME=Wealthy Prime Checker API
APP_VERSION=1.0.0
DEBUG=False

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD="   "  # Three spaces - keep the quotes!
DATABASE_NAME=wealthy_db
```

## 🐛 Troubleshooting

### Server won't start?

Check if port 8000 is already in use:
```bash
lsof -i :8000
```

### Database connection issues?

Test the connection:
```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db -c "SELECT 1;"
```

### Need to recreate tables?

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
source venv/bin/activate
python -c "from app.core.database import init_db; init_db(); print('Tables created!')"
```

## 📚 How It Works

### For a Complete Beginner:

1. **You send a number** → API receives it via POST request
2. **API checks if it's prime** → Uses efficient algorithm
3. **Creates a unique ID** → Transaction ID format: `TXN-timestamp-randomcode`
4. **Saves to database** → PostgreSQL stores it permanently
5. **Returns the result** → JSON response with all details

### The Prime Number Algorithm:

```python
def is_prime(n):
    if n < 2: return False          # 0, 1, negatives aren't prime
    if n == 2: return True           # 2 is the only even prime
    if n % 2 == 0: return False      # Other even numbers aren't prime
    
    # Check odd divisors up to √n
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True
```

### Database Flow:

```
Request → API Endpoint → Service Layer → Database Model → PostgreSQL
                                                              ↓
Response ← Format Response ← Refresh Object ← Commit ← Insert Row
```

## 🎓 Learning Resources

Since you're new to databases, here are some helpful commands:

```bash
# Connect to your database
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db

# Once connected, try these commands:
\dt                              # List all tables
\d prime_check_requests          # Describe table structure
SELECT * FROM prime_check_requests LIMIT 5;  # View first 5 records
SELECT COUNT(*) FROM prime_check_requests;   # Count total records
\q                               # Quit psql
```

## 🌟 Features

- ✅ RESTful API design
- ✅ Automatic API documentation (Swagger/ReDoc)
- ✅ PostgreSQL database persistence
- ✅ Unique transaction IDs
- ✅ Efficient prime number algorithm
- ✅ Proper error handling
- ✅ Request/response validation with Pydantic
- ✅ Database connection pooling
- ✅ Auto-reload during development

## 🎉 You're All Set!

Your API is running and connected to PostgreSQL. Try it out by:

1. Opening http://localhost:8000/docs in your browser
2. Running `./test_api.sh` to see it in action
3. Checking the database to see stored records

Happy coding! 🚀

