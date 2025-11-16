-- Database initialization script for Wealthy Prime Checker API
-- Run this script to set up the PostgreSQL database

-- Create database (run this as postgres user)
-- Note: You may need to run this separately before running the rest
-- CREATE DATABASE wealthy_db;

-- Connect to the database
\c wealthy_db;

-- Drop existing table if it exists (careful in production!)
-- DROP TABLE IF EXISTS prime_check_requests;

-- Create the prime_check_requests table
-- Note: This will be automatically created by SQLAlchemy when you run the app
-- This script is provided for reference and manual database setup

CREATE TABLE IF NOT EXISTS prime_check_requests (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    number INTEGER NOT NULL,
    is_prime BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_transaction_id ON prime_check_requests(transaction_id);
CREATE INDEX IF NOT EXISTS idx_number ON prime_check_requests(number);
CREATE INDEX IF NOT EXISTS idx_created_at ON prime_check_requests(created_at DESC);

-- Display table structure
\d prime_check_requests;

-- Show that the table is empty
SELECT COUNT(*) as total_records FROM prime_check_requests;

-- Example queries for later use:

-- Get all records
-- SELECT * FROM prime_check_requests ORDER BY created_at DESC;

-- Get specific transaction
-- SELECT * FROM prime_check_requests WHERE transaction_id = 'your_transaction_id_here';

-- Get statistics
-- SELECT 
--     COUNT(*) as total_checks,
--     SUM(CASE WHEN is_prime THEN 1 ELSE 0 END) as prime_count,
--     SUM(CASE WHEN NOT is_prime THEN 1 ELSE 0 END) as non_prime_count
-- FROM prime_check_requests;

-- Get most checked numbers
-- SELECT number, COUNT(*) as check_count, is_prime 
-- FROM prime_check_requests 
-- GROUP BY number, is_prime 
-- ORDER BY check_count DESC 
-- LIMIT 10;

GRANT ALL PRIVILEGES ON DATABASE wealthy_db TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Success message
SELECT 'Database setup complete! ✅' as status;

