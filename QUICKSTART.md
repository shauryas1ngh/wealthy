# Quick Start Guide

Get the Wealthy Prime Checker API up and running in 5 minutes! ⚡

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed: `python3 --version`
- ✅ PostgreSQL installed and running: `psql --version`
- ✅ PostgreSQL running on port 5432

## 🚀 Option 1: Automated Setup (Recommended)

### Step 1: Run Setup Script

```bash
cd /Users/shaurya/Desktop/wealthy
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Create a `.env` file from the template

### Step 2: Configure Database

Edit the `.env` file with your PostgreSQL password:

```bash
# Open in your favorite editor
nano .env  # or vim, code, etc.
```

Update this line:
```env
DATABASE_PASSWORD=your_password_here
```

### Step 3: Create Database

```bash
psql -U postgres -c "CREATE DATABASE wealthy_db;"
```

Or manually:
```bash
psql -U postgres
CREATE DATABASE wealthy_db;
\q
```

### Step 4: Run the Application

```bash
./run.sh
```

That's it! 🎉

---

## 🛠️ Option 2: Manual Setup

### Step 1: Create Virtual Environment

```bash
cd /Users/shaurya/Desktop/wealthy
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Setup Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### Step 4: Create Database

```bash
psql -U postgres -c "CREATE DATABASE wealthy_db;"
```

### Step 5: Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Verify Installation

### Method 1: Browser
Open your browser and go to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Method 2: cURL
```bash
curl http://localhost:8000/health
```

### Method 3: Test Script
```bash
# In a new terminal (keep the server running)
source venv/bin/activate
python test_api.py
```

---

## 📝 Your First API Call

### Using cURL

```bash
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'
```

Expected response:
```json
{
  "transaction_id": "TXN-1700150400000-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-16T12:00:00"
}
```

### Using the Interactive Docs

1. Go to http://localhost:8000/docs
2. Click on **POST /api/v1/prime/check**
3. Click **Try it out**
4. Enter a number (e.g., `17`)
5. Click **Execute**

---

## 🔍 Check Database

Verify that data is being saved:

```bash
psql -U postgres -d wealthy_db
```

Then run:
```sql
SELECT * FROM prime_check_requests;
```

---

## 🎯 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/prime/check` | Check if number is prime |
| GET | `/api/v1/prime/check/{transaction_id}` | Get by transaction ID |
| GET | `/api/v1/prime/history` | Get all checks history |

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
pg_isready

# Check if database exists
psql -U postgres -l | grep wealthy_db

# Recreate database if needed
psql -U postgres -c "DROP DATABASE IF EXISTS wealthy_db;"
psql -U postgres -c "CREATE DATABASE wealthy_db;"
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Denied on Scripts
```bash
chmod +x setup.sh run.sh
```

---

## 📚 Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Read the full README**: See `Readme.md` for detailed documentation
3. **Check examples**: See `api_examples.md` for code examples
4. **Run tests**: Execute `python test_api.py`

---

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal where the server is running.

---

## 🎉 Success!

You're now ready to use the Wealthy Prime Checker API!

For more information, see:
- Full Documentation: `Readme.md`
- API Examples: `api_examples.md`
- Database Schema: `init_db.sql`

**Happy coding! 🚀**

