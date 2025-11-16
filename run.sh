#!/bin/bash

# Quick run script for the Wealthy Prime Checker API

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

echo "🚀 Starting Wealthy Prime Checker API..."
echo "📊 API will be available at: http://localhost:8000"
echo "📚 Interactive docs at: http://localhost:8000/docs"
echo ""

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

