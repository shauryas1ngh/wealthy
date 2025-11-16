# Wealthy Prime Checker API

A scalable REST API built with FastAPI that checks if a number is prime, assigns a unique transaction ID to each request, and persists the data to PostgreSQL.

## 🏗️ Project Structure

```
wealthy/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── prime.py           # Prime checking endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Application settings
│   │   └── database.py            # Database connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   └── prime_check.py         # SQLAlchemy database models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── prime.py               # Pydantic request/response schemas
│   └── services/
│       ├── __init__.py
│       └── prime_service.py       # Business logic layer
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore
└── Readme.md
```

## ✨ Features

- ✅ **Prime Number Checking**: Efficient algorithm to determine if a number is prime
- 🆔 **Unique Transaction IDs**: Every request gets a unique transaction identifier
- 💾 **PostgreSQL Persistence**: All requests and results are stored in the database
- 📊 **History Tracking**: Retrieve past prime checks with pagination
- 🔍 **Transaction Lookup**: Query results by transaction ID
- 📚 **Auto-generated API Documentation**: Interactive Swagger UI and ReDoc
- 🎯 **RESTful Design**: Clean, scalable REST API architecture
- ⚡ **High Performance**: Async support with FastAPI and efficient database connections

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- PostgreSQL installed and running on port 5432
- pip (Python package manager)

### 1. Database Setup

First, create a PostgreSQL database:

```bash
# Connect to PostgreSQL
psql -U postgres

# Create the database
CREATE DATABASE wealthy_db;

# Exit psql
\q
```

### 2. Clone and Setup

```bash
# Navigate to the project directory
cd /Users/shaurya/Desktop/wealthy

# Create a virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
# Application Configuration
APP_NAME=Wealthy Prime Checker API
APP_VERSION=1.0.0
DEBUG=False

# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password_here
DATABASE_NAME=wealthy_db
```

### 4. Run the Application

```bash
# Make sure you're in the project root directory
cd /Users/shaurya/Desktop/wealthy

# Run the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📖 API Endpoints

### 1. Health Check

```bash
GET /
GET /health
```

Check if the API is running.

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

### 2. Check if Number is Prime

```bash
POST /api/v1/prime/check
```

Check if a number is prime and save the result.

**Request Body:**
```json
{
  "number": 17
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'
```

**Response:**
```json
{
  "transaction_id": "TXN-1700150400000-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-16T12:00:00.000000"
}
```

### 3. Get Prime Check by Transaction ID

```bash
GET /api/v1/prime/check/{transaction_id}
```

Retrieve a specific prime check result using its transaction ID.

**Example:**
```bash
curl http://localhost:8000/api/v1/prime/check/TXN-1700150400000-A1B2C3D4
```

**Response:**
```json
{
  "transaction_id": "TXN-1700150400000-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-16T12:00:00.000000"
}
```

### 4. Get Prime Check History

```bash
GET /api/v1/prime/history?skip=0&limit=100
```

Retrieve the history of all prime check requests with pagination.

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100, max: 1000)

**Example:**
```bash
curl "http://localhost:8000/api/v1/prime/history?skip=0&limit=10"
```

**Response:**
```json
[
  {
    "id": 1,
    "transaction_id": "TXN-1700150400000-A1B2C3D4",
    "number": 17,
    "is_prime": true,
    "created_at": "2025-11-16T12:00:00.000000"
  },
  {
    "id": 2,
    "transaction_id": "TXN-1700150500000-E5F6G7H8",
    "number": 20,
    "is_prime": false,
    "created_at": "2025-11-16T12:01:40.000000"
  }
]
```

## 🧪 Testing the API

### Using cURL

```bash
# Check if 29 is prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 29}'

# Check if 100 is prime
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 100}'

# Get history
curl http://localhost:8000/api/v1/prime/history
```

### Using Python

```python
import requests

# Check if a number is prime
response = requests.post(
    "http://localhost:8000/api/v1/prime/check",
    json={"number": 97}
)
result = response.json()
print(f"Transaction ID: {result['transaction_id']}")
print(f"Is Prime: {result['is_prime']}")

# Retrieve by transaction ID
transaction_id = result['transaction_id']
response = requests.get(
    f"http://localhost:8000/api/v1/prime/check/{transaction_id}"
)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Check if a number is prime
fetch('http://localhost:8000/api/v1/prime/check', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ number: 97 })
})
  .then(response => response.json())
  .then(data => {
    console.log('Transaction ID:', data.transaction_id);
    console.log('Is Prime:', data.is_prime);
  });
```

## 🗄️ Database Schema

The application uses a single table `prime_check_requests`:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| transaction_id | VARCHAR | Unique transaction identifier |
| number | INTEGER | The number that was checked |
| is_prime | BOOLEAN | Whether the number is prime |
| created_at | TIMESTAMP | When the request was made |

## 🔧 Configuration

All configuration is managed through environment variables (see `.env` file):

- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `DEBUG`: Enable debug mode (True/False)
- `DATABASE_HOST`: PostgreSQL host (default: localhost)
- `DATABASE_PORT`: PostgreSQL port (default: 5432)
- `DATABASE_USER`: Database username
- `DATABASE_PASSWORD`: Database password
- `DATABASE_NAME`: Database name

## 📦 Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI
- **SQLAlchemy**: SQL toolkit and ORM
- **Psycopg2**: PostgreSQL adapter for Python
- **Pydantic**: Data validation using Python type annotations

## 🚀 Production Deployment

For production deployment, consider:

1. **Use a production ASGI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Set environment variables appropriately**:
   - Set `DEBUG=False`
   - Use strong database passwords
   - Configure CORS appropriately in `app/main.py`

3. **Use a reverse proxy** (nginx, Apache) for SSL termination

4. **Set up database connection pooling** (already configured in `database.py`)

5. **Monitor and log** application performance

## 🛠️ Development

### Adding New Endpoints

1. Create a new router in `app/api/routes/`
2. Define schemas in `app/schemas/`
3. Add business logic in `app/services/`
4. Include the router in `app/main.py`

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when test files are added)
pytest
```

## 📝 License

This project is open source and available for use.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using FastAPI and PostgreSQL**
