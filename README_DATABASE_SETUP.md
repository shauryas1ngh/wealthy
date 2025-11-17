# 🗄️ Database Setup Guide for Wealthy Prime Checker

## Quick Summary
Your PostgreSQL is installed and running on port 5432! We just need to connect to it.

## Option 1: Find or Reset Your PostgreSQL Password (Easiest)

### If you just installed PostgreSQL:
When you installed PostgreSQL, you were probably asked to set a password. Common defaults are:
- `postgres`
- Your Mac password
- No password (empty string)

### To reset your postgres password:

1. **Find your PostgreSQL bin directory:**
   ```bash
   which psql
   ```

2. **Connect as superuser (might work without password):**
   ```bash
   psql postgres
   ```
   
   If that doesn't work, try:
   ```bash
   sudo -u postgres psql
   ```

3. **Once connected, set a new password:**
   ```sql
   ALTER USER postgres WITH PASSWORD 'your_new_password';
   ```

4. **Exit psql:**
   ```
   \q
   ```

## Option 2: Run Our Interactive Setup Script

Once you know your password, run:

```bash
cd /Users/shaurya/.cursor/worktrees/wealthy/YRZCT
source venv/bin/activate
python setup_db.py
```

This will:
- ✅ Test your connection
- ✅ Create the `wealthy_db` database
- ✅ Create all necessary tables
- ✅ Update your `.env` file with correct credentials

## Option 3: Manual Setup (if you know your password)

1. **Update your `.env` file with the correct password:**
   ```
   DATABASE_PASSWORD=your_actual_password
   ```

2. **Create the database:**
   ```bash
   createdb -U postgres -h localhost -p 5432 wealthy_db
   ```

3. **Run this Python script to create tables:**
   ```bash
   python -c "from app.core.database import init_db; init_db(); print('✅ Tables created!')"
   ```

## Option 4: Use Trust Authentication (Development Only!)

If you want to skip passwords for local development:

1. **Edit PostgreSQL config (requires sudo):**
   ```bash
   sudo nano /Library/PostgreSQL/18/data/pg_hba.conf
   ```

2. **Change these lines:**
   ```
   # FROM:
   host    all             all             127.0.0.1/32            scram-sha-256
   
   # TO:
   host    all             all             127.0.0.1/32            trust
   ```

3. **Restart PostgreSQL:**
   ```bash
   brew services restart postgresql@18
   # OR
   sudo pg_ctl restart -D /Library/PostgreSQL/18/data
   ```

4. **Update `.env` file:**
   ```
   DATABASE_PASSWORD=
   ```

5. **Run setup:**
   ```bash
   python quick_setup.py
   ```

## What Each File Does

- **models/prime_check.py**: Defines the database table structure (SQLAlchemy model)
- **schemas/prime.py**: Defines the API request/response format (Pydantic schemas)
- **core/database.py**: Handles database connection and session management
- **core/config.py**: Loads environment variables from `.env` file

## Your Current Setup

```
Database Host: localhost
Database Port: 5432
Database User: postgres  
Database Name: wealthy_db
Database Table: prime_check_requests
```

The table will have these columns:
- `id`: Auto-incrementing primary key
- `transaction_id`: Unique identifier for each check
- `number`: The number that was checked
- `is_prime`: Boolean result (true/false)
- `created_at`: Timestamp when the check was made

## Once Connected

Start your API:
```bash
uvicorn app.main:app --reload
```

Visit the interactive docs:
- http://localhost:8000/docs

Test the API:
```bash
curl -X POST http://localhost:8000/api/v1/check-prime \
  -H "Content-Type: application/json" \
  -d '{"number": 17}'
```

## Need Help?

1. Check if PostgreSQL is running:
   ```bash
   pg_isready -h localhost -p 5432
   ```

2. Check PostgreSQL version:
   ```bash
   psql --version
   ```

3. List all databases (if you can connect):
   ```bash
   psql -U postgres -l
   ```

