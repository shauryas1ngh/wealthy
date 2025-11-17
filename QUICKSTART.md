# ⚡ Quick Start Guide

## 🎉 Your Database is Connected and Ready!

Everything is set up and working. Here's how to use your API:

## ✅ What We Did

1. ✅ **Fixed** your `.env` file to properly handle the password (three spaces)
2. ✅ **Created** the `wealthy_db` database in PostgreSQL
3. ✅ **Created** the `prime_check_requests` table with all columns
4. ✅ **Fixed** Python 3.9 compatibility issues in the code
5. ✅ **Started** your FastAPI server on port 8000

## 🚀 Test Your API Right Now!

### Option 1: Python Test Script (Recommended for beginners)

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
python3 test_api.py
```

This will run 9 different tests and show you exactly how everything works!

### Option 2: Bash Test Script

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
./test_api.sh
```

### Option 3: Interactive Documentation (Most Fun!)

Open your web browser and go to:

**http://localhost:8000/docs**

You can test the API by:
1. Click on any endpoint (the green POST or blue GET buttons)
2. Click "Try it out"
3. Enter a number (like 17)
4. Click "Execute"
5. See the response!

## 📊 View Your Database

After making some API calls, check what was saved:

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db -c "SELECT * FROM prime_check_requests;"
```

## 🔄 If Server Stopped

Restart it anytime:

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
source venv/bin/activate
uvicorn app.main:app --reload
```

## 📝 Try This Example

1. **Check if 17 is prime:**

```bash
curl -X POST http://localhost:8000/api/v1/prime/check \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'
```

You'll get something like:

```json
{
  "transaction_id": "TXN-1700123456789-A1B2C3D4",
  "number": 17,
  "is_prime": true,
  "message": "17 is a prime number",
  "created_at": "2025-11-17T12:34:56.789Z"
}
```

2. **Look it up in the database:**

```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT * FROM prime_check_requests WHERE number = 17;"
```

You'll see the same record stored in PostgreSQL!

## 🎓 Understanding Your Files

### Database Files
- **`app/models/prime_check.py`**: Defines your database table structure
- **`app/core/database.py`**: Handles connecting to PostgreSQL
- **`.env`**: Contains your database password and settings

### API Files
- **`app/main.py`**: Your FastAPI app (the web server)
- **`app/api/routes/prime.py`**: The API endpoints (URLs)
- **`app/services/prime_service.py`**: The actual prime-checking logic

### Schema Files
- **`app/schemas/prime.py`**: Defines what requests and responses look like

## 🆘 Common Commands

### Check if server is running:
```bash
lsof -i :8000
```

### Check if PostgreSQL is running:
```bash
pg_isready -h localhost -p 5432
```

### View all data in database:
```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT * FROM prime_check_requests;"
```

### Count how many checks you've done:
```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "SELECT COUNT(*) FROM prime_check_requests;"
```

### Clear all data:
```bash
PGPASSWORD='   ' psql -U postgres -h localhost -p 5432 -d wealthy_db \
  -c "TRUNCATE TABLE prime_check_requests;"
```

## 🎯 Next Steps

1. **Test the API** using `python3 test_api.py`
2. **Open the docs** at http://localhost:8000/docs
3. **Check the database** to see your data
4. **Read `README.md`** for more detailed information

## 💡 Pro Tip

The interactive docs at `/docs` are the easiest way to learn! You can:
- See all available endpoints
- Test them directly in the browser
- See example requests and responses
- No need to use curl or write code!

## 🐛 Troubleshooting

**Server won't start?**
- Make sure port 8000 is free: `lsof -i :8000`
- Check you're in the right directory
- Make sure venv is activated: `source venv/bin/activate`

**Database errors?**
- Check PostgreSQL is running: `pg_isready -h localhost -p 5432`
- Verify your password in `.env` is: `"   "` (three spaces in quotes)

**Import errors?**
- Make sure you're in the project directory
- Make sure venv is activated

---

**🎉 Everything is working! Have fun testing your API!**

