#!/bin/bash

# Wealthy Prime Checker API - Setup Script
# This script helps set up the development environment

set -e

echo "🚀 Setting up Wealthy Prime Checker API..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if PostgreSQL is running
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL CLI (psql) not found. Make sure PostgreSQL is installed."
else
    echo "✅ PostgreSQL CLI found"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials!"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✨ Setup complete! ✨"
echo ""
echo "Next steps:"
echo "1. Make sure PostgreSQL is running on port 5432"
echo "2. Create the database: psql -U postgres -c 'CREATE DATABASE wealthy_db;'"
echo "3. Edit .env file with your database password"
echo "4. Activate the virtual environment: source venv/bin/activate"
echo "5. Run the application: uvicorn app.main:app --reload"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo ""

